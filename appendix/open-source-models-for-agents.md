## 🧠 Open-Source Models for Agents

> Audience: practitioners · Evidence class: mixed

_Last reviewed: April 2026._

Open-weight models selected for agentic relevance: native tool/function-calling, long context for trajectories, or explicit reasoning modes. Cap of 5–8; models without credible agent-workload evidence are excluded regardless of general benchmark wins. Evidence tags follow the [Benchmark and Evidence Policy](benchmark-and-evidence-policy.md).

| Model | Org | License | Params | Why it matters for agents | Evidence |
|-------|-----|---------|--------|---------------------------|----------|
| [Llama 4](https://github.com/meta-llama) | Meta | Llama 4 Community License | 17B–400B+ (MoE) | Open-weight family with tool-use support across Maverick and Scout variants; long context and multimodal input. | `[official]` |
| [Qwen3](https://github.com/QwenLM/Qwen3) | Alibaba | Apache-2.0 | 0.6B–235B (incl. MoE) | Switchable thinking / non-thinking modes; strong tool-use and multilingual coverage; widely adopted for local agent stacks. | `[official]` · `[benchmark]` [tech report](https://arxiv.org/abs/2505.09388) |
| [DeepSeek-V3 / R1](https://github.com/deepseek-ai/DeepSeek-V3) | DeepSeek | DeepSeek License | 671B MoE | V3 as strong generalist actor, R1 as open-weight reasoning planner; cost-efficient inference. | `[official]` · `[benchmark]` [R1 paper](https://arxiv.org/abs/2501.12948) |
| [GLM-4.5 / GLM-4.6](https://github.com/zai-org/GLM-4.5) | Zhipu / Z.ai | MIT | 355B MoE (A32B) | Open MoE explicitly tuned for agent and coding workloads; top-tier open-weight on agent benchmarks. | `[official]` · `[benchmark]` [paper](https://arxiv.org/abs/2508.06471) |
| [MiniMax-M2](https://github.com/MiniMax-AI/MiniMax-M2) | MiniMax | MIT | 230B MoE (A10B) | Agent-first open-weight model with interleaved thinking and tool use; designed for end-to-end agent workflows. | `[official]` |
| [Gemma 3](https://github.com/google-deepmind/gemma) | Google DeepMind | Gemma Terms of Use | 1B–27B | Efficient multimodal family; small sizes suitable for edge / on-device agents with function calling. | `[official]` |
| [Mistral Large 2](https://mistral.ai/news/mistral-large-2407/) | Mistral | Mistral Research License | 123B | Function calling and JSON-mode support from a European provider; strong tool-use reliability. | `[official]` |
| [Phi-4](https://github.com/microsoft/phi-4) | Microsoft | MIT | 14B | Compact reasoning-tuned model; viable planner/actor for on-device and resource-constrained agents. | `[official]` · `[benchmark]` [tech report](https://arxiv.org/abs/2412.08905) |

---

