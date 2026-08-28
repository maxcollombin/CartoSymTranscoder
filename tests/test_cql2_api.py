"""Smoke tests for the public :mod:`cartosym_transcoder.cql2` API."""

from __future__ import annotations

from cartosym_transcoder import cql2


def test_parse_text_returns_model():
    expr = cql2.parse_text("population > 1000")
    assert expr.operator == ">"
    assert expr.left.name == "population"


def test_to_cql2_text_roundtrips_a_selector_dict():
    d = {
        "op": "and",
        "args": [
            {"op": "=", "args": [{"property": "a"}, 1]},
            {"op": "like", "args": [{"property": "b"}, "x%"]},
        ],
    }
    assert cql2.to_cql2_text(d) == "a = 1 and b like 'x%'"


def test_to_cql2_json_passes_through_dicts():
    d = {"op": "=", "args": [{"property": "x"}, 1]}
    assert cql2.to_cql2_json(d) is d


def test_to_cql2_json_serialises_a_model():
    expr = cql2.parse_text("x = 1")
    assert cql2.to_cql2_json(expr) == {"op": "=", "args": [{"property": "x"}, 1]}


def test_vocab_is_exposed():
    assert cql2.vocab.SPATIAL_RELATE == "s_relate"
    assert "s_intersects" in cql2.vocab.KNOWN_CQL2_CALLS
