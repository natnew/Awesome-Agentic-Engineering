# Roadmap

High-level implementation order in **very small phases**. Each phase should be shippable on its own and move the repo measurably closer to the mission.

Legend: `[ ]` not started ┬À `[~]` in progress ┬À `[x]` done

---

## Phase 1 ÔÇö Foundation & Hygiene

- [x] 1.1 Audit existing sections against the mission; flag gaps and stale entries.
- [x] 1.2 Lock contribution standards in `CONTRIBUTING.md` (rubric, evidence policy, PR template).
- [x] 1.3 Add a PR template and issue templates (new entry, stale entry, suggestion).

> Note: `README.md` is intentionally **not** modified by the constitution work. The specs live under `specs/` and are not linked from the README.
> Shipped via PR #1 (merged April 22, 2026).

## Phase 2 ÔÇö Curation Bar & Rubric

- [x] 2.1 Formalize the entry rubric (reliability, evidence, uniqueness, maturity).
- [x] 2.2 Apply rubric retroactively to one section as a pilot.
- [x] 2.3 Document "What NOT to include" with examples.

> Shipped via PR #2 (merged April 22, 2026).

## Phase 3 ÔÇö Cutting-Edge Resource Expansion

- [x] 3.1 Add/refresh: orchestration frameworks (LangGraph, Agent Framework, AutoGen, CrewAI, OpenAI Agents SDK).
- [x] 3.2 Add/refresh: protocols (MCP, A2A, tool-use standards).
- [x] 3.3 Add/refresh: memory systems (episodic, semantic, vector, graph).
- [x] 3.4 Add/refresh: evaluation & safety (benchmarks, red-teaming, guardrails).
- [x] 3.5 Add/refresh: open-source models optimized for agentic use.
- [x] 3.6 Add a new section: **Reasoning & Planning Models** (o-series, thinking models, planners).
- [x] 3.7 Add a new section: **Computer-Use & Browser Agents** (expand existing appendix).

> Shipped via PR #3 (merged April 22, 2026). Validation record: `specs/2026-04-22-phase-3-cutting-edge-expansion/validation.md`.

## Phase 4 ÔÇö Automations (CI hygiene)

- [x] 4.1 GitHub Action: markdown lint on PR. _(markdownlint-cli2, advisory)_
- [x] 4.2 GitHub Action: broken-link check on PR and weekly schedule. _(markdown-link-check; scheduled run maintains a single rolling issue on failure)_
- [x] 4.3 GitHub Action: last-updated badge auto-refresh. _(live Shields.io `github/last-commit` badge ÔÇö no workflow needed)_
- [x] 4.4 Stale-entry detector. _(monthly workflow + Node 20 script; 9-month threshold; maintains single "Freshness audit" issue)_

