"""Tests for workflow 6.3 — review-pr."""

from __future__ import annotations

import json

import httpx

from repo_agent.workflows import review_pr
from repo_agent.workflows.github import GitHubClient
from repo_agent.workflows.render import review_marker
from tests.test_workflows_base import _MockState


def _gh():
    state = _MockState()
    http = httpx.Client(transport=httpx.MockTransport(state.handler), base_url="https://api.github.com")
    return GitHubClient("natnew/test-repo", client=http, token="t"), state


def test_review_pr_dry_run_with_fixture(fixtures_dir):
    payload = json.loads((fixtures_dir / "sample-pr.json").read_text(encoding="utf-8"))
    r = review_pr.run(pr_number=5, pr_payload=payload, post=False)
    assert r.status in {"ok", "warn"}
    assert review_marker(5) in r.markdown
    assert "Rubric review" in r.markdown
    assert r.artifacts["triage"]["verdict"] in {"merge", "request-changes", "block", "needs-info"}


def test_review_pr_post_upserts_single_comment(fixtures_dir):
    payload = json.loads((fixtures_dir / "sample-pr.json").read_text(encoding="utf-8"))
    gh, state = _gh()
    r1 = review_pr.run(pr_number=7, pr_payload=payload, gh_client=gh, post=True)
    r2 = review_pr.run(pr_number=7, pr_payload=payload, gh_client=gh, post=True)
    assert r1.artifacts["comment"]["action"] == "created"
    assert r2.artifacts["comment"]["action"] == "updated"
    assert r1.artifacts["comment"]["id"] == r2.artifacts["comment"]["id"]
    assert len(state.comments[7]) == 1


def test_review_pr_skip_label_suppresses_comment(fixtures_dir):
    payload = json.loads((fixtures_dir / "sample-pr.json").read_text(encoding="utf-8"))
    payload["labels"] = ["skip-review-assistant"]
    gh, state = _gh()
    r = review_pr.run(pr_number=9, pr_payload=payload, gh_client=gh, post=True)
    assert r.artifacts.get("skipped") is True
    assert r.markdown == ""
    assert state.comments.get(9, []) == []


def test_review_pr_post_without_client_returns_error(fixtures_dir):
    payload = json.loads((fixtures_dir / "sample-pr.json").read_text(encoding="utf-8"))
    r = review_pr.run(pr_number=1, pr_payload=payload, post=True, gh_client=None)
    assert r.status == "error"


def test_review_pr_needs_payload_or_client():
    r = review_pr.run(pr_number=1, pr_payload=None, gh_client=None, post=False)
    assert r.status == "error"
