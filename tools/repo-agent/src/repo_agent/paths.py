"""Locate the repository root from any working directory.

The package ships inside ``tools/repo-agent/`` at the repo root. Walk up from
this file until we find the sentinel files that define the list itself
(``README.md`` + ``RUBRIC.md`` + ``specs/``).
"""

from __future__ import annotations

from pathlib import Path

_SENTINELS = ("README.md", "RUBRIC.md", "ANTI-PATTERNS.md")


def find_repo_root(start: Path | None = None) -> Path:
    """Return the absolute path to the repository root.

    Raises ``RuntimeError`` if the sentinels cannot be found — this means the
    package is being used outside of a checkout of the list repo.
    """
    here = (start or Path(__file__)).resolve()
    for candidate in [here, *here.parents]:
        if all((candidate / name).is_file() for name in _SENTINELS):
            return candidate
    raise RuntimeError(
        "Could not locate repo root (missing README.md / RUBRIC.md / ANTI-PATTERNS.md). "
        "Run from within a checkout of Awesome-Agentic-Engineering."
    )
