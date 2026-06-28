# CLAUDE.md

This file guides Claude Code when working in this repository.

This repository is a public, maintained awesome list for agentic AI engineering, not an application codebase. There is no application build or test suite to run for normal review tasks; advisory Markdown and link checks exist and are documented in `CONTRIBUTING.md` and `AGENTS.md`. The `README.md` is the product.

Claude Code should read this file first, then use `AGENTS.md` as the shared repository operating protocol.

## North Star

* Preserve `README.md` as the canonical public artefact.
* Keep the list selective, durable, technically useful, neutral, and easy to scan.
* Apply the editorial stance to every decision: **reliability over novelty · evaluation over intuition · architecture over tooling · systems thinking over prompt engineering.**
* Help the maintainer make fast, consistent, low-friction decisions.
* Prefer small, precise edits over broad rewrites.
* Do not broaden the list beyond agentic engineering and the adjacent technical areas already represented in the README.

## Claude's Role

Claude may assist with:

* PR review and rubric scoring
* Issue triage
* README and appendix entry review
* Broken-link investigation
* Duplicate detection
* Section placement
* Neutral description rewrites
* Maintainer comment drafts
* Small safe maintainer edits when explicitly asked
* Improvements to agent instruction files when asked

Claude must not:

* Add entries without checking scope, the hard gates, evidence, link quality, duplicates, and placement
* Invent facts about a resource
* Preserve promotional claims
* Add ranking, pricing, novelty, adoption, or performance claims without strong evidence
* Rewrite the taxonomy without explicit instruction
* Edit unrelated files
* Touch protected areas unless instructed
* Ask contributors to make trivial fixes the maintainer can safely make

## Repository Facts

* `AGENTS.md` contains the full tool-agnostic operating protocol.
* `CONTRIBUTING.md` contains contributor-facing rules, the evidence policy, and the PR process.
* `RUBRIC.md` contains the seven-dimension scoring rubric; `ANTI-PATTERNS.md` lists what fails it; `appendix/benchmark-and-evidence-policy.md` sets source order and evidence tags.
* `.github/ISSUE_TEMPLATE/` and `.github/PULL_REQUEST_TEMPLATE.md` contain public contributor guidance.
* `README.md` contains introductory content, a Table of Contents, infographics, and the main curated sections; `appendix/` holds overflow and fast-moving lists.
* `CHANGELOG.md` records every content change as a bullet under `## [Unreleased]`.
* The main list uses both bullet entries and tables, plus a deep-dive template for major entries. Match the surrounding section exactly.
* Each entry goes in its single best-fit section; do not mirror an item across sections without a justified distinction.
* New categories should normally be handled separately.
* `docs/` and `assets/github/` are generated site output — do not hand-edit.

## Curation Bar

Every entry is scored against the seven dimensions in `RUBRIC.md`, each `0–3`: Reliability ×3, Evidence ×3, Agentic relevance ×3, Uniqueness ×2, Maturity ×2, Licensing ×1, Community signal ×1.

* Merge requires a weighted total of **≥ 27 / 45**.
* **Hard gates** — any `0` on Reliability, Evidence, or Agentic relevance blocks merge.
* Community signal (stars, adoption) is a **tiebreaker only** — never sufficient, and it never offsets a hard-gate failure.

## Always-Loaded Context

Keep this file short. It is an orientation layer, not a manual.

Use this routing:

* Need general agent rules → read `AGENTS.md`
* Need contribution rules or the PR process → read `CONTRIBUTING.md`
* Need the scoring rubric → read `RUBRIC.md`
* Need what fails the rubric → read `ANTI-PATTERNS.md`
* Need the evidence and source policy → read `appendix/benchmark-and-evidence-policy.md`
* Need style examples → inspect the target section in `README.md`
* Need contributor expectations → inspect `.github/ISSUE_TEMPLATE/` and `.github/PULL_REQUEST_TEMPLATE.md`
* Need maintainer precedent → inspect recent issues and merged PRs where available

Do not duplicate long sections from those files here.

## First-Pass Workflow

For any PR, issue, or README task:

1. Read the user request.
2. Read the relevant issue, PR, diff, or target README section.
3. Read the cited evidence first; if it is missing, request sources before scoring.
4. Check the repository scope and the three hard gates.
5. Check `CONTRIBUTING.md` and `RUBRIC.md` if the task concerns a submission.
6. Check neighbouring entries for style and placement.
7. Search for duplicates across `README.md` and `appendix/`.
8. Verify the link where tools allow.
9. Inspect the resource enough to understand what it is.
10. Choose the smallest useful action.
11. Produce a concise decision, edit, or maintainer comment.

## Entry Checklist

Before recommending acceptance or adding an entry, confirm:

* In scope and clears the three hard gates
* Technically useful
* Credible source
* Canonical URL
* Durable link
* Substantive claims carry an evidence tag
* No duplicate (README and appendix)
* Correct, single best-fit section
* Local format matched
* Neutral description
* No hype
* No unsupported claims
* No avoidable tracking parameters
* `Last reviewed:` and `CHANGELOG.md [Unreleased]` updated where applicable
* No unnecessary new section

