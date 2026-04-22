"""Workflow 6.1 — new-tool: URL -> rubric-aligned draft entry.

Chains:
    fetch(url) -> skills.entry_draft.draft -> validate -> rendered markdown.

Read-only toward content. With ``--open-issue`` the rendered body is upserted
into a per-URL tracking issue so humans have one stable place to discuss the
proposed entry.
"""

from __future__ import annotations

from dataclasses import asdict
from typing import Any, Callable

from ..skills import entry_draft
from .base import WorkflowResult
from .github import GitHubClient
from .idempotent import upsert_issue_by_marker
from .render import new_tool_marker, render_new_tool_body

Fetcher = Callable[[str], str]


def run(
    *,
    url: str,
    section: str,
    rationale: str = "",
    fetcher: Fetcher | None = None,
    gh_client: GitHubClient | None = None,
    open_issue: bool = False,
) -> WorkflowResult:
    draft_result = entry_draft.draft(
        url=url,
        section=section,
        rationale=rationale,
        fetcher=fetcher,
    )
    draft_dict = asdict(draft_result)

    body = render_new_tool_body(
        url=url,
        section=section,
        draft_markdown=draft_result.draft_markdown,
        validation=draft_dict["validation"],
    )

    artifacts: dict[str, Any] = {
        "url": url,
        "section": section,
        "draft": draft_dict,
    }

    verdict = draft_dict["validation"].get("verdict", "unknown")
    status = "ok" if verdict == "merge" else "warn"

    if open_issue:
        if gh_client is None:
            return WorkflowResult(
                status="error",
                summary="open_issue=True but no GitHubClient provided",
                markdown=body,
                artifacts=artifacts,
            )
        action, record = upsert_issue_by_marker(
            gh_client,
            marker=new_tool_marker(url),
            title=f"Draft entry candidate: {draft_result.metadata.get('title') or url}",
            body=body,
            labels=("phase-6", "candidate-entry"),
        )
        artifacts["issue"] = {"action": action, "number": record.get("number"), "url": record.get("html_url")}
        summary = f"Drafted entry for {url} (verdict={verdict}); issue {action} (#{record.get('number')})"
    else:
        summary = f"Drafted entry for {url} (verdict={verdict}); dry-run (no issue opened)"

    return WorkflowResult(status=status, summary=summary, markdown=body, artifacts=artifacts)
