"""Phase 11 idempotency regression for the three upsert-by-marker workflows.

Asserts the upsert-by-marker contract documented in ``specs/memory-model.md``:

* **Cold start** → exactly one body-mutating GitHub call (a ``POST``).
* **Warm start** (state already contains the produced block) → at most one
  body-mutating call (a ``PATCH``) whose request body is byte-identical to
  the artefact's existing body, and total artefact count stays at 1.

Each workflow is exercised twice against the same fake GitHub state. The
fake (`_CountingState`) sits behind ``httpx.MockTransport`` and records every
write, so the test can assert byte-equality on the second run rather than
just "it didn't crash".

No live network. No new dependencies.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone

import httpx
import pytest

from repo_agent.workflows import landscape_scan, new_tool, review_pr
from repo_agent.workflows.github import GitHubClient


NOW = datetime(2026, 4, 22, 9, 0, tzinfo=timezone.utc)
URL = "https://example.com/cooltool"
PR_NUMBER = 7


# ---------------------------------------------------------------------------
# Counting fake GitHub backend
# ---------------------------------------------------------------------------


class _CountingState:
    """A `_MockState`-compatible fake that records every body-mutating call.

    Records ``(method, path, body_dict)`` on every ``POST``/``PATCH`` to the
    issue / comment endpoints. Reads are unrecorded.
    """

    def __init__(self) -> None:
        self.issues: list[dict] = []
        self.comments: dict[int, list[dict]] = {}
        self._next_id = 1000
        self.writes: list[tuple[str, str, dict]] = []

    def _new_id(self) -> int:
        self._next_id += 1
        return self._next_id

    def handler(self, request: httpx.Request) -> httpx.Response:
        path = request.url.path
        method = request.method

        # ---- reads ---------------------------------------------------------
        if method == "GET" and path.endswith("/pulls"):
            return httpx.Response(200, json=[])
        if method == "GET" and path.endswith("/issues"):
            return httpx.Response(200, json=self.issues)
        if method == "GET" and "/issues/" in path and path.endswith("/comments"):
            num = int(path.split("/issues/")[1].split("/")[0])
            return httpx.Response(200, json=self.comments.get(num, []))

        # ---- writes (recorded) --------------------------------------------
        if method == "POST" and path.endswith("/issues"):
            body = json.loads(request.content)
            self.writes.append((method, path, body))
            issue = {
                "number": self._new_id(),
                "title": body["title"],
                "body": body["body"],
                "html_url": f"https://example/issues/{self._next_id}",
            }
            self.issues.append(issue)
            return httpx.Response(201, json=issue)

        if method == "PATCH" and "/issues/" in path and "/comments" not in path:
            num = int(path.rstrip("/").split("/")[-1])
            body = json.loads(request.content)
            self.writes.append((method, path, body))
            for it in self.issues:
                if it["number"] == num:
                    if "title" in body:
                        it["title"] = body["title"]
                    if "body" in body:
                        it["body"] = body["body"]
                    return httpx.Response(200, json=it)
            return httpx.Response(404, json={"message": "not found"})

        if method == "POST" and "/issues/" in path and path.endswith("/comments"):
            num = int(path.split("/issues/")[1].split("/")[0])
            body = json.loads(request.content)
            self.writes.append((method, path, body))
            comment = {"id": self._new_id(), "body": body["body"]}
            self.comments.setdefault(num, []).append(comment)
            return httpx.Response(201, json=comment)

        if method == "PATCH" and "/issues/comments/" in path:
            cid = int(path.rstrip("/").split("/")[-1])
            body = json.loads(request.content)
            self.writes.append((method, path, body))
            for clist in self.comments.values():
                for c in clist:
                    if c["id"] == cid:
                        c["body"] = body["body"]
                        return httpx.Response(200, json=c)
            return httpx.Response(404, json={"message": "not found"})

        return httpx.Response(404, json={"message": f"unhandled {method} {path}"})


def _make_client(state: _CountingState) -> GitHubClient:
    transport = httpx.MockTransport(state.handler)
    http = httpx.Client(transport=transport, base_url="https://api.github.com")
    return GitHubClient("natnew/test-repo", client=http, token="t")


# ---------------------------------------------------------------------------
# Workflow runners (each returns the second-run-relevant artefact body)
# ---------------------------------------------------------------------------


def _run_landscape(gh: GitHubClient) -> None:
    landscape_scan.run(since_days=7, gh_client=gh, dry_run=False, now=NOW)


def _run_new_tool(gh: GitHubClient, fixtures_dir) -> None:
    html = (fixtures_dir / "sample-page.html").read_text(encoding="utf-8")
    new_tool.run(
        url=URL,
        section="Orchestration Frameworks",
        rationale="Adds typed graph orchestration.",
        fetcher=lambda _u: html,
        gh_client=gh,
        open_issue=True,
    )


def _run_review_pr(gh: GitHubClient, fixtures_dir) -> None:
    payload = json.loads((fixtures_dir / "sample-pr.json").read_text(encoding="utf-8"))
    review_pr.run(pr_number=PR_NUMBER, pr_payload=payload, gh_client=gh, post=True)


# ---------------------------------------------------------------------------
# Idempotency assertions, parametrised across the three workflows
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "kind,runner,artefact_count_check",
    [
        (
            "landscape-digest",
            "landscape",
            lambda state: len(state.issues),
        ),
        (
            "new-tool",
            "new_tool",
            lambda state: len(state.issues),
        ),
        (
            "pr-scorecard",
            "review_pr",
            lambda state: len(state.comments.get(PR_NUMBER, [])),
        ),
    ],
)
def test_upsert_by_marker_is_idempotent(kind, runner, artefact_count_check, fixtures_dir):
    state = _CountingState()
    gh = _make_client(state)

    def run():
        if runner == "landscape":
            _run_landscape(gh)
        elif runner == "new_tool":
            _run_new_tool(gh, fixtures_dir)
        else:
            _run_review_pr(gh, fixtures_dir)

    # ---- Cold start ---------------------------------------------------------
    run()
    cold_writes = list(state.writes)
    assert len(cold_writes) == 1, (
        f"[{kind}] cold start should issue exactly one body-mutating call, "
        f"got {len(cold_writes)}: {[(m, p) for m, p, _ in cold_writes]}"
    )
    cold_method, _cold_path, cold_body = cold_writes[0]
    assert cold_method == "POST", f"[{kind}] cold start must be a POST, got {cold_method}"
    assert artefact_count_check(state) == 1, f"[{kind}] expected exactly one artefact after cold start"

    # Snapshot the body the agent just produced. The warm-start PATCH (if any)
    # must carry an identical body.
    cold_produced_body = cold_body["body"]

    # ---- Warm start ---------------------------------------------------------
    state.writes.clear()
    run()
    warm_writes = list(state.writes)

    # Total artefact count must not grow.
    assert artefact_count_check(state) == 1, (
        f"[{kind}] warm start must not create a second artefact "
        f"(found {artefact_count_check(state)})"
    )

    # At most one body-mutating call. If present, must be a PATCH with a body
    # byte-identical to what cold-start produced (the upsert helper currently
    # always re-emits the PATCH; that is the no-op short-circuit shape).
    assert len(warm_writes) <= 1, (
        f"[{kind}] warm start emitted {len(warm_writes)} body-mutating calls "
        f"(expected ≤ 1): {[(m, p) for m, p, _ in warm_writes]}"
    )
    if warm_writes:
        warm_method, _warm_path, warm_body = warm_writes[0]
        assert warm_method == "PATCH", (
            f"[{kind}] warm start write must be a PATCH (no second POST), got {warm_method}"
        )
        assert warm_body["body"] == cold_produced_body, (
            f"[{kind}] warm-start PATCH body diverged from cold-start POST body — "
            f"the renderer is non-deterministic and breaks the idempotency contract."
        )
