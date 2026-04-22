# Entry Rubric

The curation bar for every entry in this repository. Applied on every PR that adds or refreshes an entry.

> This rubric is the **formal scoring model** for the four-field "Entry Rubric (v1)" summary in [`CONTRIBUTING.md`](CONTRIBUTING.md). The v1 fields stay as the quick self-assessment contributors fill in; reviewers use the seven dimensions below to score and gate the merge.

## The seven dimensions

| # | Dimension | Weight | What it measures |
|---|-----------|-------:|------------------|
| 1 | **Reliability** | ×3 | Production-readiness, API stability, known deployments, operator track record, failure-mode transparency. |
| 2 | **Evidence** | ×3 | Claims are anchored in `[official]` docs, `[benchmark]` results with methodology, `[field report]` write-ups, or `[author assessment]` synthesized from the above. See [`appendix/benchmark-and-evidence-policy.md`](appendix/benchmark-and-evidence-policy.md). |
| 3 | **Agentic relevance** | ×3 | Direct fit to the mission scope: agent architectures, orchestration, memory, evaluation, protocols, tool use, multi-agent. |
| 4 | **Uniqueness** | ×2 | What this entry adds that existing entries in the list do not. No duplicates without added structure or judgement. |
| 5 | **Maturity** | ×2 | Release cadence, active maintenance, project age, breaking-change discipline, docs depth. |
| 6 | **Licensing / openness** | ×1 | License clarity; does it permit the use described in the entry. |
| 7 | **Community signal** | ×1 | Stars, adoption, ecosystem traction. **Tiebreaker only.** Never sufficient on its own. |

## Scoring scale

Each dimension is scored **0–3**:

| Score | Meaning |
|------:|---------|
| 0 | **Fails** — no credible signal, or signal contradicts the claim. |
| 1 | **Weak** — partial or thin signal; would not hold up to scrutiny. |
| 2 | **Solid** — clear, verifiable signal; meets the bar. |
| 3 | **Exemplary** — well-documented, widely verified, best-in-class signal. |

## Totals and thresholds

- **Maximum weighted score:** **45**.
  - Per-dimension max (score 3 × weight): Reliability 9, Evidence 9, Agentic relevance 9, Uniqueness 6, Maturity 6, Licensing 3, Community 3. Sum = 45.
- **Merge threshold:** **≥ 27 / 45** (60%).
- **Hard gates** — merge is blocked if any of these score **0**, regardless of total:
  - Reliability
  - Evidence
  - Agentic relevance
- **Tie-break** — when choosing between two otherwise-equivalent candidates for a single slot, use **Community signal**. Never use community signal to compensate for a failing hard gate.

## How to score (for reviewers)

1. Read the entry and its cited evidence first. If evidence is missing, stop and request sources.
2. Score each of the seven dimensions 0–3 using the scale above.
3. Apply the weights and sum. Write the scored table into the PR review.
4. Check the hard gates. If any is 0, request changes regardless of total.
5. If the total is below 27, request changes with specific dimensions to address.
6. Keep scoring notes terse — one line per dimension citing the signal you used.

## Worked example

**Candidate:** *FictionalFlow* — a hypothetical orchestration framework for typed multi-agent DAGs.

| Dimension | Score | Weighted | Justification |
|-----------|-----:|--------:|---------------|
| Reliability | 2 | 6 | `[field report]` from one public production deployment; stable v1 API for 9 months. |
| Evidence | 2 | 6 | `[official]` docs thorough; one `[benchmark]` on a realistic workload; no independent replication yet. |
| Agentic relevance | 3 | 9 | Core agent orchestration primitive; first-class tool use, memory, and approval gates. |
| Uniqueness | 2 | 4 | Typed DAG + checkpointing distinct from existing entries; overlaps partially with LangGraph. |
| Maturity | 2 | 4 | Semantic versioning, ~14 months old, weekly releases, responsive issue triage. |
| Licensing | 3 | 3 | Apache-2.0, clear contributor agreement. |
| Community signal | 2 | 2 | Moderate adoption; not a primary decision factor here. |
| **Total** | | **34 / 45** | **Merge:** hard gates pass, total ≥ 27. |

**Reviewer note:** Approve for merge. Flag Evidence for re-review in 6 months if independent benchmarks materialize.

## Relationship to the v1 self-assessment

Contributors fill in four fields (`Reliability`, `Evidence`, `Uniqueness`, `Maturity`) in the PR template — the quick self-assessment. Reviewers expand that into the full seven-dimension weighted score above. A PR can only merge when the reviewer's scored table meets the threshold and passes the hard gates.

## What fails the rubric

See [`ANTI-PATTERNS.md`](ANTI-PATTERNS.md) for concrete rejection patterns mapped to the dimensions they fail.

## Change control

This rubric is reviewed **quarterly**. Changes to dimensions, weights, or thresholds require a PR against `main` citing the review that prompted the change.
