# Contributing to Awesome Agentic Engineering

First off, thank you for considering contributing to Awesome Agentic Engineering! 

This repository is **not** an exhaustive directory of every tool that exists. It is a heavily curated, opinionated map of agentic AI systems — with a strict focus on architectures, frameworks, memory, evaluation, and safety for production-grade engineering.

## The Core Philosophy
We prioritize:
- **Reliability over novelty**
- **Evaluation over intuition**
- **Architecture over tooling**
- **Systems thinking over prompt engineering**

If your submission aligns with this philosophy and aids in building reliable, observable, and production-grade agentic systems, we would love to review your pull request!

## Entry Rubric (v1)

Every submission is assessed against four fast-to-read fields. Fill these in your PR or issue using the provided templates. The full scoring dimensions below remain the canonical reference for **deep-dive** entries; these four fields are the minimum bar for **every** contribution.

| Field | Definition | Example |
| :--- | :--- | :--- |
| **Reliability** | How dependable is this in production? Stability of APIs, known failure modes, and operator track record. | "LangGraph: stable v0.2 API, active maintainers, used in several public production write-ups." |
| **Evidence** | What sources back the claims? Tag as `[official]`, `[benchmark]`, `[field report]`, or `[author assessment]`. | "`[official]` docs + `[field report]` from Replit engineering blog." |
| **Uniqueness** | What does this offer that existing entries don't? Why is it not a duplicate? | "First framework with first-class typed state + checkpointing for DAG-based agents." |
| **Maturity** | Ecosystem stability — API churn, docs depth, integrations, community, release cadence. | "Production-ready: 18+ months, semantic versioning, >200 integrations." |

For deep-dive entries, also complete the full **Required Scoring Dimensions** rubric further down this document.

## Evidence Policy

Every substantive claim must be anchored to a source. Use the evidence tags below in your PRs and issues.

| Tag | Accept for | Do NOT accept as |
| :--- | :--- | :--- |
| `[official]` | Canonical docs, specs, first-party repos, architecture guides | Marketing landing pages, blog posts that are not operator write-ups |
| `[benchmark]` | Published benchmark runs, evaluation papers, benchmark repos tied to a named workload | Cherry-picked demos, launch-day numbers without methodology |
| `[field report]` | Production write-ups, incident reports, engineering blogs, operator notes | Vendor testimonials, press releases |
| `[author assessment]` | This repo's synthesis after reviewing the sources above and applying the rubric | Standalone opinion without cited sources |

Additional rules:

- **Separate benchmark performance from production maturity.** A benchmark result supports workload fit but does not prove reliability, governance fit, or cost control.
- **No GitHub-stars-as-evidence.** Popularity is not reliability.
- **Date-stamp volatile content.** Add `Last reviewed: Month YYYY` in fast-moving sections (product lists, vendor summaries, release-sensitive guidance).
- **Full policy:** [appendix/benchmark-and-evidence-policy.md](appendix/benchmark-and-evidence-policy.md).

## Contribution Flow

1. **Fork** the repository.
2. **Branch** from `main` using a descriptive name (e.g., `add-inspect-evals`, `refresh-memory-systems`).
3. **Edit** the relevant file(s). Follow the formatting of surrounding content exactly.
4. **Self-assess** against the Entry Rubric (v1) — fill in the PR template.
5. **Open a Pull Request** against `main`. The [PR template](.github/PULL_REQUEST_TEMPLATE.md) will auto-populate — complete all sections.
6. **Review** — a maintainer will score your submission against the rubric. Expect questions on evidence and uniqueness.
7. **Merge** when all rubric fields pass and links are valid.

