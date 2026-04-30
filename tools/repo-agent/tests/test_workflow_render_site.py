"""Tests for the Phase 7 site renderer."""

from __future__ import annotations

from pathlib import Path
from xml.etree import ElementTree as ET

import pytest

from repo_agent.workflows import render_site as rs


# ---------------------------------------------------------------------------
# Markdown → HTML unit tests
# ---------------------------------------------------------------------------


def test_markdown_headings_paragraphs_and_lists():
    html = rs.render_markdown_to_html("# Title\n\nHello **world**.\n\n- a\n- b\n")
    assert "<h1" in html and "Title</h1>" in html
    assert "<strong>world</strong>" in html
    assert "<ul>" in html and "<li>a</li>" in html


def test_markdown_tables():
    md = "| A | B |\n|---|---|\n| 1 | 2 |\n"
    html = rs.render_markdown_to_html(md)
    assert "<table>" in html
    assert "<th>A</th>" in html
    assert "<td>1</td>" in html


def test_markdown_fenced_code_is_escaped():
    md = "```python\nprint('<script>')\n```\n"
    html = rs.render_markdown_to_html(md)
    assert "<pre>" in html
    assert "&lt;script&gt;" in html  # HTML-escaped inside code
    assert "<script>" not in html


def test_internal_md_links_rewritten_to_html():
    md = "[rubric](RUBRIC.md) and [anchor](RUBRIC.md#scoring) and [appendix](appendix/voice-agents.md)"
    html = rs.render_markdown_to_html(md)
    assert 'href="RUBRIC.html"' in html
    assert 'href="RUBRIC.html#scoring"' in html
    assert 'href="appendix/voice-agents.html"' in html


def test_readme_md_links_rewritten_to_index_html():
    md = "[home](../README.md) and [anchor](../README.md#thesis) and [root](README.md)"
    html = rs.render_markdown_to_html(md)
    assert 'href="../index.html"' in html
    assert 'href="../index.html#thesis"' in html
    assert 'href="index.html"' in html
    # The naive .md→.html rewriter must not also fire on README.md.
    assert "README.html" not in html


def test_external_links_get_rel_noopener():
    md = "[ext](https://example.com)"
    html = rs.render_markdown_to_html(md)
    assert 'rel="noopener"' in html
    assert 'href="https://example.com"' in html


def test_in_page_anchors_untouched():
    html = rs.render_markdown_to_html("[top](#top)")
    assert 'href="#top"' in html


def test_inline_br_in_tables_passes_through():
    md = "| a | b |\n|---|---|\n| one<br>two | three |\n"
    html = rs.render_markdown_to_html(md)
    assert "<br>" in html


def test_slugify_is_stable_and_strips_emoji():
    assert rs._slugify("🧠 Thesis") == "thesis"
    assert rs._slugify("Hello World!") == "hello-world"
    assert rs._slugify("   ") == "section"


# ---------------------------------------------------------------------------
# Changelog parsing + RSS
# ---------------------------------------------------------------------------


SAMPLE_CHANGELOG = """# Changelog

## [Unreleased]

- Pending work.

## [Phase 2] - 2026-04-15

- Added the rubric.

## [Phase 1] - 2026-04-10

- Bootstrap.
"""


def test_parse_changelog_finds_all_entries():
    entries = rs.parse_changelog(SAMPLE_CHANGELOG)
    assert [e.version for e in entries] == ["Unreleased", "Phase 2", "Phase 1"]
    assert entries[0].date == ""
    assert entries[1].date == "2026-04-15"
    assert "rubric" in entries[1].body


def test_feed_xml_is_valid_rss_and_skips_unreleased():
    entries = rs.parse_changelog(SAMPLE_CHANGELOG)
    xml = rs.build_feed_xml(entries)
    root = ET.fromstring(xml.split("?>", 1)[1])
    assert root.tag == "rss"
    assert root.attrib["version"] == "2.0"
    items = root.findall("./channel/item")
    # Two dated entries; [Unreleased] is skipped.
    assert len(items) == 2
    titles = [it.findtext("title") for it in items]
    assert "Phase 2 — 2026-04-15" in titles
    # Every item has pubDate + guid + link.
    for it in items:
        assert it.findtext("pubDate")
        assert it.findtext("link", "").startswith("https://")


