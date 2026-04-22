"""Tests for the Phase 6 workflow composition layer."""

from __future__ import annotations

import json

import httpx
import pytest

from repo_agent.workflows import (
    GitHubClient,
    WorkflowResult,
    upsert_issue_by_marker,
    upsert_pr_comment_by_marker,
)
from repo_agent.workflows.github import GitHubWriteError, RepoRef


# ---------------------------------------------------------------------------
# WorkflowResult
# ---------------------------------------------------------------------------


def test_workflow_result_roundtrip():
    r = WorkflowResult(status="ok", summary="hi", markdown="# body", artifacts={"k": 1})
    d = r.to_dict()
    assert d == {"status": "ok", "summary": "hi", "markdown": "# body", "artifacts": {"k": 1}}


def test_repo_ref_parse():
    r = RepoRef.parse("natnew/Awesome-Agentic-Engineering")
    assert r.slug == "natnew/Awesome-Agentic-Engineering"


def test_repo_ref_parse_rejects_bad_input():
    with pytest.raises(ValueError):
        RepoRef.parse("not-a-slug")


# ---------------------------------------------------------------------------
# MockTransport-backed GitHub helpers
# ---------------------------------------------------------------------------


class _MockState:
    """Stateful fake GitHub backend for upsert tests."""

    def __init__(self, *, initial_issues: list[dict] | None = None, initial_comments: dict[int, list[dict]] | None = None):
        self.issues = list(initial_issues or [])
        self.comments = {k: list(v) for k, v in (initial_comments or {}).items()}
        self._next_id = 1000

    def _new_id(self) -> int:
        self._next_id += 1
        return self._next_id

    def handler(self, request: httpx.Request) -> httpx.Response:
        path = request.url.path
        method = request.method
        if method == "GET" and path.endswith("/issues"):
            # Matches both /repos/x/y/issues and filtered variants. Return all.
            return httpx.Response(200, json=self.issues)
        if method == "POST" and path.endswith("/issues"):
            body = json.loads(request.content)
            issue = {
                "number": self._new_id(),
                "title": body["title"],
                "body": body["body"],
                "html_url": f"https://example/issues/{self._next_id}",
            }
            self.issues.append(issue)
            return httpx.Response(201, json=issue)
        if method == "PATCH" and "/issues/" in path and "/comments" not in path:
            num = int(path.rstrip("/").split("/")[-1])
            body = json.loads(request.content)
            for it in self.issues:
                if it["number"] == num:
                    if "title" in body:
                        it["title"] = body["title"]
                    if "body" in body:
                        it["body"] = body["body"]
                    return httpx.Response(200, json=it)
            return httpx.Response(404, json={"message": "not found"})
        if method == "GET" and "/issues/" in path and path.endswith("/comments"):
            num = int(path.split("/issues/")[1].split("/")[0])
            return httpx.Response(200, json=self.comments.get(num, []))
        if method == "POST" and "/issues/" in path and path.endswith("/comments"):
            num = int(path.split("/issues/")[1].split("/")[0])
            body = json.loads(request.content)
            comment = {"id": self._new_id(), "body": body["body"]}
            self.comments.setdefault(num, []).append(comment)
            return httpx.Response(201, json=comment)
        if method == "PATCH" and "/issues/comments/" in path:
            cid = int(path.rstrip("/").split("/")[-1])
            body = json.loads(request.content)
            for num, clist in self.comments.items():
                for c in clist:
                    if c["id"] == cid:
                        c["body"] = body["body"]
                        return httpx.Response(200, json=c)
            return httpx.Response(404, json={"message": "not found"})
        return httpx.Response(404, json={"message": f"unhandled {method} {path}"})


def _make_client(state: _MockState, *, token: str | None = "test-token") -> GitHubClient:
    transport = httpx.MockTransport(state.handler)
    http = httpx.Client(transport=transport, base_url="https://api.github.com")
    return GitHubClient("natnew/test-repo", client=http, token=token)


def test_upsert_issue_creates_then_updates():
    state = _MockState()
    gh = _make_client(state)

    marker = "<!-- test:marker -->"

    action1, rec1 = upsert_issue_by_marker(gh, marker=marker, title="T1", body=f"{marker}\nhello")
    assert action1 == "created"
    assert rec1["number"] > 0

    action2, rec2 = upsert_issue_by_marker(gh, marker=marker, title="T1 v2", body=f"{marker}\nhello again")
    assert action2 == "updated"
    assert rec2["number"] == rec1["number"]
    assert "hello again" in rec2["body"]
    # Still only one issue in the backend.
    assert len(state.issues) == 1


def test_upsert_pr_comment_creates_then_updates():
    state = _MockState()
    gh = _make_client(state)

    marker = "<!-- test:pr-comment -->"
    a1, c1 = upsert_pr_comment_by_marker(gh, pr_number=42, marker=marker, body=f"{marker}\nv1")
    a2, c2 = upsert_pr_comment_by_marker(gh, pr_number=42, marker=marker, body=f"{marker}\nv2")
    assert a1 == "created"
    assert a2 == "updated"
    assert c1["id"] == c2["id"]
    assert len(state.comments[42]) == 1


def test_write_without_token_raises():
    state = _MockState()
    gh = _make_client(state, token=None)
    with pytest.raises(GitHubWriteError):
        gh.create_issue("x", "y")
