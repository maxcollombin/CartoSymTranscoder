"""MapLibre value-expression arrays ↔ CartoSym value expressions.

Scope: the six operators ``codecs.maplibre._expressions`` targets — ``get``
/ ``case`` / ``match`` / ``interpolate`` / ``step`` / ``coalesce`` — plus
the 5 binary arithmetic operators (``+``/``-``/``*``/``/``/``^``) and the
``viz.sd`` system identifier (OGC issue #115). Every other MapLibre
expression operator (comparisons, ``all``/``any``/``!``, ``%``, a bare
``zoom``, ``let``/``var``, other interpolation colour spaces, …) is a
deliberate out-of-scope gap — asserted here, not silently dropped.
"""

from __future__ import annotations

import pytest

from pycartosym.codecs.maplibre._expressions import (
    maplibre_expr_to_value,
    value_to_maplibre_expr,
)
from pycartosym.codecs.maplibre._zoom import scale_denominator_zoom_expr

# Round-trip cases: (MapLibre expression array, CartoSym value dict).
# Fed through maplibre_expr_to_value / value_to_maplibre_expr directly, and
# through the full Style model (Fill.color) to prove Pydantic validates the
# dict into the matching typed pycartosym.models.value_expressions
# class and the writer reconstructs the exact same array back.
ROUND_TRIP = [
    (
        ["get", "colour"],
        {"property": "colour"},
    ),
    (
        ["case", ["get", "big"], "red", "blue"],
        {"op": "case", "args": [{"property": "big"}, "red", "blue"]},
    ),
    (
        ["case", True, "a", False, "b", "c"],
        {"op": "case", "args": [True, "a", False, "b", "c"]},
    ),
    (
        ["match", ["get", "class"], "park", "green", "water", "blue", "grey"],
        {
            "op": "match",
            "args": [{"property": "class"}, "park", "green", "water", "blue", "grey"],
        },
    ),
    (
        ["match", ["get", "class"], [1, 2, 3], "a", 4, "b", "c"],
        {"op": "match", "args": [{"property": "class"}, [1, 2, 3], "a", 4, "b", "c"]},
    ),
    (
        ["step", ["get", "rank"], "small", 3, "medium", 6, "large"],
        {
            "op": "step",
            "args": [{"property": "rank"}, "small", 3, "medium", 6, "large"],
        },
    ),
    (
        ["interpolate", ["linear"], ["get", "zoom"], 0, 1, 10, 5],
        {
            "op": "interpolate",
            "interpolation": "linear",
            "args": [{"property": "zoom"}, 0, 1, 10, 5],
        },
    ),
    (
        ["interpolate", ["exponential", 1.5], ["get", "zoom"], 0, 1, 10, 5],
        {
            "op": "interpolate",
            "interpolation": "exponential",
            "base": 1.5,
            "args": [{"property": "zoom"}, 0, 1, 10, 5],
        },
    ),
    (
        ["interpolate", ["cubic-bezier", 0.2, 0, 0.8, 1], ["get", "zoom"], 0, 1, 10, 5],
        {
            "op": "interpolate",
            "interpolation": "cubic-bezier",
            "controlPoints": [0.2, 0, 0.8, 1],
            "args": [{"property": "zoom"}, 0, 1, 10, 5],
        },
    ),
    (
        ["coalesce", ["get", "a"], ["get", "b"], "fallback"],
        {
            "op": "coalesce",
            "args": [{"property": "a"}, {"property": "b"}, "fallback"],
        },
    ),
    # Nesting: get inside case inside coalesce.
    (
        ["coalesce", ["case", ["get", "ok"], ["get", "a"], None], "fallback"],
        {
            "op": "coalesce",
            "args": [
                {
                    "op": "case",
                    "args": [{"property": "ok"}, {"property": "a"}, None],
                },
                "fallback",
            ],
        },
    ),
    # Binary arithmetic (OGC issue #115's stroke.width: viz.sd / 1000 shape).
    (
        ["/", ["get", "a"], 1000],
        {"op": "/", "args": [{"property": "a"}, 1000]},
    ),
    (
        ["^", 2, ["get", "a"]],
        {"op": "^", "args": [2, {"property": "a"}]},
    ),
    # viz.sd system identifier, substituted for the zoom-driven scale
    # denominator formula.
    (
        scale_denominator_zoom_expr(),
        {"sysId": "viz.sd"},
    ),
]


