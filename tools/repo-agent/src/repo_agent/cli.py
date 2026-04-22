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
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import tools as T


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


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="repo-agent", description="Awesome-Agentic-Engineering agentic system (Phase 5)")
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

    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
