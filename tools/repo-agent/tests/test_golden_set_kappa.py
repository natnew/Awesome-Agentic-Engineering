"""Phase 9.3 — Cohen's κ regression test for the rubric scorer.

Loads the golden set under ``tests/fixtures/golden/``, runs ``score_entry()``
on each item, computes Cohen's κ per rubric dimension between the machine
score and the human reference score, and fails the suite if any dimension
falls below the floor declared in ``specs/evaluation.md`` (κ ≥ 0.6).

No new dependencies. κ is implemented inline. No mocks, no fixtures, no
network. Reads only — never writes.
"""

from __future__ import annotations

import json
from pathlib import Path

from repo_agent.rubric import load_policy, score_entry

KAPPA_FLOOR = 0.6

DIMENSIONS = (
    "Reliability",
    "Evidence",
    "Agentic relevance",
    "Uniqueness",
    "Maturity",
    "Licensing / openness",
    "Community signal",
)

GOLDEN_DIR = Path(__file__).parent / "fixtures" / "golden"


def _cohens_kappa(a: list[int], b: list[int]) -> float:
    """Unweighted Cohen's κ over discrete categories.

    Returns 1.0 on perfect agreement (including the zero-variance edge case),
    0.0 if expected agreement is 1.0 with non-perfect observed (defensive).
    """
    assert len(a) == len(b) and len(a) > 0
    n = len(a)
    categories = sorted(set(a) | set(b))
    po = sum(1 for x, y in zip(a, b) if x == y) / n
    pe = 0.0
    for c in categories:
        pa = sum(1 for x in a if x == c) / n
        pb = sum(1 for x in b if x == c) / n
        pe += pa * pb
    if pe >= 1.0:
        return 1.0 if po == 1.0 else 0.0
    return (po - pe) / (1.0 - pe)


def _load_golden_set() -> list[tuple[str, str, dict[str, int]]]:
    """Return [(slug, entry_md, human_scores), ...] sorted by filename."""
    items: list[tuple[str, str, dict[str, int]]] = []
    json_files = sorted(GOLDEN_DIR.glob("*.json"))
    assert json_files, f"No golden items found under {GOLDEN_DIR}"
    for jpath in json_files:
        meta = json.loads(jpath.read_text(encoding="utf-8"))
        mpath = jpath.with_suffix(".md")
        assert mpath.exists(), f"Missing paired Markdown for {jpath.name}"
        human = meta["human_scores"]
        missing = [d for d in DIMENSIONS if d not in human]
        assert not missing, f"{jpath.name} missing dimensions: {missing}"
        for d in DIMENSIONS:
            v = human[d]
            assert isinstance(v, int) and 0 <= v <= 3, f"{jpath.name}: bad score for {d!r}: {v!r}"
        items.append((meta["slug"], mpath.read_text(encoding="utf-8"), human))
    return items


def test_golden_set_size_and_distribution() -> None:
    items = _load_golden_set()
    assert len(items) >= 20, f"Golden set must have ≥20 items, has {len(items)}"
    outcomes: dict[str, int] = {}
    for jpath in sorted(GOLDEN_DIR.glob("*.json")):
        oc = json.loads(jpath.read_text(encoding="utf-8"))["outcome"]
        outcomes[oc] = outcomes.get(oc, 0) + 1
    for required in ("accept", "revise", "reject"):
        assert outcomes.get(required, 0) >= 5, (
            f"Need ≥5 {required} items for outcome spread, have {outcomes.get(required, 0)}"
        )


def test_kappa_floor_per_dimension() -> None:
    policy = load_policy()
    items = _load_golden_set()

    machine: dict[str, list[int]] = {d: [] for d in DIMENSIONS}
    human: dict[str, list[int]] = {d: [] for d in DIMENSIONS}
    slugs: list[str] = []

    for slug, entry_md, human_scores in items:
        result = score_entry(entry_md, policy)
        slugs.append(slug)
        for d in DIMENSIONS:
            machine[d].append(int(result.per_dimension_raw.get(d, 0)))
            human[d].append(int(human_scores[d]))

    failures: list[str] = []
    for d in DIMENSIONS:
        kappa = _cohens_kappa(machine[d], human[d])
        if kappa < KAPPA_FLOOR:
            diffs = [
                f"  {slugs[i]}: machine={machine[d][i]} human={human[d][i]}"
                for i in range(len(slugs))
                if machine[d][i] != human[d][i]
            ]
            failures.append(
                f"[{d}] κ={kappa:.3f} < {KAPPA_FLOOR}. Divergences:\n" + "\n".join(diffs)
            )

    assert not failures, "Cohen's κ floor breached:\n\n" + "\n\n".join(failures)