@pytest.mark.parametrize("mb_expr, value", ROUND_TRIP)
def test_maplibre_expr_to_value(mb_expr, value):
    assert maplibre_expr_to_value(mb_expr, "prop") == value


def test_literal_scalars_pass_through():
    for scalar in ("red", 3, 1.5, True, None):
        assert maplibre_expr_to_value(scalar, "prop") == scalar
        assert value_to_maplibre_expr(scalar, "prop") == scalar


def test_literal_operator_unwraps_its_payload():
    # ['literal', x] marks x (often an array) as a constant, not a nested
    # expression — it unwraps one-way; a plain value never re-wraps into
    # ['literal', ...] on the way back (there is nothing to disambiguate).
    assert maplibre_expr_to_value(["literal", "red"], "prop") == "red"


@pytest.mark.parametrize(
    "mb_expr",
    [
        ["==", ["get", "a"], 1],
        ["all", ["==", "a", 1], [">", "b", 2]],
        ["%", ["get", "a"], 2],
        ["zoom"],
        ["to-string", ["get", "a"]],
        ["let", "x", 1, ["var", "x"]],
        ["interpolate-hcl", ["linear"], ["get", "zoom"], 0, "red", 10, "blue"],
    ],
)
def test_out_of_scope_operator_raises(mb_expr):
    with pytest.raises(NotImplementedError):
        maplibre_expr_to_value(mb_expr, "prop")


@pytest.mark.parametrize(
    "mb_expr",
    [
        ["get", "a", "b"],  # two-arg get (object indexing) not supported
        ["case", ["get", "a"]],  # missing fallback
        ["match", ["get", "a"], "x"],  # missing fallback
        ["step", ["get", "a"]],  # missing output0
        ["interpolate", ["linear"], ["get", "a"]],  # missing stop/output pair
        ["interpolate", ["unknown-type"], ["get", "a"], 0, 1],
        # non-literal label:
        ["match", ["get", "a"], [1, ["get", "b"]], "out", "fallback"],
        ["+", 1, 2, 3],  # only 2-argument arithmetic maps in this codec
    ],
)
def test_malformed_expression_raises(mb_expr):
    with pytest.raises(NotImplementedError):
        maplibre_expr_to_value(mb_expr, "prop")


def test_unsupported_system_identifier_raises():
    """Only ``viz.sd`` (OGC issue #115) has a MapLibre expression mapping —
    any other system identifier is an honest, undecomposable gap.
    """
    from pycartosym.models.value_expressions import SystemIdentifier

    with pytest.raises(NotImplementedError):
        value_to_maplibre_expr(SystemIdentifier(sysId="viz.other"), "prop")


def test_near_miss_zoom_expression_raises():
    """A ``["/", ..., ["*", ..., ["^", 2, ["zoom"]]]]`` shape that isn't
    exactly the canonical scale-denominator formula is an honest,
    undecomposable gap — a bare ``["zoom"]`` has no mapping of its own
    outside that exact shape (deliberate exact-shape matching, see
    :func:`pycartosym.codecs.maplibre._zoom.is_scale_denominator_zoom_expr`).
    """
    with pytest.raises(NotImplementedError):
        maplibre_expr_to_value(["/", 999, ["*", 100, ["^", 2, ["zoom"]]]], "prop")


@pytest.mark.parametrize("mb_expr, _value", ROUND_TRIP)
def test_expression_through_style_model(mb_expr, _value):
    """A value expression validates through Fill.color and writes back
    to the exact same MapLibre array — the Style model is the pivot, per
    this project's conversion pipeline.
    """
    from pycartosym.models.styles import Style

    color = maplibre_expr_to_value(mb_expr, "c")
    style = Style.model_validate(
        {
            "stylingRules": [
                {
                    "name": "r",
                    "symbolizer": {"fill": {"color": color}},
                }
            ]
        }
    )
    color = style.styling_rules[0].symbolizer.fill.color
    assert value_to_maplibre_expr(color, "fill.color") == mb_expr
