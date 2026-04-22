"""Parse ``README.md`` and ``appendix/**/*.md`` into a searchable index.

The list uses Markdown headings (``##`` / ``###``) to demarcate sections and
tables / bullet lists to enumerate entries. We do not try to parse entries
perfectly — we index at the *section* and *line* granularity, which is enough
for search, freshness, and draft-placement.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

from .paths import find_repo_root

_HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
_URL = re.compile(r"\]\((https?://[^)\s]+)\)")
_LAST_REVIEWED = re.compile(
    r"Last reviewed:\s*([A-Za-z]+)\s+(\d{4})", re.IGNORECASE
)


@dataclass
class Section:
    file: str
    heading: str
    level: int
    start_line: int  # 1-based, heading line
    end_line: int  # 1-based, inclusive
    body: str
    last_reviewed: str | None = None  # e.g. "April 2026"
    urls: list[str] = field(default_factory=list)


@dataclass
class ContentIndex:
    root: Path
    files: list[str]
    sections: list[Section]

    def search(self, query: str, section: str | None = None) -> list[Section]:
        """Substring + token match over section headings and bodies."""
        q = query.strip().lower()
        if not q:
            return []
        tokens = [t for t in re.split(r"\W+", q) if t]
        out: list[tuple[int, Section]] = []
        for s in self.sections:
            if section and section.lower() not in s.heading.lower() and section.lower() not in s.file.lower():
                continue
            hay = f"{s.heading}\n{s.body}".lower()
            if q in hay:
                score = 10
            else:
                score = sum(1 for t in tokens if t in hay)
            if score > 0:
                out.append((score, s))
        out.sort(key=lambda x: (-x[0], x[1].file, x[1].start_line))
        return [s for _, s in out]

    def list_files(self) -> list[str]:
        return sorted(self.files)

    def top_level_sections(self) -> list[Section]:
        return [s for s in self.sections if s.level <= 2]


def _parse_file(path: Path, repo_root: Path) -> list[Section]:
    rel = str(path.relative_to(repo_root)).replace("\\", "/")
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    # Collect heading positions
    headings: list[tuple[int, int, str]] = []  # (lineno, level, title)
    for i, line in enumerate(lines, start=1):
        m = _HEADING.match(line)
        if m:
            headings.append((i, len(m.group(1)), m.group(2).strip()))

    sections: list[Section] = []
    if not headings:
        # Treat whole file as one synthetic section
        body = text
        sections.append(
            Section(
                file=rel,
                heading=path.stem,
                level=0,
                start_line=1,
                end_line=len(lines),
                body=body,
                last_reviewed=_extract_reviewed(body),
                urls=_extract_urls(body),
            )
        )
        return sections

    for idx, (lineno, level, title) in enumerate(headings):
        end = headings[idx + 1][0] - 1 if idx + 1 < len(headings) else len(lines)
        body = "\n".join(lines[lineno:end])  # body excludes the heading line itself
        sections.append(
            Section(
                file=rel,
                heading=title,
                level=level,
                start_line=lineno,
                end_line=end,
                body=body,
                last_reviewed=_extract_reviewed(body),
                urls=_extract_urls(body),
            )
        )
    return sections


def _extract_reviewed(body: str) -> str | None:
    m = _LAST_REVIEWED.search(body)
    if not m:
        return None
    return f"{m.group(1).title()} {m.group(2)}"


def _extract_urls(body: str) -> list[str]:
    seen: list[str] = []
    for m in _URL.finditer(body):
        u = m.group(1)
        if u not in seen:
            seen.append(u)
    return seen


def build_index(repo_root: Path | None = None) -> ContentIndex:
    root = repo_root or find_repo_root()
    files: list[Path] = [root / "README.md"]
    appendix = root / "appendix"
    if appendix.is_dir():
        files.extend(sorted(p for p in appendix.glob("*.md")))

    sections: list[Section] = []
    for f in files:
        sections.extend(_parse_file(f, root))

    rel_files = [str(f.relative_to(root)).replace("\\", "/") for f in files]
    return ContentIndex(root=root, files=rel_files, sections=sections)
