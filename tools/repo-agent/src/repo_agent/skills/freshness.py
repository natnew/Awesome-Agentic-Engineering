"""Freshness-audit skill (roadmap 5.3).

Re-implements the Phase 4 stale-entry detection in Python against the content
index, so the logic is callable from the MCP server or CLI. Does **not** open
issues — the scheduled workflow retains that responsibility. We return
structured candidates for human (or agent) review.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from ..content import build_index
from ..paths import find_repo_root

_DEFAULT_THRESHOLD_MONTHS = 9

_MONTHS = {
    "january": 1, "february": 2, "march": 3, "april": 4, "may": 5, "june": 6,
    "july": 7, "august": 8, "september": 9, "october": 10, "november": 11, "december": 12,
}


@dataclass
class StaleCandidate:
    file: str
    heading: str | None
    last_reviewed: str | None
    age_months: int | None
    reason: str  # "stale" | "missing-marker"


def _parse_reviewed(value: str | None) -> datetime | None:
    if not value:
        return None
    m = re.match(r"([A-Za-z]+)\s+(\d{4})", value.strip())
    if not m:
        return None
    month = _MONTHS.get(m.group(1).lower())
    year = int(m.group(2))
    if not month:
        return None
    return datetime(year, month, 1, tzinfo=timezone.utc)


def _months_between(a: datetime, b: datetime) -> int:
    return (b.year - a.year) * 12 + (b.month - a.month)


def audit(
    threshold_months: int = _DEFAULT_THRESHOLD_MONTHS,
    now: datetime | None = None,
    repo_root: Path | None = None,
) -> list[StaleCandidate]:
    now = now or datetime.now(tz=timezone.utc)
    root = repo_root or find_repo_root()
    index = build_index(root)

    # Work per file: one file contributes zero or more candidates.
    by_file: dict[str, list[str | None]] = {}
    for s in index.sections:
        by_file.setdefault(s.file, []).append(s.last_reviewed)

    out: list[StaleCandidate] = []
    for file, reviews in by_file.items():
        valid = [r for r in reviews if r]
        if not valid:
            out.append(
                StaleCandidate(
                    file=file,
                    heading=None,
                    last_reviewed=None,
                    age_months=None,
                    reason="missing-marker",
                )
            )
            continue
        # Use the most recent marker in the file.
        parsed = [_parse_reviewed(r) for r in valid]
        parsed = [p for p in parsed if p is not None]
        if not parsed:
            out.append(
                StaleCandidate(
                    file=file,
                    heading=None,
                    last_reviewed=None,
                    age_months=None,
                    reason="missing-marker",
                )
            )
            continue
        newest = max(parsed)
        age = _months_between(newest, now)
        if age > threshold_months:
            out.append(
                StaleCandidate(
                    file=file,
                    heading=None,
                    last_reviewed=newest.strftime("%B %Y"),
                    age_months=age,
                    reason="stale",
                )
            )
    # Deterministic ordering: stale first (oldest first), then missing markers.
    out.sort(
        key=lambda c: (
            0 if c.reason == "stale" else 1,
            -(c.age_months or 0),
            c.file,
        )
    )
    return out