## Source Preference

Prefer:

* Official repositories
* Official documentation
* Papers
* Technical reports
* Benchmarks
* Datasets
* Durable project pages
* Maintained tools and libraries
* High-quality reference material

Treat cautiously:

* Launch posts
* Vendor pages
* Thin wrappers
* Newsletter posts
* Social posts
* Unmaintained repositories
* Link farms
* Pages dominated by sales language
* Time-sensitive comparisons

## Description Rules

Match the surrounding section: many sections use tables or the deep-dive template in `CONTRIBUTING.md`. The simple pattern below applies to plain bullet lists.

`* [Name](URL) - Clear factual description.`

For tables, preserve the existing column structure.

Descriptions should:

* Start with a capital letter
* End with a full stop
* Be short and specific
* Avoid title case
* Avoid starting with "A" or "An"
* Avoid marketing taglines
* Explain what the resource is, not why it is exciting

Remove or neutralise:

* "best"
* "latest"
* "most advanced"
* "powerful"
* "revolutionary"
* "cutting-edge"
* "game-changing"
* "industry-leading"
* "fastest"
* Time-sensitive "new/now" framing
* Unsupported performance, adoption, maturity, or pricing claims

## Section Placement

| Situation | Action |
| --- | --- |
| Exact fit in an existing section | Place there. |
| Fits two sections | Choose the more specific or more discoverable one. |
| Similar to neighbouring entries | Place near those entries if local ordering allows. |
| Fast-moving or domain-specific theme | Use the relevant `appendix/` file. |
| New theme with one entry | Park, or place in the nearest broader section. |
| New theme with several strong entries | Suggest a new section; do not create it unless asked. |
| Unclear placement | Explain the options briefly and recommend one. |

## PR Triage

| Decision | Use when |
| --- | --- |
| Accept as-is | Clears the hard gates, total ≥ 27, scope, link, placement, format, and description are all sound. |
| Maintainer edit | Strong resource needing only minor wording, evidence-tag, link, placement, or formatting fixes. |
| Request changes | Relevance, evidence, uniqueness, link quality, or placement is materially unclear. |
| Close | Out of scope, duplicate, promotional, broken with no replacement, or low technical value. |
| Park | Promising but blocked on a hard gate, needs a taxonomy decision, or needs maintainer judgement. |

## Issue Triage

Suggestion issues:

* Strong, in scope, clears the hard gates → draft entry and recommend acceptance.
* Strong but wording or placement needs work → recommend maintainer edit.
* Missing evidence → ask for minimal clarification.
* Duplicate → close with a pointer to the existing entry.
* Out of scope → close politely.
* Premature or taxonomy-dependent → park.

Broken-link issues:

* Verify the link.
* Find a canonical replacement first.
* Prefer official sources over mirrors.
* Remove only when no durable replacement exists.
* Leave a concise note explaining the action.

## Small Safe Fix Rule

Protect contributor goodwill.

When a resource is suitable and the issue is minor, make or recommend a maintainer edit rather than asking the contributor to revise.

Small safe fixes include:

* Tightening a description
* Removing hype
* Fixing punctuation
* Correcting placement
* Replacing a non-canonical URL
* Matching bullet or table format
* Removing tracking parameters
* Adding a verifiable evidence tag
* Refreshing a `Last reviewed:` date

## Stop and Ask

Stop before:

* Creating a new top-level section
* Reordering large parts of the README
* Editing the Table of Contents
* Editing visual assets
* Changing contribution rules, the rubric, or the merge threshold
* Removing several entries
* Making broad scope decisions
* Editing unrelated files

## Protected Areas

Do not edit unless explicitly instructed:

* Badges
* Table of Contents
* Banner images
* Gallery images
* Infographics
* Announcement or roadmap blocks
* Contributor sections
* Generated site output under `docs/` and `assets/github/`
* Licence text
* Repository metadata unrelated to the task
* Private, draft, scratch, or local-only files

## Maintainer Comment Templates

Accept:

"Thank you — this looks relevant, the link is canonical, and the placement works. I would accept this."

Maintainer edit:

"Thank you — this is a useful resource. I would accept it with a small maintainer edit to tighten the description and keep the wording neutral."

Request changes:

"Thank you for the suggestion. I think this could fit, but I would ask for evidence of production reliability and a clearer uniqueness angle before scoring it."

Duplicate:

"Thank you — I would close this as a duplicate because the resource already appears under [section]."

Out of scope:

"Thank you for sharing this. I would close it because it sits outside the current scope of the list."

Park:

"Thank you — this may be worth revisiting, but I would park it until there is reliability evidence to clear the hard gate."

## Output Format

For PR or issue review, respond with:

* **Decision**: accept, maintainer edit, request changes, close, or park
* **Reason**: 1–3 bullets, tied to a specific rubric dimension or policy line
* **Suggested README entry**, if useful
* **Suggested maintainer comment**
* **Files changed**, if any
* **Remaining uncertainty**, if any

## Editing Rule

Do not modify `README.md`, `appendix/`, `CONTRIBUTING.md`, `.github` templates, generated `docs/` output, or other files unless explicitly asked.
