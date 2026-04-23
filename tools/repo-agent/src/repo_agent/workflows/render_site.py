"""Phase 7 — static site renderer.

Reads the Markdown sources of truth (README.md, appendix/*.md, RUBRIC.md,
ANTI-PATTERNS.md, CONTRIBUTING.md, CHANGELOG.md), emits a zero-build static
HTML site into ``docs/`` plus ``docs/feed.xml`` (RSS 2.0) and
``docs/sitemap.xml``.

Hard constraints:

* **Deterministic.** Running the renderer twice on an unchanged tree must
  produce byte-identical output (stable ordering, no wall-clock timestamps
  in page bodies).
* **Read-only toward source files.** The renderer only writes inside
  ``--output-dir`` (default ``<repo-root>/docs``).
* **No external build step** for consumers: output is plain HTML + one CSS
  file, no JS.
"""

from __future__ import annotations

import html as _html
import re
from dataclasses import dataclass
from datetime import date, datetime, timezone
from email.utils import format_datetime
from pathlib import Path
from typing import Iterable
from xml.etree import ElementTree as ET

from markdown_it import MarkdownIt
from mdit_py_plugins.anchors import anchors_plugin

from ..paths import find_repo_root

__all__ = [
    "PageSpec",
    "RenderResult",
    "render_site",
    "site_pages",
    "build_markdown_parser",
    "parse_changelog",
    "build_feed_xml",
    "build_sitemap_xml",
    "SITE_TITLE",
    "SITE_TAGLINE",
    "SITE_REPO_URL",
    "SITE_BASE_URL",
]

# ---------------------------------------------------------------------------
# Site constants — stable across runs so output stays deterministic.
# ---------------------------------------------------------------------------

SITE_TITLE = "Awesome Agentic Engineering"
SITE_TAGLINE = (
    "Stop prompting. Start engineering. "
    "A structured reference for taking AI agents into production."
)
SITE_REPO_URL = "https://github.com/natnew/Awesome-Agentic-Engineering"
SITE_BASE_URL = "https://natnew.github.io/Awesome-Agentic-Engineering/"


# ---------------------------------------------------------------------------
# Page registry
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class PageSpec:
    """One source Markdown file → one HTML page."""

    source: str  # repo-relative source path, e.g. "README.md"
    output: str  # docs-relative output path, e.g. "index.html"
    title: str  # <title> / <h1> override (we keep the source H1 if matches)
    nav_label: str  # shown in the top nav
    in_nav: bool = True  # whether to include in the top nav


def site_pages() -> list[PageSpec]:
    """Return the full registry of pages, in a stable order."""
    pages = [
        PageSpec("README.md", "index.html", SITE_TITLE, "Home"),
        PageSpec("RUBRIC.md", "rubric.html", "Entry Rubric", "Rubric"),
        PageSpec("ANTI-PATTERNS.md", "anti-patterns.html", "Anti-patterns", "Anti-patterns"),
        PageSpec("CONTRIBUTING.md", "contributing.html", "Contributing", "Contributing"),
        PageSpec("CHANGELOG.md", "changelog.html", "Changelog", "Changelog"),
    ]
    # Appendix pages, sorted by filename so ordering is deterministic.
    appendix = [
        PageSpec(
            f"appendix/{name}",
            f"appendix/{name.replace('.md', '.html')}",
            _appendix_title(name),
            _appendix_title(name),
            in_nav=False,
        )
        for name in _APPENDIX_FILES
    ]
    return pages + appendix


# Kept out of ``site_pages`` so tests can monkey-patch easily.
_APPENDIX_FILES: tuple[str, ...] = (
    "benchmark-and-evidence-policy.md",
    "browser-and-desktop-agents.md",
    "creative-ai.md",
    "customer-support-and-crm-agents.md",
    "fast-moving-product-lists.md",
    "learning-resources.md",
    "newsletters-and-communities.md",
    "open-source-models-for-agents.md",
    "voice-agents.md",
)


def _appendix_title(filename: str) -> str:
    stem = filename.removesuffix(".md")
    return stem.replace("-", " ").title().replace("And", "and").replace("Crm", "CRM")


# ---------------------------------------------------------------------------
# Markdown → HTML
# ---------------------------------------------------------------------------


