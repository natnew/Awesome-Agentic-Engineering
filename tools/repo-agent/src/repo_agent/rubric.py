"""Parse ``RUBRIC.md`` and ``ANTI-PATTERNS.md`` into structured scoring models.

The parsers are intentionally forgiving: they look for the dimension table in
``RUBRIC.md`` (7 rows with weights) and for the quick-reference table in
``ANTI-PATTERNS.md`` (pattern → failing dimensions), plus a small set of
marketing phrases harvested from the document text.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field
from pathlib import Path

from .paths import find_repo_root

_DIM_ROW = re.compile(
    r"^\|\s*\d+\s*\|\s*\*\*(?P<name>[^*]+)\*\*\s*\|\s*[×x]?(?P<weight>\d+)\s*\|\s*(?P<desc>.+?)\s*\|\s*$"
)
_AP_ROW = re.compile(r"^\|\s*\d+\.\s*(?P<name>.+?)\s*\|\s*(?P<dims>.+?)\s*\|\s*$")

# Marketing / hype phrases we flag regardless of which section they appear in.
# Sourced from ANTI-PATTERNS.md §2 and RUBRIC.md / Phase-3 validation conventions.
_HYPE_PHRASES = [
    "world-class",
    "world class",
    "state-of-the-art",
    "state of the art",
    "revolutionary",
    "game-changer",
    "game changer",
    "trending on github",
]
_STARS_AS_EVIDENCE = re.compile(r"\b\d+\s*k\s*stars\b", re.IGNORECASE)
_EVIDENCE_TAGS = ("[official]", "[benchmark]", "[field report]", "[author assessment]")

HARD_GATES = {"Reliability", "Evidence", "Agentic relevance"}
MERGE_THRESHOLD = 27  # out of 45


@dataclass
class Dimension:
    name: str
    weight: int
    description: str


@dataclass
class Rubric:
    dimensions: list[Dimension]
    merge_threshold: int = MERGE_THRESHOLD
    hard_gates: frozenset[str] = field(default_factory=lambda: frozenset(HARD_GATES))
    source_hash: str = ""

    @property
    def max_score(self) -> int:
        # score 3 × weight, summed
        return sum(3 * d.weight for d in self.dimensions)


@dataclass
class AntiPattern:
    name: str
    failing_dimensions: list[str]


@dataclass
class Policy:
    rubric: Rubric
    anti_patterns: list[AntiPattern]
    hype_phrases: tuple[str, ...] = tuple(_HYPE_PHRASES)


def parse_rubric(path: Path) -> Rubric:
    text = path.read_text(encoding="utf-8")
    dims: list[Dimension] = []
    for line in text.splitlines():
        m = _DIM_ROW.match(line)
        if m:
            dims.append(
                Dimension(
                    name=m.group("name").strip(),
                    weight=int(m.group("weight")),
                    description=m.group("desc").strip(),
                )
            )
    if len(dims) < 5:
        raise ValueError(
            f"RUBRIC.md parse failed: expected ≥5 dimensions, got {len(dims)}. "
            "Has the rubric table format changed?"
        )
    h = hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]
    return Rubric(dimensions=dims, source_hash=h)


def parse_anti_patterns(path: Path) -> list[AntiPattern]:
    text = path.read_text(encoding="utf-8")
    aps: list[AntiPattern] = []
    for line in text.splitlines():
        m = _AP_ROW.match(line)
        if m:
            name = m.group("name").strip()
            # Skip the table header row
            if name.lower() == "pattern":
                continue
            dims_raw = m.group("dims").strip()
            dims = [d.strip() for d in re.split(r",|/", dims_raw) if d.strip()]
            aps.append(AntiPattern(name=name, failing_dimensions=dims))
    if not aps:
        raise ValueError("ANTI-PATTERNS.md parse failed: no quick-reference rows found.")
    return aps


def load_policy(repo_root: Path | None = None) -> Policy:
    root = repo_root or find_repo_root()
    rubric = parse_rubric(root / "RUBRIC.md")
    aps = parse_anti_patterns(root / "ANTI-PATTERNS.md")
    return Policy(rubric=rubric, anti_patterns=aps)


# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------


@dataclass
class AntiPatternHit:
    phrase: str
    line: int


@dataclass
class ValidationResult:
    score: int
    max_score: int
    per_dimension: dict[str, int]  # weighted score per dimension
    per_dimension_raw: dict[str, int]  # 0-3 per dimension
    hard_gate_failures: list[str]
    anti_pattern_hits: list[AntiPatternHit]
    evidence_tags: list[str]
    verdict: str  # "merge" | "request-changes" | "block"
    notes: list[str]


def _raw_score_for_entry(entry_md: str, rubric: Rubric) -> dict[str, int]:
    """Heuristic, deterministic scoring.

    This is intentionally transparent so reviewers know exactly what the
    automated score signals — human review remains the merge decision.
    """
    text = entry_md.strip()
    lower = text.lower()
    has_url = bool(re.search(r"https?://", text))
    tag_counts = {tag: lower.count(tag) for tag in _EVIDENCE_TAGS}
    total_tags = sum(tag_counts.values())
    length = len(text)

    scores: dict[str, int] = {}
    for d in rubric.dimensions:
        name = d.name
        if name == "Reliability":
            # Signal: mentions of "production", "stable", version info, or [field report] tag
            s = 0
            if re.search(r"\b(production|stable|v\d+\.\d+|deployed)\b", lower):
                s += 1
            if tag_counts["[field report]"] > 0:
                s += 1
            if tag_counts["[official]"] > 0:
                s += 1
            scores[name] = min(s, 3)
        elif name == "Evidence":
            if total_tags == 0:
                scores[name] = 0
            elif total_tags == 1:
                scores[name] = 1
            elif total_tags == 2:
                scores[name] = 2
            else:
                scores[name] = 3
        elif name == "Agentic relevance":
            agentic_terms = (
                "agent",
                "tool use",
                "orchestrat",
                "multi-agent",
                "memory",
                "planner",
                "mcp",
                "workflow",
            )
            hits = sum(1 for t in agentic_terms if t in lower)
            scores[name] = min(hits, 3)
        elif name == "Uniqueness":
            # Presence of a "what's different" phrasing
            s = 0
            if re.search(r"\b(unique|distinct|unlike|differs?|novel)\b", lower):
                s += 2
            if length > 200:
                s += 1
            scores[name] = min(s, 3)
        elif name == "Maturity":
            s = 0
            if re.search(r"\b(v\d+\.\d+|semver|release cadence|maintained)\b", lower):
                s += 2
            if re.search(r"\b(apache|mit|bsd|gpl)\b", lower):
                s += 1
            scores[name] = min(s, 3)
        elif name.lower().startswith("licens"):
            scores[name] = 3 if re.search(r"\b(apache|mit|bsd|gpl|license)\b", lower) else 0
        elif name.lower().startswith("community"):
            # Tiebreaker-only by policy. Give a neutral signal if there's any URL.
            scores[name] = 2 if has_url else 0
        else:
            scores[name] = 1  # unknown dimension: neutral
    return scores


def _find_anti_patterns(entry_md: str, policy: Policy) -> list[AntiPatternHit]:
    hits: list[AntiPatternHit] = []
    for i, line in enumerate(entry_md.splitlines(), start=1):
        low = line.lower()
        for phrase in policy.hype_phrases:
            if phrase in low:
                hits.append(AntiPatternHit(phrase=phrase, line=i))
        if _STARS_AS_EVIDENCE.search(line):
            hits.append(AntiPatternHit(phrase="stars-as-evidence", line=i))
    return hits


def score_entry(entry_md: str, policy: Policy) -> ValidationResult:
    rubric = policy.rubric
    raw = _raw_score_for_entry(entry_md, rubric)
    weighted = {d.name: raw.get(d.name, 0) * d.weight for d in rubric.dimensions}
    total = sum(weighted.values())

    hard_fail = [name for name in rubric.hard_gates if raw.get(name, 0) == 0]
    ap_hits = _find_anti_patterns(entry_md, policy)

    tags_present = [tag for tag in _EVIDENCE_TAGS if tag in entry_md.lower()]

    notes: list[str] = []
    if hard_fail:
        verdict = "block"
        notes.append(f"Hard-gate failure on: {', '.join(hard_fail)}.")
    elif ap_hits:
        verdict = "request-changes"
        notes.append(f"Anti-pattern hits: {len(ap_hits)}.")
    elif total < rubric.merge_threshold:
        verdict = "request-changes"
        notes.append(
            f"Weighted score {total}/{rubric.max_score} below merge threshold "
            f"{rubric.merge_threshold}."
        )
    else:
        verdict = "merge"
        notes.append(
            f"Weighted score {total}/{rubric.max_score} ≥ {rubric.merge_threshold}; "
            "hard gates pass; no anti-pattern hits."
        )

    return ValidationResult(
        score=total,
        max_score=rubric.max_score,
        per_dimension=weighted,
        per_dimension_raw=raw,
        hard_gate_failures=hard_fail,
        anti_pattern_hits=ap_hits,
        evidence_tags=tags_present,
        verdict=verdict,
        notes=notes,
    )
