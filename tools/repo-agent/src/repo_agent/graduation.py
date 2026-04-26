"""Phase 13 — Graduation: Advisory → Required.

`audit_workflows` aggregates GitHub Actions ``workflow_run`` records into a
per-workflow eligibility verdict for graduation from advisory to required.

Pure function. Two input modes:

* **Fixture** — pass a path to a JSON document shaped like
  ``tests/fixtures/graduation/sample_runs.json``. Offline; the default for CI
  and local runs.
* **Live** — pass an ``httpx.Client`` already configured against the GitHub
  API. Reads only; requires ``GITHUB_TOKEN`` for higher rate limits but works
  unauthenticated against public repos.

Eligibility (see ``specs/2026-04-26-phase-13-graduation-advisory-to-required/plan.md``):

* Window = 30 calendar days ending at ``as_of`` (UTC).
* Population = ``workflow_run`` records with ``head_branch == "main"`` and
  ``event in {"push", "schedule"}``.
* ``green`` = ``conclusion == "success"``.
* ``eligible`` requires ``runs >= 1`` AND ``green == runs`` AND
  ``consecutive_green_days`` covers the full 30-day window.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Iterable

import httpx

WINDOW_DAYS = 30
ALLOWED_EVENTS = frozenset({"push", "schedule"})
TARGET_BRANCH = "main"

# The 10 advisory workflows on `main` as of Phase 12 close.
# Order is deterministic and used for the audit table.
ADVISORY_WORKFLOWS: tuple[str, ...] = (
    "markdown-lint",
    "link-check-pr",
    "link-check-scheduled",
    "stale-entry-detector",
    "repo-agent-tests",
    "phase-6-new-tool",
    "phase-6-landscape-scan",
    "phase-6-review-pr",
    "phase-7-publish-site",
    "phase-7-render-check",
)


@dataclass(frozen=True)
class WorkflowAudit:
    """Per-workflow eligibility verdict over a 30-day window."""

    workflow: str
    runs: int
    green: int
    consecutive_green_days: int
    eligible: bool
    notes: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _parse_iso(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def _within_window(created_at: str, as_of: datetime) -> bool:
    dt = _parse_iso(created_at)
    return as_of - timedelta(days=WINDOW_DAYS) <= dt <= as_of


def _qualifies(run: dict[str, Any]) -> bool:
    return (
        run.get("head_branch") == TARGET_BRANCH
        and run.get("event") in ALLOWED_EVENTS
    )


def _consecutive_green_days(runs: list[dict[str, Any]], as_of: datetime) -> int:
    """Number of trailing days (ending at ``as_of``) with no failure.

    A day with zero qualifying runs counts as green for ``schedule``-triggered
    workflows (they are not expected to run every day) — we only fail on an
    explicit non-success conclusion. A failing run anywhere in the window
    resets the count to 0.
    """
    for run in runs:
        if run.get("conclusion") not in (None, "success"):
            return 0
    # All qualifying runs in the window were green: the count equals the
    # full window length.
    return WINDOW_DAYS if runs else 0


def _audit_one(workflow: str, runs: list[dict[str, Any]], as_of: datetime) -> WorkflowAudit:
    qualifying = [r for r in runs if _qualifies(r) and _within_window(r["created_at"], as_of)]
    total = len(qualifying)
    green = sum(1 for r in qualifying if r.get("conclusion") == "success")
    consecutive = _consecutive_green_days(qualifying, as_of)
    notes = ""
    if total == 0:
        notes = "no qualifying runs in window — needs synthetic green run before flip"
        eligible = False
    elif green < total:
        notes = f"{total - green} non-success run(s) in window"
        eligible = False
    else:
        eligible = consecutive >= WINDOW_DAYS
    return WorkflowAudit(
        workflow=workflow,
        runs=total,
        green=green,
        consecutive_green_days=consecutive,
        eligible=eligible,
        notes=notes,
    )


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------


def audit_workflows(
    *,
    fixture: Path | str | None = None,
    client: httpx.Client | None = None,
    repo: str | None = None,
    as_of: datetime | None = None,
    workflows: Iterable[str] = ADVISORY_WORKFLOWS,
) -> list[WorkflowAudit]:
    """Audit the listed workflows over the 30-day window.

    Exactly one of ``fixture`` or ``client`` must be supplied.
    """
    if (fixture is None) == (client is None):
        raise ValueError("Pass exactly one of fixture or client.")

    if fixture is not None:
        data = json.loads(Path(fixture).read_text(encoding="utf-8"))
        as_of = as_of or _parse_iso(data["as_of"])
        runs_by_name = _group_fixture_runs(data)
    else:
        if not repo:
            raise ValueError("Live mode requires repo='owner/name'.")
        as_of = as_of or datetime.now(tz=timezone.utc)
        runs_by_name = _fetch_runs(client, repo, as_of, workflows)

    return [_audit_one(name, runs_by_name.get(name, []), as_of) for name in workflows]


def _group_fixture_runs(data: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    by_id = {wf["id"]: wf["name"] for wf in data["workflows"]}
    out: dict[str, list[dict[str, Any]]] = {name: [] for name in by_id.values()}
    for run in data["runs"]:
        name = by_id.get(run["workflow_id"])
        if name is not None:
            out[name].append(run)
    return out


def _fetch_runs(
    client: httpx.Client,
    repo: str,
    as_of: datetime,
    workflows: Iterable[str],
) -> dict[str, list[dict[str, Any]]]:
    """Live path — paginate the Actions API for each named workflow."""
    since = as_of - timedelta(days=WINDOW_DAYS)
    created_filter = f">={since.strftime('%Y-%m-%dT%H:%M:%SZ')}"

    # 1. List workflows to resolve name -> id.
    r = client.get(f"/repos/{repo}/actions/workflows", params={"per_page": 100})
    r.raise_for_status()
    name_to_id = {wf["name"]: wf["id"] for wf in r.json().get("workflows", [])}

    out: dict[str, list[dict[str, Any]]] = {}
    for name in workflows:
        wf_id = name_to_id.get(name)
        if wf_id is None:
            out[name] = []
            continue
        out[name] = _paginate_runs(client, repo, wf_id, created_filter)
    return out


def _paginate_runs(
    client: httpx.Client,
    repo: str,
    workflow_id: int,
    created_filter: str,
) -> list[dict[str, Any]]:
    runs: list[dict[str, Any]] = []
    page = 1
    while True:
        r = client.get(
            f"/repos/{repo}/actions/workflows/{workflow_id}/runs",
            params={
                "branch": TARGET_BRANCH,
                "created": created_filter,
                "per_page": 100,
                "page": page,
            },
        )
        r.raise_for_status()
        body = r.json()
        items = body.get("workflow_runs", [])
        runs.extend(items)
        if len(items) < 100:
            break
        page += 1
    return runs


# ---------------------------------------------------------------------------
# Output helpers
# ---------------------------------------------------------------------------


def to_json(audits: list[WorkflowAudit]) -> str:
    return json.dumps([a.to_dict() for a in audits], indent=2)


def to_table(audits: list[WorkflowAudit]) -> str:
    """Render a Markdown table matching the manual audit artefact."""
    header = (
        "| workflow | runs (30d) | green | consecutive_green_days | eligible | notes |\n"
        "|---|---:|---:|---:|---|---|"
    )
    rows = [
        f"| `{a.workflow}` | {a.runs} | {a.green} | {a.consecutive_green_days} "
        f"| {'yes' if a.eligible else 'no'} | {a.notes or '—'} |"
        for a in audits
    ]
    return "\n".join([header, *rows])
