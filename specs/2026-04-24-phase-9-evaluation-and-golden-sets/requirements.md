# Phase 9 — Evaluation Spec & Golden Sets: Requirements

Scope: close all of Phase 9 (9.1–9.4) in one branch. Promote `specs/evaluation.md` from descriptive skeleton to shipped spec, add a ≥20-item golden set under `tools/repo-agent/tests/fixtures/golden/`, enforce a Cohen's κ ≥ 0.6 per-dimension floor in pytest, and declare audience + evidence class on every `README.md` section and every `appendix/*.md` file.

## Context

Phase 8 closed. The repo-agent has a documented architecture spec (`specs/architecture.md`) with layer boundaries, invocation modes, and escalation paths. The rubric scorer (`tools/repo-agent/src/repo_agent/rubric.py`) is deterministic today and has never been evaluated against a human baseline. `specs/evaluation.md` already carries a descriptive skeleton naming κ ≥ 0.6 as the floor — this phase promotes that skeleton to enforceable.

The existing `evaluation.md` skeleton covers:

- Content evaluation (per PR, rubric coverage, evidence tags).
- Skill evaluation (golden set, κ floor, stub-vs-live).
- Workflow evaluation (new-tool, landscape-scan, review-pr).

9.1 makes that normative. 9.2 provides the data. 9.3 provides the enforcement. 9.4 closes the mission-level commitment that every section declares its audience and evidence class.

## In scope

1. **9.1 — Shipped `specs/evaluation.md`.** Firm up the existing skeleton: confirm the seven rubric dimensions are named (matching `RUBRIC.md` and `rubric.py`), lock the golden-set path, lock Cohen's κ per dimension as the metric, lock the floor at 0.6, lock the stub-enforcement / live-advisory split, lock the update-floor policy. Add one normative diagram or list — no hype language.
2. **9.2 — Golden set at `tools/repo-agent/tests/fixtures/golden/`.**
   - **Size:** ≥ 20 items (target: 21 to be safely above the floor).
   - **Shape:** each item is a pair: `NN-<slug>.md` (candidate entry Markdown) + `NN-<slug>.json` (human reference scores + rationale).
   - **JSON schema:** `{"slug": str, "outcome": "accept" | "revise" | "reject", "human_scores": {<dimension>: 0..3}, "rationale": str, "source": str}`. `human_scores` covers all seven dimensions by exact name matching `rubric.py` (`Reliability`, `Evidence`, `Agentic relevance`, `Uniqueness`, `Maturity`, `Licensing / openness`, `Community signal`).
   - **Composition:** a spread of outcomes covering at least 7 accept, 7 revise, 7 reject. Candidate entries are a mix of (a) lightly anonymised real entries drawn from `README.md` / `appendix/**` (accept cases), (b) synthetic revise cases with thin evidence or missing tags, (c) synthetic reject cases hitting known anti-patterns (`ANTI-PATTERNS.md`) or hard-gate failures.
   - **Curation:** this branch adds the golden set and records it as "maintainer-labelled". Inter-rater discussion will be on the PR thread; if any item's scores shift during review the commit that changes them also records the reason in the rationale field.
3. **9.3 — Pytest regression harness.**
   - **Location:** `tools/repo-agent/tests/test_golden_set_kappa.py`.
   - **What it does:** for each golden item, call `score_entry(entry_md, policy).per_dimension_raw` and collect per-dimension machine scores; pair with `human_scores`; compute Cohen's κ per dimension across all items; fail if any dimension's κ < 0.6.
   - **κ implementation:** inline, pure-Python, no new dependency. Discrete 0..3 categories; unweighted κ. Helper lives in the test file (not in `src/`) to keep the boundary small.
   - **Runs with `StubLLMClient`:** the scorer is deterministic today and does not depend on an LLM, so this is already the case — no wiring needed beyond calling `score_entry` directly.
   - **Live variant:** a `@pytest.mark.live` copy of the test is **not** added in this branch — the evaluation.md text already specifies `live` is advisory and opt-in; adding it here would bloat scope without new signal.
