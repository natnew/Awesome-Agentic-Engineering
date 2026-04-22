# Anti-patterns: What NOT to Include

Concrete patterns that will be rejected on PR review, each mapped to the rubric dimension(s) it fails. See [`RUBRIC.md`](RUBRIC.md) for scoring.

> These are **archetypes**, not accusations of specific projects. Examples are illustrative.

## 1. Generic LLM wrappers without agentic primitives

**Pattern.** A thin SDK that calls a chat completion endpoint, with no first-class support for tool use, memory, multi-step control flow, or state.

**Example (archetypal).** *"A Python package that exposes `client.chat(prompt)` and nothing else — no tool interface, no state, no orchestration."*

**Rubric dimensions it fails.** Agentic relevance (hard gate, likely 0–1), Uniqueness (low — dozens exist).

---

## 2. Vendor marketing posing as engineering content

**Pattern.** Landing pages, launch announcements, or sponsored blog posts presented as reference material. Typically long on adjectives ("world-class", "state-of-the-art") and short on methodology, code, or failure modes.

**Example (archetypal).** *"A vendor's 'Why our agent platform is the future of AI' blog post submitted as an entry in Orchestration Frameworks."*

**Rubric dimensions it fails.** Evidence (hard gate, 0), Reliability (no operator signal).

---

## 3. Unverified benchmarks / launch-day numbers

**Pattern.** Performance or capability claims without a reproducible benchmark, without a methodology statement, or sourced only from a launch post. Includes cherry-picked metrics that omit the comparison baseline.

**Example (archetypal).** *"'Beats GPT-4 on agentic tasks' cited from a single tweet thread with no eval harness, no dataset, and no baseline configuration."*

**Rubric dimensions it fails.** Evidence (hard gate, 0), Reliability (claims cannot be independently verified).

---

## 4. Duplicates that add no structure or judgement

**Pattern.** A new entry restates an existing one — same project, same claims, same tier — without new evidence, a new angle, or an additional rubric-relevant distinction. Also includes mirrored entries across sections (e.g., listing the same framework in both Orchestration and Reference Architectures without justifying the split).

**Example (archetypal).** *"Proposal to add LangGraph to Reference Architectures when it is already covered in Orchestration Frameworks, with identical bullet points."*

**Rubric dimensions it fails.** Uniqueness (0–1), Agentic relevance (no added value).

---

## 5. Archived, abandoned, or single-author prototypes presented as production frameworks

**Pattern.** A repo with no commits in 12+ months, a GitHub `archived` flag, an unresolved maintainer transition, or a single contributor and no external deployments — framed as production-grade.

**Example (archetypal).** *"A research prototype from a 2023 paper, no releases since, submitted as a 'production orchestration layer'."*

**Rubric dimensions it fails.** Maturity (0–1), Reliability (hard gate, likely 0).

---

## 6. GitHub-stars-as-evidence

**Pattern.** A submission whose primary justification is star count, trending status, or social-media virality — with no operator write-ups, no benchmarks, no stability signals.

**Example (archetypal).** *"'10k stars in a week' cited as the rationale for inclusion, with no linked field report or docs review."*

**Rubric dimensions it fails.** Evidence (hard gate, 0), Reliability (popularity ≠ production-readiness). Community signal alone is **tiebreaker-only** by design.

---

## 7. Agentic-adjacent but out-of-scope tooling

**Pattern.** Generic ML infra, chat UIs without tool use, prompt-only utilities, or content-generation demos with no agent loop, no tool interface, and no multi-step control. Useful software — just not *agentic*.

**Example (archetypal).** *"A prompt templating library, or a ChatGPT-style web UI with no MCP/tool-use layer."*

**Rubric dimensions it fails.** Agentic relevance (hard gate, 0).

---

## 8. Rubric-restatement without rubric-application

**Pattern.** An entry that lists the rubric dimensions and declares the tool passes them, without citing evidence or naming specifics. Box-ticking instead of judgement.

**Example (archetypal).** *"'Reliability: High. Evidence: Strong. Uniqueness: Yes.' — with no links, no examples, no tradeoffs."*

**Rubric dimensions it fails.** Evidence (hard gate, 0), Reliability (unsubstantiated).

---

## Quick reference

| Pattern | Primary failing dimension(s) |
|---------|-------------------------------|
| 1. Generic LLM wrappers | Agentic relevance, Uniqueness |
| 2. Vendor marketing | Evidence, Reliability |
| 3. Unverified benchmarks | Evidence, Reliability |
| 4. Duplicates without added structure | Uniqueness, Agentic relevance |
| 5. Archived / single-author prototypes | Maturity, Reliability |
| 6. Stars-as-evidence | Evidence, Reliability |
| 7. Out-of-scope tooling | Agentic relevance |
| 8. Rubric-restatement | Evidence, Reliability |

If in doubt, open a `suggestion` issue instead of a PR.
