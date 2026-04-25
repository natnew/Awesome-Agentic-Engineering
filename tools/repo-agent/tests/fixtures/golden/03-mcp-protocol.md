**Model Context Protocol (MCP)** is the open protocol for connecting agents to tools and data sources. Apache-2.0. v2024-11-05 stable. Widely deployed in production agent stacks.

Unique because it standardises the tool/resource boundary across orchestrators — LangGraph, Agent Framework, OpenAI Agents SDK, and AutoGen all consume MCP servers. Memory and tool use share one transport.

- [official] https://modelcontextprotocol.io/
- [field report] reference servers maintained for filesystem, git, and search.
- [benchmark] MCP transport latency benchmark across stdio and SSE.
