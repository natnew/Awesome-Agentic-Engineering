"""Tests for workflow 6.2 — landscape-scan."""

from __future__ import annotations

from datetime import datetime, timezone

import httpx

from repo_agent.workflows import landscape_scan
from repo_agent.workflows.github import GitHubClient
from repo_agent.workflows.render import LANDSCAPE_MARKER
from tests.test_workflows_base import _MockState


NOW = datetime(2026, 4, 22, 9, 0, tzinfo=timezone.utc)


def _gh_with(merged_prs=(), open_issues=()):
    state = _MockState()
    # Pre-seed for GET /issues → we inject those records directly.
    state.issues = list(open_issues)

    merged = list(merged_prs)

    def handler(request: httpx.Request) -> httpx.Response:
        path = request.url.path
        method = request.method
        if method == "GET" and path.endswith("/pulls"):
            return httpx.Response(200, json=merged)
        # Fall through to the real state handler.
        return state.handler(request)

    http = httpx.Client(transport=httpx.MockTransport(handler), base_url="https://api.github.com")
    return GitHubClient("natnew/test-repo", client=http, token="t"), state


def test_landscape_dry_run_without_gh_client():
    r = landscape_scan.run(dry_run=True, now=NOW, threshold_months=9)
    assert r.status == "ok"
    assert LANDSCAPE_MARKER in r.markdown
    assert "Stale entries" in r.markdown
    assert "total" in r.artifacts
    # Dry-run means no issue action was recorded.
    assert "issue" not in r.artifacts


def test_landscape_non_dry_run_upserts_single_issue_in_place():
    merged = [
        {
            "number": 10,
            "title": "Add CoolTool",
            "html_url": "https://example/pr/10",
            "merged_at": "2026-04-20T00:00:00Z",
            "created_at": "2026-04-18T00:00:00Z",
        }
    ]
    gh, state = _gh_with(merged_prs=merged, open_issues=[])
    r1 = landscape_scan.run(since_days=7, gh_client=gh, dry_run=False, now=NOW)
    r2 = landscape_scan.run(since_days=7, gh_client=gh, dry_run=False, now=NOW)
    assert r1.artifacts["issue"]["action"] == "created"
    assert r2.artifacts["issue"]["action"] == "updated"
    assert r1.artifacts["issue"]["number"] == r2.artifacts["issue"]["number"]
    assert len(state.issues) == 1
    assert r1.artifacts["candidate_pr_count"] == 1


def test_landscape_filters_prs_older_than_window():
    old = [
        {
            "number": 1,
            "title": "old",
            "html_url": "x",
            "merged_at": "2026-01-01T00:00:00Z",
            "created_at": "2026-01-01T00:00:00Z",
        }
    ]
    gh, _ = _gh_with(merged_prs=old)
    r = landscape_scan.run(since_days=7, gh_client=gh, dry_run=True, now=NOW)
    assert r.artifacts["candidate_pr_count"] == 0
