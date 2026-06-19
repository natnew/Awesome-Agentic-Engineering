---
applyTo: "README.md"
---

# README curation

`README.md` is the canonical list. Edit it only when the task is curation, an entry update, or resolving a pull request or issue. Otherwise, leave it unchanged.

## Structure and ordering

- Preserve the existing section structure and headings. Place each entry in its single best-fit section; do not mirror the same item across sections without a justified distinction.
- Keep the existing ordering of each section. Where a section is alphabetical or capped at a fixed number of entries, maintain that convention.
- Match the surrounding formatting exactly — table columns, bullet templates, emoji, and casing. When in doubt, copy the shape of an adjacent entry.
- Refresh the `Last reviewed: Month YYYY` marker in any rapidly changing section you edit.

## Descriptions

- Write neutral, engineering-focused descriptions. Say what a resource *is* and what it *demonstrates* — architectural strengths, operational constraints, and workload fit.
- Remove marketing language, superlatives ("best", "state-of-the-art", "production-ready"), rankings, pricing, and time-sensitive "new/now" framing unless backed by cited evidence.
- Keep each substantive claim anchored to an evidence tag: `[official]`, `[benchmark]`, `[field report]`, or `[author assessment]`.

## Links and duplicates

- Prefer canonical links: the project repository, official docs, the paper, or a durable project page — not redirects, aggregators, or landing pages.
- Before adding an entry, check for duplicates across **both** `README.md` and `appendix/`.
- Confirm relevance against the scope in `CONTRIBUTING.md` and the rubric in `RUBRIC.md` before adding anything.

## After a content change

For substantive content changes, add a one-line bullet under `## [Unreleased]` in `CHANGELOG.md`. Do not add changelog entries for typo-only, formatting-only, or link-normalisation fixes unless requested.
