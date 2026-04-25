# Mission

## Purpose

A rigorously curated reference for **agentic AI engineering** — tools, frameworks, patterns, and processes for building production-grade agentic systems — with an explicit evidence bar and a small internal agentic system that helps maintain the list.

## Vision (earned, not asserted)

To become a reference that engineers and researchers reach for when they need to understand, evaluate, or build agentic AI. Stronger language (e.g., "canonical", "go-to", "definitive") is reserved for the Earned tier below and must be backed by external evidence.

### Claim levels

| Tier | Language permitted | Evidence gate |
|---|---|---|
| Baseline | "curated", "opinionated", "continuously updated" | Rubric applied to every entry; freshness markers present; Phase 1–4 CI green |
| Working | "rigorous", "frontier-tracking" | Phase 5–7 shipped; advisory CI consistently green; golden-set evaluation in place (see `evaluation.md`) |
| Earned | "canonical", "definitive", "go-to" | Awesome.re acceptance; ≥3 external independent citations (talks, papers, production docs); ≥30 days of required (non-advisory) CI green on `main` |

Mission text may not use Earned-tier language until all three gates in that row hold. Gate status is tracked in `roadmap.md` Phase 7 evidence gate and Phase 13 graduation.

## Principles

- **Cutting edge, not trendy** — include what advances the field; exclude hype.
- **Engineering over prompting** — favor reliability, observability, and evaluation.
- **Curated, not exhaustive** — every entry earns its place against the rubric.
- **Structured, not a dump** — patterns, rubrics, and decision guides beat flat lists.
- **Evidence-driven** — claims are backed by benchmarks, papers, or production use; see [benchmark-and-evidence-policy](../appendix/benchmark-and-evidence-policy.md).
- **Living document** — updated continuously with dated review markers.
- **Untrusted LLM output** — any text produced by the internal repo-agent is treated as a draft requiring human review (see `safety-model.md`).

## Scope

**In scope:** agent architectures, orchestration frameworks, memory systems, evaluation and safety, protocols (MCP, A2A), tool use, multi-agent patterns, browser/desktop/voice agents, open-source models for agents, learning resources, and agentic workflows/automations.

**Out of scope:** generic LLM tooling without agentic relevance, marketing content, unverified claims, and duplication of existing Awesome lists without added structure or judgment.

**Internal-only surface (not a public product):** `tools/repo-agent/` — the MCP server, CLI, and workflows are internal automation for maintainers and contributors. No semver guarantees, no public API stability, no managed hosting. Graduation to a published product would require a dedicated spec and is not in scope today.

## Audience

Co-equal audiences with **per-section labelling** of the evidence class each section commits to:

| Audience | Primary evidence class |
|---|---|
| Engineers shipping agents to production | Production/field reports, reliability signals, operational evidence |
| Researchers surveying the agentic landscape | Peer-reviewed papers, reproducible benchmarks |
| Teams making architecture decisions | Either class, provided it is labelled on the entry |
| Contributors to the agentic ecosystem | Either class |

Every section in `README.md` and `appendix/` declares its primary audience and evidence class in its header. Shipped in Phase 9.4 as a `> Audience: <role> · Evidence class: <class>` blockquote on every README H2 and every appendix file top. Vocabulary is normative: roles ⊆ {practitioners, researchers, maintainers, all contributors}; evidence classes ⊆ {official, benchmark, field report, mixed}. See `evaluation.md` for the full rule.

## Success Criteria (measurable)

- Rubric coverage: 100% of content entries have a rubric score recorded in their PR.
- Freshness: ≥90% of appendix files carry a `Last reviewed:` marker younger than 12 months.
- Automation reliability: advisory CI green on `main` for ≥30 consecutive days before any check becomes required.
- External validation (Earned tier): awesome.re acceptance + ≥3 independent external citations.
- Agentic system integrity: every repo-agent-authored artefact is traceable (see `observability.md`) and reversible (see `safety-model.md`).
