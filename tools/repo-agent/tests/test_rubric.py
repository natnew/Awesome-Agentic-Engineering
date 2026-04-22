from repo_agent.rubric import load_policy, score_entry


def test_rubric_loads_seven_dimensions(repo_root):
    policy = load_policy(repo_root)
    assert len(policy.rubric.dimensions) == 7
    names = {d.name for d in policy.rubric.dimensions}
    assert "Reliability" in names
    assert "Evidence" in names
    assert "Agentic relevance" in names


def test_rubric_max_score_is_45(repo_root):
    policy = load_policy(repo_root)
    assert policy.rubric.max_score == 45
    assert policy.rubric.merge_threshold == 27


def test_rubric_source_hash_is_stable(repo_root):
    a = load_policy(repo_root).rubric.source_hash
    b = load_policy(repo_root).rubric.source_hash
    assert a == b and len(a) == 12


def test_anti_patterns_loaded(repo_root):
    policy = load_policy(repo_root)
    assert policy.anti_patterns, "expected anti-patterns to parse"


def test_good_entry_scores_above_threshold(repo_root, fixtures_dir):
    policy = load_policy(repo_root)
    entry = (fixtures_dir / "good-entry.md").read_text(encoding="utf-8")
    v = score_entry(entry, policy)
    assert v.verdict in {"merge", "request-changes"}  # no hard-gate fail
    assert not v.hard_gate_failures
    assert v.evidence_tags, "good entry should carry evidence tags"


def test_bad_entry_is_blocked_or_flagged(repo_root, fixtures_dir):
    policy = load_policy(repo_root)
    entry = (fixtures_dir / "bad-entry.md").read_text(encoding="utf-8")
    v = score_entry(entry, policy)
    # Bad entry has no evidence tags → Evidence=0 → hard-gate failure
    assert "Evidence" in v.hard_gate_failures
    assert v.verdict == "block"
    # Marketing phrases flagged
    phrases = {h.phrase for h in v.anti_pattern_hits}
    assert "world-class" in phrases or "world class" in phrases
    assert "state-of-the-art" in phrases or "state of the art" in phrases
    assert "revolutionary" in phrases
    assert "trending on github" in phrases
    assert "stars-as-evidence" in phrases
