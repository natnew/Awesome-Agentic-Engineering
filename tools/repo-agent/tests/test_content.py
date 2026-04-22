from repo_agent.content import build_index


def test_index_includes_readme_and_appendix(repo_root):
    idx = build_index(repo_root)
    assert "README.md" in idx.files
    assert any(f.startswith("appendix/") for f in idx.files)


def test_sections_have_headings_and_lines(repo_root):
    idx = build_index(repo_root)
    assert idx.sections, "expected at least one section"
    for s in idx.sections[:5]:
        assert s.heading
        assert s.start_line >= 1
        assert s.end_line >= s.start_line
        assert s.file


def test_search_finds_known_term(repo_root):
    idx = build_index(repo_root)
    results = idx.search("agent")
    assert results, "search for 'agent' should return results in this repo"


def test_search_empty_query_returns_empty(repo_root):
    idx = build_index(repo_root)
    assert idx.search("") == []


def test_last_reviewed_parsed_when_present(repo_root):
    idx = build_index(repo_root)
    # At least one section somewhere in the repo should carry the marker.
    marked = [s for s in idx.sections if s.last_reviewed]
    assert marked, "expected at least one section with a Last reviewed marker"
    # Format should be 'Month YYYY'
    assert all(len(s.last_reviewed.split()) == 2 for s in marked)
