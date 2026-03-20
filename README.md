# 🧠 Awesome Agentic Engineering

> **Stop prompting. Start engineering. The definitive blueprint for taking AI agents to production.**

[![Awesome](https://awesome.re/badge-flat2.svg)](https://awesome.re) [![Stars](https://img.shields.io/github/stars/natnew/Awesome-Agentic-Engineering?style=flat-square&color=yellow)](https://github.com/natnew/Awesome-Agentic-Engineering/stargazers) [![Last Update](https://img.shields.io/badge/last%20update-March%202026-blue?style=flat-square)]() [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com) [![License: MIT](https://img.shields.io/badge/License-MIT-lightgrey.svg?style=flat-square)](LICENSE)

A curated map of agentic AI systems — covering architectures, frameworks, memory, evaluation, and safety.

This is not a list of tools.

It is a structured guide to building **reliable, observable, and production-grade agentic systems**.

---

## 📑 Table of Contents

- [🧭 Thesis](#-thesis)
- [🧩 Core Agentic Patterns](#-core-agentic-patterns)
- [⚖️ Architecture Decision Guide](#️-architecture-decision-guide)
- [🏗️ Reference Architectures](#-reference-architectures)
- [🧠 Memory Systems](#-memory-systems)
- [⚙️ Orchestration Frameworks](#-orchestration-frameworks)
- [📡 Protocols and Standards](#-protocols-and-standards)
- [🧪 Evaluation & Reliability](#-evaluation-reliability)
- [🛡️ Safety, Red Teaming & Alignment Stress-Testing](#-safety-red-teaming-alignment-stress-testing)
- [📊 Signals (How to Read This List)](#-signals-how-to-read-this-list)
- [🧠 Agentic Engineering Skills](#-agentic-engineering-skills)
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

## 🧩 Core Agentic Patterns

These patterns underpin most production-grade agentic systems.

| Pattern | Description | Key Characteristic |
| :--- | :--- | :--- |
| **Single-Agent + Tool Use** | One reasoning loop with structured tool invocation | Best for focused tasks with bounded scope |
| **Supervisor / Router Agents** | Central agent delegates tasks to specialised agents | Enables modularity and scalability |
| **Multi-Agent Collaboration** | Agents operate in parallel or sequence | Patterns: debate, critique, planning/execution split |
| **Reflection / Critique Loops** | Agents evaluate and refine their own outputs | Improves reliability over multiple iterations |
| **Retrieval-Augmented Agents** | External knowledge via vector search or APIs | Reduces hallucination and improves grounding |
| **Event-Driven / Long-Running Agents** | Persistent agents reacting to triggers over time | Requires memory, state, and orchestration |

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

## 🏗️ Reference Architectures

Representative system designs for real-world use.

| 🏗️ Architecture | 📖 Description | 🟢 Strengths | 🔴 Weaknesses | 🎯 Use Cases |
| :--- | :--- | :--- | :--- | :--- |
| **DeerFlow**<br>*(Emerging)* | Open-source super agent harness orchestrating sub-agents, memory, and sandboxes.<br><br>***Demonstrates:*** Workflow-oriented orchestration and the composition of sub-agents with memory. A fuller “agent system”. | • Strong system-level example<br>• Helpful reference for memory + sandbox + skills composition<br>• Better architectural signal than minimal repos | • Higher complexity than most teams need initially<br>• Heavier operational surface<br>• Less suitable as a first learning path | **Best for:** Teams studying full-stack agent architectures, compound research/coding workflows.<br><br>**Avoid if:** You only need lightweight orchestration or your workflow does not justify sub-agents. |
| **SWE-agent**<br>*(Experimental)* | Autonomous SWE system using a specialized Agent-Computer Interface (ACI).<br><br>***Demonstrates:*** AI-native abstractions improving execution accuracy. | • Streamlined command space<br>• SOTA on SWE-bench<br>• Compressed history processor | • Benchmark-tailored<br>• High token cost & long fix latency | **Best for:** Isolated PRs, self-contained bug fixes.<br><br>**Avoid if:** Enterprise refactoring, lacking standard build tools. |

---

## 🧠 Memory Systems

Memory is a first-class concern in agentic systems.

| 🧠 Types of Memory | 🔑 Key Concepts | 🛠️ Tooling |
| :--- | :--- | :--- |
| • **Episodic:** task-specific history<br>• **Procedural:** reusable skills and behaviours<br>• **Semantic:** embedded knowledge (vector DBs) | • Context window management<br>• Memory retrieval strategies<br>• Semantic caching<br>• Memory pruning and decay<br>• Cross-agent memory sharing | • Vector databases (FAISS, Weaviate, Pinecone)<br>• Redis / KV stores for fast state<br>• Emerging standards (e.g. MCP) |

---

## ⚙️ Orchestration Frameworks

### Deep Dives 

| ⚙️ Framework | 📖 Description | 🟢 Strengths | 🔴 Weaknesses | 🎯 Use Cases |
| :--- | :--- | :--- | :--- | :--- |
| **LangGraph**<br>*(Production-ready)* | Stateful orchestration (DAG-based). | • Explicit state management<br>• Complex workflows | • Verbosity<br>• Learning curve | **Best for:** Multi-step, stateful agent systems. |
| **CrewAI**<br>*(Emerging)* | Multi-agent collaboration framework. | • Simple mental model<br>• Fast setup | • Limited control for complex systems | **Best for:** Rapid prototyping of agent teams. |
| **OpenAI Assistants / Agents APIs**<br>*(Production-ready)* | Hosted orchestration. | • Integrated tools<br>• Simplicity | • Limited transparency and control | **Best for:** Managed environments. |
| **Pydantic AI**<br>*(Production-ready)* | Framework built directly on Pydantic enforcing strict data validation & type-safe outputs from LLMs. | • Type-system integration<br>• Type-safe dependency injection<br>• Auto-retry loops | • Nascent ecosystem vs others<br>• Loop retries can spike costs | **Best for:** Production systems needing strict type safety & predictable parsing.<br><br>**Avoid if:** Tasks are mostly open-ended generative writing. |
| **Smolagents**<br>*(Emerging)* | Minimalist framework using `CodeAgents` (Python logic code generation over JSON calling). | • Extremely lightweight (~1k LOC)<br>• Code-first native execution bounds | • Sandbox escape & SSRF risks<br>• Weak typed-state enforcement | **Best for:** Fast prototyping & pure Python logic preference.<br><br>**Avoid if:** Building regulated enterprise networks needing tight security. |

---

### Frameworks Landscape

#### General Purpose
| Framework | Lang | Description |
|-----------|------|-------------|
| [LangChain](https://github.com/langchain-ai/langchain) | Py/JS | Most adopted. Modular architecture, memory, tools. |
| [LangGraph](https://github.com/langchain-ai/langgraph) | Py/JS | Graph-based orchestration. Stateful directed graphs. |
| [LlamaIndex](https://github.com/run-llama/llama_index) | Py/JS | Data-focused. Best for RAG agents. |
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
| [DeerFlow](https://github.com/bytedance/deer-flow) | Py | ByteDance. No.1 GitHub Trending Feb 2026. 25k+ stars. |

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
| [MCP (Model Context Protocol)](https://github.com/modelcontextprotocol) | Anthropic open standard. "USB-C for AI." Industry standard for tools. |
| [A2A (Agent-to-Agent)](https://github.com/google/A2A) | Google protocol for inter-agent communication. |
| [OpenAI Function Calling](https://platform.openai.com/docs/guides/function-calling) | OpenAI native tool-use. JSON schema. |
| [Tool Use (Anthropic)](https://docs.anthropic.com/en/docs/build-with-claude/tool-use) | Claude native tool-use. Structured JSON. |
| [OpenAPI](https://github.com/OAI/OpenAPI-Specification) | Industry-standard API spec. Foundation for agent tools. |

---

## 🧪 Evaluation & Reliability

This section covers frameworks and operational tooling for testing agent quality, correctness, task completion, regressions, and system behaviour. 

### Core Areas

- Output correctness  
- Reasoning quality  
- Tool-use accuracy  
- Latency and cost  
- Robustness under adversarial input  

### Evaluation Frameworks
| Framework | Description | Methodology / Best Fit |
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
| [SWE-bench](https://github.com/princeton-nlp/SWE-bench) | Industry standard for coding agents. Top: 80.9% (Opus). |
| [AgentBench](https://github.com/THUDM/AgentBench) | 8-environment LLM agent benchmark. |
| [Terminal-Bench](https://terminalbench.com) | Terminal agent performance. GPT-5.3 leads at 77.3%. |
| [GAIA](https://huggingface.co/gaia-benchmark) | General AI Assistant. Real-world tasks. |
| [WebArena](https://github.com/web-arena-x/webarena) | Web agent benchmark. Real websites. |

---

## 🛡️ Safety, Red Teaming & Alignment Stress-Testing

This section covers security scanning, red teaming, policy testing, misalignment research, and structured safety frameworks. 

### Core Risk Surfaces & Mitigations

| ⚠️ Core Risk Surfaces | 🛡️ Mitigation Strategies |
| :--- | :--- |
| Prompt injection (direct & indirect) | Input validation and filtering |
| Tool misuse | Tool permissioning and sandboxing |
| Data exfiltration | Human-in-the-loop approval gates |
| Memory poisoning | Audit logs and traceability |
| Unbounded autonomous behaviour | Policy-driven execution |

### Tooling, Frameworks & Methodologies
| Resource | Description | Best Fit | Official Link |
|----------|-------------|----------|---------------|
| **garak** | LLM vulnerability scanner probing for hallucination, leakage, injection, toxicity, and jailbreaks. | Automated red teaming & vulnerability scanning | [GitHub](https://github.com/NVIDIA/garak) |
| **OWASP GenAI Security Project** | Governance and mitigation framework for safety risks in LLMs and agentic systems. | Governance, controls, and secure-design reference | [Project Home](https://genai.owasp.org/) |
| **Anthropic Alignment Stress-Testing** | Research and operational approach for deliberately stress-testing alignment evals and oversight. | Research-driven safety evaluation methodology | [Post](https://www.alignmentforum.org/posts/EPDSdXr8YbsDkgsDG/introducing-alignment-stress-testing-at-anthropic) |
| **Model Organisms of Misalignment** | In-vitro demonstrations of alignment failures so they can be studied empirically. | Advanced safety research and methodology | [Post](https://www.alignmentforum.org/posts/ChDH335ckdvpxXaXX/model-organisms-of-misalignment-the-case-for-a-new-pillar-of-1) |
| **AI Safety via Debate** | Alignment framework for cases where direct human supervision is too hard. | Alignment and scalable oversight resource | [Paper](https://arxiv.org/abs/1805.00899) |
| **Concrete Problems in AI Safety** | Foundational framing paper for safety problems (side effects, reward hacking, safe exploration, shift). | Foundational safety resource | [Paper](https://arxiv.org/abs/1606.06565) |
| **Anthropic Agentic Misalignment** | Grounds safety concerns in concrete behaviours (blackmail, espionage) in simulated settings. | Applied safety & threat-modelling reference | [Research Post](https://www.anthropic.com/research/agentic-misalignment) |

### AI Safety and Guardrails
| Tool | Description |
|------|-------------|
| [Guardrails AI](https://github.com/guardrails-ai/guardrails) | Structural, type, quality guarantees for LLM outputs. |
| [NeMo Guardrails](https://github.com/NVIDIA/NeMo-Guardrails) | NVIDIA. Programmable conversation guardrails. |
| [LLM Guard](https://github.com/protectai/llm-guard) | Security toolkit. Input/output scanning. |
| [Rebuff](https://github.com/protectai/rebuff) | Prompt injection detection. |
| [Lakera Guard](https://lakera.ai) | Real-time protection. Prompt injection, data leakage, toxicity. |

---

## 📊 Signals (How to Read This List)

- ⭐ Production-grade  
- 🧪 Experimental  
- ⚠️ Early-stage / unstable  

---

## 🧠 Agentic Engineering Skills

Building agentic systems requires a shift in skillset:

- Problem decomposition  
- System design and orchestration  
- Tool and interface design  
- Memory modelling  
- Evaluation design  
- Failure mode analysis  
- Safety and governance thinking  

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
- Strengths and weaknesses  
- When to use / when not to use  
- Evidence of real-world usage (preferred)  

This is a **curated list**, not an exhaustive one.

---

## 📌 Final Note

The shift to agentic systems is not about more tools.

It is about:
- Designing systems that can **reason, act, evaluate, and improve**  
- Ensuring those systems are **reliable, observable, and safe**  

Build accordingly.