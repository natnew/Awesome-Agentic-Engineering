"""Pure-Python implementations of the MCP tools (no MCP dependency).

The MCP server layer (``server.py``) is a thin adapter over these functions.
Keeping the core logic here means tests never need the MCP SDK and the CLI
can call the same functions directly.
"""

from __future__ import annotations

from dataclasses import asdict
from typing import Any

from .content import build_index
from .rubric import load_policy, score_entry
from .skills import entry_draft, freshness, triage


def list_sections() -> dict[str, Any]:
    idx = build_index()
    return {
        "files": idx.list_files(),
        "top_level_sections": [
            {"file": s.file, "heading": s.heading, "level": s.level}
            for s in idx.top_level_sections()
        ],
    }


def get_rubric() -> dict[str, Any]:
    policy = load_policy()
    r = policy.rubric
    return {
        "merge_threshold": r.merge_threshold,
        "max_score": r.max_score,
        "hard_gates": sorted(r.hard_gates),
        "source_hash": r.source_hash,
        "dimensions": [asdict(d) for d in r.dimensions],
    }


def get_anti_patterns() -> dict[str, Any]:
    policy = load_policy()
    return {
        "patterns": [asdict(ap) for ap in policy.anti_patterns],
        "hype_phrases": list(policy.hype_phrases),
    }


def search_entries(query: str, section: str | None = None, limit: int = 20) -> dict[str, Any]:
    idx = build_index()
    results = idx.search(query, section=section)[:limit]
    return {
        "query": query,
        "section": section,
        "count": len(results),
        "results": [
            {
                "file": s.file,
                "heading": s.heading,
                "level": s.level,
                "start_line": s.start_line,
                "end_line": s.end_line,
                "last_reviewed": s.last_reviewed,
                "urls": s.urls[:5],
            }
            for s in results
        ],
    }


def validate_entry(entry_markdown: str) -> dict[str, Any]:
    policy = load_policy()
    v = score_entry(entry_markdown, policy)
    return asdict(v)


def propose_entry(url: str, section: str, rationale: str = "") -> dict[str, Any]:
    result = entry_draft.draft(url=url, section=section, rationale=rationale)
    return asdict(result)


def triage_pr(
    title: str,
    body: str = "",
    changed_files: list[str] | None = None,
    entry_markdown: str | None = None,
) -> dict[str, Any]:
    inp = triage.TriageInput(
        title=title,
        body=body,
        changed_files=list(changed_files or []),
        entry_markdown=entry_markdown,
    )
    return asdict(triage.triage(inp))


def freshness_audit(threshold_months: int = 9) -> dict[str, Any]:
    candidates = freshness.audit(threshold_months=threshold_months)
    return {
        "threshold_months": threshold_months,
        "count": len(candidates),
        "candidates": [asdict(c) for c in candidates],
    }
