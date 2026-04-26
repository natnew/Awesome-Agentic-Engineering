"""CLI entrypoint — mirrors every MCP tool as a subcommand.

Usage::

    repo-agent serve                              # run the MCP server on stdio
    repo-agent list-sections
    repo-agent rubric
    repo-agent anti-patterns
    repo-agent search "langgraph" [--section README]
    repo-agent validate --file entry.md
    repo-agent propose --url https://... --section "Orchestration Frameworks"
    repo-agent triage --fixture tests/fixtures/sample-pr.json
    repo-agent freshness [--threshold 9]

    # Phase 6 workflows
    repo-agent workflow new-tool --url https://... --section "..." [--open-issue --repo owner/name]
    repo-agent workflow landscape-scan [--dry-run] [--repo owner/name] [--since-days 7]
    repo-agent workflow review-pr --pr 123 [--post --repo owner/name]

    # Phase 7 site renderer
    repo-agent workflow render-site [--output-dir docs] [--check]
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

from . import tools as T
from .observability import Run


def _emit(obj: object) -> None:
    json.dump(obj, sys.stdout, indent=2, default=str)
    sys.stdout.write("\n")


def _cmd_serve(_args: argparse.Namespace) -> int:
    from .server import serve  # pragma: no cover

    serve()  # pragma: no cover
    return 0  # pragma: no cover


def _cmd_list_sections(_args: argparse.Namespace) -> int:
    _emit(T.list_sections())
    return 0


def _cmd_rubric(_args: argparse.Namespace) -> int:
    _emit(T.get_rubric())
    return 0


def _cmd_anti_patterns(_args: argparse.Namespace) -> int:
    _emit(T.get_anti_patterns())
    return 0


def _cmd_search(args: argparse.Namespace) -> int:
    _emit(T.search_entries(query=args.query, section=args.section, limit=args.limit))
    return 0


def _cmd_validate(args: argparse.Namespace) -> int:
    text = Path(args.file).read_text(encoding="utf-8") if args.file else sys.stdin.read()
    _emit(T.validate_entry(entry_markdown=text))
    return 0


def _cmd_propose(args: argparse.Namespace) -> int:
    _emit(T.propose_entry(url=args.url, section=args.section, rationale=args.rationale or ""))
    return 0


def _cmd_triage(args: argparse.Namespace) -> int:
    payload: dict = {}
    if args.fixture:
        payload = json.loads(Path(args.fixture).read_text(encoding="utf-8"))
    else:
        payload = {
            "title": args.title or "",
            "body": args.body or "",
            "changed_files": args.changed_file or [],
        }
    _emit(
        T.triage_pr(
            title=payload.get("title", ""),
            body=payload.get("body", ""),
            changed_files=payload.get("changed_files"),
            entry_markdown=payload.get("entry_markdown"),
        )
    )
    return 0


def _cmd_freshness(args: argparse.Namespace) -> int:
    _emit(T.freshness_audit(threshold_months=args.threshold))
    return 0


# ---------------------------------------------------------------------------
# Phase 6 workflows
# ---------------------------------------------------------------------------


def _make_gh_client(repo: str | None):
    if not repo:
        return None
    from .workflows.github import GitHubClient

    return GitHubClient(repo)


def _cmd_workflow_new_tool(args: argparse.Namespace) -> int:
    from .workflows import new_tool

    gh = _make_gh_client(args.repo) if args.open_issue else None
    result = new_tool.run(
        url=args.url,
        section=args.section,
        rationale=args.rationale or "",
        gh_client=gh,
        open_issue=args.open_issue,
    )
    if args.json:
        _emit(result.to_dict())
    else:
        sys.stdout.write(result.markdown)
        sys.stderr.write(f"\n[workflow:new-tool] {result.summary}\n")
    return 0 if result.status != "error" else 1


def _cmd_workflow_landscape_scan(args: argparse.Namespace) -> int:
    from .workflows import landscape_scan

    gh = _make_gh_client(args.repo) if not args.dry_run else None
    result = landscape_scan.run(
        since_days=args.since_days,
        gh_client=gh,
        dry_run=args.dry_run,
        threshold_months=args.threshold,
    )
    if args.json:
        _emit(result.to_dict())
    else:
        sys.stdout.write(result.markdown)
        sys.stderr.write(f"\n[workflow:landscape-scan] {result.summary}\n")
    return 0 if result.status != "error" else 1


def _cmd_workflow_review_pr(args: argparse.Namespace) -> int:
    from .workflows import review_pr

    payload = None
    if args.fixture:
        payload = json.loads(Path(args.fixture).read_text(encoding="utf-8"))
    gh = _make_gh_client(args.repo) if (args.post or payload is None) else None
    result = review_pr.run(
        pr_number=args.pr,
        pr_payload=payload,
        gh_client=gh,
        post=args.post,
    )
    if args.json:
        _emit(result.to_dict())
    else:
        sys.stdout.write(result.markdown)
        sys.stderr.write(f"\n[workflow:review-pr] {result.summary}\n")
    return 0 if result.status != "error" else 1


def _cmd_workflow_render_site(args: argparse.Namespace) -> int:
    from .workflows import render_site as _rs

    output_dir = Path(args.output_dir).resolve() if args.output_dir else None
    result = _rs.render_site(output_dir=output_dir)
    sys.stderr.write(f"[workflow:render-site] {result.summary()}\n")
    if args.check and result.changed:
        sys.stderr.write(
            "[workflow:render-site] --check: site is stale (files would change). "
            "Re-run without --check to regenerate.\n"
        )
        for p in result.changed:
            sys.stderr.write(f"  drift: {p}\n")
        return 1
    return 0


def _default_repo() -> str | None:
    return os.environ.get("GITHUB_REPOSITORY")


def _cmd_graduation_audit(args: argparse.Namespace) -> int:
    from . import graduation as G

    if args.live:
        if not args.repo:
            sys.stderr.write("--live requires --repo or $GITHUB_REPOSITORY\n")
            return 2
        import httpx

        token = os.environ.get("GITHUB_TOKEN")
        headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "repo-agent-phase13/0.1",
        }
        if token:
            headers["Authorization"] = f"Bearer {token}"
        client = httpx.Client(base_url="https://api.github.com", headers=headers, timeout=15.0)
        try:
            audits = G.audit_workflows(client=client, repo=args.repo)
        finally:
            client.close()
    else:
        fixture = args.fixture or str(
            Path(__file__).resolve().parents[2]
            / "tests"
            / "fixtures"
            / "graduation"
            / "sample_runs.json"
        )
        audits = G.audit_workflows(fixture=fixture)

    if args.out == "table":
        sys.stdout.write(G.to_table(audits) + "\n")
    else:
        sys.stdout.write(G.to_json(audits) + "\n")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="repo-agent", description="Awesome-Agentic-Engineering agentic system (Phase 5)")
    p.add_argument(
        "--log-json-file",
        default=None,
        help="Append the JSON observability record to this file instead of stderr.",
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("serve", help="Run the MCP server on stdio.").set_defaults(func=_cmd_serve)
    sub.add_parser("list-sections", help="List sections and appendix files.").set_defaults(
        func=_cmd_list_sections
    )
    sub.add_parser("rubric", help="Return the rubric as JSON.").set_defaults(func=_cmd_rubric)
    sub.add_parser("anti-patterns", help="Return the anti-pattern policy as JSON.").set_defaults(
        func=_cmd_anti_patterns
    )

    ps = sub.add_parser("search", help="Search entries.")
    ps.add_argument("query")
    ps.add_argument("--section", default=None)
    ps.add_argument("--limit", type=int, default=20)
    ps.set_defaults(func=_cmd_search)

    pv = sub.add_parser("validate", help="Validate an entry Markdown snippet.")
    pv.add_argument("--file", help="Path to a Markdown file (defaults to stdin).")
    pv.set_defaults(func=_cmd_validate)

    pp = sub.add_parser("propose", help="Draft an entry for a URL (draft, 5.4).")
    pp.add_argument("--url", required=True)
    pp.add_argument("--section", required=True)
    pp.add_argument("--rationale", default="")
    pp.set_defaults(func=_cmd_propose)

    pt = sub.add_parser("triage", help="Triage a PR/issue payload (5.2).")
    pt.add_argument("--fixture", help="Path to a JSON payload file.")
    pt.add_argument("--title")
    pt.add_argument("--body")
    pt.add_argument("--changed-file", action="append", help="Repeatable.")
    pt.set_defaults(func=_cmd_triage)

    pf = sub.add_parser("freshness", help="Run the freshness audit (5.3).")
    pf.add_argument("--threshold", type=int, default=9)
    pf.set_defaults(func=_cmd_freshness)

    # `draft` is a spec-facing alias of `propose`.
    pd = sub.add_parser("draft", help="Alias of `propose` (5.4).")
    pd.add_argument("--url", required=True)
    pd.add_argument("--section", required=True)
    pd.add_argument("--rationale", default="")
    pd.set_defaults(func=_cmd_propose)

    # --------------------------------------------------------------- workflows
    pw = sub.add_parser("workflow", help="Phase 6 agentic workflows.")
    wsub = pw.add_subparsers(dest="workflow_cmd", required=True)

    default_repo = _default_repo()

    wn = wsub.add_parser("new-tool", help="6.1 — draft a rubric-aligned entry for a URL.")
    wn.add_argument("--url", required=True)
    wn.add_argument("--section", required=True)
    wn.add_argument("--rationale", default="")
    wn.add_argument("--open-issue", action="store_true", help="Upsert a tracking issue.")
    wn.add_argument("--repo", default=default_repo, help="owner/name (defaults to $GITHUB_REPOSITORY).")
    wn.add_argument("--json", action="store_true", help="Emit the full result as JSON.")
    wn.set_defaults(func=_cmd_workflow_new_tool)

    wl = wsub.add_parser("landscape-scan", help="6.2 — rolling weekly digest.")
    wl.add_argument("--dry-run", action="store_true")
    wl.add_argument("--since-days", type=int, default=7)
    wl.add_argument("--threshold", type=int, default=9, help="Stale threshold (months).")
    wl.add_argument("--repo", default=default_repo)
    wl.add_argument("--json", action="store_true")
    wl.set_defaults(func=_cmd_workflow_landscape_scan)

    wr = wsub.add_parser("review-pr", help="6.3 — post an advisory rubric review comment on a PR.")
    wr.add_argument("--pr", type=int, required=True)
    wr.add_argument("--fixture", help="Path to a PR payload JSON file (offline use).")
    wr.add_argument("--post", action="store_true")
    wr.add_argument("--repo", default=default_repo)
    wr.add_argument("--json", action="store_true")
    wr.set_defaults(func=_cmd_workflow_review_pr)

    ws = wsub.add_parser("render-site", help="7.1 — regenerate the static docs/ site from Markdown sources.")
    ws.add_argument("--output-dir", default=None, help="Override output directory (default: <repo>/docs).")
    ws.add_argument("--check", action="store_true", help="Exit non-zero if the site is stale.")
    ws.set_defaults(func=_cmd_workflow_render_site)

    # ----------------------------------------------------- Phase 13 graduation
    pg = sub.add_parser("graduation", help="Phase 13 — advisory → required graduation tooling.")
    gsub = pg.add_subparsers(dest="graduation_cmd", required=True)

    ga = gsub.add_parser("audit", help="Audit advisory workflows for the 30-day green window.")
    ga.add_argument("--fixture", default=None, help="Path to a sample_runs.json fixture (offline mode).")
    ga.add_argument("--live", action="store_true", help="Query the live GitHub Actions API.")
    ga.add_argument("--repo", default=default_repo, help="owner/name (live mode; defaults to $GITHUB_REPOSITORY).")
    ga.add_argument("--out", choices=("json", "table"), default="json")
    ga.set_defaults(func=_cmd_graduation_audit)

    return p


def _redact_inputs(args: argparse.Namespace) -> dict[str, Any]:
    """Build a JSON-serialisable inputs dict from argparse, dropping callables."""
    out: dict[str, Any] = {}
    for k, v in vars(args).items():
        if k == "func" or callable(v):
            continue
        if isinstance(v, (str, int, float, bool, type(None))):
            out[k] = v
        elif isinstance(v, (list, tuple)):
            out[k] = [x for x in v if isinstance(x, (str, int, float, bool, type(None)))]
        else:
            out[k] = str(v)
    return out


def _tool_name(args: argparse.Namespace) -> str:
    cmd = getattr(args, "cmd", None) or "unknown"
    sub = getattr(args, "workflow_cmd", None)
    return f"{cmd}.{sub}" if sub else cmd


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    inputs = _redact_inputs(args)
    log_file = inputs.pop("log_json_file", None)
    with Run(
        component="cli",
        tool=_tool_name(args),
        inputs=inputs,
        log_file=log_file,
    ) as run:
        rc = args.func(args)
        if rc != 0:
            run.set_outcome("error", error_class=f"exit_{rc}")
        return rc


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
