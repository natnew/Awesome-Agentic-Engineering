"""Tests for workflow 6.1 — new-tool."""

from __future__ import annotations

import httpx

from repo_agent.workflows import new_tool
from repo_agent.workflows.github import GitHubClient
from repo_agent.workflows.render import new_tool_marker
from tests.test_workflows_base import _MockState  # reuse the mock state


def _fixture_fetcher(fixtures_dir):
    html = (fixtures_dir / "sample-page.html").read_text(encoding="utf-8")
    return lambda _url: html


def test_new_tool_dry_run_produces_draft_markdown(fixtures_dir):
    result = new_tool.run(
        url="https://example.com/x",
        section="Orchestration Frameworks",
        rationale="Adds typed graph orchestration.",
        fetcher=_fixture_fetcher(fixtures_dir),
        open_issue=False,
    )
    assert result.status in {"ok", "warn"}
    assert "```markdown" in result.markdown
    assert "Example Agent Framework" in result.markdown
    assert new_tool_marker("https://example.com/x") in result.markdown
    # Dry-run does not record an issue action.
    assert "issue" not in result.artifacts


def test_new_tool_open_issue_upserts_once(fixtures_dir):
    state = _MockState()
    transport = httpx.MockTransport(state.handler)
    gh = GitHubClient(
        "natnew/test-repo",
        client=httpx.Client(transport=transport, base_url="https://api.github.com"),
        token="t",
    )

    r1 = new_tool.run(
        url="https://example.com/x",
        section="Orchestration Frameworks",
        fetcher=_fixture_fetcher(fixtures_dir),
        gh_client=gh,
        open_issue=True,
    )
    r2 = new_tool.run(
        url="https://example.com/x",
        section="Orchestration Frameworks",
        fetcher=_fixture_fetcher(fixtures_dir),
        gh_client=gh,
        open_issue=True,
    )
    assert r1.artifacts["issue"]["action"] == "created"
    assert r2.artifacts["issue"]["action"] == "updated"
    assert r1.artifacts["issue"]["number"] == r2.artifacts["issue"]["number"]
    assert len(state.issues) == 1


def test_new_tool_open_issue_without_client_returns_error(fixtures_dir):
    r = new_tool.run(
        url="https://example.com/x",
        section="x",
        fetcher=_fixture_fetcher(fixtures_dir),
        open_issue=True,
        gh_client=None,
    )
    assert r.status == "error"
