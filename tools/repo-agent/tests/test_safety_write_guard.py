"""Write-guard test (Phase 10 — safety model).

Asserts the agent's content-path guard refuses every protected tree:

* ``README.md``
* ``appendix/**``
* ``CHANGELOG.md``
* ``docs/**``
* ``tools/repo-agent/src/**``

Offline; no mocks; no fixtures from ``conftest.py``; no I/O beyond the
repo-root probe in ``find_repo_root`` (read-only).
"""

from __future__ import annotations

import pytest

from repo_agent.input_validation import assert_not_content_path


_PROTECTED_PATHS = [
    "README.md",
    "CHANGELOG.md",
    "appendix/open-source-models-for-agents.md",
    "appendix/voice-agents.md",
    "docs/index.html",
    "docs/styles.css",
    "tools/repo-agent/src/repo_agent/rubric.py",
    "tools/repo-agent/src/repo_agent/__init__.py",
]


@pytest.mark.parametrize("path", _PROTECTED_PATHS)
def test_assert_not_content_path_refuses_protected_tree(path: str) -> None:
    with pytest.raises(ValueError, match="refusing to write"):
        assert_not_content_path(path)


_ALLOWED_PATHS = [
    "specs/safety-model.md",
    "tools/repo-agent/tests/test_input_validation.py",
    "tools/repo-agent/pyproject.toml",
    ".github/workflows/repo-agent-tests.yml",
]


@pytest.mark.parametrize("path", _ALLOWED_PATHS)
def test_assert_not_content_path_permits_non_content(path: str) -> None:
    # Should not raise.
    assert_not_content_path(path)


def test_assert_not_content_path_ignores_paths_outside_repo(tmp_path) -> None:
    # Outside the repo is not the boundary this guard protects; it must not raise.
    assert_not_content_path(tmp_path / "scratch.md")