4. **9.4 — Per-section audience + evidence class declaration.**
   - **Schema:** a single blockquote line inserted under each H1/H2 heading (or at the top of each appendix file), exactly shaped: `> Audience: <role> · Evidence class: <official | benchmark | field report | mixed>`.
   - **Surface:** `README.md` top-level H2 sections + all nine `appendix/*.md` files (flat, one declaration per file; the file's top-level section gets the marker, sub-sections inherit).
   - **Role vocabulary:** bounded set — `practitioners`, `researchers`, `maintainers`, `all contributors`. Any section using a role outside this set must justify in the PR body.
   - **Evidence class vocabulary:** matches the tags in `appendix/benchmark-and-evidence-policy.md` — `official`, `benchmark`, `field report`, `mixed`. `mixed` means the section draws on multiple classes (the common case for curated lists).
   - **No lint step added this branch.** The mission line "Enforced by a lint step added in Phase 9.4" in `evaluation.md` is edited to "declared in Phase 9.4; lint enforcement deferred to a follow-up branch" — adding a markdownlint rule for a freeform header line would be disproportionate. The declarations are human-checkable at review time.

## Out of scope

- New Python dependencies. κ is implemented inline.
- New CI workflows. `repo-agent-tests.yml` already runs `pytest -q` and will pick up the new test automatically.
- Changes to the rubric scorer's own logic in `rubric.py`. Measurement only — no code changes to the thing being measured.
- A markdownlint rule enforcing the audience/evidence-class header format. Deferred to a follow-up PR.
- A live-LLM variant of the κ test. Deferred; advisory by policy.
- Changes to `specs/mission.md` claim language. The Phase 9 completion does not trip any earned-tier gate.

## Decisions

1. **Metric.** Cohen's κ per rubric dimension across all golden items. Unweighted. Enforcement on stub; advisory on live.
2. **Floor.** 0.6 per dimension (the existing `evaluation.md` skeleton value). Breach fails the test.
3. **Golden-set size.** 21 items (accept 7 · revise 7 · reject 7).
4. **Golden-set location.** `tools/repo-agent/tests/fixtures/golden/` — directory already exists (parent), create this subfolder.
5. **Per-item format.** Matched pair: `NN-<slug>.md` + `NN-<slug>.json`. Numeric prefix gives stable ordering; JSON covers schema in §2.
6. **Human-score schema.** Seven-dimension dict matching `rubric.py` dimension names exactly. Missing dimensions in a JSON file = test failure (explicit, no silent defaulting).
7. **κ helper boundary.** In the test file only. Not added to `src/repo_agent/`. If a second caller ever needs it, promote then.
8. **9.4 header shape.** Single blockquote line: `> Audience: <role> · Evidence class: <class>`. One per section or per appendix file.
9. **9.4 vocabulary.** Role ∈ {`practitioners`, `researchers`, `maintainers`, `all contributors`}. Evidence class ∈ {`official`, `benchmark`, `field report`, `mixed`}.
10. **9.4 lint deferral.** `evaluation.md` wording changed from "enforced by a lint step" to "declared in Phase 9.4; lint enforcement deferred". Recorded as an explicit trade-off in this requirements.md.
11. **Trust boundary preserved.** The new test and the golden set never write to content files; they only read. No new side effects anywhere.

## Non-goals

- Measuring the `triage_pr` or `review-pr` workflows against human labels in this branch. The shipped evaluation.md names them; the harness landing here covers `validate_entry` / `score_entry` only. Extending to the other skills is deferred.
- Tuning the rubric scorer to raise κ. Measurement only; any tuning is a separate PR whose diff stays in `rubric.py`.
- Publishing κ on the docs site. Numbers stay in the test log until Phase 12 observability exists.

## References

- [specs/mission.md](../mission.md) — per-section audience + evidence class commitment.
- [specs/tech-stack.md](../tech-stack.md) — trust boundary; no agent writes to content.
- [specs/evaluation.md](../evaluation.md) — existing skeleton being promoted.
- [RUBRIC.md](../../RUBRIC.md) — seven dimensions + 0–3 scale + hard gates.
- [ANTI-PATTERNS.md](../../ANTI-PATTERNS.md) — source for reject-case golden items.
- [tools/repo-agent/src/repo_agent/rubric.py](../../tools/repo-agent/src/repo_agent/rubric.py) — `score_entry` and `ValidationResult`.
- [appendix/benchmark-and-evidence-policy.md](../../appendix/benchmark-and-evidence-policy.md) — evidence-tag vocabulary.
