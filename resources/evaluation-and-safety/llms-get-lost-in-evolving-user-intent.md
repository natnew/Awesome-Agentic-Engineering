# LLMs Get Lost in Evolving User Intent

> Audience: researchers and agent engineers · Evidence class: benchmark

## Resource

- **Repository:** [microsoft/evolving-intent](https://github.com/microsoft/evolving-intent)
- **Paper:** [LLMs Get Lost in Evolving User Intent](https://arxiv.org/abs/2607.20734)
- **Authors:** Jihoon Tack, Philippe Laban and Jennifer Neville
- **Organisation:** Microsoft Research, AI Interaction and Learning

## Why it matters

This work evaluates whether language models can preserve and update a user's operative intent across multi-turn interactions rather than relying on fully specified, single-turn prompts. It transforms established benchmarks into dynamic conversations in which information is incrementally revealed, revised or redirected, while retaining the original task's evaluation protocol.

The framework is directly relevant to production agent evaluation because long-running assistants must distinguish superseded instructions from current intent, incorporate corrections without retaining stale assumptions, and adapt when the user's underlying objective changes.

## Evaluation coverage

The released framework supports:

- GSM8K for mathematical reasoning;
- BIRD-SQL for text-to-SQL;
- BrowseComp+ for agentic search; and
- SWE-bench Verified for software-engineering agents.

Its evaluation scenarios include incremental argument reveal, argument revision, function switching and combined intent transitions. Reported results show substantial degradation across strong models after only a small number of intent transitions.

## Engineering use

Use this resource to design:

- multi-turn regression suites for instruction updates and corrections;
- state-management tests that detect stale or conflicting intent;
- user simulators for evolving requirements;
- acceptance tests for long-running conversational agents; and
- comparative evaluations between static-task performance and situated interaction performance.

## Evidence

- `[official]` [Microsoft Research repository](https://github.com/microsoft/evolving-intent)
- `[benchmark]` [Research paper](https://arxiv.org/abs/2607.20734)

_Last reviewed: July 2026._
