"""Phase 12 — log record schema is well-formed end-to-end.

Runs ``workflows.landscape_scan`` against an httpx ``MockTransport`` so the
upsert-by-marker code path exercises ``add_github_ref``. Captures the JSON
record via ``REPO_AGENT_LOG_FILE`` and asserts every required field is
present, well-typed, and matches the documented enum / regex shape.
"""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone

import httpx

from repo_agent.workflows import landscape_scan
from repo_agent.workflows.github import GitHubClient
from tests.test_workflows_base import _MockState

UUID_V4 = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$")
SHA256_HEX = re.compile(r"^[0-9a-f]{64}$")
ISO_8601_Z = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")

NOW = datetime(2026, 4, 22, 9, 0, tzinfo=timezone.utc)

REQUIRED_FIELDS = {
    "schema_version": int,
    "run_id": str,
    "ts": str,
    "duration_ms": int,
    "component": str,
    "tool": str,
    "inputs_hash": str,
    "llm_client": str,
    "outcome": str,
    "github_refs": list,
    "events": list,
}

VALID_COMPONENTS = {"cli", "mcp", "workflow"}
VALID_OUTCOMES = {"ok", "error", "degraded"}


def _gh_client():
    state = _MockState()
    state.issues = []

    def handler(request: httpx.Request) -> httpx.Response:
        path = request.url.path
        method = request.method
        if method == "GET" and path.endswith("/pulls"):
            return httpx.Response(200, json=[])
        return state.handler(request)

    transport = httpx.MockTransport(handler)
    http = httpx.Client(transport=transport, base_url="https://api.github.com")
    return GitHubClient("natnew/test-repo", client=http, token="t")


def _read_records(path) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def test_workflow_emits_one_well_formed_record(tmp_path, monkeypatch):
    log_path = tmp_path / "obs.jsonl"
    monkeypatch.setenv("REPO_AGENT_LOG_FILE", str(log_path))

    gh = _gh_client()
    result = landscape_scan.run(since_days=7, gh_client=gh, now=NOW, threshold_months=9)
    assert result.status == "ok"

    records = _read_records(log_path)
    assert len(records) == 1, f"expected exactly one record, got {len(records)}"
    rec = records[0]

    # Required fields present and correctly typed.
    for field, ftype in REQUIRED_FIELDS.items():
        assert field in rec, f"missing field: {field}"
        assert isinstance(rec[field], ftype), f"{field}: expected {ftype}, got {type(rec[field])}"

    # parent_run_id and error_class are required-but-nullable.
    assert "parent_run_id" in rec and (rec["parent_run_id"] is None or isinstance(rec["parent_run_id"], str))
    assert "error_class" in rec and (rec["error_class"] is None or isinstance(rec["error_class"], str))

    # Shape constraints.
    assert UUID_V4.match(rec["run_id"]), rec["run_id"]
    assert SHA256_HEX.match(rec["inputs_hash"]), rec["inputs_hash"]
    assert ISO_8601_Z.match(rec["ts"]), rec["ts"]
    assert rec["component"] in VALID_COMPONENTS
    assert rec["outcome"] in VALID_OUTCOMES
    assert rec["llm_client"] == "stub" or rec["llm_client"].startswith("live:")
    assert rec["tool"] == "workflow.landscape-scan"
    assert rec["component"] == "workflow"
    assert rec["duration_ms"] >= 0
    assert rec["schema_version"] == 1

    # github_refs: the upsert created a digest issue, so we expect exactly one
    # https URL recorded by the workflow's add_github_ref call.
    assert len(rec["github_refs"]) == 1
    assert rec["github_refs"][0].startswith("https://")


def test_dry_run_records_no_github_refs(tmp_path, monkeypatch):
    log_path = tmp_path / "obs.jsonl"
    monkeypatch.setenv("REPO_AGENT_LOG_FILE", str(log_path))

    result = landscape_scan.run(dry_run=True, now=NOW, threshold_months=9)
    assert result.status == "ok"

    records = _read_records(log_path)
    assert len(records) == 1
    assert records[0]["github_refs"] == []
    assert records[0]["outcome"] == "ok"


def test_record_does_not_leak_secret_strings(tmp_path, monkeypatch):
    log_path = tmp_path / "obs.jsonl"
    monkeypatch.setenv("REPO_AGENT_LOG_FILE", str(log_path))

    gh = _gh_client()
    landscape_scan.run(since_days=7, gh_client=gh, now=NOW, threshold_months=9)

    raw = log_path.read_text(encoding="utf-8")
    for needle in ("ghp_", "sk-", "Bearer ", "test-token"):
        assert needle not in raw, f"log leaked {needle!r}"


def test_inputs_hash_changes_when_inputs_change(tmp_path, monkeypatch):
    log_path = tmp_path / "obs.jsonl"
    monkeypatch.setenv("REPO_AGENT_LOG_FILE", str(log_path))

    landscape_scan.run(since_days=7, dry_run=True, now=NOW, threshold_months=9)
    landscape_scan.run(since_days=14, dry_run=True, now=NOW, threshold_months=9)
    landscape_scan.run(since_days=7, dry_run=True, now=NOW, threshold_months=9)

    records = _read_records(log_path)
    assert len(records) == 3
    assert records[0]["inputs_hash"] == records[2]["inputs_hash"]
    assert records[0]["inputs_hash"] != records[1]["inputs_hash"]
