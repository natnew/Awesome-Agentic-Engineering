## 🌐 Browser and Desktop Agents

> Audience: practitioners · Evidence class: mixed

_Last reviewed: April 2026._

Computer-use and browser agents operate on GUI surfaces (DOM, pixels, or accessibility trees) rather than pure APIs. Evidence tags follow the [Benchmark and Evidence Policy](benchmark-and-evidence-policy.md). Entries that are marketing-only or have no active development were removed in this phase.

### Consumer Products

| Agent | Description | Evidence |
|-------|-------------|----------|
| [OpenAI Operator](https://operator.chatgpt.com) | ChatGPT autonomous web agent; human checkpoints; built on the CUA (Computer-Using Agent) model. | `[official]` |
| [Claude Computer Use](https://docs.anthropic.com/en/docs/agents-and-tools/computer-use) | Anthropic desktop/browser control via screenshots and tool loop. | `[official]` |
| [Claude for Chrome](https://www.anthropic.com/news/claude-for-chrome) | Anthropic browsing agent running inside Chrome. | `[official]` |
| [Google Project Mariner](https://deepmind.google/technologies/project-mariner/) | Gemini browser agent with multi-task execution in the user's browser context. | `[official]` |
| [ChatGPT Atlas](https://openai.com/index/introducing-chatgpt-atlas/) | OpenAI's AI-native browser with Agent Mode. | `[official]` |
| [Dia Browser](https://www.diabrowser.com/) | AI-native browser from The Browser Company (acquired by Atlassian). | `[official]` |

### Developer Infrastructure

| Tool | Description | Evidence |
|------|-------------|----------|
| [Browser Use](https://github.com/browser-use/browser-use) | OSS browser agent library with DOM + vision hybrid; widely embedded in other agent stacks. | `[official]` |
| [Skyvern](https://github.com/Skyvern-AI/skyvern) | Vision-driven browser automation using multimodal LLMs for navigation without coded selectors. | `[official]` |
| [UI-TARS](https://github.com/bytedance/UI-TARS) | ByteDance open-source native GUI agent model + desktop app for end-to-end computer use. | `[official]` · `[benchmark]` [paper](https://arxiv.org/abs/2501.12326) |
| [Agent S2 (Simular)](https://github.com/simular-ai/Agent-S) | OSS compositional GUI automation framework with generalist + specialist models. | `[official]` · `[benchmark]` |
| [Browserbase](https://www.browserbase.com/) | Cloud browser infrastructure for agents; headless Chrome at scale with session persistence. | `[official]` |
| [Amazon Nova Act](https://labs.amazon.science/blog/nova-act) | AWS browser automation research preview aimed at enterprise reliability. | `[official]` |
| [Playwright MCP](https://github.com/microsoft/playwright-mcp) | Official MCP server wrapping Playwright for agent-driven browser automation. | `[official]` |

### Benchmarks & Evaluation

| Benchmark | Description | Evidence |
|-----------|-------------|----------|
| [OSWorld](https://os-world.github.io/) | Real computer environments benchmark for multimodal agents on open-ended tasks. | `[official]` · `[benchmark]` |
| [WebArena / VisualWebArena](https://github.com/web-arena-x/webarena) | Reproducible web agent benchmark on real-website snapshots. | `[official]` · `[benchmark]` |
| [WindowsAgentArena](https://github.com/microsoft/WindowsAgentArena) | Benchmark for Windows desktop agents across real applications. | `[official]` · `[benchmark]` |

---

