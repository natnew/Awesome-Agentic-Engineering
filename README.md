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
- [🏗️ Reference Architectures](#️-reference-architectures)
- [🧠 Memory Systems](#-memory-systems)
- [⚙️ Orchestration Frameworks](#️-orchestration-frameworks)
- [🖥 Coding Agents](#-coding-agents)
- [🌐 Browser and Desktop Agents](#-browser-and-desktop-agents)
- [🎙 Voice Agents](#-voice-agents)
- [🎨 Creative AI](#-creative-ai)
- [⚡ Task and Workflow Agents](#-task-and-workflow-agents)
- [💼 Customer Support and CRM Agents](#-customer-support-and-crm-agents)
- [📊 Data and Research Agents](#-data-and-research-agents)
- [🏠 Local and Self-Hosted AI](#-local-and-self-hosted-ai)
- [🤖 Multi-Agent Platforms](#-multi-agent-platforms)
- [📡 Protocols and Standards](#-protocols-and-standards)
- [🧪 Evaluation & Reliability](#-evaluation--reliability)
- [🛡️ Safety, Red Teaming & Alignment Stress-Testing](#️-safety-red-teaming--alignment-stress-testing)
- [🧱 Simulation & Environments](#-simulation--environments)
- [🔐 Cybersecurity Agents](#-cybersecurity-agents)
- [🧠 Open-Source Models for Agents](#-open-source-models-for-agents)
- [📚 Learning Resources](#-learning-resources)
- [📰 Newsletters and Communities](#-newsletters-and-communities)
- [📊 Signals (How to Read This List)](#-signals-how-to-read-this-list)
- [🧠 Agentic Engineering Skills](#-agentic-engineering-skills)
- [🚀 Getting Started](#-getting-started)
- [🤝 Contributing](#-contributing)
- [📌 Final Note](#-final-note)

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

## 🖥 Coding Agents

### IDE-Native Agents
| Agent | Description |
|-------|------------- |
| [Cursor](https://cursor.com) | VS Code fork. Composer mode for multi-file edits. Claude, GPT, Gemini. $29.3B valuation. |
| [GitHub Copilot](https://github.com/features/copilot) | Agent Mode in VS Code. Copilot Workspace issue-to-PR. Multi-model (Claude, GPT-5, Gemini 3). |
| [Windsurf (Codeium)](https://windsurf.com) | Cascade agentic mode. Project-level memory. 5 parallel agents. |
| [JetBrains AI](https://www.jetbrains.com/ai/) | Deep integration across all JetBrains IDEs. Context-aware completions. |
| [Amazon Q Developer](https://aws.amazon.com/q/developer/) | AWS-native. Lambda, CloudWatch, infrastructure, security scanning. |
| [Tabnine](https://www.tabnine.com/) | Privacy-first. On-premise option. Fine-tuned on your codebase. |
| [Sourcegraph Cody](https://sourcegraph.com/cody) | Excels at large codebases. Enterprise context engine. |
| [Google Antigravity](https://idx.google.com) | Free Claude Opus 4.5 access. Learning-focused. |

### Terminal and CLI Agents
| Agent | Description |
|-------|------------- |
| [Claude Code](https://docs.anthropic.com/en/docs/claude-code) | Anthropic CLI agent. Best reasoning. 80.9% SWE-bench. Agent Teams. |
| [OpenAI Codex CLI](https://github.com/openai/codex) | OpenAI terminal agent. Agents SDK. Multi-agent. |
| [Aider](https://github.com/paul-gauthier/aider) | OSS pair programmer. Git-aware. Any LLM. |
| [Cline](https://github.com/cline/cline) | VS Code extension. Full terminal and browser access for Claude/GPT. |
| [RooCode](https://github.com/RooVetGit/Roo-Code) | Cline fork. Structured modes. Reduced hallucinations. |
| [Kilo Code](https://kilocode.ai) | Emerging. Structured modes. Tighter context. |
| [OpenCode](https://github.com/opencode-ai/opencode) | BYOK terminal agent for Cursor refugees. |

### Autonomous Software Engineers
| Agent | Description |
|-------|------------- |
| [Devin](https://devin.ai) | Cognition. Fully autonomous. Sandboxed cloud env. Devin 2.0 with Interactive Planning. |
| [Copilot Workspace](https://githubnext.com/projects/copilot-workspace) | GitHub issue-to-PR agent. |
| [SWE-Agent](https://github.com/princeton-nlp/SWE-agent) | Princeton. Resolves real GitHub issues autonomously. |
| [OpenHands](https://github.com/All-Hands-AI/OpenHands) | OSS autonomous software engineer (ex-OpenDevin). |
| [Grok Build (xAI)](https://x.ai) | 8 parallel agents for code gen. |
| [Kiro](https://kiro.dev) | Spec-driven development. DevOps automation. |

### Code Review and Security
| Agent | Description |
|-------|------------- |
| [Qodo](https://www.qodo.ai/) | AI code review. Context-aware PR validation. |
| [CodeRabbit](https://coderabbit.ai/) | AI PR reviewer. Inline suggestions, security. |
| [Snyk Code](https://snyk.io/) | AI security scanner. Real-time vuln detection. |
| [PR-Agent](https://github.com/Codium-ai/pr-agent) | OSS AI PR reviewer. Auto-describe, review, improve. |

### App Builders (Prompt-to-App)
| Agent | Description |
|-------|------------- |
| [Bolt.new](https://bolt.new) | Prompt to full-stack web app in browser. |
| [Lovable](https://lovable.dev) | Describe then build then deploy from chat. |
| [v0 (Vercel)](https://v0.dev) | Prompt to React/Tailwind components. |
| [Replit Agent](https://replit.com) | Full-stack from prompt. Auto-deploys. |
| [PlayCode Agent](https://playcode.io) | Browser-based. English to websites. |
| [Dyad](https://github.com/dyad-sh/dyad) | OSS. Local-first. No-code app builder. |

---

## 🌐 Browser and Desktop Agents

### Consumer Products
| Agent | Description |
|-------|------------- |
| [OpenAI Operator](https://operator.chatgpt.com) | ChatGPT autonomous web agent. Human checkpoints. CUA tech. |
| [Manus (Meta)](https://manus.im) | Autonomous digital employee. Browser Operator extension. Acquired by Meta. |
| [Claude Computer Use](https://docs.anthropic.com/en/docs/agents-and-tools/computer-use) | Anthropic desktop/browser control via screenshots. |
| [Claude in Chrome](https://claude.ai) | Anthropic browsing agent. Beta. |
| [Google Project Mariner](https://deepmind.google/technologies/project-mariner/) | Gemini browser agent. Multi-tasking. |
| [OpenAI Atlas](https://atlas.openai.com) | AI browser with Agent Mode. |
| [Dia Browser](https://diabrowser.com) | AI-native browser (Atlassian/Browser Company). |
| [Fellou](https://fellou.ai) | Transparent. Visual workflow editing. Agentic memory. |
| [Genspark](https://genspark.ai) | 169+ on-device models. No internet required. |

### Developer Infrastructure
| Tool | Description |
|------|-------------|
| [Browser Use](https://github.com/browser-use/browser-use) | OSS browser agent library. Used by Manus. |
| [Skyvern](https://github.com/Skyvern-AI/skyvern) | Vision-driven. GPT-4V navigation without coded selectors. |
| [Agent S2 (Simular)](https://github.com/simular-ai/Agent-S) | OSS GUI automation framework. |
| [MultiOn](https://multion.ai) | Reliable web automation API. CAPTCHA handling. |
| [Browserbase](https://browserbase.com) | Cloud browser infra for agents. Headless at scale. |
| [Airtop](https://airtop.ai) | Enterprise browser automation. AI integration. |
| [Amazon Nova Act](https://aws.amazon.com/ai/nova/) | AWS browser automation. Enterprise reliability. |
| [Playwright MCP](https://github.com/microsoft/playwright-mcp) | MCP server for Playwright + AI agents. |

---

## 🎙 Voice Agents

### Platforms and APIs
| Platform | Description |
|----------|------------- |
| [ElevenLabs](https://elevenlabs.io) | Industry benchmark. Conv AI 2.0. RAG, multimodal, batch calling. 75ms. HIPAA. $11B. |
| [Vapi](https://vapi.ai) | Developer-first. Low-latency, model-agnostic. |
| [Bland AI](https://bland.ai) | Outbound call automation. CRM integration. SOC2/HIPAA. |
| [Voiceflow](https://voiceflow.com) | No-code voice and chat builder. Drag-and-drop. |
| [Synthflow](https://synthflow.ai) | No-code voice agents for SMBs. Templates. |
| [PolyAI](https://poly.ai) | Enterprise. Natural multi-turn. Hospitality/retail. |
| [Retell AI](https://retellai.com) | Human-like voice agents. Multi-language. Telephony. |
| [HeyGen](https://heygen.com) | Talking avatars. Voice cloning. Lip-sync translation. |
| [Synthesia](https://synthesia.io) | AI video avatars. 120+ languages. Enterprise. |
| [Deepgram](https://deepgram.com) | STT and TTS APIs. Sub-300ms latency. |
| [AssemblyAI](https://assemblyai.com) | STT with diarization, sentiment, summarization. |

### Open-Source Voice
| Tool | Description |
|------|-------------|
| [LiveKit Agents](https://github.com/livekit/agents) | OSS real-time voice/video AI agents. |
| [Rasa](https://github.com/RasaHQ/rasa) | OSS conversational AI. Self-hosted. NLU training. |
| [Pipecat](https://github.com/pipecat-ai/pipecat) | OSS voice and multimodal conversational AI. |
| [Vocode](https://github.com/vocodedev/vocode-python) | OSS voice-based LLM agents. |

---

## 🎨 Creative AI

### Image Generation
| Tool | Description |
|------|------------- |
| [Midjourney v7](https://midjourney.com) | Best artistic quality. Unmatched aesthetics. Discord + web. |
| [DALL-E 3.5](https://openai.com/dall-e) | Best prompt comprehension. 95% text accuracy. ChatGPT. |
| [FLUX 2](https://blackforestlabs.ai) | Open-weight. Best photorealism. 4K. 6x speed. |
| [Stable Diffusion 3.5](https://stability.ai) | Open-source. ControlNet, LoRAs, ComfyUI ecosystem. |
| [Adobe Firefly 3](https://firefly.adobe.com) | Licensed data only. Commercial indemnification. Photoshop. |
| [Google Imagen 4](https://deepmind.google) | State-of-art photorealism. API via AI Studio. |
| [Ideogram v3](https://ideogram.ai) | Best text-in-image. Zero spelling errors. Logos/posters. |
| [Leonardo AI](https://leonardo.ai) | Multi-model. Realtime Canvas. 3D gaming assets. Canva-owned. |
| [Recraft](https://recraft.ai) | Design-focused. Vector art, brand consistency. |

### Video Generation
| Tool | Description |
|------|------------- |
| [Sora 2](https://sora.com) | Best narrative coherence. Physics realism. 25s. 1080p. |
| [Google Veo 3.1](https://deepmind.google) | Best cinematic. Native audio. 4K. Vertex AI. |
| [Runway Gen-4.5](https://runwayml.com) | No.1 benchmark. Motion Brush, Director Mode. Best editing. |
| [Kling 3.0](https://klingai.com) | Best value. 4K, 2min, native audio. $0.029/sec API. |
| [Seedance 2.0](https://seedance.ai) | Quad-modal input. Lip sync. 2K resolution. |
| [Pika 2.5](https://pika.art) | Beginner-friendly. Pikaswaps. Fast renders. |
| [Luma Dream Machine](https://lumalabs.ai) | 4K HDR. Physics simulation. 3D/cinematic. |
| [HaiLuo AI](https://hailuoai.video) | Budget video. 10 free/day. MiniMax. |
| [Wan 2.1](https://github.com/Wan-Video/Wan2.1) | Best free OSS video gen. Self-hostable. No limits. |
| [HunyuanVideo](https://github.com/Tencent/HunyuanVideo) | Tencent OSS. Consumer GPU. Multi-style. |
| [LTX Video](https://github.com/Lightricks/LTX-Video) | OSS. Licensed data. Clear commercial terms. |

### Music and Audio
| Tool | Description |
|------|------------- |
| [Suno](https://suno.ai) | Text-to-song. Full tracks with vocals. Viral hit maker. |
| [Udio](https://udio.com) | High-fidelity music gen. Fine control. |
| [ElevenLabs Music](https://elevenlabs.io) | Vocals, instrumentals. Sectional editing. Stem separation. |
| [Stable Audio](https://stableaudio.com) | High-quality. Commercial license. |
| [Meta AudioCraft](https://github.com/facebookresearch/audiocraft) | OSS. MusicGen + AudioGen. |

### 3D and Design
| Tool | Description |
|------|------------- |
| [Meshy](https://meshy.ai) | Text/image to 3D. Game assets, products. |
| [Tripo AI](https://tripo3d.ai) | Fast 3D from text/images. Multi-format export. |
| [Vizcom](https://vizcom.ai) | Real-time AI rendering for industrial designers. |

---

## ⚡ Task and Workflow Agents

### Automation
| Agent | Description |
|-------|------------- |
| [n8n](https://github.com/n8n-io/n8n) | OSS workflow automation with AI agent nodes. Visual + code. |
| [Zapier AI](https://zapier.com/ai) | 7000+ apps. Natural language workflows. |
| [Make](https://make.com) | Visual workflow platform. AI capabilities. |
| [Activepieces](https://github.com/activepieces/activepieces) | OSS Zapier alternative with AI. |
| [Temporal](https://github.com/temporalio/temporal) | Durable execution for long-running agent workflows. |

### No-Code Agent Builders
| Agent | Description |
|-------|------------- |
| [Dify](https://github.com/langgenius/dify) | OSS LLMOps. Visual agent builder. RAG. 130k+ stars. |
| [Flowise](https://github.com/FlowiseAI/Flowise) | OSS drag-and-drop LLM agent builder. |
| [Langflow](https://github.com/langflow-ai/langflow) | Visual multi-agent and RAG builder. |
| [Lindy](https://lindy.ai) | No-code agents. 3000+ integrations. |
| [Relevance AI](https://relevanceai.com) | No-code agents for sales, support, research. |
| [Rivet](https://rivet.ironcladapp.com) | Visual AI workflow builder. Drag-and-drop. |
| [FastAgency](https://github.com/airtai/fastagency) | Deploy multi-agent workflows as APIs. |

---

## 💼 Customer Support and CRM Agents

### Support Agents
| Agent | Description |
|-------|------------- |
| [Intercom Fin](https://intercom.com) | Resolves 50%+ tickets. Learns from help center. |
| [Zendesk AI](https://zendesk.com) | Ticket routing, sentiment detection, Answer Bot. |
| [Ada](https://ada.cx) | Autonomous resolution. Multi-channel. SOP Playbooks. |
| [Assembled](https://assembled.com) | Workforce-aware handoffs. End-to-end resolution. |
| [Freshdesk Freddy AI](https://freshworks.com) | Auto-triage, smart routing, predictive analytics. |
| [Dixa (Mim)](https://dixa.com) | Conversational CRM. AI routing and prioritization. |

### AI-Powered CRMs
| CRM | AI Features |
|-----|------------- |
| [Salesforce Einstein + Agentforce](https://salesforce.com) | Predictions, autonomous agents, ChatGPT integration. |
| [HubSpot Breeze](https://hubspot.com) | Copilot, Agents, Intelligence. Agent marketplace. |
| [Monday CRM (Lexi)](https://monday.com) | AI sales agent. Lead sourcing, qualification. AI Blocks. |
| [Zoho CRM (Zia)](https://zoho.com/crm) | Predictive, sentiment, voice commands. |
| [Pipedrive AI](https://pipedrive.com) | Email gen, deal priority, smart reports. |
| [Dynamics 365 Copilot](https://dynamics.microsoft.com) | Drafting, summarizing, translating. Power Platform. |
| [ServiceNow AI Agents](https://servicenow.com) | Orchestrator across IT, HR, CRM. |
| [Creatio](https://creatio.com) | No-code. Pre-configured agents. |
| [Salesmate](https://salesmate.io) | Call summarization, lead qualification. |

### Sales and Outreach Agents
| Agent | Description |
|-------|------------- |
| [Clay](https://clay.com) | AI data enrichment. Personalized outreach at scale. |
| [Apollo.io](https://apollo.io) | AI prospecting, sequences, scoring. 275M+ contacts. |
| [Instantly](https://instantly.ai) | AI cold email. Unlimited accounts. Smart rotation. |
| [Lavender](https://lavender.ai) | AI email coach. Real-time scoring. |

---

## 📊 Data and Research Agents

### Deep Research
| Agent | Description |
|-------|------------- |
| [Claude Deep Research](https://claude.ai) | Multi-step investigation with citations. |
| [ChatGPT Deep Research](https://chat.openai.com) | Extended reasoning, web browsing, reports. |
| [Gemini Deep Research](https://gemini.google.com) | Google Search and Knowledge Graph. |
| [Perplexity Pro](https://perplexity.ai) | AI search with deep research mode. Real-time citations. |
| [DeerFlow](https://github.com/bytedance/deer-flow) | ByteDance OSS. Planning, tools, memory, execution. |
| [GPT Researcher](https://github.com/assafelovic/gpt-researcher) | OSS autonomous comprehensive research. |
| [STORM](https://github.com/stanford-oval/storm) | Stanford. Writes Wikipedia-like articles from scratch. |

### Data Analysis
| Agent | Description |
|-------|------------- |
| [Julius AI](https://julius.ai) | Upload CSV/Excel, ask in natural language. |
| [Hex AI](https://hex.tech) | Collaborative data platform. AI analysis. |
| [PandasAI](https://github.com/Sinaptik-AI/pandas-ai) | Chat with your data. NL to Pandas/SQL. |
| [TaskWeaver](https://github.com/microsoft/TaskWeaver) | Microsoft. Code-first data analytics agents. |

### RAG and Knowledge Bases
| Tool | Description |
|------|-------------|
| [RAGFlow](https://github.com/infiniflow/ragflow) | OSS RAG engine with agent capabilities. |
| [Pathway](https://github.com/pathwaycom/pathway) | Live data RAG. Real-time streaming. 50k+ stars. |
| [Mem0](https://github.com/mem0ai/mem0) | Memory layer for agents. Long-term across sessions. |
| [Chroma](https://github.com/chroma-core/chroma) | OSS embedding database. Fastest way to build RAG. |
| [Weaviate](https://github.com/weaviate/weaviate) | OSS vector DB. GraphQL. Multi-modal search. |
| [Qdrant](https://github.com/qdrant/qdrant) | High-performance vector DB in Rust. |
| [Milvus](https://github.com/milvus-io/milvus) | Cloud-native vector DB. Billion-scale. |
| [Pinecone](https://pinecone.io) | Managed vector DB. Serverless. Low-latency. |

---

## 🏠 Local and Self-Hosted AI

### Local LLM Runners
| Tool | Description |
|------|-------------|
| [Ollama](https://github.com/ollama/ollama) | Run LLMs locally. 162k+ stars. Dead simple CLI. |
| [llama.cpp](https://github.com/ggml-org/llama.cpp) | C/C++ inference. CPU, GPU, Apple Silicon. Foundation of local AI. |
| [vLLM](https://github.com/vllm-project/vllm) | High-throughput serving. PagedAttention. Production-grade. |
| [LM Studio](https://lmstudio.ai) | Desktop app for local LLMs. Beautiful UI. All platforms. |
| [Jan](https://github.com/janhq/jan) | OSS ChatGPT alternative. 100% offline. |
| [LocalAI](https://github.com/mudler/LocalAI) | Drop-in OpenAI API replacement. No GPU required. |
| [GPT4All](https://github.com/nomic-ai/gpt4all) | OSS local chat. Consumer hardware. |
| [Llamafile](https://github.com/Mozilla-Ocho/llamafile) | LLMs as single files. Zero setup. Mozilla. |

### Self-Hosted Agents and UIs
| Tool | Description |
|------|-------------|
| [Open WebUI](https://github.com/open-webui/open-webui) | Self-hosted ChatGPT UI. Access control. Extensions. |
| [OpenClaw](https://github.com/openclaw/openclaw) | Fastest-growing GitHub repo ever (9k to 188k stars in 60 days). Self-hosted agent across WhatsApp, Telegram, Slack, Discord, Signal. 5,700+ community skills. |
| [LibreChat](https://github.com/danny-avila/LibreChat) | Self-hosted multi-model chat. All major providers. |
| [LobeChat](https://github.com/lobehub/lobe-chat) | OSS ChatGPT/Gemini UI. Plugin system. Multi-modal. |
| [Anything LLM](https://github.com/Mintplex-Labs/anything-llm) | All-in-one AI app. RAG, agents. Desktop + Docker. |
| [DB-GPT](https://github.com/eosphoros-ai/DB-GPT) | Data interaction with local LLM. 100% private. |

---

## 🤖 Multi-Agent Platforms

| Platform | Description |
|----------|------------- |
| [ChatGPT](https://chat.openai.com) | GPTs, Deep Research, Canvas, Agent Mode, vision. GPT-5. |
| [Claude](https://claude.ai) | Tool use, computer control, MCP, code exec. Chrome, Excel, Cowork. |
| [Gemini](https://gemini.google.com) | Deep Think, Gems, multi-modal. 1M tokens. Google ecosystem. |
| [Grok](https://x.ai) | Real-time X data. Grok Build. Image gen. |
| [Meta AI](https://meta.ai) | Llama-powered. WhatsApp/Messenger. Manus acquisition. |
| [Microsoft Copilot](https://copilot.microsoft.com) | Office 365 integration. Enterprise. |
| [Coze](https://coze.com) | ByteDance agent builder. Visual workflow. Plugin marketplace. |

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

## 🧱 Simulation & Environments

| Tool | Description | Strengths | Weaknesses | Best For |
|------|-------------|-----------|------------|----------|
| [Arnis](https://github.com/louis-e/arnis) | Converts real-world geographic data into Minecraft Java and Bedrock worlds (terrain, streets, buildings). | Strong bridge between real-world geography and simulated environments. | Niche relevance unless building spatial/embodied agent systems. | Embodied AI exploration, spatial simulation environments, and synthetic task environments mapping real-world locations. |

---

## 🔐 Cybersecurity Agents

| Agent | Description |
|-------|-------------|
| [CAI](https://github.com/aliasrobotics/CAI) | AI pentesting, vuln discovery, red teaming. HITL. |
| [YAWNING TITAN](https://github.com/dstl/YAWNING-TITAN) | Graph-based cybersecurity simulation. |
| [PentestGPT](https://github.com/GreyDGL/PentestGPT) | GPT-powered pentesting. Automated reasoning. |
| [Microsoft Security Copilot](https://microsoft.com/security/copilot) | Enterprise threat detection, incident response. |
| [CrowdStrike Charlotte AI](https://crowdstrike.com) | AI security analyst. Threat hunting. |

---

## 🧠 Open-Source Models for Agents

| Model | Org | Params | Highlights |
|-------|-----|--------|------------|
| [Llama 4](https://github.com/meta-llama) | Meta | 8B-405B+ | Strong tool use. Maverick and Scout. Open-weight. |
| [Qwen 3](https://github.com/QwenLM/Qwen3) | Alibaba | 0.6B-235B | MCP-native. Best multilingual open model. |
| [DeepSeek V3/R1](https://github.com/deepseek-ai/DeepSeek-V3) | DeepSeek | 671B MoE | 68x cheaper. Strong reasoning. |
| [GLM-4](https://github.com/THUDM/GLM-4) | Zhipu | 744B MoE | Lowest hallucination rate. 77.8% SWE-bench. |
| [Mistral Large](https://mistral.ai) | Mistral | Various | Function calling, JSON mode. European. |
| [Gemma 3](https://github.com/google-deepmind/gemma) | Google | 1B-27B | Efficient on-device. Multi-modal. Edge agents. |
| [Command R+](https://cohere.com) | Cohere | 104B | RAG and enterprise tool use optimized. |
| [Phi-4](https://github.com/microsoft/phi-4) | Microsoft | 14B | Small but mighty. On-device agents. |

---

## 📚 Learning Resources

### Courses and Tutorials
- [DeepLearning.AI Agent Courses](https://www.deeplearning.ai/) - Free courses with LangChain, CrewAI, AutoGen
- [HuggingFace Agents Course](https://huggingface.co/learn/agents-course) - Open-source agent dev course
- [LangGraph Academy](https://academy.langchain.com/) - Official LangGraph path
- [Anthropic Cookbook](https://github.com/anthropics/anthropic-cookbook) - Claude agent recipes
- [Microsoft GenAI for Beginners](https://github.com/microsoft/generative-ai-for-beginners) - 21-lesson course
- [OpenAI Cookbook](https://github.com/openai/openai-cookbook) - Practical API guides

### Key Papers
- [ReAct](https://arxiv.org/abs/2210.03629) - Foundation for modern agents (reasoning + acting)
- [Toolformer](https://arxiv.org/abs/2302.04761) - Teaching LLMs to use tools
- [Voyager](https://arxiv.org/abs/2305.16291) - Open-ended embodied agent in Minecraft
- [Generative Agents](https://arxiv.org/abs/2304.03442) - Stanford simulacra of human behavior
- [Self-Refine](https://arxiv.org/abs/2303.17651) - Iterative self-refinement
- [Tree of Thoughts](https://arxiv.org/abs/2305.10601) - Deliberate problem solving
- [HuggingGPT](https://arxiv.org/abs/2303.17580) - LLM task planning + specialist models
- [MRKL Systems](https://arxiv.org/abs/2205.00445) - Neuro-symbolic agent architecture

### Books
- Building LLM Apps (O'Reilly) - Practical LLM application development
- AI Agents in Action (Manning) - Production-ready AI agents
- AI Engineering (Chip Huyen) - AI systems design and deployment

---

## 📰 Newsletters and Communities

| Resource | Description |
|----------|-------------|
| [Awesome Agents Newsletter](https://awesomeagents.ai) | Weekly tools + reviews |
| [Latent Space](https://www.latent.space/) | AI engineering podcast (Swyx + Alessio) |
| [The Rundown AI](https://therundown.ai) | Daily digest (600k+ subs) |
| [Ben's Bites](https://bensbites.co) | Daily AI with builder focus |
| [State of Agent Engineering](https://www.langchain.com/state-of-agent-engineering) | Annual report (1,300+ surveyed) |
| [r/LangChain](https://reddit.com/r/LangChain) | Agent developer community |
| [r/ClaudeAI](https://reddit.com/r/ClaudeAI) | Claude community |
| [r/LocalLLaMA](https://reddit.com/r/LocalLLaMA) | Self-hosted LLM community |

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