"""Tiny GitHub REST client for Phase 6 workflows.

Scope is deliberately minimal: only the calls the three workflows need.

* List recent merged PRs
* List recent issues
* List / create / update issues (for the weekly digest)
* List / create / update PR review comments (for 6.3)

All calls go through an injected :class:`httpx.Client`, which makes tests
trivial via ``httpx.MockTransport`` and keeps the network gated in one place.

Auth: reads ``GITHUB_TOKEN`` from the environment if a caller does not pass
``token`` explicitly. When no token is available, the client still works for
read-only calls against public repos (rate-limited) and raises clearly on
writes.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Iterable

import httpx

GITHUB_API = "https://api.github.com"


class GitHubWriteError(RuntimeError):
    """Raised when a write call is attempted without a usable token."""


@dataclass
class RepoRef:
    owner: str
    name: str

    @property
    def slug(self) -> str:
        return f"{self.owner}/{self.name}"

    @classmethod
    def parse(cls, value: str) -> "RepoRef":
        if "/" not in value:
            raise ValueError(f"Expected 'owner/name', got {value!r}")
        owner, name = value.split("/", 1)
        return cls(owner=owner, name=name)


class GitHubClient:
    """Thin wrapper with just the endpoints Phase 6 needs."""

    def __init__(
        self,
        repo: RepoRef | str,
        *,
        client: httpx.Client | None = None,
        token: str | None = None,
    ) -> None:
        self.repo = RepoRef.parse(repo) if isinstance(repo, str) else repo
        self._token = token if token is not None else os.environ.get("GITHUB_TOKEN")
        headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "repo-agent-phase6/0.1",
        }
        if self._token:
            headers["Authorization"] = f"Bearer {self._token}"
        self._client = client or httpx.Client(
            base_url=GITHUB_API, headers=headers, timeout=15.0
        )
        # When the caller injected a client, patch headers in-place so tests can
        # assert auth behaviour without constructing a full client each time.
        if client is not None:
            for k, v in headers.items():
                self._client.headers.setdefault(k, v)

    # ------------------------------------------------------------------ reads
    def list_recent_merged_prs(self, since_days: int = 7, per_page: int = 30) -> list[dict[str, Any]]:
        r = self._client.get(
            f"/repos/{self.repo.slug}/pulls",
            params={"state": "closed", "sort": "updated", "direction": "desc", "per_page": per_page},
        )
        r.raise_for_status()
        items = r.json()
        from datetime import datetime, timedelta, timezone

        cutoff = datetime.now(tz=timezone.utc) - timedelta(days=since_days)
        out: list[dict[str, Any]] = []
        for pr in items:
            merged_at = pr.get("merged_at")
            if not merged_at:
                continue
            dt = datetime.fromisoformat(merged_at.replace("Z", "+00:00"))
            if dt >= cutoff:
                out.append(pr)
        return out

    def list_recent_issues(self, since_days: int = 7, per_page: int = 30) -> list[dict[str, Any]]:
        r = self._client.get(
            f"/repos/{self.repo.slug}/issues",
            params={"state": "open", "sort": "created", "direction": "desc", "per_page": per_page},
        )
        r.raise_for_status()
        from datetime import datetime, timedelta, timezone

        cutoff = datetime.now(tz=timezone.utc) - timedelta(days=since_days)
        out: list[dict[str, Any]] = []
        for issue in r.json():
            # The /issues endpoint also returns PRs; filter them out.
            if "pull_request" in issue:
                continue
            created = issue.get("created_at")
            if not created:
                continue
            dt = datetime.fromisoformat(created.replace("Z", "+00:00"))
            if dt >= cutoff:
                out.append(issue)
        return out

    def list_issues_all(self, per_page: int = 100) -> list[dict[str, Any]]:
        """List open issues (PRs filtered out). Used by marker upsert to find an existing digest."""
        r = self._client.get(
            f"/repos/{self.repo.slug}/issues",
            params={"state": "open", "per_page": per_page},
        )
        r.raise_for_status()
        return [i for i in r.json() if "pull_request" not in i]

    def list_pr_comments(self, pr_number: int, per_page: int = 100) -> list[dict[str, Any]]:
        r = self._client.get(
            f"/repos/{self.repo.slug}/issues/{pr_number}/comments",
            params={"per_page": per_page},
        )
        r.raise_for_status()
        return r.json()

    # ----------------------------------------------------------------- writes
    def _require_token(self) -> None:
        if not self._token:
            raise GitHubWriteError(
                "No GITHUB_TOKEN available — refusing to write. "
                "Use --dry-run or pass a token explicitly."
            )

    def create_issue(self, title: str, body: str, labels: Iterable[str] = ()) -> dict[str, Any]:
        self._require_token()
        r = self._client.post(
            f"/repos/{self.repo.slug}/issues",
            json={"title": title, "body": body, "labels": list(labels)},
        )
        r.raise_for_status()
        return r.json()

    def update_issue(self, issue_number: int, *, title: str | None = None, body: str | None = None) -> dict[str, Any]:
        self._require_token()
        payload: dict[str, Any] = {}
        if title is not None:
            payload["title"] = title
        if body is not None:
            payload["body"] = body
        r = self._client.patch(
            f"/repos/{self.repo.slug}/issues/{issue_number}",
            json=payload,
        )
        r.raise_for_status()
        return r.json()

    def create_pr_comment(self, pr_number: int, body: str) -> dict[str, Any]:
        self._require_token()
        r = self._client.post(
            f"/repos/{self.repo.slug}/issues/{pr_number}/comments",
            json={"body": body},
        )
        r.raise_for_status()
        return r.json()

    def update_pr_comment(self, comment_id: int, body: str) -> dict[str, Any]:
        self._require_token()
        r = self._client.patch(
            f"/repos/{self.repo.slug}/issues/comments/{comment_id}",
            json={"body": body},
        )
        r.raise_for_status()
        return r.json()
