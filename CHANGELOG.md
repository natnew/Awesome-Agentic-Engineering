# Changelog

All notable changes to Awesome Agentic Engineering are documented here.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
and this list uses date-stamped phase headings rather than SemVer versions
because the repo is a curated knowledge base, not a shipped package.

The RSS feed at [`feed.xml`](docs/feed.xml) is generated from this file.

## [Unreleased]

- **Added** image-blaster to the Creative AI appendix (3D and Design) as a set of Claude skills that turns an image into a 3D environment, meshes and sound effects.
- **Added** Founder skill to Fast-Moving Product Lists (Multi-Agent Platforms) as a set of eleven Claude skills with board and consumer-panel sub-agents for testing a business idea.
- **Added** OpenChatCut to the Creative AI appendix (Video Generation) as a local-first video editor whose built-in and MCP agents share one set of editing tools.
- **Added** 15 Motion Design Styles to the Creative AI appendix (Video Generation) as a code-generated film showcase published with prompts, source and a review rubric.
- **Added** video-talkcraft to the Creative AI appendix (Video Generation) as a noncommercially licensed skill for voiceover-driven Remotion videos.
- **Added** anything2explainer to the Creative AI appendix (Video Generation) as a noncommercially licensed skill that builds narrated explainer videos with parallel build and QC agents.
- **Added** video-shotcraft to the Creative AI appendix (Video Generation) as a Claude Code and Codex skill that builds product films from Remotion motion recipes.
- **Removed** the Evidence Policy badge link from the bottom of the README Contributing section.
- **Removed** the audience and evidence-class tags, `Last reviewed` lines, and introductory text from the README sections, leaving each section as a title followed by its resource list.
- **Added** Humanizer to the Spec-Driven Development resources as an agent skill that removes patterns of AI-generated writing.
- **Removed** the Get Started, Architecture Decision Guide, Memory Systems, and Formal Evaluation Rubric sections from the README, and the two appendix links that pointed to them.
- **Added** agent-desktop to Browser and Desktop Agents (Developer Infrastructure) as an accessibility-tree CLI for desktop automation by agents.
- **Removed** the README Thesis, Reference Stack, Core Agentic Patterns, Benchmark and Evidence Policy, Skills and Operating Principles, What NOT to Do, and Signals sections, plus the prose, taxonomy, practice, and concept subsections in Spec-Driven Development, Memory Systems, Agent Authority, and Evaluation & Safety, leaving their resource lists. **Changed** the README order so Contributing is the last section.
- **Added** CLI-Anything to Browser and Desktop Agents (Developer Infrastructure) as a generator of agent-usable CLI harnesses for existing software.
- **Changed** the README resource tables (reference architectures, spec-driven development, memory systems, orchestration frameworks, protocols, authority resources, reasoning models, and evaluation and safety) to `- [Name](link): Description` lists. Per-entry strengths, constraints, suitability, paradigm, and governance columns were removed from the architecture and framework deep dives.
- **Added** MoneyPrinterTurbo to the Creative AI appendix (Video Generation) as a topic-to-short-video generator with an agent workflow.
- **Added** a Contributors section to the README that credits people who have added resources, with profile pictures and links to their contributions.
- **Added** OpenMontage to the Creative AI appendix (Video Generation) as an agentic video production system driven by coding assistants.
- **Added** CityRT to the Creative AI appendix (3D and Design) as a browser city-building game.
- **Added** VoiceStudio to the Voice Agents appendix (Open-Source Voice) as a voice cloning and dubbing studio with a local API and MCP server.
- **Added** Things Workshop to the Creative AI appendix (3D and Design) as a collection of interactive 3D explainers.
- **Added** freellmapi to Fast-Moving Product Lists (Self-Hosted Agents and UIs) as a self-hosted OpenAI-compatible router over free-tier LLM providers.

