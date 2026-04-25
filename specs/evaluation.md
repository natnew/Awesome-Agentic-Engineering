# Evaluation

> Status: shipped (Phase 9). Spec history: `specs/2026-04-24-phase-9-evaluation-and-golden-sets/`.

Scope: evaluation of (a) content-entry curation and (b) the repo-agent's rubric-scoring skill itself. Content evaluation happens at PR review time; skill evaluation happens in CI against a golden set.

## Content evaluation (per entry)

Every entry added or refreshed via PR must carry a rubric score recorded in the PR body. The rubric is defined in [`RUBRIC.md`](../RUBRIC.md) and covers seven dimensions: `Reliability`, `Evidence`, `Agentic relevance`, `Uniqueness`, `Maturity`, `Licensing / openness`, and `Community signal`.

- **Rubric coverage target:** 100% of content PRs merged after Phase 9.
- **Evidence tags required on the entry:** at least one of `[official]`, `[benchmark]`, `[field report]`, or `[author assessment]` (see [`appendix/benchmark-and-evidence-policy.md`](../appendix/benchmark-and-evidence-policy.md)).
- **Per-section header declaration:** every `README.md` H2 section and every `appendix/*.md` file declares its primary audience and evidence class as a single blockquote line of the form `> Audience: <role> · Evidence class: <class>`. Declared in Phase 9.4; lint enforcement deferred to a follow-up branch (a markdownlint custom rule for a freeform header line is disproportionate to the value; declarations are human-checkable at review time).
  - **Role vocabulary:** `practitioners`, `researchers`, `maintainers`, `all contributors`.
  - **Evidence class vocabulary:** `official`, `benchmark`, `field report`, `mixed`. `mixed` is the common case for curated lists drawing on multiple classes.

## Skill evaluation (repo-agent rubric scorer)

The `validate_entry` / `triage_pr` / `review-pr` skills produce rubric scores via [`tools/repo-agent/src/repo_agent/rubric.py`](../tools/repo-agent/src/repo_agent/rubric.py) `score_entry()`. These must be evaluated against a human baseline.

### Golden set

- **Location:** [`tools/repo-agent/tests/fixtures/golden/`](../tools/repo-agent/tests/fixtures/golden/).
- **Size floor:** ≥ 20 items covering a spread of (accept, revise, reject) outcomes. Today: 21 items, 7 per outcome.
- **Per-item format:** matched pair — `NN-<slug>.md` (the candidate entry Markdown) and `NN-<slug>.json` (the human reference labels). Two-digit prefixes give stable ordering across all loaders.
- **JSON schema (normative):**

  ```json
  {
    "slug": "string",
    "outcome": "accept | revise | reject",
    "human_scores": {
      "Reliability": 0-3,
      "Evidence": 0-3,
      "Agentic relevance": 0-3,
      "Uniqueness": 0-3,
      "Maturity": 0-3,
      "Licensing / openness": 0-3,
      "Community signal": 0-3
    },
    "rationale": "string",
    "source": "string"
  }
  ```

  Dimension keys must match the names emitted by `score_entry().per_dimension_raw` exactly (case-sensitive). Missing dimensions are a test failure — no silent defaulting.

- **Curation:** maintainers label items. Disagreements are resolved by discussion on the PR thread; the decision is recorded in the item's `rationale` field. Any score change after the initial commit also records the reason in `rationale`.

### Agreement floor

- **Target:** Cohen's κ ≥ 0.6 between the skill's `per_dimension_raw[<dim>]` and `human_scores[<dim>]` on the golden set, measured **per rubric dimension** (unweighted κ over discrete categories `0..3`).
- **Regression test:** [`tools/repo-agent/tests/test_golden_set_kappa.py`](../tools/repo-agent/tests/test_golden_set_kappa.py) loads the golden set, runs `score_entry()` on each item, computes κ per dimension, and fails the suite if any dimension drops below the floor. The test imports nothing beyond `repo_agent.rubric` and the standard library — κ is implemented inline with no new dependency.
- **Stub-vs-live:** in CI the stub is exercised (the heuristic scorer is deterministic and does not call out to an LLM today). A separate `@pytest.mark.live` variant exercising a live provider is **deferred**: stub κ is the enforcement floor, live κ is advisory and contributor-local when it lands.

### When to update the floor

- On a deliberate prompt or scorer change, the PR author re-runs the harness and records the new κ values in the PR body. **Raising** the floor (tightening the gate) is encouraged. **Lowering** the floor requires a maintainer override and a note in [`CHANGELOG.md`](../CHANGELOG.md) under an `### Evaluation` subheading explaining the regression.

## Workflow evaluation (Phase 6 workflows)

- `workflow new-tool`: golden fixture of ≥3 URLs with expected draft shape. Test asserts the draft contains the rubric table and an evidence tag.
- `workflow landscape-scan`: fixture asserts digest upsert is idempotent (see [`memory-model.md`](./memory-model.md)).
- `workflow review-pr`: fixture asserts a scorecard comment is produced and that `skip-review-assistant` suppresses it.

All three already have offline tests via `httpx.MockTransport`; Phase 9 adds the κ regression on top of `score_entry()` itself, since the three workflows all delegate to it.

## Reporting

- **PR body:** contributor records rubric score and evidence tags.
- **CI:** the κ regression test logs κ per dimension to the workflow log and, in Phase 12 ([`observability.md`](./observability.md)), to a structured log record.
- **Quarterly:** κ values and coverage percentages are appended to [`CHANGELOG.md`](../CHANGELOG.md) under a `### Evaluation` subheading.

---

Last reviewed: April 2026 · See [roadmap.md](./roadmap.md) Phase 9.
