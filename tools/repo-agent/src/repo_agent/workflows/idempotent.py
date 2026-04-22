"""Idempotent upsert helpers.

Both helpers find a prior record by a stable HTML-comment marker embedded in
the body and update it in place, or create a new record if none exists.

Each returns ``(status, record)`` where ``status`` is ``"created"`` or
``"updated"``.
"""

from __future__ import annotations

from typing import Any, Iterable

from .github import GitHubClient


def _find_by_marker(records: Iterable[dict[str, Any]], marker: str) -> dict[str, Any] | None:
    for r in records:
        body = r.get("body") or ""
        if marker in body:
            return r
    return None


def upsert_issue_by_marker(
    client: GitHubClient,
    *,
    marker: str,
    title: str,
    body: str,
    labels: Iterable[str] = (),
) -> tuple[str, dict[str, Any]]:
    """Create a new issue or update the existing one carrying ``marker``."""
    existing = _find_by_marker(client.list_issues_all(), marker)
    if existing:
        updated = client.update_issue(existing["number"], title=title, body=body)
        return "updated", updated
    created = client.create_issue(title=title, body=body, labels=labels)
    return "created", created


def upsert_pr_comment_by_marker(
    client: GitHubClient,
    *,
    pr_number: int,
    marker: str,
    body: str,
) -> tuple[str, dict[str, Any]]:
    """Create a new PR comment or update the existing one carrying ``marker``."""
    existing = _find_by_marker(client.list_pr_comments(pr_number), marker)
    if existing:
        updated = client.update_pr_comment(existing["id"], body)
        return "updated", updated
    created = client.create_pr_comment(pr_number, body)
    return "created", created
