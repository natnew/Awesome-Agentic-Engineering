"""Structured observability for repo-agent invocations.

Phase 12 — emits one JSON record per invocation (CLI subcommand, MCP tool call,
or workflow run). Records go to **stderr** by default; opt in to file output
via the ``REPO_AGENT_LOG_FILE`` environment variable or by passing ``log_file``
to :class:`Run` directly.

Stdlib only. No external log sink, no third-party telemetry. See
``specs/observability.md`` for the normative schema.
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
import time
import uuid
from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import IO, Any, Iterator, Mapping

LOG_SCHEMA_VERSION = 1

_VALID_COMPONENTS = frozenset({"cli", "mcp", "workflow"})
_VALID_OUTCOMES = frozenset({"ok", "error", "degraded"})


def make_run_id() -> str:
    """Return a fresh UUIDv4 string."""
    return str(uuid.uuid4())


def canonical_inputs_hash(payload: Mapping[str, Any]) -> str:
    """SHA-256 hex digest of canonical-JSON-serialised inputs.

    Canonical form: sorted keys, no whitespace, UTF-8. Non-JSON-serialisable
    inputs raise :class:`TypeError` (deliberate — callers must pre-convert
    anything exotic before hashing).
    """
    blob = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def _utc_now_iso() -> str:
    return datetime.now(tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _resolve_sink(log_file: str | os.PathLike[str] | None) -> tuple[IO[str], bool]:
    """Return (sink, owns_handle). Owned handles are closed by the caller."""
    path = log_file if log_file is not None else os.environ.get("REPO_AGENT_LOG_FILE") or None
    if path:
        return open(path, "a", encoding="utf-8"), True
    return sys.stderr, False


@dataclass
class Run:
    """Context manager that emits one log record on exit.

    Use as::

        with Run(component="cli", tool="search", inputs={"query": "agent"}) as r:
            ...
            r.add_github_ref("https://github.com/owner/repo/issues/1")

    On normal exit, ``outcome="ok"`` is emitted unless the caller called
    :meth:`set_outcome`. On exception, ``outcome="error"`` is emitted with
    ``error_class`` set to the exception's class name; the exception is **not**
    suppressed.
    """

    component: str
    tool: str
    inputs: Mapping[str, Any]
    llm_client: str = "stub"
    parent_run_id: str | None = None
    log_file: str | os.PathLike[str] | None = None
    run_id: str = field(default_factory=make_run_id)
    outcome: str = "ok"
    error_class: str | None = None
    github_refs: list[str] = field(default_factory=list)
    events: list[dict[str, Any]] = field(default_factory=list)
    _start: float = 0.0
    _ts: str = ""

    # ----------------------------------------------------------- mutators

    def add_github_ref(self, url: str | None) -> None:
        """Record a GitHub URL the agent wrote to on this run."""
        if isinstance(url, str) and url.startswith("https://"):
            self.github_refs.append(url)

    def add_event(self, kind: str, note: str | None = None) -> None:
        """Record a structured sub-event (e.g. ``stub-fallback``)."""
        self.events.append(
            {
                "ts": _utc_now_iso(),
                "kind": str(kind),
                "note": str(note) if note is not None else None,
            }
        )

    def set_outcome(self, outcome: str, error_class: str | None = None) -> None:
        if outcome not in _VALID_OUTCOMES:
            raise ValueError(f"invalid outcome: {outcome!r}")
        self.outcome = outcome
        self.error_class = str(error_class) if error_class is not None else None

    # ----------------------------------------------------------- emission

    def to_record(self, *, duration_ms: int) -> dict[str, Any]:
        return {
            "schema_version": LOG_SCHEMA_VERSION,
            "run_id": self.run_id,
            "parent_run_id": self.parent_run_id,
            "ts": self._ts,
            "duration_ms": duration_ms,
            "component": self.component,
            "tool": self.tool,
            "inputs_hash": canonical_inputs_hash(self.inputs),
            "llm_client": self.llm_client,
            "outcome": self.outcome,
            "error_class": self.error_class,
            "github_refs": list(self.github_refs),
            "events": list(self.events),
        }

    # ----------------------------------------------------------- context

    def __enter__(self) -> "Run":
        if self.component not in _VALID_COMPONENTS:
            raise ValueError(f"invalid component: {self.component!r}")
        self._start = time.monotonic()
        self._ts = _utc_now_iso()
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        if exc_type is not None and self.outcome == "ok":
            self.outcome = "error"
            self.error_class = exc_type.__name__
        duration_ms = int((time.monotonic() - self._start) * 1000)

        try:
            record = self.to_record(duration_ms=duration_ms)
            sink, owned = _resolve_sink(self.log_file)
            try:
                sink.write(json.dumps(record, ensure_ascii=False) + "\n")
                sink.flush()
            finally:
                if owned:
                    sink.close()
        except Exception:  # pragma: no cover - logging must never mask the user's error
            pass
        return None  # do not suppress


@contextmanager
def run_context(
    *,
    component: str,
    tool: str,
    inputs: Mapping[str, Any],
    **kwargs: Any,
) -> Iterator[Run]:
    """Convenience factory mirroring :class:`Run` as a function-style context."""
    r = Run(component=component, tool=tool, inputs=inputs, **kwargs)
    with r as ctx:
        yield ctx
