"""Triage skill (roadmap 5.2).

Classifies an incoming PR or issue against the rubric. Takes a PR-like
payload (title, body, changed files, optional entry Markdown) and returns:

* rubric score on any entry Markdown it can locate,
* suggested labels,
* a short human-readable verdict.

Never calls GitHub — the caller supplies the payload.
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field
from typing import Any

from ..rubric import ValidationResult, load_policy, score_entry


@dataclass
class TriageInput:
    title: str
    body: str = ""
    changed_files: list[str] = field(default_factory=list)
    entry_markdown: str | None = None  # if None, extracted from body


@dataclass
class TriageResult:
    labels: list[str]
    verdict: str
    summary: str
    validation: dict[str, Any] | None


_ENTRY_BLOCK = re.compile(
    r"```(?:markdown|md)?\s*\n(?P<body>.+?)\n```", re.DOTALL | re.IGNORECASE
)


def _extract_entry(body: str) -> str | None:
    m = _ENTRY_BLOCK.search(body)
    if m:
        return m.group("body").strip()
    return None


def _suggest_labels(inp: TriageInput, v: ValidationResult | None) -> list[str]:
    labels: list[str] = []
    touches_content = any(
        f == "README.md" or f.startswith("appendix/") for f in inp.changed_files
    )
    touches_meta = any(
        f in {"RUBRIC.md", "ANTI-PATTERNS.md", "CONTRIBUTING.md"} for f in inp.changed_files
    )

    if touches_content:
        labels.append("area:content")
    if touches_meta:
        labels.append("area:policy")
    if not touches_content and not touches_meta:
        labels.append("area:infra")

    if v is None:
        labels.append("needs-entry-markdown")
        return labels

    if v.hard_gate_failures:
        labels.append("blocked:hard-gate")
    if v.anti_pattern_hits:
        labels.append("anti-pattern")
    if not v.evidence_tags:
        labels.append("needs-evidence")
    if v.verdict == "merge":
        labels.append("ready-for-review")
    elif v.verdict == "request-changes":
        labels.append("needs-changes")
    elif v.verdict == "block":
        labels.append("out-of-scope")
    return labels


def triage(inp: TriageInput) -> TriageResult:
    policy = load_policy()
    entry = inp.entry_markdown or _extract_entry(inp.body)
    validation: ValidationResult | None = None
    if entry:
        validation = score_entry(entry, policy)

    labels = _suggest_labels(inp, validation)

    if validation is None:
        verdict = "needs-info"
        summary = (
            f"PR/issue '{inp.title}' — no entry Markdown block found. "
            "Ask the contributor to include the proposed entry in a ```markdown fenced block."
        )
    else:
        summary = (
            f"Score {validation.score}/{validation.max_score}; verdict={validation.verdict}. "
            + " ".join(validation.notes)
        )
        verdict = validation.verdict

    return TriageResult(
        labels=labels,
        verdict=verdict,
        summary=summary,
        validation=asdict(validation) if validation else None,
    )
