"""MCP server (stdio transport).

Thin adapter that registers the pure functions in :mod:`repo_agent.tools` as
MCP tools via the official Python SDK's ``FastMCP`` facade.

Run with::

    repo-agent serve

Or from the installed package::

    python -m repo_agent serve
"""

from __future__ import annotations

from . import tools as T


def build_server():  # pragma: no cover - thin SDK wiring
    # Import lazily so that unit tests (and the CLI's non-serve commands)
    # do not require the ``mcp`` SDK to be importable.
    from mcp.server.fastmcp import FastMCP

    mcp = FastMCP("repo-agent")

    @mcp.tool()
    def list_sections() -> dict:
        """List every section and appendix file in the curated list."""
        return T.list_sections()

    @mcp.tool()
    def get_rubric() -> dict:
        """Return the curation rubric (dimensions, weights, thresholds, hard gates)."""
        return T.get_rubric()

    @mcp.tool()
    def get_anti_patterns() -> dict:
        """Return the anti-pattern policy (rejection patterns + hype phrases)."""
        return T.get_anti_patterns()

    @mcp.tool()
    def search_entries(query: str, section: str | None = None, limit: int = 20) -> dict:
        """Full-text search across README.md and appendix/**."""
        return T.search_entries(query=query, section=section, limit=limit)

    @mcp.tool()
    def validate_entry(entry_markdown: str) -> dict:
        """Score an entry against the rubric and flag anti-pattern hits."""
        return T.validate_entry(entry_markdown=entry_markdown)

    @mcp.tool()
    def propose_entry(url: str, section: str, rationale: str = "") -> dict:
        """Draft a rubric-aligned entry stub for a URL, with self-validation."""
        return T.propose_entry(url=url, section=section, rationale=rationale)

    @mcp.tool()
    def triage_pr(
        title: str,
        body: str = "",
        changed_files: list[str] | None = None,
        entry_markdown: str | None = None,
    ) -> dict:
        """Classify an incoming PR or issue against the rubric."""
        return T.triage_pr(
            title=title,
            body=body,
            changed_files=changed_files,
            entry_markdown=entry_markdown,
        )

    @mcp.tool()
    def freshness_audit(threshold_months: int = 9) -> dict:
        """Return structured stale-entry candidates (does not open issues)."""
        return T.freshness_audit(threshold_months=threshold_months)

    return mcp


def serve() -> None:  # pragma: no cover - requires live stdio
    mcp = build_server()
    mcp.run()
