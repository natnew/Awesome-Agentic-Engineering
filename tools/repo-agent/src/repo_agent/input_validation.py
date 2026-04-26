"""Input-validation helpers (Phase 10 — safety model).

Three pure-stdlib helpers used at the agent's untrusted-input boundary:

* :func:`sanitise_text` — strip HTML element syntax (``<tag>``, ``</tag>``,
  ``<tag attr=...>``), drop null bytes, truncate. HTML *comments*
  (``<!-- ... -->``) are preserved on purpose: the agent's idempotency
  contract uses ``<!-- repo-agent: ... -->`` markers in issue/comment
  bodies and stripping them would break upsert (see
  ``specs/memory-model.md`` Phase 11).
* :func:`validate_url` — accept only ``https://`` URLs; reject every other
  scheme and every malformed input.
* :func:`assert_not_content_path` — raise ``ValueError`` if the supplied path
  resolves under any content-file tree the agent must never write to.

Design constraints (see ``specs/safety-model.md``):

* No new dependencies. ``re``, ``urllib.parse``, and ``pathlib`` only.
* Pure functions; no I/O, no globals, no env reads.
* The HTML strip is *not* a full sanitiser. It removes tag syntax to defang
  the most common prompt-injection vector (instruction text wrapped in
  ``<system>``-style tags). For browser-rendered output a full sanitiser
  would be required — and the repo has no browser-rendered input surface.
"""

from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import urlparse

from .paths import find_repo_root

__all__ = [
    "sanitise_text",
    "validate_url",
    "assert_not_content_path",
    "CONTENT_PATH_PATTERNS",
]


# Element tag matcher. The negative lookahead ``(?!!--)`` skips HTML comment
# starts (``<!--``) so that ``<!-- repo-agent: ... -->`` markers survive — the
# upsert-by-marker contract in ``workflows/idempotent.py`` depends on them.
_TAG_RE = re.compile(r"<(?!!--)[^>]*>")

# The trees the agent must never write to. Order does not matter; membership
# is checked by ``Path.is_relative_to``.
CONTENT_PATH_PATTERNS: tuple[str, ...] = (
    "README.md",
    "CHANGELOG.md",
    "appendix",
    "docs",
    "tools/repo-agent/src",
)


def sanitise_text(text: str, max_chars: int = 8_000) -> str:
    """Return ``text`` with HTML tag syntax stripped, null bytes removed, and
    truncated to ``max_chars`` characters.

    Order matters: tags are stripped *before* truncation so the result never
    ends mid-tag.

    A non-string ``text`` raises ``TypeError`` — silent coercion would hide
    upstream bugs.
    """
    if not isinstance(text, str):
        raise TypeError(f"sanitise_text expects str, got {type(text).__name__}")
    if max_chars < 0:
        raise ValueError("max_chars must be non-negative")
    stripped = _TAG_RE.sub("", text)
    stripped = stripped.replace("\x00", "")
    if len(stripped) > max_chars:
        stripped = stripped[:max_chars]
    return stripped


def validate_url(url: str) -> str:
    """Return ``url`` unchanged iff it is a well-formed ``https://`` URL.

    Raises ``ValueError`` for any other scheme (``http``, ``javascript``,
    ``data``, ``file``, …), for empty strings, for relative paths, and for
    any input ``urllib.parse`` cannot parse into both a scheme and a netloc.
    """
    if not isinstance(url, str):
        raise TypeError(f"validate_url expects str, got {type(url).__name__}")
    if not url:
        raise ValueError("validate_url: empty URL")
    try:
        parsed = urlparse(url)
    except ValueError as exc:
        raise ValueError(f"validate_url: malformed URL {url!r}") from exc
    if parsed.scheme.lower() != "https":
        raise ValueError(
            f"validate_url: only https:// is permitted, got scheme {parsed.scheme!r}"
        )
    if not parsed.netloc:
        raise ValueError(f"validate_url: missing host in {url!r}")
    return url


def assert_not_content_path(path: str | Path, *, repo_root: Path | None = None) -> None:
    """Raise ``ValueError`` if ``path`` resolves under any content-file tree.

    The set of protected trees is ``CONTENT_PATH_PATTERNS``. Any attempt to
    write under those paths is a violation of the trust boundary documented
    in ``specs/safety-model.md`` and must be refused at the source.
    """
    root = (repo_root or find_repo_root()).resolve()
    candidate = Path(path)
    if not candidate.is_absolute():
        candidate = (root / candidate).resolve()
    else:
        candidate = candidate.resolve()
    try:
        rel = candidate.relative_to(root)
    except ValueError:
        # Outside the repo entirely — not the boundary this guard protects.
        return
    rel_posix = rel.as_posix()
    for pattern in CONTENT_PATH_PATTERNS:
        if rel_posix == pattern or rel_posix.startswith(pattern + "/"):
            raise ValueError(
                f"assert_not_content_path: refusing to write under content tree "
                f"{pattern!r} (path={rel_posix!r}). See specs/safety-model.md."
            )
