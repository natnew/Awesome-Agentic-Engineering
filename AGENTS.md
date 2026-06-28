# AGENTS.md

Operating protocol for AI coding agents working in this repository.

Claude Code should read `CLAUDE.md` first, then use this file as the shared repository contract. Other agents should start here. Follow repository-local guidance over generic awesome-list assumptions.

## Repository North Star

This is a public, maintained awesome list for agentic AI engineering. The `README.md` is the product: a durable, high-signal, navigable map of how to build reliable, observable, production-grade agentic systems — for readers, contributors, and AI agents.

The list is curated, not accumulated. Each entry should help a reader understand an architecture, find a credible resource, or compare related tools. Selectivity, durability, clear placement, evidence discipline, and neutral description quality matter more than volume.

Editorial stance, applied to every inclusion decision and maintainer comment: **reliability over novelty · evaluation over intuition · architecture over tooling · systems thinking over prompt engineering.**

## Agent Role

Agents may help with:

* README and appendix maintenance when explicitly asked
* New entry review and rubric scoring
* Pull request review
* Issue triage and issue-to-entry conversion
* Broken-link checks
* Duplicate detection across `README.md` and `appendix/`
* Section placement
* Description tightening and promo-wording neutralisation
* Evidence-tag checks
* Maintainer comment drafts
* Small, safe cleanup edits when explicitly requested

Agents must not:

* Add speculative or low-signal entries
* Inflate claims or preserve promotional wording
* Reorganise the list or move entries between sections without explicit instruction
* Run broad formatting sweeps
* Edit unrelated files
* Rewrite the maintainer's style unnecessarily
* Turn one contribution into a broad structural change
* Change the rubric, merge threshold, or contribution templates as part of an unrelated task
* Touch protected or generated areas unless explicitly instructed

## Read Order

Before reviewing or editing, read in this order:

1. `README.md` — scope, taxonomy, section formatting, protected areas, and existing examples
2. `CONTRIBUTING.md` — submission requirements, evidence policy, and entry templates
3. `RUBRIC.md` — the seven scoring dimensions, the scale, and the worked example
4. `ANTI-PATTERNS.md` — what fails the rubric and why
5. `appendix/benchmark-and-evidence-policy.md` — source order, evidence tags, date-stamping
6. `.github/ISSUE_TEMPLATE/` and `.github/PULL_REQUEST_TEMPLATE.md` — contributor expectations
7. `CLAUDE.md`, if the agent is Claude Code or needs the Claude-specific review format
8. Recent issues and merged PRs, where available, for maintainer precedent

Do not assume the generic awesome-list pattern overrides this repository's existing structure.

## Repository Facts

* `README.md` holds the canonical list: Thesis, the Agentic Engineering Reference Stack, an Architecture Decision Guide, the core sections (patterns, reference architectures, memory, evaluation, protocols, authority/identity, safety), Signals, and Contributing.
* `appendix/` holds overflow and fast-moving lists (reference stack, browser/desktop agents, voice, creative, CRM, open-source models, newsletters, learning resources, fast-moving product lists).
* Sections use a mixture of bullets and tables, with several major-entry templates. Match the local section style exactly.
* Some sections carry an `Audience:` / `Evidence class:` line and explanatory text before entries. Preserve it.
* Major entries use the deep-dive template in `CONTRIBUTING.md` (What it is, What it demonstrates, Architectural strengths, Operational constraints, Ecosystem maturity, Governance fit, Workload suitability, Design paradigm, Evidence basis). Landscape-table entries condense to the surrounding table layout.
* Add new entries to their single best-fit section; do not mirror the same item across sections without a justified distinction.
* For package- or tool-style submissions, prefer the canonical GitHub repository or official docs over a package registry or marketing page.
* Every content change adds a one-line bullet under `## [Unreleased]` in `CHANGELOG.md`.
* Rapidly changing sections carry a `Last reviewed: Month YYYY` marker; refresh it in the same change.
* Descriptions are neutral, engineering-focused, concise, and non-promotional.

## Curation Bar

Every entry is scored against the seven dimensions in `RUBRIC.md`, each `0–3`:

| Dimension | Weight | Note |
| :--- | :--- | :--- |
| Reliability | ×3 | Hard gate — any `0` blocks merge |
| Evidence | ×3 | Hard gate — any `0` blocks merge |
| Agentic relevance | ×3 | Hard gate — any `0` blocks merge |
| Uniqueness | ×2 | |
| Maturity | ×2 | |
| Licensing / openness | ×1 | |
| Community signal | ×1 | Tiebreaker only |

* **Merge requires a weighted total of ≥ 27 / 45** *and* no `0` on the three hard gates.
* Community signal (stars, adoption) is a **tiebreaker only** — never sufficient on its own, and it never offsets a hard-gate failure. No GitHub-stars-as-evidence.

## Scope Rules

Belongs:

