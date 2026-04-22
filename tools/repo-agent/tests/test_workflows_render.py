"""Tests for render.py (snapshot-lite: assert markers + key structural bits)."""

from __future__ import annotations

from repo_agent.workflows.render import (
    LANDSCAPE_MARKER,
    new_tool_marker,
    render_landscape_digest,
    render_new_tool_body,
    render_review_comment,
    render_scorecard,
    review_marker,
)


_FAKE_VALIDATION = {
    "score": 30,
    "max_score": 45,
    "per_dimension_raw": {"Reliability": 2, "Evidence": 2, "Agentic relevance": 3},
    "per_dimension": {"Reliability": 10, "Evidence": 8, "Agentic relevance": 12},
    "hard_gate_failures": [],
    "anti_pattern_hits": [],
    "evidence_tags": ["[official]"],
    "verdict": "merge",
    "notes": ["Looks good."],
}


def test_scorecard_renders_dimensions_and_total():
    out = render_scorecard(_FAKE_VALIDATION)
    assert "| Reliability | 2 | 10 |" in out
    assert "**30 / 45**" in out
    assert "[official]" in out


def test_scorecard_no_validation_returns_placeholder():
    assert "No validation data" in render_scorecard({})


def test_new_tool_body_contains_marker_and_draft():
    body = render_new_tool_body(
        url="https://example.com/x",
        section="Orchestration Frameworks",
        draft_markdown="- **[X](https://example.com/x)** — desc. _Last reviewed: April 2026._",
        validation=_FAKE_VALIDATION,
    )
    assert new_tool_marker("https://example.com/x") in body
    assert "## Draft entry for `https://example.com/x`" in body
    assert "```markdown" in body
    assert "Rubric scorecard" in body


def test_landscape_digest_marker_and_sections():
    stale = [{"file": "appendix/voice-agents.md", "last_reviewed": "June 2025", "age_months": 10, "reason": "stale"}]
    prs = [{"number": 1, "title": "Add X", "html_url": "https://example/pr/1", "merged_at": "2026-04-20T00:00:00Z"}]
    issues = [{"number": 2, "title": "Suggest Y", "html_url": "https://example/issue/2", "created_at": "2026-04-21T00:00:00Z"}]
    body = render_landscape_digest(
        generated_at="2026-04-22 09:00 UTC",
        stale=stale,
        candidate_prs=prs,
        candidate_issues=issues,
    )
    assert LANDSCAPE_MARKER in body
    assert "Stale entries" in body
    assert "Candidate additions from recent PRs" in body
    assert "Candidate additions from recent issues" in body
    assert "appendix/voice-agents.md" in body
    assert "#1 Add X" in body


def test_landscape_digest_empty_sections_render_none_line():
    body = render_landscape_digest(
        generated_at="now",
        stale=[],
        candidate_prs=[],
        candidate_issues=[],
    )
    assert body.count("_None this week._") == 3


def test_review_comment_marker_and_suggested_actions():
    triage = {
        "labels": ["area:content", "ready-for-review"],
        "verdict": "merge",
        "summary": "Score 30/45",
        "validation": _FAKE_VALIDATION,
    }
    body = render_review_comment(pr_number=7, triage_result=triage)
    assert review_marker(7) in body
    assert "Rubric review" in body
    assert "`merge`" in body
    assert "`area:content`" in body
    assert "Ready for a human reviewer" in body
    assert "skip-review-assistant" in body  # opt-out mention


def test_review_comment_needs_info_path():
    triage = {"labels": ["needs-entry-markdown"], "verdict": "needs-info", "summary": "No markdown block.", "validation": None}
    body = render_review_comment(pr_number=9, triage_result=triage)
    assert "fenced block" in body
