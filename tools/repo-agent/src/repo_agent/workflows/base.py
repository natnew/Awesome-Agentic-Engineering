"""Base types shared by every Phase 6 workflow."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Protocol

Status = str  # "ok" | "warn" | "error"


@dataclass
class WorkflowResult:
    """Uniform return type for every workflow entry point.

    Attributes:
        status: ``"ok"``, ``"warn"`` (ran but surfaced a soft issue), or ``"error"``.
        summary: One-line human summary, safe for logs and CI output.
        markdown: Rendered markdown body (issue/comment body or CLI stdout).
        artifacts: Arbitrary JSON-serialisable extras for callers/tests.
    """

    status: Status
    summary: str
    markdown: str = ""
    artifacts: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class Workflow(Protocol):
    """Every workflow module exposes a ``run(...) -> WorkflowResult`` function."""

    def run(self, *args: Any, **kwargs: Any) -> WorkflowResult:  # pragma: no cover - protocol
        ...
