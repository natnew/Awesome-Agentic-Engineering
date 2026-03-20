# 🧠 Awesome Agentic Engineering

> **Stop prompting. Start engineering. A structured reference for taking AI agents into production.**

[![Awesome](https://awesome.re/badge-flat2.svg)](https://awesome.re) [![Last Update](https://img.shields.io/badge/last%20update-March%202026-blue?style=flat-square)]() [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com) [![License: MIT](https://img.shields.io/badge/License-MIT-lightgrey.svg?style=flat-square)](LICENSE)

A curated map of agentic AI systems — covering architectures, frameworks, memory, evaluation, and safety.

This is not a list of tools.

We reject "tool list energy." It is a structured guide to building **reliable, observable, and production-grade agentic systems**, rigorously evaluated against engineering dimensions.

---

## 📑 Table of Contents

- [🧭 Thesis](#-thesis)
- [⚖️ Architecture Decision Guide](#️-architecture-decision-guide)
- [🧩 Core Agentic Patterns](#-core-agentic-patterns)
- [🏗️ Reference Architectures](#-reference-architectures)
- [🧠 Memory Systems](#-memory-systems)
- [📊 Formal Evaluation Rubric](#-formal-evaluation-rubric)
- [⚙️ Orchestration Frameworks](#-orchestration-frameworks)
- [📡 Protocols and Standards](#-protocols-and-standards)
- [🧪 Evaluation & Safety](#-evaluation--safety)
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

| 📈 The Shift (Agentic systems are moving to) | 📉 The Challenge (Implementations suffer from) | 🎯 Our Focus (This repository prioritises) |
| :--- | :--- | :--- |
| • Stateful, multi-step reasoning<br>• Multi-agent collaboration & orchestration<br>• Feedback-driven learning loops<br>• Tool-augmented execution environments | • Fragility under iteration<br>• Poor observability & evaluation<br>• Weak memory & context management<br>• Limited safety & governance | • **Reliability** over novelty<br>• **Evaluation** over intuition<br>• **Architecture** over tooling<br>• **Systems thinking** over prompt engineering |

---

## ⚖️ Architecture Decision Guide

| If your task is... | Start with... | Escalate to... | Avoid... |
| :--- | :--- | :--- | :--- |
| **bounded, tool-using, low-risk** | single-agent + tools | typed state, retries | multi-agent teams |
| **long-running, inspectable, enterprise** | graph/workflow orchestration | approval gates, persistence | opaque emergent loops |
| **open-ended research** | planner/executor or supervisor | critique loops, memory | rigid pipelines only |
| **high-reliability extraction** | prompt chains + strict schemas | validator feedback loops | unconstrained conversational agents |
| **complex parallel execution** | modular multi-agent setups | shared workspace/memory | treating LLMs as deterministic |

---

## 🧩 Core Agentic Patterns

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

Representative system designs for real-world use.

| Architecture | Ecosystem Maturity | Description | Architectural Strengths | Operational Constraints | Workload Suitability | Design Paradigm | Governance Fit |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **DeerFlow** | *Emerging* | **Is:** Open-source orchestration system combining sub-agents, memory, and sandboxes.<br>**Demonstrates:** Workflow-oriented orchestration across agents with shared execution context. | Strong system-level reference for memory, sandbox, and skills composition. | Higher setup complexity and a heavier runtime surface than most teams need initially. | Strong fit for compound research/coding workflows and teams studying full-stack agent architectures. Poor fit for lightweight orchestration or narrowly scoped tasks. | Hierarchical multi-agent orchestration. | Requires explicit sandbox policy, tool boundaries, and operator oversight before untrusted code execution. |
| **SWE-agent** | *Experimental* | **Is:** Autonomous SWE system using a specialized Agent-Computer Interface (ACI).<br>**Demonstrates:** Narrow action spaces and interface design tuned for code-repair tasks. | Streamlined command space, compressed history handling, and a clear task boundary for patch workflows. | Benchmark-oriented design, high token cost, and long end-to-end fix latency on larger tasks. | Strong fit for isolated PRs and self-contained bug fixes. Poor fit for broad refactors or environments without standard build tooling. | Single agent with a highly specialized action space (ACI). | Needs tight repository scoping, review gates, and execution controls to reduce silent code regressions. |

---

## 🧠 Memory Systems

Memory is a first-class concern in agentic systems. Rather than treating memory as a simple array of previous messages, production systems require structured approaches to state, persistence, and retrieval.

### Memory Taxonomy

Different types of memory serve distinct functional roles in an agentic architecture:

| Type | Definition | Implementation Examples |
| :--- | :--- | :--- |
| **Working Memory** (Thread State) | Short-term context for the current execution loop or active conversation thread. Ephemeral. | Context window, LangGraph `State`, in-memory message lists. |
| **Episodic Memory** | Autobiographical history of past actions, inputs, and outcomes. Enables reflection on past mistakes. | Checkpoint logs, event stores, prompt / trajectory histories. |
| **Procedural Memory** | Reusable skills, system prompts, and tool configurations. Defines *how* the agent operates. | Static configuration, retrieved skill libraries, GitHub workflows. |
| **Semantic Memory** | Embedded, factual knowledge about the world, the user, or the domain. Defines *what* the agent knows. | Vector databases (FAISS, Pinecone), knowledge graphs, Letta core memory. |

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

---

## 📊 Formal Evaluation Rubric

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

## ⚙️ Orchestration Frameworks

### Deep Dives

| Framework | Ecosystem Maturity | Description | Architectural Strengths | Operational Constraints | Workload Suitability | Design Paradigm | Governance Fit |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **LangGraph** | *Production-ready* | **Is:** Stateful orchestration framework building directed acyclic graphs (DAGs).<br>**Demonstrates:** Deterministic execution control mixed with LLM reasoning. | Explicit state management, persistence, and support for complex multi-actor workflows. | Verbose abstractions, steep learning curve, and graph sprawl if the workflow is over-modeled. | Strong fit for multi-step, stateful, and interruptible agent systems. Poor fit for simple single-prompt completions or linear chains. | DAG-based state machine. | Good fit for auditable workflows and approval gates, but graph edges must be tightly constrained to avoid runaway loops. |
| **CrewAI** | *Emerging* | **Is:** Multi-agent collaboration framework where agents are assigned roles, goals, and tools.<br>**Demonstrates:** Role-based agentic workflows. | Simple mental model and fast team-based decomposition for prototypes. | Less control for highly complex or non-standard systems. | Strong fit for rapid prototyping of agent teams. Poor fit for deterministic execution, rigorous type safety, or custom orchestration loops. | Role-based sequential or hierarchical process execution. | Requires added guardrails and observability to manage emergent loops and inconsistent agent behaviour. |
| **OpenAI Assistants / Agents APIs** | *Production-ready* | **Is:** Hosted orchestration and state management by OpenAI.<br>**Demonstrates:** Managed state and tool execution. | Integrated tools, simplified operations, and reduced infrastructure ownership. | Limited transparency and control, with strong provider coupling. | Strong fit for managed environments and teams optimizing for delivery speed. Poor fit for provider portability, local models, or complex multi-agent setups. | Hosted black-box orchestration. | Viable for hosted approval flows, but bounded by vendor policy, uptime, and data-handling constraints. |
| **Pydantic AI** | *Production-ready* | **Is:** Framework built directly on Pydantic enforcing strict data validation and type-safe outputs from LLMs.<br>**Demonstrates:** Type-driven agentic execution and dependency injection. | Strong type-system integration, schema enforcement, dependency injection, and retry support. | Smaller surrounding ecosystem than older orchestration stacks; retry loops can increase latency and cost. | Strong fit for production systems needing strict type safety and predictable parsing. Poor fit for open-ended generative writing or weakly structured tasks. | Strongly typed, schema-first LLM interactions. | Good fit where schema validation and dependency control matter, but retry policies need explicit cost and failure bounds. |
| **Smolagents** | *Emerging* | **Is:** Minimalist framework using `CodeAgents` (Python logic code generation over JSON calling).<br>**Demonstrates:** Code-first model execution bounds. | Lightweight core and direct execution model that stays close to Python control flow. | Weak typed-state enforcement and high exposure if generated code runs with broad permissions. | Strong fit for fast prototyping and Python-native experimentation. Poor fit for regulated networks or systems that need strict sandboxing and observability. | Python-native logic execution via LLM generation. | Requires strong sandboxing, network controls, and review boundaries before production use. |

---

### Frameworks Landscape

#### General Purpose
| Framework | Lang | Description |
|-----------|------|-------------|
| [LangChain](https://github.com/langchain-ai/langchain) | Py/JS | Modular framework with chains, tools, memory, and broad integration coverage. |
| [LangGraph](https://github.com/langchain-ai/langgraph) | Py/JS | Graph-based orchestration. Stateful directed graphs. |
| [LlamaIndex](https://github.com/run-llama/llama_index) | Py/JS | Data-centric framework for retrieval-heavy and RAG-oriented agent systems. |
| [Haystack](https://github.com/deepset-ai/haystack) | Py | Pipeline-based. Search and retrieval. |
| [Semantic Kernel](https://github.com/microsoft/semantic-kernel) | C#/Py/Java | Microsoft enterprise. Azure integration. |
| [Pydantic AI](https://github.com/pydantic/pydantic-ai) | Py | Type-safe. Clean Pythonic API. Production-ready. |
| [DSPy](https://github.com/stanfordnlp/dspy) | Py | Stanford. Programming not prompting. Auto-optimizes. |
| [Mastra](https://github.com/mastra-ai/mastra) | TS | TypeScript-first. Observational Memory. Apache 2.0. |
| [Anthropic SDK](https://github.com/anthropics/anthropic-sdk-python) | Py/TS | Official Claude SDK. Tool use, computer control, streaming. |

#### Multi-Agent Orchestration
| Framework | Lang | Description |
|-----------|------|-------------|
| [AutoGen](https://github.com/microsoft/autogen) | Py | Microsoft multi-agent conversations. |
| [CrewAI](https://github.com/crewAIInc/crewAI) | Py | Role-based crew members with goals and tools. |
| [MetaGPT](https://github.com/geekan/MetaGPT) | Py | PM, architect, engineer roles. Software company sim. |
| [OpenAI Agents SDK](https://github.com/openai/openai-agents-python) | Py | Official. Multi-step agents with handoffs. |
| [Google ADK](https://github.com/google/adk-python) | Py | Native Gemini. Multi-agent orchestration. |
| [Strands Agents](https://github.com/strands-agents/sdk-python) | Py | AWS-backed. Model-driven tool use. |
| [CAMEL](https://github.com/camel-ai/camel) | Py | Role-based simulation. Collaborative reasoning. |
| [AutoGPT](https://github.com/Significant-Gravitas/AutoGPT) | Py | Pioneer. Now full platform with visual builder. |
| [AgentScope](https://github.com/modelscope/agentscope) | Py | Alibaba multi-agent framework. |
| [DeerFlow](https://github.com/bytedance/deer-flow) | Py | ByteDance orchestration system for planning, tools, memory, and execution. |

#### Lightweight / Minimalist
| Framework | Lang | Description |
|-----------|------|-------------|
| [Smolagents](https://github.com/huggingface/smolagents) | Py | HuggingFace minimal agents. ~1000 lines. |
| [Agno](https://github.com/agno-agi/agno) | Py | Lightweight, model-agnostic. |
| [Upsonic](https://github.com/upsonic/upsonic) | Py | MCP support. Minimal setup. |
| [Portia AI](https://github.com/portia-ai/portia-sdk-python) | Py | Reliable agents in production. |
| [MicroAgent](https://github.com/aymenfurter/microagent) | Py | Self-editing prompts and code. |

---

## 📡 Protocols and Standards

| Protocol | Description |
|----------|-------------|
| [MCP (Model Context Protocol)](https://github.com/modelcontextprotocol) | Open standard for exposing tools, memory, and file systems to agents. |
| [A2A (Agent-to-Agent)](https://github.com/google/A2A) | Google protocol for inter-agent communication. |
| [OpenAI Function Calling](https://platform.openai.com/docs/guides/function-calling) | OpenAI native tool-use. JSON schema. |
| [Tool Use (Anthropic)](https://docs.anthropic.com/en/docs/build-with-claude/tool-use) | Claude native tool-use. Structured JSON. |
| [OpenAPI](https://github.com/OAI/OpenAPI-Specification) | Industry-standard API spec. Foundation for agent tools. |

---

## 🧪 Evaluation & Safety

This section covers frameworks and operational tooling for testing agent quality, correctness, task completion, regressions, and system behaviour, as well as security scanning, red teaming, policy testing, and misalignment research.

### Core Evaluation Areas

- Output correctness  
- Reasoning quality  
- Tool-use accuracy  
- Latency and cost  
- Robustness under adversarial input  

### Evaluation Frameworks
| Framework | Description | Methodology / Workload Suitability |
|-----------|-------------|------------------------|
| [OpenAI Evals](https://developers.openai.com/api/docs/guides/evals/) | Core framework for testing and improving AI systems. | Foundational evaluation framework and methodology. |
| [DeepEval](https://deepeval.com/docs/getting-started) | Dedicated open-source LLM evaluation framework with metrics for hallucination, answer relevance, task completion, etc. | Application-level evaluation and regression testing. |
| [promptfoo](https://www.promptfoo.dev/docs/intro/) | CLI and library for evaluation and red teaming of LLM apps. | Regression testing, prompt/application evals, adversarial testing. |
| [Inspect](https://inspect.aisi.org.uk/) | UK AI Security Institute's framework for rigorous LLM evals covering coding, reasoning, agent behavior, and model-graded scoring. | Rigorous research-grade and agent-task evaluation. |

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
| Benchmark | Description |
|-----------|-------------|
| [SWE-bench](https://github.com/princeton-nlp/SWE-bench) | Coding-agent benchmark grounded in real GitHub issues and patches. |
| [AgentBench](https://github.com/THUDM/AgentBench) | 8-environment LLM agent benchmark. |
| [Terminal-Bench](https://terminalbench.com) | Evaluates terminal-agent execution on shell-based tasks. |
| [GAIA](https://huggingface.co/gaia-benchmark) | General AI Assistant. Real-world tasks. |
| [WebArena](https://github.com/web-arena-x/webarena) | Web agent benchmark. Real websites. |

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

To keep this repository genuinely opinionated, we advocate against these common anti-patterns:

- **Do not begin with multi-agent systems when a single agent plus tools will do.** Escalate to multi-agent only when task decomposition requires it.
- **Do not add memory before defining what deserves persistence.** Avoid "state bloat" by being intentional about what is stored and why.
- **Do not treat tracing as optional for long-running systems.** Observability is the only way to debug non-deterministic agentic failures.
- **Do not confuse benchmark wins with production readiness.** Real-world reliability requires evaluation on *your* specific data and edge cases.
- **Do not use framework abstractions as a substitute for architecture.** Understand your control flow before outsourcing it to a library.

---

## 📊 Signals (How to Read This List)

- ⭐ Production-grade  
- 🧪 Experimental  
- ⚠️ Early-stage / unstable  

---

## 🚀 Getting Started

1. Choose a core pattern (e.g. single-agent + tools)  
2. Add structured tool use  
3. Introduce evaluation early  
4. Layer in memory only when needed  
5. Expand into multi-agent systems with clear roles  
6. Add observability and safety constraints  

---

## 🤝 Contributing

Contributions are welcome! Please read the [**CONTRIBUTING.md**](CONTRIBUTING.md) for full details before submitting a pull request.

At a high level, submissions must meet the following criteria:

- Clear description of purpose  
- Architectural strengths and operational constraints  
- Governance fit and workload suitability  
- Evidence of ecosystem maturity or real-world usage (preferred)  

This is a **curated list**, not an exhaustive one.

---

## 📌 Final Note

The shift to agentic systems is not about more tools.

It is about:
- Designing systems that can **reason, act, evaluate, and improve**  
- Ensuring those systems are **reliable, observable, and safe**  

Build accordingly.