def build_markdown_parser() -> MarkdownIt:
    """Configured parser: CommonMark + GFM tables + heading anchors + safe HTML.

    We enable ``html=True`` because the sources contain inline ``<br>`` tags
    inside tables — a constrained, well-audited usage. We do **not** accept
    user-submitted Markdown at render time; the inputs are the curated repo
    files, so passing through the inline HTML they already use is safe.
    """
    md = (
        MarkdownIt("commonmark", {"html": True, "linkify": False, "typographer": False})
        .enable("table")
        .enable("strikethrough")
        .use(anchors_plugin, max_level=4, permalink=False, slug_func=_slugify)
    )
    return md


_SLUG_RE = re.compile(r"[^a-z0-9\- ]+")
_WS_RE = re.compile(r"[\s-]+")


def _slugify(text: str) -> str:
    """GitHub-style slugger (good enough for in-page anchors)."""
    text = text.strip().lower()
    # Strip emoji and punctuation we don't want in anchors.
    text = _SLUG_RE.sub("", text)
    text = _WS_RE.sub("-", text).strip("-")
    return text or "section"


# Rewrite `foo.md` and `foo.md#anchor` → `foo.html` / `foo.html#anchor`.
_MD_LINK_RE = re.compile(r'(href="(?!https?://|#|mailto:)[^"]*?)\.md(#[^"]*)?(")')


def _rewrite_internal_links(html_body: str) -> str:
    return _MD_LINK_RE.sub(lambda m: f"{m.group(1)}.html{m.group(2) or ''}{m.group(3)}", html_body)


# Add ``rel="noopener"`` to every external anchor.
_EXT_A_RE = re.compile(r'<a href="(https?://[^"]+)"([^>]*)>')


def _add_rel_noopener(html_body: str) -> str:
    def _sub(m: re.Match[str]) -> str:
        attrs = m.group(2)
        if "rel=" in attrs:
            return m.group(0)
        return f'<a href="{m.group(1)}" rel="noopener"{attrs}>'

    return _EXT_A_RE.sub(_sub, html_body)


# Tables under these h3 section ids are wide (4–7 columns with long prose)
# and render poorly inside the 860px content column. Tag them so the
# stylesheet can apply fixed-layout desktop rules and a stacked-card mobile
# layout. Scope is intentionally narrow — see
# specs/2026-04-22-phase-7-publishing-and-reach/plan.md (task 7.1).
_LANDSCAPE_H3_IDS = frozenset(
    {
        "frameworks-landscape",
        "evaluation-frameworks",
        "tracing-and-monitoring",
        "benchmarks",
        "safety-tooling-methodologies",
    }
)

# Match h1/h2/h3 only — h4 subsections (e.g. under "Frameworks Landscape")
# must stay inside the parent section so their tables get tagged too.
_HEADING_BOUNDARY_RE = re.compile(r'<h([123])(?:\s+id="([^"]+)")?[^>]*>')


def _tag_landscape_tables(html_body: str) -> str:
    """Add ``class="landscape-table"`` to every ``<table>`` that appears
    under one of the wide-table h3 sections. Idempotent."""
    headings = list(_HEADING_BOUNDARY_RE.finditer(html_body))
    if not headings:
        return html_body
    parts: list[str] = [html_body[: headings[0].start()]]
    for i, m in enumerate(headings):
        start = m.start()
        end = headings[i + 1].start() if i + 1 < len(headings) else len(html_body)
        segment = html_body[start:end]
        hid = m.group(2) or ""
        if hid in _LANDSCAPE_H3_IDS:
            segment = segment.replace("<table>", '<table class="landscape-table">')
        parts.append(segment)
    return "".join(parts)


def render_markdown_to_html(md_text: str, parser: MarkdownIt | None = None) -> str:
    parser = parser or build_markdown_parser()
    body = parser.render(md_text)
    body = _rewrite_internal_links(body)
    body = _add_rel_noopener(body)
    body = _tag_landscape_tables(body)
    return body


# ---------------------------------------------------------------------------
# Page template (hand-written, deterministic)
# ---------------------------------------------------------------------------

_CSS_HREF = "styles.css"


def _nav_html(pages: Iterable[PageSpec], current_output: str, prefix: str) -> str:
    parts = ['<nav class="site-nav" aria-label="Primary"><ul>']
    for p in pages:
        if not p.in_nav:
            continue
        href = f"{prefix}{p.output}"
        cls = ' class="active"' if p.output == current_output else ""
        parts.append(f'<li{cls}><a href="{href}">{_html.escape(p.nav_label)}</a></li>')
    parts.append("</ul></nav>")
    return "".join(parts)