- **Added** Anime.js to the Creative AI appendix (3D and Design) as a JavaScript animation library.
- **Added** Orca to Fast-Moving Product Lists (Multi-Agent Platforms) as a runtime for running multiple CLI coding agents.
- **Added** Zookeeper to the Creative AI appendix (3D and Design) as a conversational text-to-CAD agent.
- **Added** The Agency to Fast-Moving Product Lists (Multi-Agent Platforms) as a collection of role-based agent definitions.
- **Added** Napkin AI to the Creative AI appendix (3D and Design) as a text-to-diagram and visuals tool with an API.
- **Added** codebase-memory-mcp to Fast-Moving Product Lists (RAG and Knowledge Bases) as a local MCP server for code knowledge graphs.
- **Added** You.com to Fast-Moving Product Lists (Deep Research) as a search and inference API for AI applications.
- **Added** Learn Harness Engineering to the Learning Resources courses and tutorials as a project-based course on coding-agent harnesses.
- **Added** Harness² to the Spec-Driven Development resources as a research framework for recursive agent harnessing, with first-party benchmark claims left untagged.
- **Added** Cloudflare security-audit skill to the Evaluation & Safety safety tooling as an agent skill for security audits.
- **Added** Craft Anything to Browser and Desktop Agents as an early-alpha Rust engine with CLI and MCP tools that drives a coding agent to rebuild studied software.
- **Added** Yogurt to Fast-Moving Product Lists (Self-Hosted Agents and UIs) as a local meeting-notes app with an optional read-only MCP server.
- **Added** Kimi 3D Make and Astryx to the Creative AI appendix (3D and Design), and Rea Video to Video Generation.
- **Added** roadmap.sh and HUMAN.md to the Learning Resources courses and tutorials.
- **Added** Impeccable to the Creative AI appendix (3D and Design) as a design-guidance skill and anti-pattern detector for coding agents.
- **Added** Playwright CLI to Browser and Desktop Agents as the CLI counterpart to Playwright MCP for coding agents.
- **Added** img2threejs to the Creative AI appendix (3D and Design) as an agent skill for image-to-procedural-Three.js reconstruction.
- **Added** Awesome DESIGN.md to the Spec-Driven Development resources as a design-level spec pattern for coding agents.
- **Added** Matt Pocock Skills to the Spec-Driven Development resources as a cross-CLI pack of `SKILL.md` engineering skills.
- **Added** agent-qa to Browser and Desktop Agents for Web, Android and iOS QA with inspectable evidence, persistent memory and evidence-gated learning, with explicit v0.2 limitations.
- **Added** PerspectiveGap to the Evaluation & Safety benchmarks for testing how models split context and write prompts for sub-agents, with omission and cross-role leakage as the scored failures.
- **Added** LazyMind to Orchestration Frameworks as an emerging skill-to-workflow runtime with explicit first-party evidence limits.
- **Added** NVIDIA OpenShell to the Agent Authority, Identity & Delegation resources for out-of-process policy enforcement in agent sandboxes.
- **Added** AgentWorld to the Evaluation & Safety benchmarks for long-horizon multi-agent collaboration with a causal contribution metric.
- **Added** "On Evaluating and Improving Conversational Agents in Production" and AECP to the Learning Resources key papers, covering statistically grounded offline evaluation and artifact-only multi-agent communication.
- **Added** Hyperconsciousness to Memory Systems as a developer-alpha encrypted knowledge store with scoped, expiring MCP grants.
- **Added** Hermeneutic to Memory Systems for correction-derived episodic memory, with bounded retrieval evidence and explicit effectiveness limits.
- **Added** YYLO Benchmark to the Evaluation & Safety benchmarks for longitudinal evaluation of agent runs with fresh-repository attempt isolation and hash-linked receipts as immutable evidence.
- **Added** Repo0 to the Spec-Driven Development resources as a paper on design-driven repository generation via a Dual-DAG of requirements and components.
- **Added** Proxifield to Reference Architectures and the Learning Resources key papers; fixed Markdown and link-check findings, replaced the unavailable Live Site button with publishing instructions, and removed the Portia entry after no working official source could be verified.
- **Added** DataPrep-Bench to the Evaluation & Safety benchmarks for evaluating LLMs and agents on automated training-data preparation workflows.
- **Added** ClawBench to the Evaluation & Safety benchmarks for live-site browser-agent evaluation with isolated runs and captured execution evidence.
- **Added** LLMs Get Lost in Evolving User Intent to the Evaluation & Safety benchmarks for testing agents under incrementally revealed, revised, and redirected user intent.
- **Added** Harness Handbook to the Spec-Driven Development resources as a paper on behaviour localization for evolving agent harnesses.

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
