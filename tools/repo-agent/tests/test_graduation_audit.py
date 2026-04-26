"""Tests for Phase 13 graduation audit (`repo_agent.graduation`)."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

import httpx
import pytest

from repo_agent import graduation as G


FIXTURE = Path(__file__).parent / "fixtures" / "graduation" / "sample_runs.json"
AS_OF = datetime(2026, 4, 26, 0, 0, tzinfo=timezone.utc)


def _by_name(audits):
    return {a.workflow: a for a in audits}


# ---------------------------------------------------------------------------
# 1. Fixture round-trip
# ---------------------------------------------------------------------------
def test_audit_fixture_round_trip_covers_every_advisory_workflow():
    audits = G.audit_workflows(fixture=FIXTURE)
    names = [a.workflow for a in audits]
    assert names == list(G.ADVISORY_WORKFLOWS)
    assert len(audits) == 10
    by = _by_name(audits)
    # markdown-lint has 3 successful push runs in window: eligible.
    assert by["markdown-lint"].eligible is True
    assert by["markdown-lint"].green == by["markdown-lint"].runs == 3
    # link-check-pr has a failure in window: not eligible.
    assert by["link-check-pr"].eligible is False
    assert "non-success" in by["link-check-pr"].notes


# ---------------------------------------------------------------------------
# 2. 30-day window edges
# ---------------------------------------------------------------------------
@pytest.mark.parametrize(
    "as_of_iso, expected_runs",
    [
        # Sample has a markdown-lint run on 2026-03-28. Window = 30 days.
        # as_of 2026-04-26 -> earliest in-window 2026-03-27 -> all 3 included.
        ("2026-04-26T00:00:00Z", 3),
        # Move as_of forward by 2 days -> earliest in-window 2026-03-29 ->
        # the 2026-03-28 run drops off, leaving 2.
        ("2026-04-28T00:00:00Z", 2),
    ],
)
def test_audit_window_edge_drops_runs_outside_30_days(as_of_iso, expected_runs):
    audits = G.audit_workflows(
        fixture=FIXTURE,
        as_of=datetime.fromisoformat(as_of_iso.replace("Z", "+00:00")),
    )
    assert _by_name(audits)["markdown-lint"].runs == expected_runs


# ---------------------------------------------------------------------------
# 3. Determinism: all-green workflow is eligible
# ---------------------------------------------------------------------------
def test_audit_all_green_workflow_is_eligible():
    audits = G.audit_workflows(fixture=FIXTURE)
    a = _by_name(audits)["link-check-scheduled"]
    assert a.runs == 4
    assert a.green == 4
    assert a.eligible is True
    assert a.consecutive_green_days == G.WINDOW_DAYS


# ---------------------------------------------------------------------------
# 4. Single failure disqualifies and resets the consecutive-green count
# ---------------------------------------------------------------------------
def test_audit_single_failure_disqualifies():
    audits = G.audit_workflows(fixture=FIXTURE)
    a = _by_name(audits)["link-check-pr"]
    assert a.runs == 2
    assert a.green == 1
    assert a.consecutive_green_days == 0
    assert a.eligible is False


# ---------------------------------------------------------------------------
# 5. Live path: pagination + non-main / non-push exclusion
# ---------------------------------------------------------------------------
def test_audit_live_paginates_and_filters_branch_and_event():
    """Live mode must paginate workflow runs and exclude non-main / non-{push,schedule}."""
    pages_served = {"runs": 0}

    def handler(request: httpx.Request) -> httpx.Response:
        path = request.url.path
        if path.endswith("/actions/workflows"):
            return httpx.Response(
                200,
                json={"workflows": [{"id": 42, "name": "markdown-lint"}]},
            )
        if "/actions/workflows/42/runs" in path:
            pages_served["runs"] += 1
            page = int(request.url.params.get("page", "1"))
            if page == 1:
                # 100 runs forces a second page; 50 main+push successes,
                # 50 non-qualifying records that must be filtered out.
                main_runs = [
                    {
                        "head_branch": "main",
                        "event": "push",
                        "conclusion": "success",
                        "created_at": "2026-04-20T00:00:00Z",
                    }
                ] * 50
                noise = [
                    {
                        "head_branch": "feature/x",
                        "event": "pull_request",
                        "conclusion": "success",
                        "created_at": "2026-04-20T00:00:00Z",
                    }
                ] * 50
                return httpx.Response(200, json={"workflow_runs": main_runs + noise})
            # Page 2: a few more main pushes, then stop (< per_page).
            tail = [
                {
                    "head_branch": "main",
                    "event": "push",
                    "conclusion": "success",
                    "created_at": "2026-04-21T00:00:00Z",
                }
            ] * 5
            return httpx.Response(200, json={"workflow_runs": tail})
        return httpx.Response(404)

    client = httpx.Client(transport=httpx.MockTransport(handler), base_url="https://api.github.com")
    audits = G.audit_workflows(
        client=client,
        repo="natnew/test-repo",
        as_of=AS_OF,
        workflows=("markdown-lint",),
    )
    client.close()

    assert pages_served["runs"] == 2  # paginated
    a = audits[0]
    # 50 main+push (page 1) + 5 main+push (page 2) = 55. Noise filtered out.
    assert a.runs == 55
    assert a.green == 55
    assert a.eligible is True


# ---------------------------------------------------------------------------
# 6. JSON output schema
# ---------------------------------------------------------------------------
def test_audit_json_output_schema():
    audits = G.audit_workflows(fixture=FIXTURE)
    payload = json.loads(G.to_json(audits))
    assert isinstance(payload, list) and len(payload) == 10
    required = {"workflow", "runs", "green", "consecutive_green_days", "eligible", "notes"}
    for row in payload:
        assert set(row.keys()) == required
        assert isinstance(row["workflow"], str)
        assert isinstance(row["runs"], int)
        assert isinstance(row["green"], int)
        assert isinstance(row["consecutive_green_days"], int)
        assert isinstance(row["eligible"], bool)
        assert isinstance(row["notes"], str)


# ---------------------------------------------------------------------------
# Bonus: input-mode validation
# ---------------------------------------------------------------------------
def test_audit_requires_exactly_one_input_mode():
    with pytest.raises(ValueError):
        G.audit_workflows()  # neither
    with pytest.raises(ValueError):
        G.audit_workflows(fixture=FIXTURE, client=httpx.Client())  # both


def test_audit_table_output_is_markdown():
    audits = G.audit_workflows(fixture=FIXTURE)
    table = G.to_table(audits)
    assert table.startswith("| workflow ")
    # Header + separator + 10 data rows.
    assert len(table.splitlines()) == 12
    # Every advisory workflow appears.
    for name in G.ADVISORY_WORKFLOWS:
        assert re.search(rf"\| `{re.escape(name)}` \|", table)
