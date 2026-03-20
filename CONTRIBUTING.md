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
```

For minor landscape table entries, carefully condense your criteria to match the standard layout used in that section.
*(Column names may vary slightly across sections—just match the surrounding table exactly.)*

### Updating Existing Sections

We highly encourage updates to existing sections if definitions become outdated, or if the architectural strengths, operational constraints, or governance profile of a framework substantively shift due to a major ecosystem update. 

## The Pull Request Process

1. **Fork the repository** and create your branch from `main`.
2. Ensure the formatting seamlessly matches the existing markdown.
3. Keep the **Pull Request title** clear and descriptive (e.g., `Add Inspect to Evaluation Frameworks`).
4. In the PR body, briefly explain **why** the resource meets the critical bar for this specific repository.

Thanks for helping keep the repository engineering-focused and usable.