def _footer_html(prefix: str) -> str:
    return (
        '<footer class="site-footer">'
        f'<p>Source of truth: <a href="{SITE_REPO_URL}" rel="noopener">GitHub</a> · '
        f'<a href="{prefix}feed.xml">Subscribe (RSS)</a> · '
        f'<a href="{SITE_REPO_URL}/blob/main/LICENSE" rel="noopener">MIT License</a></p>'
        "<p><small>Generated by <code>repo-agent workflow render-site</code>. "
        "Pages are rebuilt from Markdown on every push to <code>main</code>.</small></p>"
        "</footer>"
    )


def render_page(
    *,
    page: PageSpec,
    pages: list[PageSpec],
    body_html: str,
) -> str:
    depth = page.output.count("/")
    prefix = "../" * depth
    nav = _nav_html(pages, page.output, prefix)
    footer = _footer_html(prefix)
    title = _html.escape(page.title)
    return (
        "<!DOCTYPE html>\n"
        '<html lang="en">\n'
        "<head>\n"
        '<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        f"<title>{title} · {_html.escape(SITE_TITLE)}</title>\n"
        f'<meta name="description" content="{_html.escape(SITE_TAGLINE)}">\n'
        f'<link rel="stylesheet" href="{prefix}{_CSS_HREF}">\n'
        f'<link rel="alternate" type="application/rss+xml" '
        f'title="{_html.escape(SITE_TITLE)} — Changelog" href="{prefix}feed.xml">\n'
        "</head>\n"
        "<body>\n"
        '<header class="site-header">\n'
        f'<p class="site-title"><a href="{prefix}index.html">{_html.escape(SITE_TITLE)}</a></p>\n'
        f"{nav}\n"
        "</header>\n"
        '<main class="site-main">\n'
        '<article class="content">\n'
        f"{body_html}"
        "</article>\n"
        "</main>\n"
        f"{footer}\n"
        "</body>\n"
        "</html>\n"
    )


# ---------------------------------------------------------------------------
# Styles — single CSS file. Kept small, no webfonts.
# ---------------------------------------------------------------------------

