# CLAUDE.md

Claude-specific operating layer for this repository. `AGENTS.md` is the full shared protocol; this file adds orientation, verification commands, and the Claude review format. Where the two differ, the more specific rule wins.

## What this repository is

A curated public awesome list for agentic AI engineering. **`README.md` is the product**; `appendix/` holds overflow and fast-moving lists. There is no application, package, or test suite — the work is Markdown curation: entry review, PR/issue triage, link repair, and small maintainer edits.

Editorial stance for every decision: **reliability over novelty · evaluation over intuition · architecture over tooling · systems thinking over prompt engineering.**

## Where the rules live

Read the authoritative file for the task instead of relying on memory or on this summary.

| Need | Source |
| --- | --- |
| Scope, workflows, placement, duplicates, link and style rules, decision matrix, comment style | `AGENTS.md` |
| Scoring: seven dimensions, weights, scale, worked example | `RUBRIC.md` |
| Rejection patterns | `ANTI-PATTERNS.md` |
| Evidence tags, source order, date-stamping | `appendix/benchmark-and-evidence-policy.md` |
| Contributor rules, deep-dive template, PR process | `CONTRIBUTING.md` |
| What contributors are asked to supply | `.github/PULL_REQUEST_TEMPLATE.md`, `.github/ISSUE_TEMPLATE/` |
| Entry format | The target section of `README.md` — copy an adjacent entry |

`.github/copilot-instructions.md` and `.github/instructions/*.md` restate the same policy for Copilot. If you change policy in `AGENTS.md` or here (only when asked), flag those files for the same update.

## Invariants

* **Merge bar:** weighted total **≥ 27 / 45** and **no `0`** on Reliability, Evidence, or Agentic relevance. Community signal is a tiebreaker only and never offsets a hard gate.
* **Evidence before scoring.** Read cited sources first; if missing, request them. Never infer a score from popularity, and never invent facts about a resource.
* **Duplicates:** search both `README.md` and `appendix/` (URL, project name, paper title, renamed repos) before adding or approving.
* **One best-fit section per entry.** Do not move existing entries or create sections unless asked.
* **Match local format exactly.** Most sections are tables; new rows are appended to the end of the table, not sorted. Evidence cells use the form `` `[official]` · `[benchmark]` ``. Major entries use the deep-dive template in `CONTRIBUTING.md`.
* **Neutral descriptions:** say what it is and demonstrates; no superlatives, rankings, pricing, "new/now" framing, or unsupported performance/adoption/maturity claims. Descriptions start with a capital, not "A"/"An", and end with a full stop.
* **Canonical, durable HTTPS links** — official repo, docs, paper, or project page; no trackers, shorteners, or forks.
* **Bookkeeping in the same change:** refresh `Last reviewed: Month YYYY` in any dated section you edit, and add one bullet under `## [Unreleased]` in `CHANGELOG.md` for substantive content changes, e.g. `- **Added** X to the Evaluation & Safety benchmarks for ...` (`Added` / `Changed` / `Removed` / `Fixed`). Typo-, formatting-, or link-normalisation-only fixes need no bullet unless asked.

## Boundaries

* **Default is read-only.** Edit `README.md`, `appendix/`, policy files, or `.github/` only when the task explicitly asks; review tasks produce a decision and a comment, not edits.
* **Never hand-edit** `docs/` or `assets/github/` (generated site output), badges, banners, infographics, the Table of Contents, or `LICENSE`.
* **Do not create** `specs/`, `tasks/`, `skills/`, `tools/`, `private/`, `scratch/`, or `.local/`; they are local-only working areas. `tools/repo-agent` is absent from this repo, so the `phase-6-*`, `phase-7-*`, and `repo-agent-tests` workflows skip by design — do not try to run `repo-agent` or regenerate `docs/`.
* **Stop and ask** before: a new top-level section, reordering large parts of the README, removing several entries, broad scope calls, or changing the rubric, threshold, templates, or contribution rules.
* **Prefer a maintainer edit** to asking a contributor for a trivial fix (wording, punctuation, placement, canonical URL, evidence tag, date marker).

## Verification

Node 20+ and Python 3 are enough. Run on the files you changed before committing:

```sh
# Blocking in CI (hygiene.yml): mojibake / encoding scan over tracked Markdown
sed -n "/python - <<'EOF'/,/^ *EOF\$/{//!p}" .github/workflows/hygiene.yml \
  | python3 -c "import sys,textwrap;exec(textwrap.dedent(sys.stdin.read()))"

# Advisory in CI: Markdown style
npx -y markdownlint-cli2 README.md CHANGELOG.md

# Advisory in CI: links in changed files
npx -y markdown-link-check -c .markdown-link-check.json README.md

# Freshness markers
node .github/scripts/find-stale-entries.mjs
```

* The encoding scan is the only CI check that fails a PR. Write plain UTF-8; watch for corrupted smart quotes and dashes when pasting.
* `README.md` and `RUBRIC.md` already carry markdownlint findings (e.g. MD060). Fix only findings on lines you touched; do not sweep.
* Link checks go through a proxy here and some sites rate-limit or time out; confirm a failure by fetching the URL directly before calling it broken. Add a `.markdown-link-check.json` ignore only for a verified canonical URL, with a dated `comment`.
* Re-read your diff: only the intended files changed, format matches neighbours, no hype, bookkeeping done.

## Working efficiently

* Most tasks are one entry or one PR — work inline; don't spawn agents for them.
* When a task spans several candidates or broken links, verifying links and searching for duplicates are independent — run them in parallel (parallel tool calls, or one subagent per candidate).
* For judgement calls on placement or wording, check recent merged PRs and `CHANGELOG.md [Unreleased]` for maintainer precedent.

## Review output format

For a PR or issue review, respond with:

* **Decision** — accept, maintainer edit, request changes, close, or park (definitions in `AGENTS.md` → Decision Matrix)
* **Score** — the seven-dimension table from `RUBRIC.md` when an entry is being assessed, one line of justification per dimension
* **Reason** — 1–3 bullets, each tied to a rubric dimension or policy line
* **Suggested entry** — in the target section's exact format, if useful
* **Maintainer comment** — warm, concise, decision-oriented (examples in `AGENTS.md` → Maintainer Comment Style)
* **Files changed** and **remaining uncertainty**, if any