* Agent architectures, orchestration, and multi-agent systems
* Memory systems and context management
* Evaluation, tracing, observability, and testing for agents
* Protocols and standards (e.g. tool-use and interop specs)
* Tool use and structured outputs
* Agent authority, identity, delegation, permissions, and auditability
* Production operations: deployment, reliability, governance, cost control
* Reasoning and planning models with engineering substance
* Durable references: canonical repos, official docs, papers, datasets, benchmarks, and high-signal explainers

Does not belong (see `ANTI-PATTERNS.md`):

* Generic LLM wrappers with no agentic primitives
* Vendor marketing or launch posts without engineering content
* Unverified or launch-day benchmarks without methodology
* Duplicates that add no new structure or judgement
* Archived, abandoned, or single-author prototypes framed as production
* Stars-as-evidence
* Out-of-scope tooling: chat UIs, prompt-only utilities
* Rubric-restatement without applied judgement
* Time-sensitive or superlative framing ("new", "now", "best", "state-of-the-art", "production-ready") unless backed by cited evidence
* Pricing claims unless the surrounding section already tracks pricing

## Quality Bar

An entry qualifies when all are true:

* It is clearly relevant to agentic engineering and clears the three hard gates.
* The weighted rubric total is ≥ 27 / 45.
* Substantive claims carry an evidence tag and credible sources.
* The link is canonical, durable, and reachable.
* The resource adds something distinct from existing entries.
* It fits an existing section without forcing a taxonomy change.
* The description is neutral, concise, specific, and non-promotional.
* Formatting matches the surrounding section.
* No duplicate or stronger existing equivalent is already present in `README.md` or `appendix/`.

## Evidence Rules

* Every substantive claim carries a tag: `[official]`, `[benchmark]`, `[field report]`, or `[author assessment]`.
* Prefer official sources, papers, canonical repos, datasets, and durable docs or project pages over thin wrapper or marketing pages.
* Separate **benchmark performance** from **production maturity** — a benchmark proves workload fit, not reliability.
* Date-stamp volatile content with `Last reviewed: Month YYYY`.
* Missing evidence → request sources before scoring; do not infer a score from popularity.

## README Formatting Rules

Infer format from the surrounding section before editing.

* Preserve the existing heading structure, anchors, and back-to-top links.
* Preserve badges, banners, infographics, Table of Contents, `Audience:` / `Evidence class:` lines, and other protected areas.
* Match the section's existing format: bullet list, table, deep-dive template, or grouped subsection — including column order, emoji, and casing.
* Use HTTPS links and canonical names.
* Keep descriptions short, start with a capital letter, end with a full stop.
* Do not use title case for descriptions.
* Do not start descriptions with "A" or "An".
* Do not perform broad formatting changes unless explicitly asked.

## Link Quality Rules

Verify that:

* The link resolves and points to the canonical source.
* Repository links point to the main project, not an arbitrary fork.
* Paper links prefer the official publisher page, arXiv, DOI, or project page.
* Documentation links prefer official docs.
* Dataset and benchmark links prefer the official page or a maintained repository.
* URLs omit avoidable tracking parameters and shortened links.
* Login-gated resources are avoided unless the section already accepts that kind of resource.

Run the link checker locally when adding or changing links (see Local Checks).

## Description Style

Descriptions should be neutral, factual, specific, short, present tense where possible, and free of hype or unsupported claims. Describe *what it is* and *what it demonstrates* — architectural strengths, operational constraints, governance fit, workload suitability.

Prefer:

* "Framework for evaluating LLM agents across task environments."
* "Typed-state orchestration library with checkpointing for DAG-based agents."
* "Open-source tool for tracing agent execution and debugging tool calls."
* "Protocol for exposing tools and context to agents across providers."

Avoid: "powerful", "revolutionary", "cutting-edge", "best", "latest", "industry-leading", "production-ready" (unless cited), and unsupported claims about performance, adoption, or maturity.

## Section Placement Rules

1. Identify the closest existing section in `README.md` or `appendix/`.
2. Compare the candidate with neighbouring entries.
3. Prefer the narrowest accurate section.
4. If two sections fit, choose the one where readers would most naturally look first.
5. Use the `appendix/` files for fast-moving or domain-specific lists.
6. Avoid creating a new section for a single item.
7. Do not move existing entries unless explicitly asked.
8. If placement is uncertain, state the trade-off and recommend one option.

## Duplicate Checking Rules

Before adding or approving, check **both** `README.md` and `appendix/` for:

* Same URL or the same project under a different URL
* Same paper title
* Same organisation and product name
* Renamed repositories
* An existing entry in a nearby section
* An existing issue or PR suggesting the same resource
* A stronger canonical source already listed

If a duplicate exists, recommend closing, editing, or redirecting rather than adding another entry.

## Decision Matrix

