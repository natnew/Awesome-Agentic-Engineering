# Tech Stack

The repo is primarily a **curated knowledge base**. A small internal **agentic system** (`tools/repo-agent/`) helps maintain it. The stack is chosen to support both roles with minimal dependencies and no build toolchain for readers.

## Content Layer

- **Markdown** — all curated content, appendices, and specs.
- **GitHub-flavored Markdown tables** — for rubrics, decision guides, and comparisons.
- **Relative links** — appendices under `appendix/`, specs under `specs/`.

## Repository & Collaboration

- **Git + GitHub** — source of truth, PR-driven curation.
- **GitHub Issues & Discussions** — triage, proposals, and community input.
- **CODEOWNERS / CONTRIBUTING.md** — contribution standards and review flow.
- **Shields.io badges** — freshness, PR status, license signals (live, no workflow).

## Automation & CI (advisory today)

- **GitHub Actions** — 10 workflows total. All content-quality checks run `continue-on-error: true` until the Phase 13 graduation gate holds.
- **markdownlint-cli2** — consistent Markdown style.
- **markdown-link-check** — broken link detection (PR + weekly schedule with a single rolling issue).
- **Stale-entry detector** — monthly Node 20 script, 9-month threshold, single rolling "Freshness audit" issue.

## Internal Agentic Layer (`tools/repo-agent/`)

Internal automation only — not a public product. See `architecture.md` for layering.

- **Python** — `>=3.12` (pinned in `pyproject.toml`).
- **MCP SDK** — `mcp>=1.2.0` via FastMCP, stdio transport.
- **HTTP** — `httpx>=0.27` (sync client; `MockTransport` in tests).
- **Modeling** — `pydantic>=2.6`.
- **Rendering** — `markdown-it-py>=3.0`, `mdit-py-plugins>=0.4` (render-time only, in CI).
- **Test** — `pytest>=8.0`; `live` marker opt-in, skipped by default. 73 tests green at Phase 9 close.
- **Lint/format** — `ruff>=0.4`.
- **LLM abstraction** — `LLMClient` protocol; `StubLLMClient` is the default and is the only client exercised in CI.
- **Evaluation harness (Phase 9)** — golden set of 21 labelled entries under `tools/repo-agent/tests/fixtures/golden/` (paired `*.md` + `*.json`); per-dimension Cohen's κ regression in `tests/test_golden_set_kappa.py` with floor κ ≥ 0.6 (stub-enforced; live-advisory). No new dependencies introduced — κ is computed inline.

## LLM Provider Posture

- **Default:** `StubLLMClient`. Deterministic, offline, no secrets. CI uses only the stub.
- **Opt-in live providers:** contributors may wire a provider locally to exercise draft-generation paths. No live provider is ever required to contribute, run tests, or run CI.
- **No provider lock-in:** model-agnostic; prefer open weights where viable.
- **Data handling:** repo content that a live provider sees is already public. No private data leaves the repo via the agent (see `safety-model.md`).

## Trust Boundary for Agent Output

All text produced by the repo-agent (drafts, scorecards, triage labels, digests) is **untrusted output**. Policy:

1. The agent **never writes to content files** (`README.md`, `appendix/**`, `CHANGELOG.md`, `tools/**` source).
2. The agent may only **upsert issue or comment bodies** behind stable HTML-comment markers (see `memory-model.md`).
3. Any change to content files must be opened and merged by a human through a normal PR.
4. `skip-review-assistant` label on a PR suppresses the agent's scorecard comment.

## Explicit Exclusions (what this stack does **not** include)

To keep the contributor burden and blast radius low:

- **No database, no vector store, no cache service.** All state is in Markdown files or GitHub issues/comments.
- **No hosted or paid services required to contribute, run tests, or run CI.**
- **No build step for readers.** Consuming the repo requires only a Markdown renderer.
- **No JavaScript runtime in the published site.** `docs/` is static HTML + one CSS file.
- **No secrets in public workflows.** Workflows requiring tokens use `GITHUB_TOKEN` only.
- **No auto-opened content PRs.** Humans open and merge content PRs.
- **No Earned-tier claims in documentation** until the gate in `mission.md` is met.

## Publishing & Discoverability

- **GitHub Pages** — published from `/docs` on `main`. No `gh-pages` branch.
- **RSS 2.0** — `docs/feed.xml` generated from `CHANGELOG.md`.
- **Sitemap** — `docs/sitemap.xml`.
- **awesome.re** — submission tracked in `specs/2026-04-22-phase-7-publishing-and-reach/submission-checklist.md`.

## Guardrails

- Every dependency added must justify its maintenance cost and be listed above with a version floor.
- Every automation must be reproducible locally by a contributor with no secrets.
- Every risky change lands behind an advisory check first; graduation to required follows `roadmap.md` Phase 13.
