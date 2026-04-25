# Phase 9 — Evaluation Spec & Golden Sets: Plan

Six task groups, sequential. Close Phase 9 in one branch.

## 1. Promote `specs/evaluation.md` (9.1)

1.1. Read the existing `specs/evaluation.md` skeleton end to end. Confirm every section lines up with `RUBRIC.md` (seven dimensions, 0–3 scale, hard gates) and `rubric.py` (`ValidationResult.per_dimension_raw` schema). Note any drift.
1.2. Add a short "Status: shipped (Phase 9)" line at the top referencing `2026-04-24-phase-9-evaluation-and-golden-sets/`.
1.3. Edit the Skill evaluation → Golden set section so the per-item format (`NN-<slug>.md` + `NN-<slug>.json`) and JSON schema (seven-dimension human_scores, outcome, rationale, source) are explicit. Today these are implied; make them normative.
1.4. Edit the Agreement floor section so "stub is enforcement floor, live is advisory" is restated alongside the κ 0.6 number, with a pointer to `tools/repo-agent/tests/test_golden_set_kappa.py`.
1.5. Edit the Phase 9.4 line from "enforced by a lint step added in Phase 9.4" to "declared in Phase 9.4; lint enforcement deferred to a follow-up branch". This matches the scope decision in `requirements.md` §10.
1.6. Add a "Last reviewed: April 2026" footer and a pointer to `roadmap.md` Phase 9.

## 2. Build the golden set (9.2)

2.1. Create directory `tools/repo-agent/tests/fixtures/golden/`.
2.2. Add a short `README.md` in that directory describing the pair format, the outcome distribution (7/7/7), and the curation process.
2.3. Generate 7 **accept** items:
  - Derive from real entries in `README.md`, `appendix/open-source-models-for-agents.md`, `appendix/browser-and-desktop-agents.md`, `appendix/voice-agents.md`, `appendix/customer-support-and-crm-agents.md`. Anonymise project names only if needed to keep the test durable; most entries already carry evidence tags.
  - For each: write a candidate entry Markdown block with at least one evidence tag and an agentic-relevance signal. Human scores should all be ≥ 2 on hard gates; total well above 27/45.
2.4. Generate 7 **revise** items:
  - Synthetic entries with one of: thin evidence (one tag only), weak agentic relevance (only `tool` mentioned, no `agent`), missing maturity signal, or a marketing-adjacent phrase that is borderline but not a hard anti-pattern.
  - Human scores cluster around the merge threshold (25–28/45 weighted).
2.5. Generate 7 **reject** items:
  - Synthetic entries hitting hard-gate failures (no evidence tags at all, zero agentic terms) or explicit anti-patterns from `ANTI-PATTERNS.md` (stars-as-evidence, hype phrases).
  - Human scores: hard-gate dimension at 0.
2.6. For every item: write the paired `NN-<slug>.json` with `{"slug", "outcome", "human_scores": {…7 dims…}, "rationale", "source"}`. Use stable two-digit prefixes `01-` through `21-`.
2.7. Sanity check: run a quick `jq`-style scan (or a throwaway Python one-liner) to confirm all 21 JSON files parse and carry all seven dimension keys exactly.

## 3. Build the κ regression test (9.3)

3.1. Create `tools/repo-agent/tests/test_golden_set_kappa.py`.
3.2. Implement `_cohens_kappa(machine: list[int], human: list[int]) -> float` — unweighted κ over discrete 0..3 categories. ~30 lines, no dependencies. Return `1.0` on perfect agreement, `0.0` on chance, negative on worse-than-chance. Handle the degenerate case (zero variance) by returning `1.0` iff arrays are identical else `0.0`.
3.3. Implement `_load_golden_set(root: Path) -> list[dict]` — glob `*.json`, open each, validate the seven required dimension keys, return sorted list.
3.4. Implement the main test:
  - Load policy via `repo_agent.rubric.load_policy()`.
  - For each golden item, read the paired `.md`, call `score_entry(entry_md, policy)`, collect `per_dimension_raw`.
  - For each of the seven dimensions: pair (machine, human) across all 21 items, compute κ, assert `κ ≥ 0.6`. On failure, the assertion message names the dimension, the κ value, and the item-by-item diffs.
3.5. Run `pytest -q` from `tools/repo-agent/`. **Expected:** 72 → 73 passed. If any dimension falls below 0.6, treat as a curation signal — iterate the golden set's human scores (not the scorer) until the floor holds, recording each change in the rationale field per requirements.md §7.
3.6. Confirm the test respects the trust boundary: no file writes, no network, no mocks, no fixture autouse.

## 4. Declare audience + evidence class on every section (9.4)

4.1. Add the blockquote line `> Audience: <role> · Evidence class: <class>` under each H2 section in `README.md`. Use the bounded vocabulary from `requirements.md` §9. Insert immediately after the section heading, before the first line of content; separate with a blank line.
4.2. Add the blockquote line at the top of each `appendix/*.md` file (all 9 files), immediately after the H1 title line and any existing "Last reviewed:" block. One declaration per file.
4.3. Scan for stray occurrences of the mission line "Enforced by a lint step added in Phase 9.4" outside `evaluation.md` — none expected; delete any found.
4.4. Verify with `grep`: every appendix file carries exactly one `> Audience:` line; `README.md` carries one per top-level H2.

## 5. Validate (all of 9.1–9.4)

5.1. Open `validation.md` and walk the checklist.
5.2. Confirm `pytest -q` from `tools/repo-agent/` ⇒ 73 passed (72 prior + 1 new κ test).
5.3. Confirm `git diff --name-only origin/main...HEAD` matches the expected set: `specs/roadmap.md`, `specs/evaluation.md`, `specs/2026-04-24-phase-9-evaluation-and-golden-sets/*` (3 files, gitignored — recorded only on branch), `tools/repo-agent/tests/fixtures/golden/` (22 files: README + 21 pairs = README + 21 × 2 = 43), `tools/repo-agent/tests/test_golden_set_kappa.py`, `README.md`, `appendix/*.md` (9 files). Note: the spec files under `specs/2026-04-24-…/` are gitignored by `.gitignore:210` and will need `-f` or will stay local-only per prior phases' convention.
5.4. Confirm no changes to: `tools/repo-agent/src/**`, `.github/workflows/**`, `tools/repo-agent/pyproject.toml`, `CHANGELOG.md`, `RUBRIC.md`, `ANTI-PATTERNS.md`.
5.5. Confirm no hype language and no earned-tier claims were introduced.

## 6. Close out

6.1. Check off 9.1, 9.2, 9.3, 9.4 in `specs/roadmap.md` and append a shipping-note paragraph matching the format of prior phases. Name the branch, the spec directory, the new test, and the header-declaration surface.
6.2. Commit — one commit, message `docs(phase-9): close Phase 9 — evaluation spec + golden set + κ regression + per-section evidence class declarations`. Use `git add -f` for the tracked-but-gitignored spec files (`specs/evaluation.md`, `specs/roadmap.md`, `specs/2026-04-24-phase-9-evaluation-and-golden-sets/*`) per the convention established in Phase 8.
6.3. Do **not** open the PR — wait for explicit user instruction.