| Decision | Use when |
| :--- | :--- |
| Accept as-is | Clears the three hard gates, total ≥ 27, canonical link, correct placement, matching format, neutral description, no duplicate. |
| Edit as maintainer | Strong resource needing a small, safe fix: typo, formatting or column alignment, canonical URL, placement, neutralising promo wording, adding a verifiable evidence tag, or refreshing a `Last reviewed:` date. |
| Request changes | Substantive gap in evidence, uniqueness, relevance, or placement the contributor must resolve. Name the specific dimension(s) and what would clear them. |
| Close | Clear anti-pattern, out of scope, duplicate with no added judgement, or no durable technical substance. Point to `CONTRIBUTING.md` or the relevant `ANTI-PATTERNS.md` item. |
| Park | Promising but blocked on a hard gate (e.g. too new for reliability signal) or not yet supported by the taxonomy. Note what evidence would unblock it. |

Minimise contributor friction: prefer a maintainer edit over a round-trip when the issue is minor.

## Issue-to-Entry Workflow

For suggestion and new-entry issues:

1. Check scope and the three hard gates.
2. Read the cited evidence first; request sources if missing.
3. Check source and link quality.
4. Check duplicates across `README.md` and `appendix/`.
5. Identify the best-fit section.
6. Draft a neutral entry only once evidence clears the hard gates and the total reaches ≥ 27.
7. Recommend accept, maintainer edit, request changes, close, or park.
8. Keep the maintainer comment concise and cite the dimension or policy line.

For broken-link / stale-entry issues:

1. Verify the reported link or `Last reviewed:` marker.
2. Search for a canonical replacement, preferring official sources over mirrors.
3. Preserve the entry if a durable replacement exists; refresh the marker.
4. Recommend removal only when no credible replacement exists.
5. State the action clearly.

## Pull Request Review Workflow

1. Read the PR title, description, and diff.
2. Confirm it changes only relevant files.
3. Read the cited evidence, then check each added or changed link.
4. Score the seven dimensions and check the three hard gates.
5. Check scope, source quality, and duplicates.
6. Check section placement and local formatting.
7. Neutralise description language where needed.
8. Confirm `Last reviewed:` and a `CHANGELOG.md` `[Unreleased]` bullet are updated where applicable.
9. Decide: accept, maintainer edit, request changes, close, or park.
10. Draft a concise, cited maintainer comment.

## Local Checks (Node 20; advisory in CI, never block merge)

Run these for link changes, content additions, structural edits, and larger Markdown changes. They are optional for tiny typo-only edits.

```sh
# Markdown style
npx -y markdownlint-cli2 "**/*.md" "#node_modules"

# Broken-link check (single file)
npx -y markdown-link-check -c .markdown-link-check.json README.md

# All tracked markdown
git ls-files "*.md" | xargs -I {} npx -y markdown-link-check -c .markdown-link-check.json {}

# Stale-entry / freshness audit (default threshold 9 months)
node .github/scripts/find-stale-entries.mjs
FRESHNESS_MONTHS=12 node .github/scripts/find-stale-entries.mjs
```


## Stop and Ask

Stop and ask the maintainer before:

* Creating a new top-level section
* Reordering large parts of `README.md`
* Changing the Table of Contents structure
* Editing infographics, banners, badges, or visual assets
* Changing the rubric, merge threshold, decision process, or contribution rules
* Removing multiple entries
* Making judgement-heavy scope changes
* Editing files unrelated to the stated task

## Protected Areas

Do not create, edit, or commit these unless explicitly instructed:

* Badges, banner images, infographics, and other assets
* Table of Contents and any generated indexes
* Generated site output under `docs/` and `assets/github/`
* `CHANGELOG.md` history beyond the single `[Unreleased]` bullet for your change
* Licence text and repository metadata unrelated to the task
* Local-only and SDD working areas: `specs/`, `tasks/`, `skills/`, `tools/`, `private/`, `scratch/`, `.local/`
* Credentials, secrets, tokens, keys, personal notes, and draft files

If unsure whether a file belongs in the public repository, leave it untouched and explain the concern.

## Maintainer Comment Style

Warm, concise, respectful, and decision-oriented. Thank the contributor, give a clear reason tied to a specific rubric dimension or policy line, and link the canonical doc. Prefer fixing small things yourself over a round-trip. Gate on the rubric, not tone.

Prefer:

* "Thank you — relevant, canonical link, clears the hard gates. I'd place it under Orchestration Frameworks with a shorter neutral description."
* "Thank you. Useful resource; I'll accept with a small maintainer edit to remove the ranking claim and add the `[official]` tag."
* "Thank you for raising this — closing as a duplicate, since the resource already appears under Memory Systems."
* "Thank you — parking this until there's reliability evidence; a production field report would unblock it."

Avoid long explanations, harsh or defensive wording, and asking contributors for trivial edits the maintainer can safely make.

## Final Response Pattern

When finishing a task, summarise:

* What was reviewed
* The decision or recommended decision, with the deciding rubric dimension
* What changed, if anything
* Any risks or uncertainties
* A suggested maintainer comment, if relevant
* Follow-up needed, if any

Do not modify `README.md`, `appendix/`, or other content files unless the task explicitly asks.
