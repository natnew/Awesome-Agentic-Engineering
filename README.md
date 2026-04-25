# 🧠 Awesome Agentic Engineering

> **Stop prompting. Start engineering. A structured reference for taking AI agents into production.**

[![Awesome](https://awesome.re/badge-flat2.svg)](https://awesome.re) [![Last Commit](https://img.shields.io/github/last-commit/natnew/Awesome-Agentic-Engineering?label=last%20updated&style=flat-square)](https://github.com/natnew/Awesome-Agentic-Engineering/commits) [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com) [![License: MIT](https://img.shields.io/badge/License-MIT-lightgrey.svg?style=flat-square)](LICENSE)

A curated map of agentic AI systems — covering architectures, frameworks, memory, evaluation, and safety.

**🌐 Live site:** <https://natnew.github.io/Awesome-Agentic-Engineering/>

This is not a list of tools.

We reject "tool list energy." It is a structured guide to building **reliable, observable, and production-grade agentic systems**, rigorously evaluated against engineering dimensions.

---

## 📑 Table of Contents

> Audience: all contributors · Evidence class: mixed

- [🧭 Thesis](#-thesis)
- [⚖️ Architecture Decision Guide](#️-architecture-decision-guide)
- [🧩 Core Agentic Patterns](#-core-agentic-patterns)
- [🏗️ Reference Architectures](#-reference-architectures)
- [📐 Spec-Driven Development](#-spec-driven-development)
- [🧠 Memory Systems](#-memory-systems)
- [📊 Formal Evaluation Rubric](#-formal-evaluation-rubric)
- [Benchmark and Evidence Policy](#benchmark-and-evidence-policy)
- [⚙️ Orchestration Frameworks](#-orchestration-frameworks)
- [📡 Protocols and Standards](#-protocols-and-standards)
- [� Reasoning & Planning Models](#-reasoning--planning-models)
- [�🧪 Evaluation & Safety](#-evaluation--safety)
- [🧠 Skills and Operating Principles](#-skills-and-operating-principles)
- [🚫 What NOT to Do](#-what-not-to-do)
- [📊 Signals (How to Read This List)](#-signals-how-to-read-this-list)
- [🚀 Getting Started](#-getting-started)
- [🤝 Contributing](#-contributing)
- [📌 Final Note](#-final-note)

### 📂 Appendix
- [🌐 Browser and Desktop Agents](appendix/browser-and-desktop-agents.md)
- [🎙 Voice Agents](appendix/voice-agents.md)
- [🎨 Creative AI](appendix/creative-ai.md)
- [💼 Customer Support and CRM Agents](appendix/customer-support-and-crm-agents.md)
- [🧠 Open-Source Models for Agents](appendix/open-source-models-for-agents.md)
- [📰 Newsletters and Communities](appendix/newsletters-and-communities.md)
- [📚 Learning Resources](appendix/learning-resources.md)
- [⚡ Fast-Moving Product Lists](appendix/fast-moving-product-lists.md)


---

## 🧭 Thesis

> Audience: all contributors · Evidence class: mixed

| 📈 The Shift (Agentic systems are moving to) | 📉 The Challenge (Implementations suffer from) | 🎯 Our Focus (This repository prioritises) |
| :--- | :--- | :--- |
| • Stateful, multi-step reasoning<br>• Multi-agent collaboration & orchestration<br>• Feedback-driven learning loops<br>• Tool-augmented execution environments | • Fragility under iteration<br>• Poor observability & evaluation<br>• Weak memory & context management<br>• Limited safety & governance | • **Reliability** over novelty<br>• **Evaluation** over intuition<br>• **Architecture** over tooling<br>• **Systems thinking** over prompt engineering |

---

## ⚖️ Architecture Decision Guide

> Audience: practitioners · Evidence class: mixed

| If your task is... | Start with... | Escalate to... | Avoid... |
| :--- | :--- | :--- | :--- |
| **bounded, tool-using, low-risk** | single-agent + tools | typed state, retries | multi-agent teams |
| **long-running, inspectable, enterprise** | graph/workflow orchestration | approval gates, persistence | opaque emergent loops |
| **open-ended research** | planner/executor or supervisor | critique loops, memory | rigid pipelines only |
| **high-reliability extraction** | prompt chains + strict schemas | validator feedback loops | unconstrained conversational agents |
| **complex parallel execution** | modular multi-agent setups | shared workspace/memory | treating LLMs as deterministic |

---

## 🧩 Core Agentic Patterns

> Audience: practitioners · Evidence class: mixed

These patterns underpin most production-grade agentic systems.

| Pattern | Description | Key Characteristic |
| :--- | :--- | :--- |
| **Single-Agent + Tool Use** | One reasoning loop with structured tool invocation | Suited to focused tasks with bounded scope |
| **Supervisor / Router Agents** | Central agent delegates tasks to specialised agents | Enables modularity and scalability |
| **Multi-Agent Collaboration** | Agents operate in parallel or sequence | Patterns: debate, critique, planning/execution split |
| **Reflection / Critique Loops** | Agents evaluate and refine their own outputs | Improves reliability over multiple iterations |
| **Retrieval-Augmented Agents** | External knowledge via vector search or APIs | Reduces hallucination and improves grounding |
| **Event-Driven / Long-Running Agents** | Persistent agents reacting to triggers over time | Requires memory, state, and orchestration |

---

## 🏗️ Reference Architectures

> Audience: practitioners · Evidence class: mixed

Representative system designs for real-world use.

| Architecture | Ecosystem Maturity | Description | Architectural Strengths | Operational Constraints | Workload Suitability | Design Paradigm | Governance Fit |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **DeerFlow** | *Emerging* | **Is:** Open-source orchestration system combining sub-agents, memory, and sandboxes.<br>**Demonstrates:** Workflow-oriented orchestration across agents with shared execution context. | Strong system-level reference for memory, sandbox, and skills composition. | Higher setup complexity and a heavier runtime surface than most teams need initially. | Strong fit for compound research/coding workflows and teams studying full-stack agent architectures. Poor fit for lightweight orchestration or narrowly scoped tasks. | Hierarchical multi-agent orchestration. | Requires explicit sandbox policy, tool boundaries, and operator oversight before untrusted code execution. |
| **SWE-agent** | *Experimental* | **Is:** Autonomous SWE system using a specialized Agent-Computer Interface (ACI).<br>**Demonstrates:** Narrow action spaces and interface design tuned for code-repair tasks. | Streamlined command space, compressed history handling, and a clear task boundary for patch workflows. | Benchmark-oriented design, high token cost, and long end-to-end fix latency on larger tasks. | Strong fit for isolated PRs and self-contained bug fixes. Poor fit for broad refactors or environments without standard build tooling. | Single agent with a highly specialized action space (ACI). | Needs tight repository scoping, review gates, and execution controls to reduce silent code regressions. |

---

## 📐 Spec-Driven Development

> Audience: practitioners · Evidence class: mixed

_Last reviewed: April 2026._

Agentic systems amplify whatever intent you feed them — including vague intent. **Spec-driven development (SDD)** treats the specification as the load-bearing artifact: a durable, reviewable document that describes *what* the system should do and *how* it should behave, from which plans, code, and tests are generated (and regenerated) by agents. It is the production-grade answer to "vibe coding."

In an agentic context, the spec does three things at once:

1. **Anchors intent** — a typed, versioned contract the agent (and humans) refer back to across long sessions.
2. **Defines the acceptance surface** — plans, tasks, and tests are derived from the spec, not improvised per prompt.
3. **Makes re-generation safe** — regenerating code from an updated spec is cheaper and more reviewable than patching drift.

### Core practices

| Practice | What it means | Why it matters for agents |
| :--- | :--- | :--- |
| **Spec before plan before code** | Write a scoped spec (problem, constraints, acceptance criteria) before any plan or implementation. Plans and code are generated *from* the spec. | Agents behave better against a fixed target than against a shifting prompt. |
| **Executable specs** | Encode acceptance criteria as runnable checks (tests, evals, schema validators) alongside prose. | Lets agents self-verify and lets CI reject regressions without human review on every step. |
| **Typed contracts at boundaries** | Specify tool signatures, state shape, and I/O schemas with types (Pydantic, JSON Schema, TypeSpec). | Narrows the action space the agent can hallucinate into. |
| **Review the spec, not the diff** | Human review focuses on the spec and acceptance checks; the diff is a consequence. | Makes agent-authored PRs tractable at volume. |
| **Versioned and diffable** | Specs live in the repo, are PR-reviewed, and evolve with the code. | Gives rollback, blame, and audit trail — same hygiene as code. |
| **One spec, many artifacts** | Generate plans, tasks, tests, and docs from the same spec. | Keeps planner, actor, and verifier aligned. |

### Resources

Evidence tags follow the [Benchmark and Evidence Policy](#benchmark-and-evidence-policy).

| Resource | Role | Description | Evidence |
| :--- | :--- | :--- | :--- |
| **[GitHub Spec Kit](https://github.com/github/spec-kit)** | Toolkit / methodology | Open-source toolkit for spec-driven development with agentic coding assistants (Copilot, Claude Code, Cursor, Gemini CLI). Defines the `/specify` → `/plan` → `/tasks` → `/implement` workflow used in this repo's own `specs/` directory. | `[official]` [repo](https://github.com/github/spec-kit) · `[official]` [announce](https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/) |
| **[Kiro](https://kiro.dev)** | IDE | AWS IDE built around spec-driven development: specs, steering files, and hooks drive agent work from requirements through tasks. First-party reference implementation of SDD in an IDE. | `[official]` [docs](https://kiro.dev/docs/) · `[field report]` [AWS launch post](https://aws.amazon.com/blogs/aws/introducing-kiro-an-ai-ide-that-thinks-like-a-developer/) |
| **[OpenAI Model Spec](https://model-spec.openai.com/)** | Behavioural spec | First-party example of treating *model behaviour* as a versioned, public spec — objectives, rules, defaults, and conflict resolution. A reference for how to write a spec an agent can actually be aligned to. | `[official]` [spec](https://model-spec.openai.com/) · `[official]` [post](https://openai.com/index/sharing-the-latest-model-spec/) |
| **[AGENTS.md](https://agents.md/)** | Project-level agent spec | Simple convention for a repository-scoped file that instructs coding agents about build, test, style, and conventions. Widely supported across agent CLIs. | `[official]` [site](https://agents.md/) |
| **[Anthropic Claude Skills (SKILL.md)](https://www.claude.com/skills)** | Skill-level spec | Declarative, self-contained skill specs (`SKILL.md`) that package instructions, tools, and examples agents can discover and load on demand. Treats individual capabilities as versioned spec artifacts. | `[official]` [docs](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview) |
| **[Pydantic AI](https://ai.pydantic.dev/)** | Typed contracts | Python framework that makes schema-first I/O the default for LLM calls — the practical form of "typed contracts at boundaries" for agent code. | `[official]` [docs](https://ai.pydantic.dev/) |

### Where SDD applies

SDD is not limited to new projects or a single team. The spec becomes a portable artifact in three directions:

| Context | How SDD applies | Notes |
| :--- | :--- | :--- |
| **Greenfield projects** | Write the spec first; agents scaffold the repo, tests, and initial implementation from it. | Easiest case — no legacy constraints; the spec defines the system boundary. |
| **Brownfield projects** | Reverse-engineer specs from existing code and behaviour, then use them as the contract for future agent-authored changes. | Start narrow (one module or flow), treat the spec as the accepted behaviour, and expand coverage incrementally. Agents modify against the spec, not the full legacy codebase. |
| **Shared across orgs** | Specs, prompts, evals, and skill packs (`SKILL.md`, `AGENTS.md`, prompt libraries) are repo-level artifacts that can be open-sourced, forked, and re-used — like shared test suites or style guides. | Treat prompts and evals as first-class, versioned assets; publish them alongside code so research, patterns, and hard-won lessons compound across teams rather than staying trapped in one org. |

> **How this repo uses SDD:** the [`specs/`](specs/) directory contains phased specs (requirements → plan → validation) generated and executed against with Spec Kit. The `tasks/todo.md`, phase validation scripts, and PR bodies are derived artifacts. See [CONTRIBUTING.md](CONTRIBUTING.md) for the contributor-facing workflow.

---

## 🧠 Memory Systems

> Audience: practitioners · Evidence class: mixed

_Last reviewed: April 2026._

Memory is a first-class concern in agentic systems. Rather than treating memory as a simple array of previous messages, production systems require structured approaches to state, persistence, retrieval, and **experience reuse**. Four categories — working, episodic, procedural, semantic — remain the core architectural choices, but recent frontier research also shows memory is increasingly being used to **improve future agent behaviour**, not merely to store past context.

### Memory Taxonomy

Different types of memory serve distinct functional roles in an agentic architecture:

| Type | Definition | Implementation Examples |
| :--- | :--- | :--- |
| **Working Memory** (Thread State) | Short-term context for the current execution loop or active conversation thread. Ephemeral. | Context window, LangGraph `State`, in-memory message lists. |
| **Episodic Memory** | Autobiographical history of past actions, inputs, and outcomes. Enables reflection on past mistakes. | Checkpoint logs, event stores, prompt / trajectory histories. |
| **Procedural Memory** | Reusable skills, system prompts, and tool configurations. Defines *how* the agent operates. | Static configuration, retrieved skill libraries, GitHub workflows. |
| **Semantic Memory** | Embedded, factual knowledge about the world, the user, or the domain. Defines *what* the agent knows. | Vector databases (FAISS, Pinecone), knowledge graphs, Letta core memory. |

### Frontier Research: Memory Beyond Storage

Recent research shows frontier agent systems moving beyond simple retrieval towards **experience transformation**: converting prior trajectories, workflows, and reasoning patterns into reusable guidance for future tasks. Memory becomes part of the learning loop, not just the context pipeline.

| System | Best Fit in Taxonomy | Why it matters | Evidence |
| :--- | :--- | :--- | :--- |
| **Agent Workflow Memory (AWM)** | Episodic + Procedural | Induces reusable workflows from prior experience and selectively retrieves them to guide future generations; improves long-horizon web-agent tasks in both offline and online settings. | `[official]` [repo](https://github.com/zorazrw/agent-workflow-memory) · `[benchmark]` [paper](https://arxiv.org/abs/2409.07429) |
| **Synapse** | Episodic | Stores exemplar trajectories as memory and retrieves them via similarity search, using complete state–action histories (not shallow few-shot examples) to improve multi-step computer control. | `[official]` [site](https://ltzheng.github.io/Synapse/) · `[benchmark]` [paper](https://arxiv.org/abs/2306.07863) |
| **ReasoningBank** | Episodic + Procedural (semantic-adjacent) | Distils generalisable reasoning strategies from self-judged successful *and* failed experiences, then retrieves and updates them over time so the agent improves through continued interaction. | `[benchmark]` [paper](https://arxiv.org/abs/2509.25140) |

### Architectural Patterns: Shared vs. Private Memory

In multi-agent systems, memory boundaries are architectural decisions:
- **Private Agent Memory**: Each agent maintains its own semantic and episodic stores. Prevents context leakage and maintains strong role boundaries.
- **Shared Workspace (Global Memory)**: A common blackboard or shared state where multiple agents read and write. Requires collision management and strict typing.

### Retrieval and Persistence Decisions

Managing the memory lifecycle is critical for long-running agents.

| Mechanism | Description | Best Practices & Risks |
| :--- | :--- | :--- |
| **Checkpointing** | Saving the exact thread state at a specific point in time (e.g., node transitions). | Enables "time travel" (rewind and replay) and human-in-the-loop approvals. |
| **Write Policies** | Rules defining when and how an agent commits data to long-term storage. | Prefer explicit `SaveMemory` tool calls over passive auto-saving to maintain control. |
| **Retrieval Triggers** | Determining when to query past memory (e.g., pre-fetch vs. just-in-time). | Use vector search for semantic recall, but use explicit graph keys for structured state. |
| **Summarisation / Compression** | Reducing token counts of episodic histories. | Summarise older interactions into a rolling summary while preserving recent exact messages. |
| **Pruning / Decay** | Deleting or archiving old or irrelevant memories. | Implement TTL (time-to-live) for working memory to prevent context exhaustion. |
| **Contamination / Poisoning** | Malicious or incorrect data persisting in long-term memory. | **Risk**: Once poisoned, an agent's future logic breaks. Require validation or bounds on semantic writes. |

### Systems and Protocols

Specialised infrastructure for managing agent memory.

| System | Role | Description |
| :--- | :--- | :--- |
| **LangGraph Persistence** | Thread-level state | Built-in check-pointers (SQLite, Postgres) for DAG-based execution loops, enabling interrupt/resume. |
| **LangMem** | Long-term memory extraction | LangChain's framework for extracting user preferences and entity profiles in the background. |
| **Letta** (formerly MemGPT) | OS-level memory abstraction | Advanced core memory management with explicit paging (read/write limits) to mimic virtual memory. |
| **Mem0** | Personalized memory layer | Managed memory API focusing on user contexts, interactions, and entity relationships. |
| **Zep / Graphiti** | Enterprise memory & graphs | Fast, long-term memory for AI assistants; uses temporal knowledge graphs to map entity relationships over time. |
| **MCP** (Model Context Protocol) | Interoperability fabric | While not a DB itself, MCP provides a standard protocol to expose memory stores and file systems universally across tools and agents. |

> **Design implication:** the key question is no longer only *what* the agent remembers, but *how memory changes future behaviour*. Systems like Synapse, Agent Workflow Memory, and ReasoningBank signal a shift — memory is becoming part of the agent's learning loop, enabling reusable routines and self-improvement over time.

---

## 📊 Formal Evaluation Rubric

> Audience: maintainers · Evidence class: mixed

> **🎯 Evaluation principle:** rubrics assess quality, test suites verify behaviour, assertions enforce invariants, and LLM-as-a-judge is used only in tightly scoped regression tests.

Every major framework and architecture in this repository is judged against the following **Required Scoring Dimensions**. We evaluate systems based on engineering rigor, not marketing copy.

| Dimension | Evaluation Criteria |
| :--- | :--- |
| **Control flow explicitness** | How observable and deterministic is the execution path? |
| **State model** | How is agent state typed, managed, and persisted? |
| **Memory support** | Are there built-in primitives for short-term, episodic, and semantic memory? |
| **Observability / tracing** | Is it easy to trace intermediate reasoning steps and tool calls? |
| **Human-in-the-loop support** | Does it natively support interrupt-and-resume or approval gates? |
| **Type safety / structured outputs** | Are outputs guaranteed against strict schemas? |
| **Provider portability** | How tightly coupled is it to one specific LLM provider? |
| **Security posture** | Are there built-in mechanisms for sandboxing, access control, or guardrails? |
| **Architectural strengths** | Which design choices materially improve decomposition, control, state handling, or interface clarity? |
| **Operational constraints** | What deployment burden, runtime cost, debugging friction, or failure modes does it introduce? |
| **Ecosystem maturity** | How stable are the APIs, docs, integrations, and operator knowledge base? |
| **Governance fit** | Does it support auditability, approval gates, access boundaries, policy enforcement, and regulated environments? |
| **Workload suitability** | Which workflows, task shapes, and team contexts does it fit well or poorly? |

---

## Benchmark and Evidence Policy

> Audience: maintainers · Evidence class: official

Canonical resources are trusted here because they define what counts as evidence. Prefer official docs, architecture guides, papers, benchmark repos, and first-party repositories when establishing capabilities, methodology, or interface details.

| Evidence Tag | Use For |
| :--- | :--- |
| `[official]` | Official docs, architecture guides, specifications, benchmark documentation, or first-party repositories. |
| `[benchmark]` | Published benchmark runs, evaluation papers, or benchmark repos tied to a named workload. |
| `[field report]` | Production write-ups, incident reports, engineering blogs, or operator notes about real deployments. |
| `[author assessment]` | This repository's synthesis after reviewing the sources above and applying the rubric. |

- Do not treat marketing copy, launch-day demos, or GitHub stars as sufficient evidence for production claims.
- Separate benchmark performance from production maturity. A benchmark result can support workload fit, but it does not by itself prove reliability, governance fit, cost control, or operational maturity.
- Record `Last reviewed: Month YYYY` in rapidly changing sections such as product lists, vendor capability summaries, and release-sensitive guidance.
- See [appendix/benchmark-and-evidence-policy.md](appendix/benchmark-and-evidence-policy.md) for the full policy.

## ⚙️ Orchestration Frameworks

> Audience: practitioners · Evidence class: mixed

_Last reviewed: April 2026._

### Deep Dives

Evidence tags follow the [Benchmark and Evidence Policy](#benchmark-and-evidence-policy). Scored against [RUBRIC.md](RUBRIC.md); cap of 5–8 deep-dive entries enforced.

| Framework | Ecosystem Maturity | Description | Architectural Strengths | Operational Constraints | Workload Suitability | Design Paradigm | Governance Fit | Evidence |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **LangGraph** | *Production-ready* | **Is:** Stateful orchestration framework building directed graphs with typed state.<br>**Demonstrates:** Deterministic execution control mixed with LLM reasoning. | Explicit state management, persistence, and support for complex multi-actor workflows. | Verbose abstractions, steep learning curve, and graph sprawl if the workflow is over-modeled. | Strong fit for multi-step, stateful, and interruptible agent systems. Poor fit for simple single-prompt completions or linear chains. | DAG-based state machine. | Good fit for auditable workflows and approval gates, but graph edges must be tightly constrained to avoid runaway loops. | `[official]` [docs](https://langchain-ai.github.io/langgraph/) · `[field report]` [LinkedIn SQL Bot](https://blog.langchain.dev/customers-linkedin/) |
| **Microsoft Agent Framework** | *Production-ready* | **Is:** Microsoft's unified agent framework merging Semantic Kernel and AutoGen; first-class MCP and A2A support.<br>**Demonstrates:** Enterprise-grade agent composition with typed plugins, approval workflows, and Azure integration. | Strong .NET + Python parity, typed function-calling, native MCP/A2A, and OpenTelemetry tracing. | Broader Azure coupling in the managed path; framework surface is still stabilizing post-merger. | Strong fit for enterprise teams already on Azure / Semantic Kernel and needing multi-language agents. Poor fit for teams wanting a minimal Python-only stack. | Typed plugin graph with pluggable orchestration (sequential, group chat, handoff). | Strong — supports approval gates, policy plugins, and audit logging out of the box. | `[official]` [repo](https://github.com/microsoft/agent-framework) · `[official]` [announce](https://devblogs.microsoft.com/foundry/introducing-microsoft-agent-framework/) |
| **AutoGen** | *Production-ready* | **Is:** Microsoft Research multi-agent conversation framework; now an orchestration pattern inside Microsoft Agent Framework.<br>**Demonstrates:** Conversable agents with group chat, code-executor, and human-proxy patterns. | Battle-tested multi-agent conversation patterns, large research footprint, flexible role composition. | Emergent conversation loops need explicit termination conditions; observability requires added tooling. | Strong fit for research on multi-agent collaboration and code-gen crews. Poor fit for strictly deterministic workflows. | Conversational multi-agent loop with configurable managers. | Needs explicit stop conditions and sandboxed code execution to be safe in production. | `[official]` [v0.4 docs](https://microsoft.github.io/autogen/) · `[benchmark]` [AutoGen paper](https://arxiv.org/abs/2308.08155) |
| **OpenAI Agents SDK** | *Production-ready* | **Is:** OpenAI's official agents SDK with handoffs, guardrails, and sessions; successor path to Assistants API.<br>**Demonstrates:** First-party multi-step agents with tool-use, tracing, and structured handoffs. | Tight integration with OpenAI tools, built-in tracing, ergonomic Python API, provider-agnostic via LiteLLM. | Primary optimization target is OpenAI models; porting to other providers loses some ergonomics. | Strong fit for teams shipping OpenAI-backed agents quickly with tracing. Poor fit for strict provider portability or local-only models. | Handoff-based multi-agent loop with sessions. | Viable for hosted approval flows; guardrails are first-class primitives. | `[official]` [docs](https://openai.github.io/openai-agents-python/) · `[official]` [repo](https://github.com/openai/openai-agents-python) |
| **CrewAI** | *Emerging* | **Is:** Multi-agent collaboration framework where agents are assigned roles, goals, and tools.<br>**Demonstrates:** Role-based agentic workflows with sequential and hierarchical processes. | Simple mental model and fast team-based decomposition for prototypes; growing enterprise feature set. | Less control for highly complex or non-standard systems; observability and typed state are weaker than LangGraph/MAF. | Strong fit for rapid prototyping of agent teams. Poor fit for deterministic execution, rigorous type safety, or custom orchestration loops. | Role-based sequential or hierarchical process execution. | Requires added guardrails and observability to manage emergent loops and inconsistent agent behaviour. | `[official]` [docs](https://docs.crewai.com/) · `[field report]` [case studies](https://www.crewai.com/case-studies) |
| **Pydantic AI** | *Production-ready* | **Is:** Framework built directly on Pydantic enforcing strict data validation and type-safe outputs from LLMs.<br>**Demonstrates:** Type-driven agentic execution and dependency injection. | Strong type-system integration, schema enforcement, dependency injection, and retry support. | Smaller surrounding ecosystem than older orchestration stacks; retry loops can increase latency and cost. | Strong fit for production systems needing strict type safety and predictable parsing. Poor fit for open-ended generative writing or weakly structured tasks. | Strongly typed, schema-first LLM interactions. | Good fit where schema validation and dependency control matter, but retry policies need explicit cost and failure bounds. | `[official]` [docs](https://ai.pydantic.dev/) |
| **Smolagents** | *Emerging* | **Is:** Minimalist framework using `CodeAgents` (Python logic code generation over JSON calling).<br>**Demonstrates:** Code-first model execution bounds. | Lightweight core and direct execution model that stays close to Python control flow. | Weak typed-state enforcement and high exposure if generated code runs with broad permissions. | Strong fit for fast prototyping and Python-native experimentation. Poor fit for regulated networks or systems that need strict sandboxing and observability. | Python-native logic execution via LLM generation. | Requires strong sandboxing, network controls, and review boundaries before production use. | `[official]` [docs](https://huggingface.co/docs/smolagents) |

---

### Frameworks Landscape

Broader catalog beyond the deep-dive set. Each subsection capped at 8 entries; entries that cannot clear the rubric were removed in this phase (see PR body for cut list).

#### General Purpose

| Framework | Lang | Description | Evidence |
|-----------|------|-------------|----------|
| [LangChain](https://github.com/langchain-ai/langchain) | Py/JS | Modular framework with chains, tools, memory, and broad integration coverage. | `[official]` |
| [LangGraph](https://github.com/langchain-ai/langgraph) | Py/JS | Graph-based orchestration. Stateful typed-state graphs with checkpointing. | `[official]` |
| [LlamaIndex](https://github.com/run-llama/llama_index) | Py/JS | Data-centric framework for retrieval-heavy and RAG-oriented agent systems. | `[official]` |
| [Haystack](https://github.com/deepset-ai/haystack) | Py | Pipeline-based framework for search, retrieval, and hybrid agent workflows. | `[official]` |
| [Semantic Kernel](https://github.com/microsoft/semantic-kernel) | C#/Py/Java | Microsoft enterprise kernel; now a composable layer inside Microsoft Agent Framework. | `[official]` |
| [Microsoft Agent Framework](https://github.com/microsoft/agent-framework) | Py/.NET | Microsoft's unified agent framework merging Semantic Kernel and AutoGen; first-class MCP and A2A support. | `[official]` |
| [Pydantic AI](https://github.com/pydantic/pydantic-ai) | Py | Type-safe, Pydantic-native; schema-first LLM interactions with dependency injection. | `[official]` |
| [DSPy](https://github.com/stanfordnlp/dspy) | Py | Stanford. Programming not prompting; compiler optimizes prompts against metrics. | `[official]` · `[benchmark]` |

#### Multi-Agent Orchestration

| Framework | Lang | Description | Evidence |
|-----------|------|-------------|----------|
| [AutoGen](https://github.com/microsoft/autogen) | Py | Microsoft Research multi-agent conversations; v0.4 redesigned for async event-driven execution. | `[official]` · `[benchmark]` |
| [CrewAI](https://github.com/crewAIInc/crewAI) | Py | Role-based crew members with goals, tools, and sequential/hierarchical processes. | `[official]` |
| [OpenAI Agents SDK](https://github.com/openai/openai-agents-python) | Py | Official OpenAI multi-step agents with handoffs, guardrails, sessions, and tracing. | `[official]` |
| [Google ADK](https://github.com/google/adk-python) | Py | Native Gemini multi-agent orchestration; deploys to Vertex AI Agent Engine. | `[official]` |
| [MetaGPT](https://github.com/geekan/MetaGPT) | Py | PM / architect / engineer roles simulating a software company; research-oriented. | `[official]` · `[benchmark]` |
| [CAMEL](https://github.com/camel-ai/camel) | Py | Role-based simulation and collaborative reasoning research framework. | `[official]` · `[benchmark]` |
| [DeerFlow](https://github.com/bytedance/deer-flow) | Py | ByteDance orchestration system for planning, tools, memory, and execution. | `[official]` |
| [AgentScope](https://github.com/modelscope/agentscope) | Py | Alibaba multi-agent framework with message-passing runtime and distributed mode. | `[official]` |

#### Lightweight / Minimalist

| Framework | Lang | Description | Evidence |
|-----------|------|-------------|----------|
| [Smolagents](https://github.com/huggingface/smolagents) | Py | HuggingFace minimal agents (~1000 lines); code-action agents with sandboxed execution. | `[official]` |
| [Agno](https://github.com/agno-agi/agno) | Py | Lightweight, model-agnostic agent framework with native multi-modal support. | `[official]` |
| [Upsonic](https://github.com/upsonic/upsonic) | Py | MCP-first framework with minimal setup and typed task graphs. | `[official]` |
| [Portia AI](https://github.com/portia-ai/portia-sdk-python) | Py | Plan-based agent framework aimed at reliable production deployments with approval gates. | `[official]` |
| [Mastra](https://github.com/mastra-ai/mastra) | TS | TypeScript-first framework with observability, workflows, and memory. | `[official]` |

---

## 📡 Protocols and Standards

> Audience: practitioners · Evidence class: official

_Last reviewed: April 2026._

Protocols are the stable contracts between agents, tools, and hosts. Each entry below distinguishes the **specification** from any specific implementation — mixing the two is a repeat anti-pattern (see [ANTI-PATTERNS.md](ANTI-PATTERNS.md)).

| Protocol | Kind | Description | Evidence |
|----------|------|-------------|----------|
| [MCP (Model Context Protocol)](https://modelcontextprotocol.io/) | Open spec | Anthropic-authored open standard for exposing tools, resources, prompts, and sampling to LLM hosts; wide multi-vendor adoption in 2025–2026. | `[official]` [spec](https://spec.modelcontextprotocol.io/) |
| [A2A (Agent2Agent)](https://github.com/a2aproject/A2A) | Open spec | Google-originated, Linux Foundation–hosted protocol for secure cross-agent communication across vendors and frameworks. | `[official]` [spec](https://a2a-protocol.org/) |
| [OpenAI Function / Tool Calling](https://platform.openai.com/docs/guides/function-calling) | Vendor API | Native structured tool invocation for OpenAI models; JSON-schema-typed tool definitions. | `[official]` |
| [Anthropic Tool Use](https://docs.anthropic.com/en/docs/build-with-claude/tool-use) | Vendor API | Native structured tool invocation for Claude models; supports parallel tool calls and computer-use tools. | `[official]` |
| [OpenAPI](https://github.com/OAI/OpenAPI-Specification) | Open spec | Industry-standard HTTP API specification; foundation for typed, discoverable tool surfaces behind MCP or direct function-calling. | `[official]` |

---

## 🧭 Reasoning & Planning Models

> Audience: researchers · Evidence class: benchmark

_Last reviewed: April 2026._

Models that do **explicit reasoning or planning at inference time** — chain-of-thought baked into the decoding loop, extended thinking budgets, or trained planner heads. They change the shape of agent loops: the model absorbs work that used to live in a planner node, which shifts where you spend tokens, latency, and trust. Cap of 5–8 entries; selected for agentic relevance, not general benchmark wins. Same-family tiers (e.g. `mini` / `nano`, Sonnet / Haiku, Flash / Flash-Lite) are grouped into one row because they share the same reasoning interface and differ mainly in latency and cost.

| Model | Provider | Reasoning Mode | Why it matters for agents | Evidence |
|-------|----------|----------------|---------------------------|----------|
| **GPT-5.4 (family: `gpt-5.4` / `mini` / `nano`)** | OpenAI | Tunable reasoning effort (`none`/`low`/`medium`/`high`/`xhigh`) with native computer-use, web/file search, and function tools | Single family covers planner (`gpt-5.4`), subagent/actor (`mini`), and high-volume tool-calling (`nano`) — lets one agent loop span tiers without swapping SDKs. | `[official]` [model index](https://developers.openai.com/api/docs/models) · `[official]` [`gpt-5.4`](https://developers.openai.com/api/docs/models/gpt-5.4) · [`mini`](https://developers.openai.com/api/docs/models/gpt-5.4-mini) · [`nano`](https://developers.openai.com/api/docs/models/gpt-5.4-nano) |
| **Claude Opus 4.7 / Sonnet 4.6 / Haiku 4.5** | Anthropic | Configurable extended-thinking budget, interleaved with tool calls | Same thinking-budget dial across a planner/worker/fast-actor trio; agent-friendly latency/cost staging without changing prompt contract. | `[official]` [system cards](https://www.anthropic.com/system-cards) · `[official]` [extended thinking](https://docs.anthropic.com/en/docs/build-with-claude/extended-thinking) |
| **Gemini 3.1 Pro / 3 Flash / 3.1 Flash-Lite** | Google DeepMind | Deep Think parallel-hypothesis reasoning (Pro); thinking-capable Flash tier for cheaper loops | Three-tier reasoning ladder over Google's long-context stack — Pro for planning, Flash/Flash-Lite for high-fanout tool calls in the same agent graph. | `[official]` [model cards](https://deepmind.google/models/model-cards/) · `[official]` [Gemini 3.1 Pro card](https://deepmind.google/models/gemini/) |
| **DeepSeek-R1** | DeepSeek | RL-trained reasoning traces, open weights | First strong open-weight reasoning model; reproducible baseline for planner research and local agent stacks. | `[official]` [repo](https://github.com/deepseek-ai/DeepSeek-R1) · `[benchmark]` [paper](https://arxiv.org/abs/2501.12948) |
| **Qwen3 (thinking mode)** | Alibaba | Switchable thinking / non-thinking modes | Open-weight family with explicit thinking toggle — useful when you want the same model in both planner and actor roles. | `[official]` [repo](https://github.com/QwenLM/Qwen3) · `[benchmark]` [tech report](https://arxiv.org/abs/2505.09388) |
| **Grok 4** | xAI | Native reasoning with tool use | Aggressive frontier-reasoning entrant; useful as a diversity source in multi-model planner ensembles. | `[official]` [page](https://x.ai/news/grok-4) |

> Decision guide: if your agent loop already does explicit plan → act → verify steps, a reasoning model can often **replace** the planner node — but it rarely removes the need for typed state, tracing, and eval. Treat reasoning as a cheaper planner, not a free reliability upgrade.

---

## 🧪 Evaluation & Safety

> Audience: researchers · Evidence class: benchmark

_Last reviewed: April 2026._

This section covers frameworks and operational tooling for testing agent quality, correctness, task completion, regressions, and system behaviour, as well as security scanning, red teaming, policy testing, and misalignment research. Evidence tags follow the [Benchmark and Evidence Policy](#benchmark-and-evidence-policy).

### Core Evaluation Areas

- Output correctness  
- Reasoning quality  
- Tool-use accuracy  
- Latency and cost  
- Robustness under adversarial input  

### Evaluation Frameworks

| Framework | Description | Methodology / Workload Suitability | Evidence |
|-----------|-------------|------------------------|----------|
| [OpenAI Evals](https://github.com/openai/evals) | Core framework for testing and improving AI systems. | Foundational evaluation framework and methodology. | `[official]` |
| [DeepEval](https://deepeval.com/docs/getting-started) | Open-source LLM evaluation framework with metrics for hallucination, answer relevance, and task completion. | Application-level evaluation and regression testing. | `[official]` |
| [promptfoo](https://www.promptfoo.dev/docs/intro/) | CLI and library for evaluation and red teaming of LLM apps. | Regression testing, prompt/application evals, adversarial testing. | `[official]` |
| [Inspect](https://inspect.aisi.org.uk/) | UK AI Security Institute's framework for rigorous LLM evals covering coding, reasoning, agent behavior, and model-graded scoring. | Rigorous research-grade and agent-task evaluation. | `[official]` · `[benchmark]` |
| [Azure AI Evaluation SDK](https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/evaluation-approach-gen-ai) | Azure Foundry evaluation SDK with built-in agent, safety, and quality evaluators. | Enterprise agent evaluation tied to Foundry tracing. | `[official]` |

### Key Practices

- Golden datasets  
- Regression testing  
- Adversarial / red-team inputs  
- Continuous evaluation pipelines  

### Tracing and Monitoring

| Tool | Description |
|------|-------------|
| [Langfuse](https://github.com/langfuse/langfuse) | OSS LLM observability. Traces, evals, prompts. |
| [LangSmith](https://smith.langchain.com) | LangChain platform. Tracing, testing, evaluation. |
| [Braintrust](https://braintrustdata.com) | Eval-driven development. Experiment tracking. |
| [Arize Phoenix](https://github.com/Arize-ai/phoenix) | OSS AI observability. Traces, evals, embeddings. |
| [Helicone](https://github.com/Helicone/helicone) | OSS LLM observability. One-line integration. |
| [Weights and Biases Weave](https://wandb.ai/site/weave) | Trace and evaluate LLM apps. |

### Benchmarks

| Benchmark | Description | Evidence |
|-----------|-------------|----------|
| [SWE-bench](https://github.com/princeton-nlp/SWE-bench) | Coding-agent benchmark grounded in real GitHub issues and patches; `Verified` subset is the canonical agent workload. | `[official]` · `[benchmark]` |
| [AgentBench](https://github.com/THUDM/AgentBench) | 8-environment LLM agent benchmark covering OS, DB, web, and game tasks. | `[official]` · `[benchmark]` |
| [Terminal-Bench](https://terminalbench.com) | Evaluates terminal-agent execution on shell-based tasks with scored task completions. | `[official]` · `[benchmark]` |
| [GAIA](https://huggingface.co/gaia-benchmark) | General AI assistant benchmark with real-world multi-step tasks and tool use. | `[official]` · `[benchmark]` |
| [WebArena / VisualWebArena](https://github.com/web-arena-x/webarena) | Web agent benchmark on real-website snapshots; visual variant tests multimodal web agents. | `[official]` · `[benchmark]` |
| [τ-bench](https://github.com/sierra-research/tau-bench) | Tool-use + user-simulation benchmark measuring agent reliability and consistency across trials. | `[official]` · `[benchmark]` |
| [OSWorld](https://github.com/xlang-ai/OSWorld) | Computer-use benchmark for multimodal agents on real desktop OS tasks across Ubuntu/Windows/macOS; complements web-only benchmarks. | `[official]` · `[benchmark]` [paper](https://arxiv.org/abs/2404.07972) |
| [LiveCodeBench](https://livecodebench.github.io) | Contamination-resistant coding benchmark with time-stamped problems from LeetCode/AtCoder/Codeforces; complements SWE-bench's repo-issue workload. | `[official]` · `[benchmark]` [paper](https://arxiv.org/abs/2403.07974) |
| [WebVoyager](https://github.com/MinorJerry/WebVoyager) | Web-agent benchmark on live production websites (not snapshots); tests multimodal browsing under real network and UI drift conditions. | `[official]` · `[benchmark]` [paper](https://arxiv.org/abs/2401.13919) |

### Safety Risk Surfaces & Mitigations

| ⚠️ Core Risk Surfaces | 🛡️ Mitigation Strategies |
| :--- | :--- |
| Prompt injection (direct & indirect) | Input validation and filtering |
| Tool misuse | Tool permissioning and sandboxing |
| Data exfiltration | Human-in-the-loop approval gates |
| Memory poisoning | Audit logs and traceability |
| Unbounded autonomous behaviour | Policy-driven execution |

### Safety Tooling & Methodologies

| Resource | Description | Workload Suitability | Official Link |
|----------|-------------|----------|---------------|
| **garak** | LLM vulnerability scanner probing for hallucination, leakage, injection, toxicity, and jailbreaks. | Automated red teaming & vulnerability scanning | [GitHub](https://github.com/NVIDIA/garak) |
| **OWASP GenAI Security Project** | Governance and mitigation framework for safety risks in LLMs and agentic systems. | Governance, controls, and secure-design reference | [Project Home](https://genai.owasp.org/) |
| **Anthropic Alignment Stress-Testing** | Research and operational approach for deliberately stress-testing alignment evals and oversight. | Research-driven safety evaluation methodology | [Post](https://www.alignmentforum.org/posts/EPDSdXr8YbsDkgsDG/introducing-alignment-stress-testing-at-anthropic) |
| **Model Organisms of Misalignment** | In-vitro demonstrations of alignment failures so they can be studied empirically. | Advanced safety research and methodology | [Post](https://www.alignmentforum.org/posts/ChDH335ckdvpxXaXX/model-organisms-of-misalignment-the-case-for-a-new-pillar-of-1) |
| **AI Safety via Debate** | Alignment framework for cases where direct human supervision is too hard. | Alignment and scalable oversight resource | [Paper](https://arxiv.org/abs/1805.00899) |
| **Concrete Problems in AI Safety** | Foundational framing paper for safety problems (side effects, reward hacking, safe exploration, shift). | Foundational safety resource | [Paper](https://arxiv.org/abs/1606.06565) |
| **Anthropic Agentic Misalignment** | Grounds safety concerns in concrete behaviours (blackmail, espionage) in simulated settings. | Applied safety & threat-modelling reference | [Research Post](https://www.anthropic.com/research/agentic-misalignment) |

### AI Guardrails

| Tool | Description |
|------|-------------|
| [Guardrails AI](https://github.com/guardrails-ai/guardrails) | Structural, type, quality guarantees for LLM outputs. |
| [NeMo Guardrails](https://github.com/NVIDIA/NeMo-Guardrails) | NVIDIA. Programmable conversation guardrails. |
| [LLM Guard](https://github.com/protectai/llm-guard) | Security toolkit. Input/output scanning. |
| [Rebuff](https://github.com/protectai/rebuff) | Prompt injection detection. |
| [Lakera Guard](https://lakera.ai) | Real-time protection. Prompt injection, data leakage, toxicity. |

---

## 🧠 Skills and Operating Principles

> Audience: practitioners · Evidence class: field report

Building agentic systems requires a shift in skillset:

- Problem decomposition  
- System design and orchestration  
- Tool and interface design  
- Memory modelling  
- Evaluation design  
- Failure mode analysis  
- Safety and governance thinking  

---

## 🚫 What NOT to Do

> Audience: all contributors · Evidence class: mixed

To keep this repository genuinely opinionated, we advocate against these common anti-patterns:

- **Do not begin with multi-agent systems when a single agent plus tools will do.** Escalate to multi-agent only when task decomposition requires it.
- **Do not add memory before defining what deserves persistence.** Avoid "state bloat" by being intentional about what is stored and why.
- **Do not treat tracing as optional for long-running systems.** Observability is the only way to debug non-deterministic agentic failures.
- **Do not confuse benchmark wins with production readiness.** Real-world reliability requires evaluation on *your* specific data and edge cases.
- **Do not use framework abstractions as a substitute for architecture.** Understand your control flow before outsourcing it to a library.

---

## 📊 Signals (How to Read This List)

> Audience: all contributors · Evidence class: mixed

- ⭐ Production-grade  
- 🧪 Experimental  
- ⚠️ Early-stage / unstable  

---

## 🚀 Getting Started

> Audience: practitioners · Evidence class: mixed

1. Choose a core pattern (e.g. single-agent + tools)  
2. Add structured tool use  
3. Introduce evaluation early  
4. Layer in memory only when needed  
5. Expand into multi-agent systems with clear roles  
6. Add observability and safety constraints  

---

## 🤝 Contributing

> Audience: all contributors · Evidence class: mixed

Contributions are welcome! Please read the [**CONTRIBUTING.md**](CONTRIBUTING.md) for full details before submitting a pull request.

At a high level, submissions must meet the following criteria:

- Clear description of purpose  
- Architectural strengths and operational constraints  
- Governance fit and workload suitability  
- Evidence of ecosystem maturity or real-world usage (preferred)  
- Evidence tags and `Last reviewed` markers where claims are time-sensitive or likely to change

This is a **curated list**, not an exhaustive one.

See [appendix/benchmark-and-evidence-policy.md](appendix/benchmark-and-evidence-policy.md) for the sourcing, evidence-tagging, and `Last reviewed` policy.

---

## 📌 Final Note

> Audience: all contributors · Evidence class: mixed

The shift to agentic systems is not about more tools.

It is about:
- Designing systems that can **reason, act, evaluate, and improve**  
- Ensuring those systems are **reliable, observable, and safe**  

Build accordingly.
