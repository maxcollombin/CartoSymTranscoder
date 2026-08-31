"""Guards for :mod:`pycartosym.cql2.vocab`.

The module derives the CQL2 predicate/function vocabulary from the Pydantic
models and maps arithmetic operators via grammar *token names*. These tests
fail loudly if either source drifts (a renamed token, a model ``op`` enum
that lost a canonical name).
"""

from __future__ import annotations

import pytest

from pycartosym.cql2 import vocab as v
from pycartosym.grammar.generated.CartoSymCSSGrammar import CartoSymCSSGrammar


def test_predicate_sets_hold_canonical_names():
    assert {"s_intersects", "s_within", "s_coveredby"} <= v.SPATIAL_PREDICATES
    assert {"t_before", "t_after", "t_during"} <= v.TEMPORAL_PREDICATES
    assert {"a_contains", "a_overlaps"} <= v.ARRAY_PREDICATES
    assert v.TEXT_OP_PREDICATES == frozenset({"contains", "startswith", "endswith"})
    assert {"casei", "accenti", "concatenate"} <= v.CHARACTER_FUNCTIONS
    assert v.GEOM_BUFFER == frozenset({"s_buffer"})
    assert v.SPATIAL_RELATE == "s_relate"


def test_dispatch_sets_are_canonical_only():
    """Back-compat bare aliases in the models must not leak into dispatch."""
    assert all(o.startswith("s_") for o in v.SPATIAL_PREDICATES)
    assert all(o.startswith("t_") for o in v.TEMPORAL_PREDICATES)
    assert all(o.startswith("a_") for o in v.ARRAY_PREDICATES)


def test_canon_maps_recover_camelcase():
    assert v.SPATIAL_CANON["s_coveredby"] == "s_coveredBy"
    assert v.TEXT_OP_CANON["startswith"] == "startsWith"
    assert v.LOWER_UPPER_CANON["lowercase"] == "lowerCase"
    assert v.GEOM_BINARY_CANON["s_symdifference"] == "s_symDifference"
    assert v.GEOM_UNARY_CANON["s_convexhull"] == "s_convexHull"


def test_wkt_and_temporal_literal_names():
    assert v.WKT_TO_GEOJSON["multipolygon"] == "MultiPolygon"
    assert v.WKT_TYPES == frozenset(v.WKT_TO_GEOJSON)
    assert v.TEMPORAL_LITERAL_NAMES == frozenset({"date", "timestamp", "interval"})


@pytest.mark.parametrize(
    "ctx_cls, table",
    [
        ("ArithmeticOperatorMulContext", "ARITH_MUL_BY_TOKEN"),
        ("ArithmeticOperatorAddContext", "ARITH_ADD_BY_TOKEN"),
    ],
)
def test_arith_token_names_exist_on_grammar_context(ctx_cls, table):
    """Every key in the ARITH_*_BY_TOKEN maps must be a real token accessor."""
    cls = getattr(CartoSymCSSGrammar, ctx_cls)
    for token_name in getattr(v, table):
        assert hasattr(cls, token_name), f"{ctx_cls} has no {token_name}() accessor"


def test_known_calls_is_union_of_parts():
    assert v.WKT_TYPES <= v.KNOWN_CQL2_CALLS
    assert v.SPATIAL_PREDICATES <= v.KNOWN_CQL2_CALLS
    assert "bbox" in v.KNOWN_CQL2_CALLS
    assert v.SPATIAL_RELATE in v.KNOWN_CQL2_CALLS
