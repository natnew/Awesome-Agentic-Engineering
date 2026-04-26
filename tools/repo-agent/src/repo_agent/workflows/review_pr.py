"""Workflow 6.3 — PR review assistant.

Loads a PR payload (either via :class:`GitHubClient` or a pre-built dict for
tests), runs :mod:`skills.triage`, and renders a rubric-scorecard comment.
Posts/updates the comment in place when ``post=True``.

Supports a ``skip-review-assistant`` label as an explicit opt-out signal.
"""

from __future__ import annotations

from typing import Any

from ..observability import Run
from ..skills import triage
from .base import WorkflowResult
from .github import GitHubClient
from .idempotent import upsert_pr_comment_by_marker
from .render import render_review_comment, review_marker

SKIP_LABEL = "skip-review-assistant"


def _pr_payload_from_github(gh: GitHubClient, pr_number: int) -> dict[str, Any]:
    r = gh._client.get(f"/repos/{gh.repo.slug}/pulls/{pr_number}")
    r.raise_for_status()
    pr = r.json()
    files_r = gh._client.get(f"/repos/{gh.repo.slug}/pulls/{pr_number}/files")
    files_r.raise_for_status()
    return {
        "title": pr.get("title", ""),
        "body": pr.get("body") or "",
        "labels": [l.get("name") for l in pr.get("labels") or []],
        "changed_files": [f.get("filename", "") for f in files_r.json()],
    }


def run(
    *,
    pr_number: int,
    pr_payload: dict[str, Any] | None = None,
    gh_client: GitHubClient | None = None,
    post: bool = False,
) -> WorkflowResult:
    with Run(
        component="workflow",
        tool="workflow.review-pr",
        inputs={"pr_number": int(pr_number), "post": bool(post)},
    ) as obs:
        return _run_inner(
            obs,
            pr_number=pr_number,
            pr_payload=pr_payload,
            gh_client=gh_client,
            post=post,
        )


def _run_inner(
    obs: Run,
    *,
    pr_number: int,
    pr_payload: dict[str, Any] | None,
    gh_client: GitHubClient | None,
    post: bool,
) -> WorkflowResult:
    if pr_payload is None:
        if gh_client is None:
            obs.set_outcome("error", error_class="missing_gh_client_or_payload")
            return WorkflowResult(
                status="error",
                summary="review-pr needs either pr_payload or gh_client",
                markdown="",
                artifacts={"pr_number": pr_number},
            )
        pr_payload = _pr_payload_from_github(gh_client, pr_number)

    labels = pr_payload.get("labels") or []
    if SKIP_LABEL in labels:
        obs.add_event("skipped", note=SKIP_LABEL)
        return WorkflowResult(
            status="ok",
            summary=f"PR #{pr_number} carries `{SKIP_LABEL}` — skipped.",
            markdown="",
            artifacts={"skipped": True, "pr_number": pr_number},
        )

    from dataclasses import asdict

    result = triage.triage(
        triage.TriageInput(
            title=pr_payload.get("title", ""),
            body=pr_payload.get("body", ""),
            changed_files=list(pr_payload.get("changed_files") or []),
            entry_markdown=pr_payload.get("entry_markdown"),
        )
    )
    triage_dict = asdict(result)
    body = render_review_comment(pr_number=pr_number, triage_result=triage_dict)

    artifacts: dict[str, Any] = {
        "pr_number": pr_number,
        "triage": triage_dict,
    }

    verdict = triage_dict["verdict"]
    status = "ok" if verdict in {"merge", "needs-info"} else "warn"

    if post:
        if gh_client is None:
            obs.set_outcome("error", error_class="missing_gh_client")
            return WorkflowResult(
                status="error",
                summary="post=True but no GitHubClient provided",
                markdown=body,
                artifacts=artifacts,
            )
        action, record = upsert_pr_comment_by_marker(
            gh_client,
            pr_number=pr_number,
            marker=review_marker(pr_number),
            body=body,
        )
        artifacts["comment"] = {"action": action, "id": record.get("id"), "url": record.get("html_url")}
        obs.add_github_ref(record.get("html_url"))
        obs.add_event(f"comment-{action}")
        summary = f"Review comment {action} on PR #{pr_number} (verdict={verdict})"
    else:
        summary = f"Review dry-run for PR #{pr_number} (verdict={verdict})"

    if status == "warn":
        obs.set_outcome("degraded")
    return WorkflowResult(status=status, summary=summary, markdown=body, artifacts=artifacts)
