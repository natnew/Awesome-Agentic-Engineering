from repo_agent.llm import StubLLMClient, default_client


def test_stub_returns_placeholder_for_schema():
    c = default_client()
    out = c.complete("hello", {"title": "string", "tags": "list[string]", "n": "int"})
    assert out == {"title": "[stub:title]", "tags": [], "n": 0}


def test_stub_no_schema_returns_text():
    c = StubLLMClient()
    out = c.complete("hello world")
    assert "text" in out and out["text"].startswith("[stub llm] ")
