"""Entry-draft skill (roadmap 5.4).

Takes a URL, fetches the page, extracts title + description using only the
Python stdlib HTML parser, and drafts a rubric-aligned entry stub in the
conventions of the target section. Runs ``validate_entry`` on the draft and
returns the draft + validation block together.

Network fetch is performed with ``httpx`` but gated behind a ``fetcher``
callable so tests can pass fixtures instead of hitting the network.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from html.parser import HTMLParser
from typing import Any, Callable

import httpx

from ..rubric import load_policy, score_entry


@dataclass
class PageMetadata:
    url: str
    title: str
    description: str


@dataclass
class DraftResult:
    section: str
    draft_markdown: str
    metadata: dict[str, Any]
    validation: dict[str, Any]


Fetcher = Callable[[str], str]  # url -> html


def default_fetcher(url: str) -> str:
    with httpx.Client(
        follow_redirects=True, timeout=10.0, headers={"User-Agent": "repo-agent/0.1"}
    ) as client:
        r = client.get(url)
        r.raise_for_status()
        return r.text


class _MetaExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.title = ""
        self.description = ""
        self._in_title = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "title":
            self._in_title = True
            return
        if tag == "meta":
            a = dict(attrs)
            name = (a.get("name") or a.get("property") or "").lower()
            content = a.get("content") or ""
            if not content:
                return
            if name in {"description", "og:description", "twitter:description"} and not self.description:
                self.description = content.strip()
            if name in {"og:title", "twitter:title"} and not self.title:
                self.title = content.strip()

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._in_title = False

    def handle_data(self, data: str) -> None:
        if self._in_title and not self.title:
            self.title = data.strip()


def extract_metadata(url: str, html: str) -> PageMetadata:
    p = _MetaExtractor()
    p.feed(html)
    title = p.title or url
    description = p.description or "(no description found; contributor to add)"
    return PageMetadata(url=url, title=title, description=description)


def _format_entry(meta: PageMetadata, rationale: str) -> str:
    # Use the list's conventional bullet + evidence-tag pattern.
    desc = meta.description.strip()
    if len(desc) > 220:
        desc = desc[:217].rstrip() + "..."
    rationale_line = rationale.strip() or "Rationale to be added by contributor."
    return (
        f"- **[{meta.title}]({meta.url})** — {desc} "
        f"[official]({meta.url}). "
        f"_Why it earns its place:_ {rationale_line} "
        f"_Last reviewed: April 2026._"
    )


def draft(
    url: str,
    section: str,
    rationale: str = "",
    fetcher: Fetcher | None = None,
) -> DraftResult:
    fetch = fetcher or default_fetcher
    html = fetch(url)
    meta = extract_metadata(url, html)
    entry_md = _format_entry(meta, rationale)

    policy = load_policy()
    validation = score_entry(entry_md, policy)

    return DraftResult(
        section=section,
        draft_markdown=entry_md,
        metadata=asdict(meta),
        validation=asdict(validation),
    )