_STYLES_CSS = """\
:root {
  --fg: #1b1f23;
  --bg: #ffffff;
  --muted: #57606a;
  --accent: #0969da;
  --border: #d0d7de;
  --code-bg: #f6f8fa;
  --quote: #656d76;
}
@media (prefers-color-scheme: dark) {
  :root {
    --fg: #e6edf3;
    --bg: #0d1117;
    --muted: #8b949e;
    --accent: #58a6ff;
    --border: #30363d;
    --code-bg: #161b22;
    --quote: #8b949e;
  }
}
* { box-sizing: border-box; }
html { -webkit-text-size-adjust: 100%; }
body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen,
    Ubuntu, Cantarell, "Helvetica Neue", sans-serif;
  font-size: 16px;
  line-height: 1.55;
  color: var(--fg);
  background: var(--bg);
}
a { color: var(--accent); text-decoration: none; }
a:hover, a:focus { text-decoration: underline; }
.site-header {
  border-bottom: 1px solid var(--border);
  padding: 1rem 1.25rem;
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  align-items: center;
  justify-content: space-between;
}
.site-title { margin: 0; font-weight: 700; font-size: 1.05rem; }
.site-title a { color: var(--fg); }
.site-nav ul {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-wrap: wrap;
  gap: 0.25rem 1rem;
}
.site-nav a { color: var(--muted); font-size: 0.95rem; }
.site-nav li.active a { color: var(--fg); font-weight: 600; }
.site-main { max-width: 860px; margin: 0 auto; padding: 1.5rem 1.25rem 3rem; }
.content h1, .content h2, .content h3, .content h4 {
  line-height: 1.25;
  margin-top: 2rem;
}
.content h1 { font-size: 2rem; margin-top: 0; }
.content h2 { font-size: 1.5rem; border-bottom: 1px solid var(--border); padding-bottom: 0.3rem; }
.content h3 { font-size: 1.2rem; }
.content p, .content ul, .content ol { margin: 0.75rem 0; }
.content code {
  font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace;
  font-size: 0.9em;
  background: var(--code-bg);
  padding: 0.1em 0.35em;
  border-radius: 4px;
}
.content pre {
  background: var(--code-bg);
  padding: 0.9rem 1rem;
  border-radius: 6px;
  overflow-x: auto;
  font-size: 0.9rem;
}
.content pre code { background: transparent; padding: 0; font-size: inherit; }
.content blockquote {
  margin: 1rem 0;
  padding: 0.25rem 1rem;
  color: var(--quote);
  border-left: 4px solid var(--border);
}
.content table {
  border-collapse: collapse;
  display: block;
  overflow-x: auto;
  margin: 1rem 0;
  font-size: 0.95rem;
}
.content th, .content td {
  border: 1px solid var(--border);
  padding: 0.45rem 0.75rem;
  text-align: left;
  vertical-align: top;
}
.content th { background: var(--code-bg); }
.content img { max-width: 100%; height: auto; }
.content hr { border: 0; border-top: 1px solid var(--border); margin: 2rem 0; }

/* Wide reference tables (Frameworks Landscape, Evaluation Frameworks,
   Tracing and Monitoring, Benchmarks, Safety Tooling & Methodologies).
   Keep the 860px content column; use fixed table layout so cells wrap
   inside the column instead of forcing horizontal scroll, and collapse
   to stacked cards on small viewports. Tagged by the renderer via
   _tag_landscape_tables(). */
.content table.landscape-table {
  display: table;
  width: 100%;
  table-layout: fixed;
  overflow-x: visible;
  font-size: 0.9rem;
}
.content table.landscape-table th,
.content table.landscape-table td {
  padding: 0.5rem 0.6rem;
  word-wrap: break-word;
  overflow-wrap: anywhere;
  vertical-align: top;
}
.content table.landscape-table code,
.content table.landscape-table a {
  word-break: break-word;
  overflow-wrap: anywhere;
}
@media (max-width: 720px) {
  .content table.landscape-table,
  .content table.landscape-table thead,
  .content table.landscape-table tbody,
  .content table.landscape-table tr,
  .content table.landscape-table th,
  .content table.landscape-table td {
    display: block;
    width: 100%;
  }
  .content table.landscape-table thead {
    position: absolute;
    left: -9999px;
    top: -9999px;
  }
  .content table.landscape-table tr {
    border: 1px solid var(--border);
    border-radius: 6px;
    margin: 0.75rem 0;
    padding: 0.25rem 0.75rem;
    background: var(--bg);
  }
  .content table.landscape-table td {
    border: 0;
    border-bottom: 1px solid var(--border);
    padding: 0.5rem 0;
  }
  .content table.landscape-table td:last-child { border-bottom: 0; }
  .content table.landscape-table td:first-child {
    font-weight: 600;
    font-size: 1rem;
  }
}
.site-footer {
  border-top: 1px solid var(--border);
  padding: 1.5rem 1.25rem;
  color: var(--muted);
  font-size: 0.9rem;
  text-align: center;
}
.site-footer p { margin: 0.25rem 0; }
"""


# ---------------------------------------------------------------------------
# Changelog → RSS
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ChangelogEntry:
    version: str
    date: str  # ISO YYYY-MM-DD, or "" for [Unreleased]
    body: str  # raw Markdown body under the heading
    anchor: str  # in-page anchor on changelog.html


_CHANGELOG_HEADING_RE = re.compile(
    r"^## \[(?P<version>[^\]]+)\](?:\s*-\s*(?P<date>\d{4}-\d{2}-\d{2}))?\s*$",
    re.MULTILINE,
)


def parse_changelog(changelog_md: str) -> list[ChangelogEntry]:
    """Return changelog entries newest-first in source order.

    Recognizes ``## [version] - YYYY-MM-DD`` and ``## [Unreleased]`` headings.
    """
    matches = list(_CHANGELOG_HEADING_RE.finditer(changelog_md))
    entries: list[ChangelogEntry] = []
    for i, m in enumerate(matches):
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(changelog_md)
        body = changelog_md[start:end].strip()
        version = m.group("version")
        iso_date = m.group("date") or ""
        anchor = _slugify(f"{version} {iso_date}".strip())
        entries.append(ChangelogEntry(version=version, date=iso_date, body=body, anchor=anchor))
    return entries


def _entry_summary(body_md: str, limit: int = 400) -> str:
    # First non-empty, non-heading line.
    for line in body_md.splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        if len(s) > limit:
            s = s[: limit - 1].rstrip() + "\u2026"
        return s
    return ""


