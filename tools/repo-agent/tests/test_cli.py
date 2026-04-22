import io
import json
import sys

from repo_agent.cli import main


def _run(args, monkeypatch):
    buf = io.StringIO()
    monkeypatch.setattr(sys, "stdout", buf)
    rc = main(args)
    return rc, buf.getvalue()


def test_cli_rubric(monkeypatch):
    rc, out = _run(["rubric"], monkeypatch)
    assert rc == 0
    data = json.loads(out)
    assert data["merge_threshold"] == 27


def test_cli_list_sections(monkeypatch):
    rc, out = _run(["list-sections"], monkeypatch)
    assert rc == 0
    data = json.loads(out)
    assert "README.md" in data["files"]


def test_cli_search(monkeypatch):
    rc, out = _run(["search", "agent", "--limit", "3"], monkeypatch)
    assert rc == 0
    data = json.loads(out)
    assert data["count"] >= 1
    assert len(data["results"]) <= 3


def test_cli_freshness(monkeypatch):
    rc, out = _run(["freshness", "--threshold", "9"], monkeypatch)
    assert rc == 0
    data = json.loads(out)
    assert data["threshold_months"] == 9


def test_cli_triage_fixture(monkeypatch, fixtures_dir):
    rc, out = _run(["triage", "--fixture", str(fixtures_dir / "sample-pr.json")], monkeypatch)
    assert rc == 0
    data = json.loads(out)
    assert data["verdict"] in {"merge", "request-changes", "block"}


def test_cli_validate_file(monkeypatch, fixtures_dir):
    rc, out = _run(
        ["validate", "--file", str(fixtures_dir / "bad-entry.md")], monkeypatch
    )
    assert rc == 0
    data = json.loads(out)
    assert data["verdict"] == "block"