def test_sitemap_xml_lists_every_page():
    pages = rs.site_pages()
    xml = rs.build_sitemap_xml(pages)
    root = ET.fromstring(xml.split("?>", 1)[1])
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    locs = [u.findtext("sm:loc", namespaces=ns) for u in root.findall("sm:url", ns)]
    assert len(locs) == len(pages)
    assert all(loc and loc.startswith("https://") for loc in locs)


# ---------------------------------------------------------------------------
# End-to-end render against a minimal repo tree
# ---------------------------------------------------------------------------


def _seed_minimal_repo(root: Path) -> None:
    (root / "README.md").write_text(
        "# Awesome Agentic Engineering\n\nHello [rubric](RUBRIC.md).\n",
        encoding="utf-8",
    )
    (root / "RUBRIC.md").write_text("# Rubric\n\nSeven dimensions.\n", encoding="utf-8")
    (root / "ANTI-PATTERNS.md").write_text("# Anti-patterns\n\nDo not.\n", encoding="utf-8")
    (root / "CONTRIBUTING.md").write_text("# Contributing\n\nHi.\n", encoding="utf-8")
    (root / "CHANGELOG.md").write_text(SAMPLE_CHANGELOG, encoding="utf-8")
    app = root / "appendix"
    app.mkdir()
    for name in rs._APPENDIX_FILES:
        (app / name).write_text(f"# {name}\n\nbody\n", encoding="utf-8")


@pytest.fixture
def minimal_repo(tmp_path: Path) -> Path:
    _seed_minimal_repo(tmp_path)
    return tmp_path


def test_render_site_produces_expected_files(minimal_repo: Path):
    out = minimal_repo / "docs"
    result = rs.render_site(repo_root=minimal_repo, output_dir=out)

    # Every registered page plus the shared assets.
    expected = {
        "index.html",
        "rubric.html",
        "anti-patterns.html",
        "contributing.html",
        "changelog.html",
        "styles.css",
        ".nojekyll",
        "sitemap.xml",
        "feed.xml",
    }
    for name in expected:
        assert (out / name).exists(), f"missing {name}"
    for appendix in rs._APPENDIX_FILES:
        assert (out / "appendix" / appendix.replace(".md", ".html")).exists()

    # Everything in `result.written` was created fresh.
    assert len(result.changed) == len(result.written)
    assert not result.skipped


def test_render_site_is_idempotent(minimal_repo: Path):
    out = minimal_repo / "docs"
    rs.render_site(repo_root=minimal_repo, output_dir=out)
    second = rs.render_site(repo_root=minimal_repo, output_dir=out)
    # Second run must not change any bytes.
    assert second.changed == []
    assert len(second.skipped) == len(second.written)


def test_rendered_html_has_nav_and_footer_and_rss_link(minimal_repo: Path):
    out = minimal_repo / "docs"
    rs.render_site(repo_root=minimal_repo, output_dir=out)
    index = (out / "index.html").read_text(encoding="utf-8")
    assert "<!DOCTYPE html>" in index
    assert 'class="site-nav"' in index
    assert 'class="site-footer"' in index
    assert 'type="application/rss+xml"' in index
    # Internal .md link got rewritten.
    assert 'href="RUBRIC.html"' in index
    # External repo link has rel=noopener.
    assert 'rel="noopener"' in index


def test_appendix_pages_use_relative_prefix_for_assets(minimal_repo: Path):
    out = minimal_repo / "docs"
    rs.render_site(repo_root=minimal_repo, output_dir=out)
    page = (out / "appendix" / "voice-agents.html").read_text(encoding="utf-8")
    assert 'href="../styles.css"' in page
    assert 'href="../index.html"' in page
    assert 'href="../feed.xml"' in page


def test_nojekyll_is_empty(minimal_repo: Path):
    out = minimal_repo / "docs"
    rs.render_site(repo_root=minimal_repo, output_dir=out)
    assert (out / ".nojekyll").read_bytes() == b""