> Shipped via PR [#4](https://github.com/natnew/Awesome-Agentic-Engineering/pull/4) on branch `feature/phase-4-automations-ci-hygiene`. Spec: `specs/2026-04-22-phase-4-automations-ci-hygiene/`.
>
> **Rollout mode:** advisory (`continue-on-error: true` at the tool step). Both PR checks execute on every pull request, surface violations in the logs, and display green on the checks tab.
>
> **First-run findings** (to be addressed in follow-up PRs before graduating to required checks):
> - Link check: 3 real 404s in `README.md`; 2 `alignmentforum.org` 429s to add to the ignore list.
> - Markdownlint: 74 violations across `README.md`, `CONTRIBUTING.md`, `appendix/**`, `tasks/todo.md` ÔÇö mostly auto-fixable (MD022/MD032/MD049/MD012/MD009) plus 2 broken TOC fragments in `README.md` (MD051).
> - Freshness: 5 appendix files missing a `Last reviewed:` marker.
>
> **Graduation path:** small, scoped follow-up PRs for links, lint auto-fix, TOC fragments, and freshness markers ÔåÆ then flip `continue-on-error` off and require both checks in branch protection.

## Phase 5 ÔÇö The Repo as an Agentic System (v0)

- [x] 5.1 Define an **MCP server** surface for repo operations (search, propose entry, validate).
- [x] 5.2 Ship a **triage skill** ÔÇö classifies incoming PRs/issues against the rubric.
- [x] 5.3 Ship a **freshness-audit skill** ÔÇö callable variant of the Phase 4 detector; returns structured candidates.
- [x] 5.4 Ship an **entry-draft skill** ÔÇö takes a URL and drafts a rubric-aligned entry.

> Shipped on branch `feature/phase-5-repo-as-agentic-system` (PR [#5](https://github.com/natnew/Awesome-Agentic-Engineering/pull/5), commit `5f1f0ff`). Spec kept local at `specs/2026-04-22-phase-5-repo-as-agentic-system/` (per `.gitignore`, not pushed). Tool lives at `tools/repo-agent/` (Python 3.12, official MCP SDK via FastMCP, stdio transport).
>
> **Delivered:** 8 MCP tools (the 6 in the spec plus `triage_pr` and `freshness_audit` for parity) ÔÇö `list_sections`, `get_rubric`, `get_anti_patterns`, `search_entries`, `validate_entry`, `propose_entry`, `triage_pr`, `freshness_audit`. Every tool is also a CLI subcommand. 31 pytest tests passing, no live network in the default run. `LLMClient` protocol + `StubLLMClient` default means the whole system runs with zero API keys.
>
> **Validation status (24/27):** 24 items verified locally, 3 pending PR-time observation (MCP inspector round-trip, CI first run). See `specs/2026-04-22-phase-5-repo-as-agentic-system/validation.md`.
>
> **Design decisions worth flagging:** (1) skills are read-only ÔÇö they return proposed Markdown as strings, never write to content files. Issue-opening for 5.3 stays with the existing Phase 4 scheduled workflow by design. (2) The `repo-agent-tests.yml` workflow is advisory (`continue-on-error: true`) and path-scoped, matching the Phase 4 rollout pattern.

## Phase 6 ÔÇö Agentic Workflows (v1)

- [x] 6.1 End-to-end workflow: *new tool released ÔåÆ draft entry ÔåÆ human review ÔåÆ PR*.
- [x] 6.2 End-to-end workflow: *weekly landscape scan ÔåÆ digest issue with candidates*.
- [x] 6.3 End-to-end workflow: *PR review assistant that scores against the rubric*.

> Shipped on branch `feature/phase-6-agentic-workflows`. Spec: `specs/2026-04-22-phase-6-agentic-workflows/`. Tools: `tools/repo-agent/src/repo_agent/workflows/` + three `.github/workflows/phase-6-*.yml` (advisory, `continue-on-error: true`).
>
> **Delivered:** three composed workflows on top of the Phase 5 skills ÔÇö `workflow new-tool` (URL ÔåÆ rubric-aligned draft + tracking issue), `workflow landscape-scan` (weekly rolling digest issue), `workflow review-pr` (single maintained rubric scorecard comment per content PR). All three are **read-only toward repo content** ÔÇö they upsert issues/comments by stable HTML-comment markers but never write files and never open PRs automatically.
>
> **Design decisions worth flagging:** (1) no new top-level Python dependencies ÔÇö workflows reuse the Phase 5 `httpx` + `LLMClient` stack, `StubLLMClient` remains the default. (2) `GitHubClient` accepts an injected `httpx.Client`, so all 24 new tests run offline via `httpx.MockTransport`. (3) Opt-out label `skip-review-assistant` suppresses the PR comment. (4) Each workflow exposes a full CLI (`repo-agent workflow ...`) so contributors can run them locally with no setup beyond `pip install -e`.

## Phase 7 ÔÇö Publishing & Reach

- [x] 7.1 Docs-style homepage (GitHub Pages) generated from README + specs.
- [x] 7.2 Public changelog / RSS of additions.
- [x] 7.3 Submit to `awesome.re` and adjacent communities.

> Shipped on branch `feature/phase-7-publishing-and-reach` (PR [#7](https://github.com/natnew/Awesome-Agentic-Engineering/pull/7), commit `9c6c566`). Spec: `specs/2026-04-22-phase-7-publishing-and-reach/`. Site source under `docs/`, generated by `repo-agent workflow render-site`.
>
> **Delivered:** a zero-build static site (one hand-written CSS file, no JS) under `docs/` with 14 pages (landing + rubric + anti-patterns + contributing + changelog + 9 appendix pages), a `sitemap.xml`, and an RSS 2.0 `feed.xml` generated from `CHANGELOG.md`. Two advisory CI workflows (`phase-7-publish-site.yml` opens regeneration PRs on `main`; `phase-7-render-check.yml` fails stale PRs). `specs/2026-04-22-phase-7-publishing-and-reach/submission-checklist.md` tracks the awesome.re submission and adjacent-community announcements (manual actions by design).
>
> **Validation status (37/41):** 37 items verified locally (71/71 pytest green, idempotent renderer, 15.5 KB gzipped landing page, valid RSS 2.0, YAML-lint clean). 4 items pending post-merge: Pages enablement + first live URL load, first CI run green, awesome.re submission PR opened.
>
> **Evidence gate for claim-tier promotion (hard gate, all four):**
>
> 1. GitHub Pages live at the recorded URL and loading 200 OK.
> 2. First post-merge CI run of `phase-7-publish-site.yml` and `phase-7-render-check.yml` green.
> 3. awesome.re submission PR opened (recorded in `submission-checklist.md`).
> 4. ÔëÑ1 independent external citation observed (talk, paper, or production docs referencing this repo), recorded in `CHANGELOG.md`.
>
> Until all four hold, `mission.md` claim language stays at **Working** tier. Earned-tier language also requires the additional gates in `mission.md` and Phase 13.

## Phase 8 ÔÇö Architecture Spec (`architecture.md`)

- [x] 8.1 Document the repo-agent's layer boundaries (content, MCP server, CLI, skills, workflows, LLMClient).
- [x] 8.2 Document invocation modes (CLI, MCP stdio, CI workflow) and their behavioural contracts.
- [x] 8.3 Document escalation paths (LLM unavailable, GitHub API failure, disputed rubric score, broken render).
- [x] 8.4 Add one cross-layer integration test exercising CLI ÔåÆ skill ÔåÆ content read path.

> Exit criteria: `specs/architecture.md` committed; 1 new test in `tools/repo-agent/tests/` green.
>
> 8.1 shipped on branch `feature/phase-8-architecture-spec` (smallest-slice PR, docs-only). Spec: `specs/2026-04-24-phase-8-architecture-spec/`. Descriptive layer-boundary doc with one Mermaid diagram covering the six layers (content, skills, tools, MCP server, CLI, workflows) plus the `LLMClient` cross-cut. 8.2ÔÇô8.4 remain open and will land in follow-up branches; the integration-test shape (CLI subprocess ÔåÆ `search_entries` ÔåÆ `appendix/*.md`) is recorded in the spec's `requirements.md` for 8.4.
>
> 8.2 shipped on branch `feature/phase-8-2-invocation-modes` (docs-only). Spec: `specs/2026-04-24-phase-8-2-invocation-modes/`. New "Invocation modes & behavioural contracts" section in `architecture.md` with a three-row contract table (CLI ┬À MCP stdio ┬À CI workflow) covering entrypoints, inputs, outputs (stdout shape + exit codes), and permitted side effects, plus one Mermaid `sequenceDiagram`. Descriptive-only ÔÇö no code, test, or workflow changes. 8.3 and 8.4 remain open.
>
> 8.3 + 8.4 shipped on branch `feature/phase-8-close`. Spec: `specs/2026-04-24-phase-8-close/`. **Closes Phase 8.** New "Escalation paths" section in `architecture.md` with a six-row table (LLM unavailable ┬À GitHub API failure ┬À disputed rubric score ┬À broken render ┬À marker collision ┬À external URL fetch failure), one prose paragraph per mode, and one Mermaid `flowchart TD` decision diagram. 8.4 test added at `tools/repo-agent/tests/test_integration_cli_search.py` ÔÇö spawns the CLI via `subprocess`, invokes `search`, asserts the content layer returns real hits in `README.md` / `appendix/**`. Fixture-free, offline, no mocks. Descriptive-only ÔÇö no changes to `tools/repo-agent/src/**`, `.github/workflows/**`, `pyproject.toml`, or content files.

## Phase 9 ÔÇö Evaluation Spec (`evaluation.md`) & Golden Sets

- [x] 9.1 Define evaluation of the rubric-scoring skill itself (inter-rater agreement target vs. human baseline on a fixed set).
- [x] 9.2 Create a golden set of ≥20 labelled historical PRs/entries under `tools/repo-agent/tests/fixtures/golden/`.
- [x] 9.3 Add a pytest regression harness that scores the golden set and fails if agreement drops below the documented floor.
- [x] 9.4 Declare per-section evidence class in `README.md` and appendix headers (closes the mission per-section labelling commitment).

> Exit criteria: `specs/evaluation.md` committed; golden set present; regression test green; every appendix header declares audience + evidence class.
>
> Shipped on branch `feature/phase-9-evaluation-and-golden-sets`. Spec: `specs/2026-04-24-phase-9-evaluation-and-golden-sets/`. **Closes Phase 9.** `specs/evaluation.md` promoted to a shipped spec defining the seven rubric dimensions, a normative JSON schema for golden labels, and the κ ≥ 0.6 per-dimension floor (stub-enforced; live-advisory). Golden set of 21 entries under `tools/repo-agent/tests/fixtures/golden/` (7 accept · 7 revise · 7 reject) with paired `*.md` content and `*.json` human labels. Regression test at `tools/repo-agent/tests/test_golden_set_kappa.py` — runs the deterministic heuristic scorer over all 21 entries, computes unweighted Cohen's κ per dimension, and asserts every dimension clears the 0.6 floor. Per-section evidence class declared as a `> Audience: <role> · Evidence class: <class>` blockquote on every README H2 (19) and every appendix file top (9). Vocabulary: roles ⊆ {practitioners, researchers, maintainers, all contributors}; evidence classes ⊆ {official, benchmark, field report, mixed}. Test count moves from 71 → 73 (2 new κ tests). No changes to `tools/repo-agent/src/**`, `pyproject.toml`, `.github/workflows/**`, or `docs/**`.

## Phase 10 ÔÇö Safety Model (`safety-model.md`)

- [ ] 10.1 Write down the trust boundary already in use (LLM output untrusted; no agent writes to content files; no auto-opened content PRs).
- [ ] 10.2 Document the secret policy (`GITHUB_TOKEN` only in public workflows; no LLM provider secrets in CI).
- [ ] 10.3 Document the prompt-injection posture for content the agent ingests (issue bodies, PR diffs, remote URLs).
- [ ] 10.4 Enumerate approval controls: who may merge content PRs, who may flip an advisory check to required, how the `skip-review-assistant` label works.

> Exit criteria: `specs/safety-model.md` committed; one test asserting the agent raises on an attempt to write under `README.md` / `appendix/**`.

## Phase 11 ÔÇö Memory & State Model (`memory-model.md`)

- [ ] 11.1 Document the HTML-comment marker scheme used by workflows (landscape digest, new-tool tracking issue, PR review scorecard).
- [ ] 11.2 Document state ownership (issues, comments, `CHANGELOG.md`, freshness markers) with TTL / rotation rules.
- [ ] 11.3 Document conflict resolution when a marker is edited by a human or a second agent run.
- [ ] 11.4 Add a test asserting upsert-by-marker is idempotent.

> Exit criteria: `specs/memory-model.md` committed; idempotency test green.

## Phase 12 ÔÇö Observability (`observability.md`)

- [ ] 12.1 Define structured log schema for every repo-agent invocation (run id, tool, inputs hash, outcome, duration).
- [ ] 12.2 Emit logs from CLI and workflow entrypoints; store workflow logs as GitHub Actions artefacts.
- [ ] 12.3 Define the audit record: for every issue or comment the agent writes, a log line links run id ÔåÆ GitHub URL.
- [ ] 12.4 Add a test asserting that a workflow run produces a parseable log record with required fields.

> Exit criteria: `specs/observability.md` committed; log-schema test green; at least one workflow uploads a log artefact.

## Phase 13 ÔÇö Graduation: Advisory ÔåÆ Required

- [ ] 13.1 Measure: ÔëÑ30 consecutive days of green runs on `main` for each advisory check (`markdown-lint`, `link-check-pr`, `link-check-scheduled`, `stale-entry-detector`, `repo-agent-tests`, `phase-6-*`, `phase-7-*`).
- [ ] 13.2 Flip `continue-on-error` to `false` one check at a time, in PRs dedicated to each flip.
- [ ] 13.3 Add each flipped check to branch protection on `main`.
- [ ] 13.4 Update `mission.md` claim tier to **Earned** only if the mission-level gate (awesome.re + ÔëÑ3 external citations) also holds.

> Exit criteria: all 10 workflows required on `main`; Earned-tier gate status recorded in `mission.md`.

## Phase 14 ÔÇö Continuous Improvement

- [ ] 14.1 Quarterly rubric review.
- [ ] 14.2 Contributor feedback loop (survey + issue triage day).
- [ ] 14.3 Retire or archive low-signal sections.

---

## Working Rules

- Ship one phase's smallest useful slice before starting the next.
- Every automation must be reproducible locally by a contributor with no secrets.
- Every new section must pass the rubric before merge.
- Prefer reversible changes; isolate risky ones behind advisory CI until the Phase 13 gate holds.
- No Earned-tier claim language in any spec or public page until the Phase 13 gate holds.
