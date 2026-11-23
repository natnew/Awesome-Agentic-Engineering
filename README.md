<div align="center">

# 🧠 Awesome Agentic Engineering

> **Stop prompting. Start engineering. A structured reference for taking AI agents into production.**

[![Awesome](https://awesome.re/badge-flat2.svg)](https://awesome.re) [![Last Commit](https://img.shields.io/github/last-commit/natnew/Awesome-Agentic-Engineering?label=last%20updated&style=flat-square)](https://github.com/natnew/Awesome-Agentic-Engineering/commits) [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com) [![License: MIT](https://img.shields.io/badge/License-MIT-lightgrey.svg?style=flat-square)](LICENSE)

A curated map of agentic AI systems — covering architectures, frameworks, memory, evaluation, and safety.

This is not a tool list. It's a structured guide to building **reliable, observable, production-grade agentic systems**, evaluated against rigorous engineering dimensions.

[Site source and publishing instructions](docs/README.md)

</div>

---

## 📑 Table of Contents

- [🏗️ Reference Architectures](#reference-architectures)
- [📐 Spec-Driven Development](#-spec-driven-development)
- [⚙️ Orchestration Frameworks](#orchestration-frameworks)
- [📡 Protocols and Standards](#-protocols-and-standards)
- [🛂 Agent Authority, Identity & Delegation](#-agent-authority-identity--delegation)
- [🧭 Reasoning & Planning Models](#-reasoning--planning-models)
- [🧪 Evaluation & Safety](#-evaluation--safety)
- [Related Projects](#related-projects)
- [🌟 Contributors](#-contributors)
- [🤝 Contributing](#-contributing)

### 📂 Appendix

- [🧱 Agentic Engineering Reference Stack](appendix/agentic-engineering-reference-stack.md)
- [🌐 Browser and Desktop Agents](appendix/browser-and-desktop-agents.md)
- [🎙 Voice Agents](appendix/voice-agents.md)
- [🎨 Creative AI](appendix/creative-ai.md)
- [💼 Customer Support and CRM Agents](appendix/customer-support-and-crm-agents.md)
- [🧠 Open-Source Models for Agents](appendix/open-source-models-for-agents.md)
- [📰 Newsletters and Communities](appendix/newsletters-and-communities.md)
- [📚 Learning Resources](appendix/learning-resources.md)
- [⚡ Fast-Moving Product Lists](appendix/fast-moving-product-lists.md)

---

<a id="reference-architectures"></a>

## 🏗️ Reference Architectures

- [DeerFlow](https://github.com/bytedance/deer-flow): Open-source orchestration system combining sub-agents, memory, and sandboxes; demonstrates workflow-oriented orchestration across agents with shared execution context. *Emerging.*
- [SWE-agent](https://github.com/SWE-agent/SWE-agent): Autonomous software-engineering system using a specialised Agent-Computer Interface (ACI); demonstrates narrow action spaces and interface design tuned for code-repair tasks. *Experimental.*
- [Proxifield](https://arxiv.org/abs/2609.20889): Multi-agent communication protocol with sparse semantic routing; demonstrates proposal, peer-reply, and action-commitment rounds, studied on simulated drone search-and-rescue and HiddenBench collective reasoning. *Research preprint.* `[official]` `[benchmark]`

---

## 📐 Spec-Driven Development

- [GitHub Spec Kit](https://github.com/github/spec-kit): Open-source toolkit for spec-driven development with agentic coding assistants (Copilot, Claude Code, Cursor, Gemini CLI). Defines the `/specify` → `/plan` → `/tasks` → `/implement` workflow used in this repo's own `specs/` directory. `[official]` [announce](https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/)
- [Kiro](https://kiro.dev): AWS IDE built around spec-driven development: specs, steering files, and hooks drive agent work from requirements through tasks. First-party reference implementation of SDD in an IDE. `[official]` [docs](https://kiro.dev/docs/) · `[official]` [launch post](https://kiro.dev/blog/introducing-kiro/)
- [OpenAI Model Spec](https://model-spec.openai.com/): First-party example of treating *model behaviour* as a versioned, public spec — objectives, rules, defaults, and conflict resolution. A reference for how to write a spec an agent can actually be aligned to. `[official]` [post](https://openai.com/index/sharing-the-latest-model-spec/)
- [AGENTS.md](https://agents.md/): Simple convention for a repository-scoped file that instructs coding agents about build, test, style, and conventions. Widely supported across agent CLIs. `[official]`
- [Anthropic Claude Skills (SKILL.md)](https://www.claude.com/skills): Declarative, self-contained skill specs (`SKILL.md`) that package instructions, tools, and examples agents can discover and load on demand. Treats individual capabilities as versioned spec artifacts. `[official]` [docs](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview)
- [Harness Handbook](https://arxiv.org/abs/2607.13285): Paper proposing behaviour-centric maps from agent-harness behaviours to source locations, with progressive disclosure for planning edits across evolving harness codebases. `[benchmark]`
- [Repo0](https://arxiv.org/abs/2608.19854): Paper proposing full-repository generation from natural-language requirements with architecture as an explicit intermediate state: a Dual-DAG aligns requirement and component graphs, evolves module boundaries under modularity metrics until convergence, then drives test-driven implementation. `[benchmark]`
- [Harness²](https://github.com/google-research/harness2): Research framework that refines an agent's harness (prompts, tools, memory, skills, subagents) per task and keeps a persistent improvement harness, with model weights fixed. Supports OpenCode and Codex executors; model-backed runs need Google Cloud configuration. Not an officially supported Google product. `[official]` [paper](https://arxiv.org/abs/2610.14224)
- [Pydantic AI](https://ai.pydantic.dev/): Python framework that makes schema-first I/O the default for LLM calls — the practical form of "typed contracts at boundaries" for agent code. `[official]`
- [Matt Pocock Skills](https://github.com/mattpocock/skills): Open-source collection of `SKILL.md` engineering skills (for example `tdd`, `to-spec`, `code-review` and `grill-me`) that install into Claude Code, Codex, Copilot, Gemini CLI and other agent CLIs. Worked example of encoding engineering workflow discipline as reusable skill specs. `[official]`
- [Awesome DESIGN.md](https://github.com/VoltAgent/awesome-design-md): Curated collection of `DESIGN.md` files, each describing a brand's design system (for example Stripe, Linear and Vercel) in a form coding agents read before generating UI. Extends the repository-file spec pattern of `AGENTS.md` to visual design. `[official]`
- [Humanizer](https://github.com/blader/humanizer): Open-source agent skill (`SKILL.md`) that rewrites text to remove patterns of AI-generated writing, based on Wikipedia's "Signs of AI writing" guide. Installs into Claude Code, Codex and other agents through the Skills CLI; states it does not aim to evade AI detectors. `[official]`

---

<a id="orchestration-frameworks"></a>

## ⚙️ Orchestration Frameworks

### Deep Dives

- [LangGraph](https://langchain-ai.github.io/langgraph/): Stateful orchestration framework building directed graphs with typed state; demonstrates deterministic execution control mixed with LLM reasoning. *Production-ready.* `[official]` · `[field report]` [LinkedIn SQL Bot](https://www.linkedin.com/blog/engineering/ai/practical-text-to-sql-for-data-analytics)
- [Microsoft Agent Framework](https://github.com/microsoft/agent-framework): Microsoft's unified agent framework merging Semantic Kernel and AutoGen, with first-class MCP and A2A support; demonstrates enterprise-grade agent composition with typed plugins, approval workflows, and Azure integration. *Production-ready.* `[official]` · `[official]` [announce](https://devblogs.microsoft.com/foundry/introducing-microsoft-agent-framework-the-open-source-engine-for-agentic-ai-apps/)
- [AutoGen](https://microsoft.github.io/autogen/): Microsoft Research multi-agent conversation framework, now an orchestration pattern inside Microsoft Agent Framework; demonstrates conversable agents with group chat, code-executor, and human-proxy patterns. *Production-ready.* `[official]` · `[benchmark]` [AutoGen paper](https://arxiv.org/abs/2308.08155)
- [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/): OpenAI's official agents SDK with handoffs, guardrails, and sessions, and the successor path to the Assistants API; demonstrates first-party multi-step agents with tool use, tracing, and structured handoffs. *Production-ready.* `[official]` [repo](https://github.com/openai/openai-agents-python)
- [CrewAI](https://docs.crewai.com/): Multi-agent collaboration framework where agents are assigned roles, goals, and tools; demonstrates role-based agentic workflows with sequential and hierarchical processes. *Emerging.* `[official]` · `[field report]` [case studies](https://www.crewai.com/case-studies)
- [LazyMind](https://github.com/LazyAGI/LazyMind): Local-first runtime that turns reusable agent skills into observable workflows with editable, versioned artifacts; demonstrates skill-derived execution with review checkpoints and step-level recovery. Public evidence is currently first-party. *Emerging.* `[official]` · `[official]` [workflow format](https://github.com/LazyAGI/LazyMind/blob/9bea30bb4aaedc3a0a1759a7e9dc03f9704e9fb7/docs/workflow-format.md) · `[official]` [releases](https://github.com/LazyAGI/LazyMind/releases)
- [Pydantic AI](https://ai.pydantic.dev/): Framework built directly on Pydantic, enforcing strict data validation and type-safe outputs from LLMs; demonstrates type-driven agentic execution and dependency injection. *Production-ready.* `[official]`
- [Smolagents](https://huggingface.co/docs/smolagents): Minimalist framework using `CodeAgents` (Python logic code generation over JSON calling); demonstrates code-first model execution bounds. *Emerging.* `[official]`

---

### Frameworks Landscape

#### General Purpose

- [LangChain](https://github.com/langchain-ai/langchain): Modular framework with chains, tools, memory, and broad integration coverage. Py/JS. `[official]`
- [LangGraph](https://github.com/langchain-ai/langgraph): Graph-based orchestration. Stateful typed-state graphs with checkpointing. Py/JS. `[official]`
- [LlamaIndex](https://github.com/run-llama/llama_index): Data-centric framework for retrieval-heavy and RAG-oriented agent systems. Py/JS. `[official]`
- [Haystack](https://github.com/deepset-ai/haystack): Pipeline-based framework for search, retrieval, and hybrid agent workflows. Py. `[official]`
- [Semantic Kernel](https://github.com/microsoft/semantic-kernel): Microsoft enterprise kernel; now a composable layer inside Microsoft Agent Framework. C#/Py/Java. `[official]`
- [Microsoft Agent Framework](https://github.com/microsoft/agent-framework): Microsoft's unified agent framework merging Semantic Kernel and AutoGen; first-class MCP and A2A support. Py/.NET. `[official]`
- [Pydantic AI](https://github.com/pydantic/pydantic-ai): Type-safe, Pydantic-native; schema-first LLM interactions with dependency injection. Py. `[official]`
- [DSPy](https://github.com/stanfordnlp/dspy): Stanford. Programming not prompting; compiler optimises prompts against metrics. Py. `[official]` · `[benchmark]`

#### Multi-Agent Orchestration

- [AutoGen](https://github.com/microsoft/autogen): Microsoft Research multi-agent conversations; v0.4 redesigned for async event-driven execution. Py. `[official]` · `[benchmark]`
- [CrewAI](https://github.com/crewAIInc/crewAI): Role-based crew members with goals, tools, and sequential/hierarchical processes. Py. `[official]`
- [OpenAI Agents SDK](https://github.com/openai/openai-agents-python): Official OpenAI multi-step agents with handoffs, guardrails, sessions, and tracing. Py. `[official]`
- [Google ADK](https://github.com/google/adk-python): Native Gemini multi-agent orchestration; deploys to Vertex AI Agent Engine. Py. `[official]`
- [MetaGPT](https://github.com/geekan/MetaGPT): PM / architect / engineer roles simulating a software company; research-oriented. Py. `[official]` · `[benchmark]`
- [CAMEL](https://github.com/camel-ai/camel): Role-based simulation and collaborative reasoning research framework. Py. `[official]` · `[benchmark]`
- [DeerFlow](https://github.com/bytedance/deer-flow): ByteDance orchestration system for planning, tools, memory, and execution. Py. `[official]`
- [AgentScope](https://github.com/modelscope/agentscope): Alibaba multi-agent framework with message-passing runtime and distributed mode. Py. `[official]`

#### Lightweight / Minimalist

- [Smolagents](https://github.com/huggingface/smolagents): HuggingFace minimal agents (~1000 lines); code-action agents with sandboxed execution. Py. `[official]`
- [Agno](https://github.com/agno-agi/agno): Lightweight, model-agnostic agent framework with native multi-modal support. Py. `[official]`
- [Upsonic](https://github.com/upsonic/upsonic): MCP-first framework with minimal setup and typed task graphs. Py. `[official]`
- [Mastra](https://github.com/mastra-ai/mastra): TypeScript-first framework with observability, workflows, and memory. TS. `[official]`

---

## 📡 Protocols and Standards

- [MCP (Model Context Protocol)](https://modelcontextprotocol.io/): Open spec. Anthropic-authored open standard for exposing tools, resources, prompts, and sampling to LLM hosts; wide multi-vendor adoption in 2025–2026. `[official]` [spec](https://modelcontextprotocol.io/specification/)
- [A2A (Agent2Agent)](https://github.com/a2aproject/A2A): Open spec. Google-originated, Linux Foundation–hosted protocol for secure cross-agent communication across vendors and frameworks. `[official]` [spec](https://a2a-protocol.org/)
- [OpenAI Function / Tool Calling](https://platform.openai.com/docs/guides/function-calling): Vendor API. Native structured tool invocation for OpenAI models; JSON-schema-typed tool definitions. `[official]`
- [Anthropic Tool Use](https://docs.anthropic.com/en/docs/build-with-claude/tool-use): Vendor API. Native structured tool invocation for Claude models; supports parallel tool calls and computer-use tools. `[official]`
- [OpenAPI](https://github.com/OAI/OpenAPI-Specification): Open spec. Industry-standard HTTP API specification; foundation for typed, discoverable tool surfaces behind MCP or direct function-calling. `[official]`

---

## 🛂 Agent Authority, Identity & Delegation

- [Bridging the AI Agent Authority Gap](https://thehackernews.com/2026/04/bridging-ai-agent-authority-gap.html): Frames AI agents as a delegated identity type whose authority originates from humans, bots, service accounts, and machine identities, and argues for governing the delegation source before the agent.
- [OWASP GenAI Security Project](https://genai.owasp.org/): Governance and threat-modelling reference for agentic systems, including excessive agency and tool-use risks.
- [Model Context Protocol](https://modelcontextprotocol.io/): Tool and context protocol. Tool access expands the authority surface of agentic systems; MCP is a primary vector for that expansion and where scoping must be applied.
- [Auth0 AI Agents / Token Vault](https://auth0.com/ai): Practical identity pattern for managing agent access to user-authorised systems with short-lived, scoped tokens.
- [NVIDIA OpenShell](https://github.com/NVIDIA/OpenShell): Out-of-process runtime policy enforcement for agent sandboxes. Enforces declarative YAML policy outside the agent process, with Landlock filesystem confinement fixed at sandbox creation, network egress policy that can be updated on a running sandbox, and process restrictions; pre-1.0, see the [docs](https://docs.nvidia.com/openshell/latest/about/why-open-shell).

---

## 🧭 Reasoning & Planning Models

- [GPT-5.4 (`gpt-5.4` / `mini` / `nano`)](https://developers.openai.com/api/docs/models/gpt-5.4): OpenAI. Tunable reasoning effort with native computer-use, web/file search, and function tools; one family covers planner, subagent/actor, and high-volume tool-calling tiers. `[official]` [model index](https://developers.openai.com/api/docs/models) · [`mini`](https://developers.openai.com/api/docs/models/gpt-5.4-mini) · [`nano`](https://developers.openai.com/api/docs/models/gpt-5.4-nano)
- [Claude Opus 4.7 / Sonnet 4.6 / Haiku 4.5](https://www.anthropic.com/system-cards): Anthropic. Configurable extended-thinking budget interleaved with tool calls; the same dial across a planner/worker/fast-actor trio. `[official]` [extended thinking](https://docs.anthropic.com/en/docs/build-with-claude/extended-thinking)
- [Gemini 3.1 Pro / 3 Flash / 3.1 Flash-Lite](https://deepmind.google/models/model-cards/): Google DeepMind. Deep Think parallel-hypothesis reasoning (Pro) and a thinking-capable Flash tier; a three-tier reasoning ladder over a long-context stack. `[official]` [Gemini 3.1 Pro card](https://deepmind.google/models/gemini/)
- [DeepSeek-R1](https://github.com/deepseek-ai/DeepSeek-R1): DeepSeek. RL-trained reasoning traces with open weights; a reproducible baseline for planner research and local agent stacks. `[official]` · `[benchmark]` [paper](https://arxiv.org/abs/2501.12948)
- [Qwen3 (thinking mode)](https://github.com/QwenLM/Qwen3): Alibaba. Open-weight family with switchable thinking and non-thinking modes, usable in both planner and actor roles. `[official]` · `[benchmark]` [tech report](https://arxiv.org/abs/2505.09388)
- [Grok 4](https://x.ai/news/grok-4): xAI. Native reasoning with tool use; a diversity source in multi-model planner ensembles. `[official]`
- [Multi-Head Latent Control](https://arxiv.org/search/?query=Multi-Head+Latent+Control%3A+A+Unified+Interface+for+LLM+Agent+Decision+Making&searchtype=title): Huawei. Dedicated latent control heads select among answering, tool use, clarification, abstention, and delegation; useful for studying where policy, escalation, and safe refusal sit in agent loops. `[benchmark]`

---

## 🧪 Evaluation & Safety

### Evaluation Frameworks

- [OpenAI Evals](https://github.com/openai/evals): Core framework for testing and improving AI systems; foundational evaluation framework and methodology. `[official]`
- [DeepEval](https://deepeval.com/docs/getting-started): Open-source LLM evaluation framework with metrics for hallucination, answer relevance, and task completion; suited to application-level evaluation and regression testing. `[official]`
- [promptfoo](https://www.promptfoo.dev/docs/intro/): CLI and library for evaluation and red teaming of LLM apps; suited to regression testing, prompt/application evals, and adversarial testing. `[official]`
- [Inspect](https://inspect.aisi.org.uk/): UK AI Security Institute's framework for rigorous LLM evals covering coding, reasoning, agent behaviour, and model-graded scoring; suited to research-grade and agent-task evaluation. `[official]` · `[benchmark]`
- [Azure AI Evaluation SDK](https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/evaluation-approach-gen-ai): Azure Foundry evaluation SDK with built-in agent, safety, and quality evaluators; suited to enterprise agent evaluation tied to Foundry tracing. `[official]`
- [ai-evaluation](https://github.com/future-agi/ai-evaluation): Open-source LLM evaluation framework with 50+ metrics, LLM-as-Judge, and guardrail scanners (jailbreak, PII, injection). `[official]`
- [agent-opt](https://github.com/future-agi/agent-opt): Prompt and agent optimisation library with six algorithms (Bayesian, ProTeGi, GEPA, and more) for iterative tuning across eval datasets. `[official]`
- [simulate-sdk](https://github.com/future-agi/simulate-sdk): Persona- and scenario-driven SDK for simulating voice and text AI agents; suited to pre-production simulation and stress testing. `[official]`
- [EvalShift](https://github.com/evalshift/evalshift-cli): Open-source CLI that replays recorded agent runs on the current and a candidate model and reports per-case tool-call and output regressions with paired statistics; suited to model-migration regression testing and CI gating of model changes. `[official]`

### Tracing and Monitoring

- [Langfuse](https://github.com/langfuse/langfuse): OSS LLM observability. Traces, evals, prompts.
- [LangSmith](https://smith.langchain.com): LangChain platform. Tracing, testing, evaluation.
- [Braintrust](https://braintrustdata.com): Eval-driven development. Experiment tracking.
- [Arize Phoenix](https://github.com/Arize-ai/phoenix): OSS AI observability. Traces, evals, embeddings.
- [Helicone](https://github.com/Helicone/helicone): OSS LLM observability. One-line integration.
- [Weights and Biases Weave](https://wandb.ai/site/weave): Trace and evaluate LLM apps.
- [traceAI](https://github.com/future-agi/traceAI): OpenTelemetry-native tracing for LLM and agent apps with 50+ framework integrations.
- [agenttrace](https://github.com/luoyuctl/agenttrace): Local-first TUI and report generator for auditing AI coding-agent session logs, token and cost usage, latency, tool failures, health, and CI regression checks.
- [Future AGI](https://github.com/future-agi/future-agi): Self-hostable end-to-end agent engineering platform with tracing, evals, guardrails, and gateway.
- [OrcaReplay](https://github.com/Continuum-AI-Corp/OrcaReplay): Records a coding-agent run below the harness, then replays it offline with no model called or forks it from a checkpoint onto another model.

### Benchmarks

- [SWE-bench](https://github.com/princeton-nlp/SWE-bench): Coding-agent benchmark grounded in real GitHub issues and patches; `Verified` subset is the canonical agent workload. `[official]` · `[benchmark]`
- [AgentBench](https://github.com/THUDM/AgentBench): 8-environment LLM agent benchmark covering OS, DB, web, and game tasks. `[official]` · `[benchmark]`
- [Terminal-Bench](https://terminalbench.com): Evaluates terminal-agent execution on shell-based tasks with scored task completions. `[official]` · `[benchmark]`
- [GAIA](https://huggingface.co/gaia-benchmark): General AI assistant benchmark with real-world multi-step tasks and tool use. `[official]` · `[benchmark]`
- [WebArena / VisualWebArena](https://github.com/web-arena-x/webarena): Web agent benchmark on real-website snapshots; visual variant tests multimodal web agents. `[official]` · `[benchmark]`
- [τ-bench](https://github.com/sierra-research/tau-bench): Tool-use + user-simulation benchmark measuring agent reliability and consistency across trials. `[official]` · `[benchmark]`
- [LLMs Get Lost in Evolving User Intent](https://github.com/microsoft/evolving-intent): Evaluates whether models track changing user intent across multi-turn conversations with argument reveals, revisions, function switches, and combined transitions; supports GSM8K, BIRD-SQL, BrowseComp+, and SWE-bench Verified. `[official]` · `[benchmark]` [paper](https://arxiv.org/abs/2607.20734)
- [OSWorld](https://github.com/xlang-ai/OSWorld): Computer-use benchmark for multimodal agents on real desktop OS tasks across Ubuntu/Windows/macOS; complements web-only benchmarks. `[official]` · `[benchmark]` [paper](https://arxiv.org/abs/2404.07972)
- [LiveCodeBench](https://livecodebench.github.io): Contamination-resistant coding benchmark with time-stamped problems from LeetCode/AtCoder/Codeforces; complements SWE-bench's repo-issue workload. `[official]` · `[benchmark]` [paper](https://arxiv.org/abs/2403.07974)
- [WebVoyager](https://github.com/MinorJerry/WebVoyager): Web-agent benchmark on live production websites (not snapshots); tests multimodal browsing under real network and UI drift conditions. `[official]` · `[benchmark]` [paper](https://arxiv.org/abs/2401.13919)
- [ClawBench](https://github.com/TIGER-AI-Lab/ClawBench): Browser-agent benchmark on live production websites with isolated runs, final-request interception, and five-layer execution evidence. `[official]` · `[benchmark]` [paper](https://arxiv.org/abs/2604.08523)
- [DataPrep-Bench](https://datapreparationbench.github.io/): Evaluates LLMs and agents on automated training-data preparation workflows, adding a data-centric workload for comparing multi-stage preparation capabilities beyond conventional task-execution benchmarks. `[official]` · `[benchmark]` [paper](https://arxiv.org/abs/2607.20465)
- [YYLO Benchmark](https://github.com/yylo-dev/yylo-benchmark): Longitudinal evaluation and immutable evidence for agent runs: private fresh-repository attempt workspaces, deterministic and LLM-judge evaluation profiles, and hash-linked receipts, manifests, and evaluator provenance. `[official]` · `[benchmark]`
- [AgentWorld](https://github.com/openagents-org/agentworld): Long-horizon multi-agent collaboration benchmark in an MMORPG sandbox: 100 human-annotated tasks plus augmented variants for 3–20 role-differentiated agents, Python success verifiers, and a causal-graph metric (CCE) measuring the share of actions that contributed to task success. `[official]` · `[benchmark]` [paper](https://arxiv.org/abs/2609.31590)
- [PerspectiveGap](https://github.com/WhymustIhaveaname/PerspectiveGap): Multi-agent orchestration prompting benchmark: 110 scenarios over 10 loop topologies test whether a model gives each sub-agent the context fragments it needs and writes role prompts without omissions or cross-role leakage, scored by a deterministic strict-pass check. `[official]` · `[benchmark]` [paper](https://arxiv.org/abs/2606.08878)
- [From Prompts to Posteriors](https://arxiv.org/abs/2610.29331): Tests whether LLM agents update beliefs as Bayes' rule prescribes; in-context updating is mostly poor, while reasoning plus code execution approaches the correct posterior. `[benchmark]`

### Safety Tooling & Methodologies

- [garak](https://github.com/NVIDIA/garak): LLM vulnerability scanner probing for hallucination, leakage, injection, toxicity, and jailbreaks.
- [OWASP GenAI Security Project](https://genai.owasp.org/): Governance and mitigation framework for safety risks in LLMs and agentic systems.
- [Anthropic Alignment Stress-Testing](https://www.alignmentforum.org/posts/EPDSdXr8YbsDkgsDG/introducing-alignment-stress-testing-at-anthropic): Research and operational approach for deliberately stress-testing alignment evals and oversight.
- [Model Organisms of Misalignment](https://www.alignmentforum.org/posts/ChDH335ckdvpxXaXX/model-organisms-of-misalignment-the-case-for-a-new-pillar-of-1): In-vitro demonstrations of alignment failures so they can be studied empirically.
- [AI Safety via Debate](https://arxiv.org/abs/1805.00899): Alignment framework for cases where direct human supervision is too hard.
- [Concrete Problems in AI Safety](https://arxiv.org/abs/1606.06565): Foundational framing paper for safety problems (side effects, reward hacking, safe exploration, shift).
- [Anthropic Agentic Misalignment](https://www.anthropic.com/research/agentic-misalignment): Grounds safety concerns in concrete behaviours (blackmail, espionage) in simulated settings.
- [Cloudflare security-audit skill](https://www.skills.sh/cloudflare/security-audit-skill): Agent skill for security audits, listed under the `cloudflare` namespace and installed with `npx skills add cloudflare/security-audit-skill`.

### AI Guardrails

- [Guardrails AI](https://github.com/guardrails-ai/guardrails): Structural, type, quality guarantees for LLM outputs.
- [NeMo Guardrails](https://github.com/NVIDIA/NeMo-Guardrails): NVIDIA. Programmable conversation guardrails.
- [LLM Guard](https://github.com/protectai/llm-guard): Security toolkit. Input/output scanning.
- [Rebuff](https://github.com/protectai/rebuff): Prompt injection detection.
- [Lakera Guard](https://lakera.ai): Real-time protection. Prompt injection, data leakage, toxicity.

---

## Related Projects

- [Awesome Physical AI](https://github.com/natnew/Awesome-Physical-AI) — Robotics, embodied AI, and physical-world agent systems.
- [Awesome Agentic AI Security](https://github.com/natnew/Awesome-Agentic-AI-Security) — Security research, threat models, defenses, and governance for agentic AI systems.
- [Awesome AI Scientists](https://github.com/natnew/Awesome-AI-Scientists) — AI scientist systems for literature intelligence, hypothesis generation, experiment planning, tool use, evaluation, and scientific communication.

---

## 🌟 Contributors

<div align="center">

Thank you to everyone who has added a resource to this list. 📚 marks a contributed resource; select it to see what was added.

<table>
  <tr>
    <td align="center" width="33%">
      <a href="https://github.com/SuhaniNagpal7"><img src="https://github.com/SuhaniNagpal7.png?size=160" width="80" height="80" alt="Suhani Nagpal"><br><sub><b>Suhani Nagpal</b></sub></a><br>
      <a href="https://github.com/natnew/Awesome-Agentic-Engineering/commit/cd9bd1dfd96decfde7a87c40c5892a66e5eedf5d" title="Added Future AGI products to Evaluation, Tracing &amp; Monitoring, and AI Guardrails">📚</a>
    </td>
    <td align="center" width="33%">
      <a href="https://github.com/reacher-z"><img src="https://github.com/reacher-z.png?size=160" width="80" height="80" alt="reacher-z"><br><sub><b>reacher-z</b></sub></a><br>
      <a href="https://github.com/natnew/Awesome-Agentic-Engineering/pull/28" title="Added ClawBench to agent benchmarks">📚</a>
    </td>
    <td align="center" width="33%">
      <a href="https://github.com/InsightFactoryAPP"><img src="https://github.com/InsightFactoryAPP.png?size=160" width="80" height="80" alt="InsightFactoryAPP"><br><sub><b>InsightFactoryAPP</b></sub></a><br>
      <a href="https://github.com/natnew/Awesome-Agentic-Engineering/pull/34" title="Added YYLO Benchmark to Evaluation &amp; Safety benchmarks">📚</a>
    </td>
  </tr>
  <tr>
    <td align="center" width="33%">
      <a href="https://github.com/xizhuomengcontin"><img src="https://github.com/xizhuomengcontin.png?size=160" width="80" height="80" alt="xizhuomengcontin"><br><sub><b>xizhuomengcontin</b></sub></a><br>
      <a href="https://github.com/natnew/Awesome-Agentic-Engineering/pull/36" title="Added OrcaReplay to Tracing and Monitoring">📚</a>
    </td>
    <td align="center" width="33%">
      <a href="https://github.com/roli-lpci"><img src="https://github.com/roli-lpci.png?size=160" width="80" height="80" alt="Roli Bosch"><br><sub><b>Roli Bosch</b></sub></a><br>
      <a href="https://github.com/natnew/Awesome-Agentic-Engineering/pull/38" title="Added Hermeneutic to Memory Systems">📚</a>
    </td>
    <td align="center" width="33%">
      <a href="https://github.com/louis030195"><img src="https://github.com/louis030195.png?size=160" width="80" height="80" alt="Louis Beaumont"><br><sub><b>Louis Beaumont</b></sub></a><br>
      <a href="https://github.com/natnew/Awesome-Agentic-Engineering/pull/39" title="Added Hyperconsciousness to Memory Systems">📚</a>
    </td>
  </tr>
  <tr>
    <td align="center" width="33%">
      <a href="https://github.com/WhymustIhaveaname"><img src="https://github.com/WhymustIhaveaname.png?size=160" width="80" height="80" alt="WhymustIhaveaname"><br><sub><b>WhymustIhaveaname</b></sub></a><br>
      <a href="https://github.com/natnew/Awesome-Agentic-Engineering/pull/48" title="Added PerspectiveGap to Evaluation &amp; Safety benchmarks">📚</a>
    </td>
    <td align="center" width="33%">
      <a href="https://github.com/pranshuchittora"><img src="https://github.com/pranshuchittora.png?size=160" width="80" height="80" alt="pranshuchittora"><br><sub><b>pranshuchittora</b></sub></a><br>
      <a href="https://github.com/natnew/Awesome-Agentic-Engineering/pull/51" title="Added agent-qa to Browser and Desktop Agents">📚</a>
    </td>
    <td align="center" width="33%">
      <a href="https://github.com/NicoYang1984"><img src="https://github.com/NicoYang1984.png?size=160" width="80" height="80" alt="NicoYang1984"><br><sub><b>NicoYang1984</b></sub></a><br>
      <a href="https://github.com/natnew/Awesome-Agentic-Engineering/pull/52" title="Added LazyMind to Orchestration Frameworks">📚</a>
    </td>
  </tr>
</table>

Add a resource and your profile picture lands here. See the [contributing guide](CONTRIBUTING.md) to get started.

</div>

---

<div align="center">

## 🤝 Contributing

<img src="assets/github/contributors-banner.png" alt="We love Contributors" width="720">

Thrilled to have you here.<br>
Whether it's a quick typo fix, a fresh resource,<br>
a doc polish, or a sweeping overhaul — every contribution helps this list grow.<br>
Jump in and join the community — PRs of every size are welcome.

📝 [Read the contributing guide](CONTRIBUTING.md) · 🐛 [good first issues](https://github.com/natnew/Awesome-Agentic-Engineering/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22)

</div>
