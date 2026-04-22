"""LLM client protocol + deterministic stub default.

Skills that optionally use an LLM go through this protocol so the whole system
runs and tests pass with zero API keys. Real providers can be plugged in by a
contributor without changes to skill code.
"""

from __future__ import annotations

from typing import Any, Protocol


class LLMClient(Protocol):
    """Minimal contract for optional LLM use inside skills."""

    def complete(self, prompt: str, schema: dict[str, Any] | None = None) -> dict[str, Any]:
        """Return a structured dict. Implementations should honour ``schema`` keys."""
        ...


class StubLLMClient:
    """Deterministic, offline stub.

    Returns placeholders keyed by the schema so downstream code is exercised in
    tests without any network call or API key. Never raises.
    """

    name = "stub"

    def complete(self, prompt: str, schema: dict[str, Any] | None = None) -> dict[str, Any]:
        if not schema:
            return {"text": "[stub llm] " + prompt[:80]}
        out: dict[str, Any] = {}
        for key, hint in schema.items():
            if hint == "string":
                out[key] = f"[stub:{key}]"
            elif hint == "int":
                out[key] = 0
            elif hint == "list[string]":
                out[key] = []
            else:
                out[key] = None
        return out


def default_client() -> LLMClient:
    return StubLLMClient()