For proposals (new sections, major refactors, or resource ideas you don't want to author yourself), open an issue using one of the [issue templates](.github/ISSUE_TEMPLATE/) first.

## 🚫 What NOT to Submit

To protect the curation bar, these will be closed or requested to change:

- **Marketing pages or launch posts** without engineering-focused content.
- **Duplicate entries** already covered in the README or appendices (check both before submitting).
- **Unverified claims** — "state of the art", "production-ready", or performance numbers without `[official]`, `[benchmark]`, or `[field report]` evidence.
- **Tools without agentic relevance** — generic LLM libraries, prompt-only utilities, or chat UIs that don't support tool use, memory, or multi-step reasoning.
- **GitHub-stars-as-evidence** — popularity is not a signal of reliability or production readiness.
- **Demo repos, tutorials, or single-author prototypes** presented as production frameworks.
- **Entries that restate the rubric without applying it** — we want judgement, not box-ticking.

If you're unsure whether something qualifies, open a `suggestion` issue first rather than a PR.

## 📊 Formal Evaluation Rubric

We reject "tool list energy." Every major framework and architecture is judged against the same dimensions. Submissions proposing deep-dives or major entries should evaluate the tool based on these **Required Scoring Dimensions**:

- **Control flow explicitness**: How observable and deterministic is the execution path?
- **State model**: How is agent state typed, managed, and persisted?
- **Memory support**: Are there built-in primitives for short-term, episodic, and semantic memory?
- **Observability / tracing**: Is it easy to trace intermediate reasoning steps and tool calls?
- **Human-in-the-loop support**: Does it natively support interrupt-and-resume or approval gates?
- **Type safety / structured outputs**: Are outputs guaranteed against strict schemas?
- **Provider portability**: How tightly coupled is it to one specific LLM provider?
- **Security posture**: Are there built-in mechanisms for sandboxing, access control, or guardrails?
- **Architectural strengths**: Which design choices materially improve decomposition, control, state handling, or interface clarity?
- **Operational constraints**: What deployment burden, runtime cost, debugging friction, or failure modes does it introduce?
- **Ecosystem maturity**: How stable are the APIs, docs, integrations, and operator knowledge base?
- **Governance fit**: Does it support auditability, approval gates, access boundaries, policy enforcement, and regulated environments?
- **Workload suitability**: Which workflows, task shapes, and team contexts does it fit well or poorly?

## Guidelines for Submissions

To keep the repository highly structured and focused, **all major contributions must meet the following criteria**:

1. **Rigorous Evaluation**: Use the rubric above to formulate your assessment.
2. **No Marketing Fluff**: Provide an honest, engineering-focused assessment of the system's pros and cons. 
3. **Evidence of Real-World Usage**: Preference is heavily given to tools with demonstrated production adoption and operational maturity.
4. **Evidence Discipline**: Anchor substantive claims to canonical sources, tag the evidence type, and add `Last reviewed` dates for rapidly changing sections.

See [appendix/benchmark-and-evidence-policy.md](appendix/benchmark-and-evidence-policy.md) for the source order, evidence tags, and date-stamping rule.

### Formatting Your Pull Request

To ensure consistency, every **major entry** (e.g., deep dives, reference architectures) must use the following standard template:

```markdown
### [Framework/Architecture Name]
- **What it is**: [Concise definition]
- **What it demonstrates**: [Why is this a significant example?]
- **Architectural strengths**: [Key engineering advantages based on the rubric]
- **Operational constraints**: [Trade-offs, limitations, and operational friction]
- **Ecosystem maturity**: [API stability, docs, surrounding tooling, and operator familiarity]
- **Governance fit**: [Auditability, approval boundaries, access control, and policy alignment]
- **Workload suitability**: [Where it fits well, and where it creates unnecessary complexity or risk]
- **Design paradigm**: [e.g., Node-based DAG, Actor Model, Pipeline]
- **Evidence basis**: [[official] / [benchmark] / [field report] / [author assessment]]
```

For minor landscape table entries, carefully condense your criteria to match the standard layout used in that section.
If you update a rapidly changing section such as a product list or API capability summary, add or refresh a visible `Last reviewed: Month YYYY` marker in that document.
*(Column names may vary slightly across sections—just match the surrounding table exactly.)*

### Updating Existing Sections

We highly encourage updates to existing sections if definitions become outdated, or if the architectural strengths, operational constraints, or governance profile of a framework substantively shift due to a major ecosystem update. 

## The Pull Request Process

1. **Fork the repository** and create your branch from `main`.
2. Ensure the formatting seamlessly matches the existing markdown.
3. Keep the **Pull Request title** clear and descriptive (e.g., `Add Inspect to Evaluation Frameworks`).
4. In the PR body, briefly explain **why** the resource meets the critical bar for this specific repository.

Thanks for helping keep the repository engineering-focused and usable.
