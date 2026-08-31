"""MapLibre layer ``filter`` ↔ CartoSym selector mapping."""

from __future__ import annotations

import pytest

from pycartosym.codecs.maplibre._filter import (
    filter_to_selector,
    selector_to_filter,
    strip_datalayer_id,
)


@pytest.mark.parametrize(
    "mb_filter, selector",
    [
        (
            ["==", "position", "left"],
            {"op": "=", "args": [{"property": "position"}, "left"]},
        ),
        (
            ["==", ["get", "position"], "left"],
            {"op": "=", "args": [{"property": "position"}, "left"]},
        ),
        (
            ["!=", "cls", "water"],
            {"op": "<>", "args": [{"property": "cls"}, "water"]},
        ),
        (
            [">=", "rank", 3],
            {"op": ">=", "args": [{"property": "rank"}, 3]},
        ),
        (
            ["all", ["==", "a", 1], [">", "b", 2]],
            {
                "op": "and",
                "args": [
                    {"op": "=", "args": [{"property": "a"}, 1]},
                    {"op": ">", "args": [{"property": "b"}, 2]},
                ],
            },
        ),
        (
            ["any", ["==", "a", 1], ["==", "a", 2]],
            {
                "op": "or",
                "args": [
                    {"op": "=", "args": [{"property": "a"}, 1]},
                    {"op": "=", "args": [{"property": "a"}, 2]},
                ],
            },
        ),
        (
            ["in", "type", "road", "rail"],
            {"op": "in", "args": [{"property": "type"}, ["road", "rail"]]},
        ),
        (
            ["in", ["get", "type"], ["literal", ["road", "rail"]]],
            {"op": "in", "args": [{"property": "type"}, ["road", "rail"]]},
        ),
        (
            ["!in", "type", "road"],
            {
                "op": "not",
                "args": [{"op": "in", "args": [{"property": "type"}, ["road"]]}],
            },
        ),
        (
            ["has", "name"],
            {
                "op": "not",
                "args": [{"op": "isNull", "args": [{"property": "name"}]}],
            },
        ),
        (
            ["!has", "name"],
            {"op": "isNull", "args": [{"property": "name"}]},
        ),
        (
            ["!", ["==", "a", 1]],
            {"op": "not", "args": [{"op": "=", "args": [{"property": "a"}, 1]}]},
        ),
    ],
)
def test_filter_to_selector(mb_filter, selector):
    assert filter_to_selector(mb_filter) == selector


CANONICAL_FILTERS = [
    ["==", ["get", "position"], "left"],
    ["!=", ["get", "cls"], "water"],
    [">", ["get", "b"], 2],
    ["all", ["==", ["get", "a"], 1], [">", ["get", "b"], 2]],
    ["any", ["==", ["get", "a"], 1], ["==", ["get", "a"], 2]],
    ["in", ["get", "type"], ["literal", ["road", "rail"]]],
    ["!in", ["get", "type"], ["literal", ["road"]]],
    ["has", "name"],
    ["!", ["has", "name"]],
    ["!", ["==", ["get", "a"], 1]],
]


@pytest.mark.parametrize("mb_filter", CANONICAL_FILTERS)
def test_round_trip_is_a_fixed_point(mb_filter):
    assert selector_to_filter(filter_to_selector(mb_filter)) == mb_filter


@pytest.mark.parametrize(
    "mb_filter",
    [
        ["==", "$type", "Polygon"],
        ["==", "$id", 5],
        ["==", ["geometry-type"], "Point"],
        ["step", ["zoom"], 0, 10, 1],
        ["==", ["get", "a"], ["get", "b"]],
    ],
)
def test_unsupported_filters_raise(mb_filter):
    with pytest.raises(NotImplementedError):
        filter_to_selector(mb_filter)


def test_none_combinator():
    assert filter_to_selector(["none", ["==", "x", "y"]]) == {
        "op": "not",
        "args": [{"op": "or", "args": [{"op": "=", "args": [{"property": "x"}, "y"]}]}],
    }


def test_selector_with_sysid_operand_raises():
    with pytest.raises(NotImplementedError):
        selector_to_filter({"op": "=", "args": [{"sysId": "dataLayer.id"}, "Landuse"]})


def test_strip_datalayer_id_drops_a_lone_conjunct():
    selector = {"op": "=", "args": [{"sysId": "dataLayer.id"}, "Landuse"]}
    assert strip_datalayer_id(selector) is None


def test_strip_datalayer_id_handles_reversed_operand_order():
    selector = {"op": "=", "args": ["Landuse", {"sysId": "dataLayer.id"}]}
    assert strip_datalayer_id(selector) is None


def test_strip_datalayer_id_leaves_other_selectors_untouched():
    selector = {"op": "=", "args": [{"property": "k"}, "v"]}
    assert strip_datalayer_id(selector) == selector
    assert strip_datalayer_id(None) is None


def test_strip_datalayer_id_unwraps_single_surviving_sibling():
    selector = {
        "op": "and",
        "args": [
            {"op": "=", "args": [{"sysId": "dataLayer.id"}, "Landuse"]},
            {"op": "=", "args": [{"property": "k"}, "v"]},
        ],
    }
    assert strip_datalayer_id(selector) == {
        "op": "=",
        "args": [{"property": "k"}, "v"],
    }


def test_strip_datalayer_id_keeps_and_with_several_survivors():
    selector = {
        "op": "and",
        "args": [
            {"op": "=", "args": [{"sysId": "dataLayer.id"}, "Landuse"]},
            {"op": "=", "args": [{"property": "k"}, "v"]},
            {"op": ">", "args": [{"property": "n"}, 1]},
        ],
    }
    assert strip_datalayer_id(selector) == {
        "op": "and",
        "args": [
            {"op": "=", "args": [{"property": "k"}, "v"]},
            {"op": ">", "args": [{"property": "n"}, 1]},
        ],
    }