def build_feed_xml(
    entries: Iterable[ChangelogEntry],
    *,
    base_url: str = SITE_BASE_URL,
    site_title: str = SITE_TITLE,
    site_tagline: str = SITE_TAGLINE,
) -> str:
    """Return an RSS 2.0 feed XML string for the dated changelog entries."""
    rss = ET.Element("rss", {"version": "2.0"})
    channel = ET.SubElement(rss, "channel")
    ET.SubElement(channel, "title").text = f"{site_title} — Changelog"
    ET.SubElement(channel, "link").text = f"{base_url}changelog.html"
    ET.SubElement(channel, "description").text = site_tagline
    ET.SubElement(channel, "language").text = "en"

    for entry in entries:
        if not entry.date:
            # Skip [Unreleased] — no stable pubDate.
            continue
        item = ET.SubElement(channel, "item")
        ET.SubElement(item, "title").text = f"{entry.version} — {entry.date}"
        link = f"{base_url}changelog.html#{entry.anchor}"
        ET.SubElement(item, "link").text = link
        ET.SubElement(item, "guid", {"isPermaLink": "true"}).text = link
        try:
            dt = datetime.combine(date.fromisoformat(entry.date), datetime.min.time(), tzinfo=timezone.utc)
            ET.SubElement(item, "pubDate").text = format_datetime(dt, usegmt=True)
        except ValueError:
            pass
        summary = _entry_summary(entry.body)
        if summary:
            ET.SubElement(item, "description").text = summary

    ET.indent(rss, space="  ")
    return '<?xml version="1.0" encoding="utf-8"?>\n' + ET.tostring(rss, encoding="unicode")


# ---------------------------------------------------------------------------
# Sitemap
# ---------------------------------------------------------------------------


def build_sitemap_xml(pages: Iterable[PageSpec], *, base_url: str = SITE_BASE_URL) -> str:
    urlset = ET.Element("urlset", {"xmlns": "http://www.sitemaps.org/schemas/sitemap/0.9"})
    for p in pages:
        u = ET.SubElement(urlset, "url")
        ET.SubElement(u, "loc").text = f"{base_url}{p.output}"
    ET.indent(urlset, space="  ")
    return '<?xml version="1.0" encoding="utf-8"?>\n' + ET.tostring(urlset, encoding="unicode")


# ---------------------------------------------------------------------------
# Orchestrator
# ---------------------------------------------------------------------------


@dataclass
class RenderResult:
    written: list[Path]
    skipped: list[Path]  # already up-to-date (byte-equal)
    changed: list[Path]  # written because bytes differ from prior content

    def summary(self) -> str:
        return (
            f"{len(self.written)} files written "
            f"({len(self.changed)} changed, {len(self.skipped)} unchanged)"
        )


def _read_if_exists(path: Path) -> bytes | None:
    try:
        return path.read_bytes()
    except FileNotFoundError:
        return None


def _write_if_changed(path: Path, new_bytes: bytes, result: RenderResult) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    prior = _read_if_exists(path)
    result.written.append(path)
    if prior == new_bytes:
        result.skipped.append(path)
        return
    path.write_bytes(new_bytes)
    result.changed.append(path)


def render_site(
    *,
    repo_root: Path | None = None,
    output_dir: Path | None = None,
) -> RenderResult:
    """Render the full site. Idempotent; safe to run repeatedly."""
    root = repo_root or find_repo_root()
    out = output_dir or (root / "docs")

    parser = build_markdown_parser()
    pages = site_pages()
    result = RenderResult(written=[], skipped=[], changed=[])

    # Pages.
    for page in pages:
        src = root / page.source
        md_text = src.read_text(encoding="utf-8")
        body_html = render_markdown_to_html(md_text, parser)
        page_html = render_page(page=page, pages=pages, body_html=body_html)
        _write_if_changed(out / page.output, page_html.encode("utf-8"), result)

    # Stylesheet.
    _write_if_changed(out / "styles.css", _STYLES_CSS.encode("utf-8"), result)

    # .nojekyll — disable GitHub Pages Jekyll processing.
    _write_if_changed(out / ".nojekyll", b"", result)

    # Sitemap + RSS.
    _write_if_changed(
        out / "sitemap.xml",
        (build_sitemap_xml(pages) + "\n").encode("utf-8"),
        result,
    )
    changelog_md_path = root / "CHANGELOG.md"
    if changelog_md_path.exists():
        entries = parse_changelog(changelog_md_path.read_text(encoding="utf-8"))
        _write_if_changed(
            out / "feed.xml",
            (build_feed_xml(entries) + "\n").encode("utf-8"),
            result,
        )

    return result
