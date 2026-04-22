from repo_agent import tools as T


def test_list_sections_shape():
    out = T.list_sections()
    assert "files" in out and "top_level_sections" in out
    assert "README.md" in out["files"]


def test_get_rubric_shape():
    out = T.get_rubric()
    assert out["merge_threshold"] == 27
    assert out["max_score"] == 45
    assert isinstance(out["dimensions"], list)
    assert len(out["dimensions"]) == 7


def test_get_anti_patterns_shape():
    out = T.get_anti_patterns()
    assert out["patterns"], "expected anti-patterns list"
    assert "world-class" in out["hype_phrases"]


def test_search_entries_returns_results():
    out = T.search_entries("agent", limit=5)
    assert out["count"] >= 1
    assert len(out["results"]) <= 5
    for r in out["results"]:
        assert r["file"] and r["heading"]


def test_validate_entry_happy_path(fixtures_dir):
    entry = (fixtures_dir / "good-entry.md").read_text(encoding="utf-8")
    out = T.validate_entry(entry)
    assert "score" in out and "verdict" in out
    assert 0 <= out["score"] <= out["max_score"]


def test_validate_entry_blocks_marketing(fixtures_dir):
    entry = (fixtures_dir / "bad-entry.md").read_text(encoding="utf-8")
    out = T.validate_entry(entry)
    assert out["verdict"] == "block"


def test_propose_entry_uses_fixture_fetcher(monkeypatch, fixtures_dir):
    from repo_agent.skills import entry_draft

    html = (fixtures_dir / "sample-page.html").read_text(encoding="utf-8")
    monkeypatch.setattr(entry_draft, "default_fetcher", lambda url: html)

    out = T.propose_entry(
        url="https://example.com/framework",
        section="Orchestration Frameworks",
        rationale="Typed agent primitives with first-class memory.",
    )
    assert out["section"] == "Orchestration Frameworks"
    assert "Example Agent Framework" in out["draft_markdown"]
    assert "validation" in out
    assert out["metadata"]["title"] == "Example Agent Framework"
