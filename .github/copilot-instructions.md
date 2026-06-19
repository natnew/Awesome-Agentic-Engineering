# Copilot instructions

## What this repository is

**Awesome Agentic Engineering** is a curated list about building reliable, observable, production-grade agentic AI systems. It is a maintained public resource, **not an application codebase**. Almost all work is Markdown curation: reviewing pull requests, assessing proposed entries, checking sources, preserving the structure and tone of `README.md`, and keeping links and formatting consistent.

The editorial stance is: **reliability over novelty, evaluation over intuition, architecture over tooling**. Apply this lens to every inclusion decision and every review comment.

## How to treat this repository

- Treat changes as curation, not engineering. There is no application to build or run.
- The canonical content lives in `README.md`, with overflow and fast-moving lists under `appendix/`.
- The curation contract is defined in `CONTRIBUTING.md`, `RUBRIC.md`, and `ANTI-PATTERNS.md`. Read these before judging any entry.
- Match the formatting of surrounding content exactly — column order, bullet templates, emoji, and casing.

## Contribution standard

Every entry is scored against the seven-dimension rubric in `RUBRIC.md` (each 0–3): Reliability ×3, Evidence ×3, Agentic relevance ×3, Uniqueness ×2, Maturity ×2, Licensing ×1, Community signal ×1.

- Merge requires a weighted total of **≥ 27 / 45**.
- **Hard gates:** any `0` on Reliability, Evidence, or Agentic relevance blocks merge.
- Community signal (stars, adoption) is a **tiebreaker only** — never sufficient on its own.

**Belongs:** agent architectures, orchestration, memory, evaluation, protocols and standards, tool use, multi-agent systems, and agent authority, identity, permissions, auditability, and production operations — with engineering substance and real-world signal.

**Does not belong:** generic LLM wrappers with no agentic primitives, vendor marketing or launch posts, unverified or launch-day benchmarks, duplicates that add no new structure or judgement, archived or single-author prototypes framed as production, stars-as-evidence, and out-of-scope tooling (chat UIs, prompt-only utilities). See `ANTI-PATTERNS.md`.

## Reviewing suggested additions

1. Read the cited evidence first. If sources are missing, request them before scoring.
2. Score the seven dimensions and check the three hard gates.
3. Confirm the entry sits in its single best-fit section, and check for duplicates across **both** `README.md` and `appendix/`.
4. Verify every link resolves and points to a canonical destination.
5. Check that formatting matches the surrounding block, and that `Last reviewed:` markers and a `CHANGELOG.md` `[Unreleased]` bullet are updated where applicable.

## Handling weak entries

- **Promotional copy** — neutralise marketing language, superlatives, rankings, pricing, and "new/now" framing, or request a neutral rewrite.
- **Poorly sourced claims** — every substantive claim needs an evidence tag (`[official]`, `[benchmark]`, `[field report]`, or `[author assessment]`). Prefer official docs, papers, canonical repos, and durable project pages over thin wrapper or landing pages.
- **Duplicates** — point to the existing entry; accept only if the new entry adds a distinct, justified angle.
- **Stale entries** — flag an outdated `Last reviewed:` marker rather than silently rewriting the content.

## When uncertain

- Prefer a small, safe, reversible edit (typo, alignment, link normalisation, neutralising promo wording) over a large change.
- If an entry needs a judgement call on evidence, uniqueness, or scope, leave a clear, specific review note and defer to a human maintainer rather than merging.
- Name the specific rubric dimension or policy line behind any concern, and keep the tone warm and concise.

## What not to change without maintainer direction

- Do not restructure `README.md` or move entries between sections without an explicit request.
- Do not edit generated site output under `docs/` or `assets/github/` by hand.
- Do not change the rubric, the merge threshold, the decision process, or the contribution templates as part of an unrelated change.
- Do not add new entries on your own initiative; suggest them for a maintainer to decide.
