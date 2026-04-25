# Golden set — Phase 9.2

Twenty-one labelled candidate entries used to evaluate the rubric scorer
([`tools/repo-agent/src/repo_agent/rubric.py`](../../../src/repo_agent/rubric.py)
`score_entry()`) against a human baseline. The test that consumes this
directory is
[`test_golden_set_kappa.py`](../../test_golden_set_kappa.py).

## Layout

Every item is a matched pair:

- `NN-<slug>.md` — the candidate entry Markdown (the input to `score_entry`).
- `NN-<slug>.json` — the human reference labels.

Two-digit numeric prefixes (`01-` through `21-`) give stable ordering.

## Outcome distribution

- `accept` — 7 items (`01-` through `07-`).
- `revise` — 7 items (`08-` through `14-`).
- `reject` — 7 items (`15-` through `21-`).

## JSON schema

```json
{
  "slug": "string",
  "outcome": "accept | revise | reject",
  "human_scores": {
    "Reliability": 0,
    "Evidence": 0,
    "Agentic relevance": 0,
    "Uniqueness": 0,
    "Maturity": 0,
    "Licensing / openness": 0,
    "Community signal": 0
  },
  "rationale": "string",
  "source": "string"
}
```

The seven dimension keys must match the names emitted by
`score_entry().per_dimension_raw` exactly (case-sensitive). Missing keys are a
test failure — there is no silent defaulting.

## Curation

Maintainers label items. Disagreements are resolved by discussion on the PR
thread; the decision is recorded in the item's `rationale`. Any score change
after the initial commit also records the reason in `rationale`.

The current floor is **Cohen's κ ≥ 0.6 per dimension** (declared in
[`specs/evaluation.md`](../../../../../specs/evaluation.md)). Lowering the floor
requires a maintainer override and a note in `CHANGELOG.md`.
