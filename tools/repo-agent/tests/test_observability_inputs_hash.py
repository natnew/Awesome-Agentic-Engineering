"""Phase 12 — inputs_hash stability and sensitivity."""

from __future__ import annotations

import pytest

from repo_agent.observability import canonical_inputs_hash


def test_inputs_hash_stable_across_key_order():
    a = {"url": "https://example.com", "section": "Memory", "limit": 20}
    b = {"limit": 20, "section": "Memory", "url": "https://example.com"}
    assert canonical_inputs_hash(a) == canonical_inputs_hash(b)


def test_inputs_hash_stable_across_repeated_calls():
    payload = {"q": "agent", "n": 3, "flag": True, "tags": ["a", "b"]}
    h0 = canonical_inputs_hash(payload)
    for _ in range(10):
        assert canonical_inputs_hash(payload) == h0


@pytest.mark.parametrize(
    "mutate",
    [
        lambda d: {**d, "q": "different"},
        lambda d: {**d, "n": d["n"] + 1},
        lambda d: {**d, "flag": not d["flag"]},
        lambda d: {**d, "tags": [*d["tags"], "c"]},
        lambda d: {**d, "extra": None},
    ],
)
def test_inputs_hash_changes_when_any_field_mutates(mutate):
    base = {"q": "agent", "n": 3, "flag": True, "tags": ["a", "b"]}
    assert canonical_inputs_hash(base) != canonical_inputs_hash(mutate(base))


def test_inputs_hash_is_64_hex_chars():
    h = canonical_inputs_hash({"x": 1})
    assert len(h) == 64
    int(h, 16)  # parses as hex


def test_inputs_hash_raises_on_non_serialisable():
    class Opaque:
        pass

    with pytest.raises(TypeError):
        canonical_inputs_hash({"obj": Opaque()})
