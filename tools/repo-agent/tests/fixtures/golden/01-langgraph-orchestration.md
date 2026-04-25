**LangGraph** is a graph-based orchestration framework for stateful, multi-agent workflows. Built and maintained by LangChain. Apache-2.0. v0.2.x stable.

Why it earns a slot: explicit checkpointing, durable execution, clean MCP tool integration, and a well-documented memory model. Differs from chain-style orchestrators by treating the agent run as a graph with cycles, which makes planner/critic loops natural.

- [official] https://langchain-ai.github.io/langgraph/
- [field report] production deployments at Replit, Elastic.
- [benchmark] internal harness comparing to plain chain orchestration.
