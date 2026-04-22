import json

from repo_agent import tools as T
from repo_agent.skills import entry_draft


def test_triage_with_entry_markdown(fixtures_dir):
    payload = json.loads((fixtures_dir / "sample-pr.json").read_text(encoding="utf-8"))
    out = T.triage_pr(
        title=payload["title"],
        body=payload["body"],
        changed_files=payload["changed_files"],
    )
    assert out["verdict"] in {"merge", "request-changes", "block"}
    assert "area:content" in out["labels"]
    assert out["validation"] is not None


def test_triage_without_entry_requests_info():
    out = T.triage_pr(title="Refactor CI", body="No entry here.", changed_files=[".github/workflows/x.yml"])
    assert out["verdict"] == "needs-info"
    assert "needs-entry-markdown" in out["labels"]
    assert "area:infra" in out["labels"]


def test_freshness_audit_runs_on_repo():
    out = T.freshness_audit(threshold_months=9)
    assert "candidates" in out
    assert out["threshold_months"] == 9
    # Deterministic: stale candidates come before missing-marker
    kinds = [c["reason"] for c in out["candidates"]]
    stale_idx = [i for i, k in enumerate(kinds) if k == "stale"]
    miss_idx = [i for i, k in enumerate(kinds) if k == "missing-marker"]
    if stale_idx and miss_idx:
        assert max(stale_idx) < min(miss_idx)


def test_entry_draft_extracts_metadata(fixtures_dir):
    html = (fixtures_dir / "sample-page.html").read_text(encoding="utf-8")
    meta = entry_draft.extract_metadata("https://example.com", html)
    assert meta.title == "Example Agent Framework"
    assert "typed" in meta.description.lower()


def test_entry_draft_self_validates(fixtures_dir):
    html = (fixtures_dir / "sample-page.html").read_text(encoding="utf-8")
    result = entry_draft.draft(
        url="https://example.com",
        section="Orchestration Frameworks",
        rationale="Adds typed memory primitives absent elsewhere in the list.",
        fetcher=lambda _url: html,
    )
    assert result.draft_markdown
    assert "validation" in result.__dict__
    # The draft includes an [official] tag, so Evidence should not hard-fail.
    v = result.validation
    assert "Evidence" not in v["hard_gate_failures"]
