# repo-agent

MCP server + skills that turn **Awesome-Agentic-Engineering** into a v0 agentic system.

Phase 5 of the [roadmap](../../specs/roadmap.md). Spec: [`specs/2026-04-22-phase-5-repo-as-agentic-system/`](../../specs/2026-04-22-phase-5-repo-as-agentic-system/).

This directory is **infrastructure**, not a listed resource. Nothing here is linked from the curated `README.md`. Delete this folder and the list still renders fine.

## What you get

| Tool (MCP + CLI) | Roadmap | Purpose |
|---|---|---|
| `list_sections` | 5.1 | Enumerate README + appendix files and top-level sections. |
| `get_rubric` | 5.1 | Return `RUBRIC.md` as structured JSON (dimensions, weights, threshold, hard gates). |
| `get_anti_patterns` | 5.1 | Return `ANTI-PATTERNS.md` as structured JSON + hype-phrase list. |
| `search_entries` | 5.1 | Token/substring search across README + appendix. |
| `validate_entry` | 5.1 | Score an entry against the rubric, flag anti-pattern hits, emit a verdict. |
| `propose_entry` | 5.1 / 5.4 | Fetch a URL, extract metadata, draft a rubric-aligned entry, self-validate. |
| `triage_pr` | 5.2 | Classify a PR/issue payload — score, labels, verdict. |
| `freshness_audit` | 5.3 | Callable version of the Phase 4 stale detector; returns structured candidates. |

Everything is deterministic. No LLM key is required to run the server or the tests.

### Phase 6 workflows

These compose the tools above into end-to-end workflows. All three are **advisory** and **read-only toward content** — they may post comments or maintain a single rolling issue, never write to files and never open PRs automatically.

| Workflow | Roadmap | Purpose |
|---|---|---|
| `workflow new-tool` | 6.1 | URL → rubric-aligned draft entry + optional tracking issue. |
| `workflow landscape-scan` | 6.2 | Weekly digest: stale entries + recent-PR/issue candidates → one rolling issue. |
| `workflow review-pr` | 6.3 | On a content PR: rubric scorecard → single maintained review comment. |

### Phase 7 site renderer

| Workflow | Roadmap | Purpose |
|---|---|---|
| `workflow render-site` | 7.1 | Render `README.md` + `appendix/*.md` + `RUBRIC.md` + `ANTI-PATTERNS.md` + `CONTRIBUTING.md` + `CHANGELOG.md` to `docs/` (zero-build static HTML + `feed.xml` RSS + `sitemap.xml`). |

```powershell
repo-agent workflow render-site                  # regenerate docs/
repo-agent workflow render-site --check          # exit 1 if docs/ is stale (for CI)
repo-agent workflow render-site --output-dir out # render into a custom directory
```

The renderer is deterministic — running it twice on an unchanged tree produces byte-identical output. See [`docs/README.md`](../../docs/README.md) for how to preview the site locally.

## Install

Requires Python 3.12+.

```powershell
cd tools/repo-agent
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
```

## Run

```powershell
# Start the MCP server on stdio
repo-agent serve

# Or invoke any tool directly as a CLI subcommand
repo-agent rubric
repo-agent list-sections
repo-agent search "langgraph" --limit 5
repo-agent validate --file path/to/entry.md
repo-agent propose --url https://example.com --section "Orchestration Frameworks"
repo-agent triage --fixture tests/fixtures/sample-pr.json
repo-agent freshness --threshold 9
```

Every subcommand emits JSON on stdout.

### Phase 6 workflows (CLI)

```powershell
# 6.1 — draft an entry for a URL (prints markdown to stdout)
repo-agent workflow new-tool --url https://example.com/x --section "Orchestration Frameworks"

# 6.1 — same, plus upsert a tracking issue (needs GITHUB_TOKEN + --repo)
$env:GITHUB_TOKEN = "ghp_..."
repo-agent workflow new-tool --url https://example.com/x --section "..." --open-issue --repo owner/name

# 6.2 — weekly digest (dry-run renders markdown, no network writes)
repo-agent workflow landscape-scan --dry-run

# 6.2 — non-dry-run upserts one rolling issue in place
repo-agent workflow landscape-scan --repo owner/name

# 6.3 — advisory review comment on a PR (from a local fixture)
repo-agent workflow review-pr --pr 42 --fixture tests/fixtures/sample-pr.json

# 6.3 — post/update the comment on the live PR
repo-agent workflow review-pr --pr 42 --repo owner/name --post
```

Each workflow accepts `--json` to emit the full `WorkflowResult` (status, summary, markdown, artifacts) instead of just the rendered markdown.

## Test

```powershell
pytest -q
```

Live network tests are gated behind the `live` marker and skipped by default. CI runs the default suite only.

## MCP client config (example)

For Claude Desktop, VS Code, Cursor, or any stdio-capable MCP client:

```jsonc
{
  "mcpServers": {
    "repo-agent": {
      "command": "repo-agent",
      "args": ["serve"]
    }
  }
}
```

Or run via the module path if you prefer not to install the script shim:

```jsonc
{
  "mcpServers": {
    "repo-agent": {
      "command": "python",
      "args": ["-m", "repo_agent", "serve"]
    }
  }
}
```

## Architecture

```
src/repo_agent/
  paths.py         # locate the repo root from anywhere
  content.py       # parse README + appendix into an indexed set of sections
  rubric.py        # parse RUBRIC.md + ANTI-PATTERNS.md; score entries
  llm.py           # LLMClient protocol + deterministic stub
  tools.py         # pure-Python core: one function per MCP tool
  server.py        # thin FastMCP adapter over tools.py
  cli.py           # argparse CLI that mirrors every MCP tool
  skills/
    triage.py      # 5.2
    freshness.py   # 5.3
    entry_draft.py # 5.4
  workflows/       # Phase 6
    base.py        # WorkflowResult + protocol
    github.py      # tiny GH REST client (httpx, test-injectable)
    render.py      # shared markdown renderers (+ stable markers)
    idempotent.py  # upsert_issue/pr_comment_by_marker
    new_tool.py       # 6.1
    landscape_scan.py # 6.2
    review_pr.py      # 6.3
```

**No write operations.** Every skill returns proposed Markdown as a string. Humans (or Phase 6 workflows) decide what to commit.

## Plugging in a real LLM

`skills/` is currently deterministic. When Phase 6 adds LLM-backed skills, implement the `LLMClient` protocol in [`llm.py`](src/repo_agent/llm.py) and inject it at call time. Example keys you might use (not shipped):

```powershell
$env:OPENAI_API_KEY = "sk-..."
# or
$env:ANTHROPIC_API_KEY = "..."
# or point at a local model
$env:OLLAMA_BASE_URL = "http://localhost:11434"
```

No real provider is implemented in this PR — only the protocol and the stub.

## Reversibility

This tool has no effect on the curated list. Remove it with:

```powershell
Remove-Item -Recurse tools/repo-agent
Remove-Item .github/workflows/repo-agent-tests.yml
```

The repo returns to its pre-Phase-5 state.
