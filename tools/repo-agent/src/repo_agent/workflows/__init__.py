"""Phase 6 — agentic workflows.

Each workflow composes Phase 5 tools/skills into an end-to-end flow. Workflows
are read-only toward repo content: they may open/update issues and PR comments
(via the injected ``GitHubClient``) but never write to files in the repo.

The package exposes:

* :class:`WorkflowResult` — uniform return type for every workflow.
* :class:`Workflow` — minimal protocol a workflow must satisfy.
* :class:`GitHubClient` — small read + idempotent-upsert client.
* Three workflow entry points:
    - :mod:`repo_agent.workflows.new_tool`       (roadmap 6.1)
    - :mod:`repo_agent.workflows.landscape_scan` (roadmap 6.2)
    - :mod:`repo_agent.workflows.review_pr`      (roadmap 6.3)
"""

from __future__ import annotations

from .base import Workflow, WorkflowResult
from .github import GitHubClient
from .idempotent import upsert_issue_by_marker, upsert_pr_comment_by_marker

__all__ = [
    "Workflow",
    "WorkflowResult",
    "GitHubClient",
    "upsert_issue_by_marker",
    "upsert_pr_comment_by_marker",
]
