# Changelog

All notable changes to Awesome Agentic Engineering are documented here.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
and this list uses date-stamped phase headings rather than SemVer versions
because the repo is a curated knowledge base, not a shipped package.

The RSS feed at [`feed.xml`](feed.xml) is generated from this file.

## [Unreleased]

- Placeholder — add a bullet here in the same PR that adds or refreshes an entry.

## [Phase 7 — Publishing & Reach] - 2026-04-22

- **Added** a zero-build static site under `docs/` published via GitHub Pages.
  Pages are generated from `README.md`, `appendix/*.md`, `RUBRIC.md`,
  `ANTI-PATTERNS.md`, `CONTRIBUTING.md`, and this `CHANGELOG.md` by the new
  `repo-agent workflow render-site` command.
- **Added** this `CHANGELOG.md` and an RSS 2.0 `feed.xml` generated from it.
- **Added** `specs/2026-04-22-phase-7-publishing-and-reach/submission-checklist.md`
  tracking the `awesome.re` submission and adjacent-community announcements.
- **Added** two advisory GitHub Actions workflows: `phase-7-publish-site.yml`
  (regenerates `docs/` on `main`) and `phase-7-render-check.yml` (fails PRs
  whose `docs/` output drifts from Markdown sources).
- **Changed** `tools/repo-agent/pyproject.toml` to depend on `markdown-it-py`
  and `mdit-py-plugins` (both pure-Python, no native build step).

## [Phase 6 — Agentic Workflows (v1)] - 2026-04-22

- **Added** three end-to-end workflows composed on top of the Phase 5 skills:
  `workflow new-tool` (URL → rubric-aligned draft + tracking issue),
  `workflow landscape-scan` (weekly rolling digest issue), and
  `workflow review-pr` (single maintained rubric scorecard comment per content PR).
- **Added** three path-scoped GitHub Actions workflows under
  `.github/workflows/phase-6-*.yml`, all advisory (`continue-on-error: true`).
- **Added** the `skip-review-assistant` opt-out label for PR authors.
- Shipped in [PR #6](https://github.com/natnew/Awesome-Agentic-Engineering/pull/6).

## [Phase 5 — The Repo as an Agentic System (v0)] - 2026-04-22

- **Added** an MCP server (`tools/repo-agent/`) exposing 8 tools:
  `list_sections`, `get_rubric`, `get_anti_patterns`, `search_entries`,
  `validate_entry`, `propose_entry`, `triage_pr`, `freshness_audit`.
- **Added** three skills: triage, freshness audit, entry draft.
- **Added** a full CLI mirror (`repo-agent <subcommand>`) and an `LLMClient`
  protocol with a `StubLLMClient` default so the system runs with zero API keys.
- Shipped in [PR #5](https://github.com/natnew/Awesome-Agentic-Engineering/pull/5).

## [Phase 4 — Automations & CI Hygiene] - 2026-04-22

- **Added** four GitHub Actions: markdown-lint on PR, broken-link check on PR,
  weekly scheduled link check (rolling single issue), and a monthly
  stale-entry detector (9-month threshold).
- **Added** a live `github/last-commit` Shields.io badge to the README.
- All workflows ship advisory (`continue-on-error: true`) with a documented
  graduation path to required checks.
- Shipped in [PR #4](https://github.com/natnew/Awesome-Agentic-Engineering/pull/4).

## [Phase 3 — Cutting-Edge Resource Expansion] - 2026-04-22

- **Added / refreshed** orchestration frameworks (LangGraph, Agent Framework,
  AutoGen, CrewAI, OpenAI Agents SDK), protocols (MCP, A2A), memory systems,
  evaluation & safety tooling, and open-source agent models.
- **Added** a new *Reasoning & Planning Models* section.
- **Expanded** the *Computer-Use & Browser Agents* appendix.
- Shipped in [PR #3](https://github.com/natnew/Awesome-Agentic-Engineering/pull/3).

## [Phase 2 — Curation Bar & Rubric] - 2026-04-22

- **Added** `RUBRIC.md` with the seven-dimension formal scoring model.
- **Added** `ANTI-PATTERNS.md` cataloguing what NOT to include.
- **Applied** the rubric retroactively to one section as a pilot.
- Shipped in [PR #2](https://github.com/natnew/Awesome-Agentic-Engineering/pull/2).

## [Phase 1 — Foundation & Hygiene] - 2026-04-22

- **Added** `CONTRIBUTING.md` with the contribution standards, evidence policy,
  and v1 Entry Rubric self-assessment.
- **Added** PR and issue templates (new entry, stale entry, suggestion).
- **Audited** existing sections against the mission and flagged gaps.
- Shipped in [PR #1](https://github.com/natnew/Awesome-Agentic-Engineering/pull/1).
