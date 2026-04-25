# Phase 9 — Evaluation Spec & Golden Sets: Validation

Merge gate — all items must hold before opening the PR.

## A. Spec (9.1)

1. `specs/evaluation.md` has a "Status: shipped (Phase 9)" line pointing at `2026-04-24-phase-9-evaluation-and-golden-sets/`.
2. Every one of the seven rubric dimensions from `RUBRIC.md` is named in `evaluation.md` at least once (`Reliability`, `Evidence`, `Agentic relevance`, `Uniqueness`, `Maturity`, `Licensing / openness`, `Community signal`).
3. `evaluation.md` explicitly states the golden-set location (`tools/repo-agent/tests/fixtures/golden/`), the per-item format (`NN-<slug>.md` + `NN-<slug>.json`), and the JSON schema.
4. `evaluation.md` names Cohen's κ as the metric, 0.6 as the floor, stub as the enforcement surface, live as advisory, and points at `tools/repo-agent/tests/test_golden_set_kappa.py`.
5. `evaluation.md` explicitly defers lint enforcement of 9.4 headers to a follow-up branch (wording updated from the earlier "enforced by a lint step" phrasing).
6. `evaluation.md` carries a "Last reviewed: April 2026" footer pointing at `roadmap.md` Phase 9.
7. No earned-tier language introduced anywhere in `evaluation.md`.

## B. Golden set (9.2)

8. `tools/repo-agent/tests/fixtures/golden/` exists and contains exactly: one `README.md`, twenty-one `NN-<slug>.md` files, and twenty-one matching `NN-<slug>.json` files. Total: 43 files.
9. Filename prefixes are `01-` through `21-`, contiguous.
10. Outcome distribution: exactly 7 `accept`, 7 `revise`, 7 `reject` across the 21 JSON files.
11. Every JSON file parses and carries all seven dimension keys exactly as spelled in `rubric.py` (case-sensitive, including `Licensing / openness` and `Community signal`).
12. Every human score is an integer in `{0, 1, 2, 3}`.
13. Every rationale is a non-empty string. Every `source` field is present (may be `"synthetic"` for synthetic items).
14. The golden-set `README.md` describes the pair format, the 7/7/7 distribution, and the curation convention.

## C. κ regression test (9.3)

15. `tools/repo-agent/tests/test_golden_set_kappa.py` exists.
16. The file implements `_cohens_kappa` inline; no new dependencies added to `pyproject.toml`.
17. The file does not import anything from `repo_agent.*` other than what `rubric.load_policy` / `rubric.score_entry` provide.
18. The file contains no mocks, no monkeypatches, no fixtures from `conftest.py`, and makes no network or filesystem-write calls.
19. `pytest -q` from `tools/repo-agent/` passes with **73** tests (72 prior + 1 new).
20. The new test, when run in isolation (`pytest tests/test_golden_set_kappa.py -q`), passes in under 10 seconds.
21. Per-dimension κ values are asserted individually; if any single dimension's κ drops below 0.6 the assertion message names the dimension, the computed κ, and at least one item whose machine-vs-human score diverged most.

## D. Per-section declarations (9.4)

22. Every `appendix/*.md` file (all 9) carries exactly one `> Audience: <role> · Evidence class: <class>` blockquote line near the top of the file (after the H1 title and any pre-existing "Last reviewed:" block).
23. Every H2 section in `README.md` carries exactly one `> Audience: … · Evidence class: …` blockquote line directly after the heading.
24. The role token on every declaration is drawn from {`practitioners`, `researchers`, `maintainers`, `all contributors`}. No other roles present.
25. The evidence-class token on every declaration is drawn from {`official`, `benchmark`, `field report`, `mixed`}. No other classes present.
26. No regex occurrence of "Enforced by a lint step added in Phase 9.4" remains anywhere in the repo.

## E. Scope discipline

27. `git diff --name-only origin/main...HEAD` contains exactly these paths (plus the gitignored `specs/2026-04-24-…/*` files after `git add -f`):
  - `specs/evaluation.md`
  - `specs/roadmap.md`
  - `specs/2026-04-24-phase-9-evaluation-and-golden-sets/requirements.md`
  - `specs/2026-04-24-phase-9-evaluation-and-golden-sets/plan.md`
  - `specs/2026-04-24-phase-9-evaluation-and-golden-sets/validation.md`
  - `tools/repo-agent/tests/test_golden_set_kappa.py`
  - `tools/repo-agent/tests/fixtures/golden/README.md`
  - `tools/repo-agent/tests/fixtures/golden/NN-*.md` × 21
  - `tools/repo-agent/tests/fixtures/golden/NN-*.json` × 21
  - `README.md`
  - `appendix/*.md` × 9
28. No changes to: `tools/repo-agent/src/**`, `tools/repo-agent/pyproject.toml`, `.github/workflows/**`, `CHANGELOG.md`, `RUBRIC.md`, `ANTI-PATTERNS.md`, `CONTRIBUTING.md`, `docs/**`.
29. `specs/roadmap.md` has `[x]` on 9.1, 9.2, 9.3, 9.4 and a new shipping-note paragraph naming the branch, spec directory, new test, and header-declaration surface.
30. No hype / earned-tier phrases (`world-class`, `state-of-the-art`, `revolutionary`, `best-in-class`, `industry-leading`) anywhere in the diff.

## F. Post-commit

31. Branch `feature/phase-9-evaluation-and-golden-sets` is exactly one commit ahead of `origin/main`.
32. `pytest -q` still green (73 passed) after all files are committed.
33. The PR is **not** opened by the agent; title is staged for user approval: `docs(phase-9): close Phase 9 — evaluation spec + golden set + κ regression + per-section evidence class declarations`.
