"""Workflow 6.2 — weekly landscape scan.

Composes:
    freshness.audit()  +  gh.list_recent_merged_prs()  +  gh.list_recent_issues()

Renders a single digest body and upserts a rolling issue by marker so the
weekly run updates one place instead of creating a new issue every Monday.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from ..observability import Run
from ..skills import freshness
from .base import WorkflowResult
from .github import GitHubClient
from .idempotent import upsert_issue_by_marker
from .render import LANDSCAPE_MARKER, render_landscape_digest

DIGEST_TITLE = "Weekly landscape scan — rolling digest"


def run(
    *,
    since_days: int = 7,
    gh_client: GitHubClient | None = None,
    dry_run: bool = False,
    now: datetime | None = None,
    threshold_months: int = 9,
) -> WorkflowResult:
    with Run(
        component="workflow",
        tool="workflow.landscape-scan",
        inputs={
            "since_days": int(since_days),
            "dry_run": bool(dry_run),
            "threshold_months": int(threshold_months),
        },
    ) as obs:
        return _run_inner(
            obs,
            since_days=since_days,
            gh_client=gh_client,
            dry_run=dry_run,
            now=now,
            threshold_months=threshold_months,
        )


def _run_inner(
    obs: Run,
    *,
    since_days: int,
    gh_client: GitHubClient | None,
    dry_run: bool,
    now: datetime | None,
    threshold_months: int,
) -> WorkflowResult:
    now = now or datetime.now(tz=timezone.utc)

    stale = [_stale_to_dict(s) for s in freshness.audit(threshold_months=threshold_months, now=now)]

    candidate_prs: list[dict[str, Any]] = []
    candidate_issues: list[dict[str, Any]] = []
    if gh_client is not None:
        for pr in gh_client.list_recent_merged_prs(since_days=since_days):
            candidate_prs.append(
                {
                    "number": pr["number"],
                    "title": pr["title"],
                    "html_url": pr["html_url"],
                    "merged_at": pr["merged_at"],
                }
            )
        for issue in gh_client.list_recent_issues(since_days=since_days):
            candidate_issues.append(
                {
                    "number": issue["number"],
                    "title": issue["title"],
                    "html_url": issue["html_url"],
                    "created_at": issue["created_at"],
                }
            )

    body = render_landscape_digest(
        generated_at=now.strftime("%Y-%m-%d %H:%M UTC"),
        stale=stale,
        candidate_prs=candidate_prs,
        candidate_issues=candidate_issues,
    )

    total = len(stale) + len(candidate_prs) + len(candidate_issues)
    artifacts: dict[str, Any] = {
        "stale_count": len(stale),
        "candidate_pr_count": len(candidate_prs),
        "candidate_issue_count": len(candidate_issues),
        "total": total,
    }

    if dry_run or gh_client is None:
        return WorkflowResult(
            status="ok",
            summary=f"Landscape scan dry-run: {total} candidate(s) ({len(stale)} stale, "
            f"{len(candidate_prs)} PRs, {len(candidate_issues)} issues)",
            markdown=body,
            artifacts=artifacts,
        )

    action, record = upsert_issue_by_marker(
        gh_client,
        marker=LANDSCAPE_MARKER,
        title=DIGEST_TITLE,
        body=body,
        labels=("phase-6", "landscape-scan"),
    )
    artifacts["issue"] = {"action": action, "number": record.get("number"), "url": record.get("html_url")}
    obs.add_github_ref(record.get("html_url"))
    obs.add_event(f"issue-{action}")
    return WorkflowResult(
        status="ok",
        summary=f"Landscape scan: {total} candidate(s); digest issue {action} (#{record.get('number')})",
        markdown=body,
        artifacts=artifacts,
    )


def _stale_to_dict(c: Any) -> dict[str, Any]:
    return {
        "file": c.file,
        "heading": c.heading,
        "last_reviewed": c.last_reviewed,
        "age_months": c.age_months,
        "reason": c.reason,
    }
