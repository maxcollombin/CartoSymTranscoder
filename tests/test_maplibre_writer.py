"""MapLibre writer — Style → style JSON, and the read↔write round-trip.

Scope mirrors the reader: ``fill`` / ``line`` / ``marker`` (single
``Circle``) symbolizers with literal values. The round-trip checked here
is a **model fixed point**
(``read → write → read`` yields the same Style); the emitted MapLibre is
not byte-identical to the input (a CartoSym Style has no sources / zoom /
metadata to round-trip).
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from cartosym_transcoder.codecs.maplibre import MaplibreReader, MaplibreWriter
from cartosym_transcoder.models.styles import Style

from ._maplibre_spec import assert_maplibre_valid
from .test_maplibre_reader import IN_SCOPE

_ATOMIC = Path(__file__).parent / "fixtures" / "maplibre" / "atomic"


@pytest.mark.parametrize("stem", list(IN_SCOPE))
def test_write_output_is_spec_valid(stem: str):
    style = MaplibreReader().read(_ATOMIC / f"{stem}.json")
    assert_maplibre_valid(MaplibreWriter().write(style))


@pytest.mark.parametrize("stem", list(IN_SCOPE))
def test_round_trip_is_a_model_fixed_point(stem: str):
    read = MaplibreReader()
    style = read.read(_ATOMIC / f"{stem}.json")
    again = read.read(MaplibreWriter().write(style))
    assert again.to_dict() == style.to_dict()


def test_empty_style_has_no_sources():
    out = MaplibreWriter().write(Style(styling_rules=[]))
    assert out == {"version": 8, "sources": {}, "layers": []}


def test_fill_and_line_layers_from_a_hand_built_style():
    style = Style.from_dict(
        {
            "stylingRules": [
                {"name": "areas", "symbolizer": {"fill": {"color": "#eee"}}},
                {
                    "name": "roads",
                    "symbolizer": {"stroke": {"color": "#333", "width": 2}},
                },
            ]
        }
    )
    out = MaplibreWriter().write(style)
    assert [(lyr["id"], lyr["type"]) for lyr in out["layers"]] == [
        ("areas", "fill"),
        ("roads", "line"),
    ]
    assert out["layers"][0]["paint"] == {"fill-color": "#eee"}
    assert out["layers"][1]["paint"] == {"line-color": "#333", "line-width": 2}
    assert_maplibre_valid(out)


def test_visibility_false_becomes_layout_none():
    style = Style.from_dict(
        {
            "stylingRules": [
                {
                    "name": "hidden",
                    "symbolizer": {"visibility": False, "fill": {"color": "red"}},
                }
            ]
        }
    )
    out = MaplibreWriter().write(style)
    assert out["layers"][0]["layout"] == {"visibility": "none"}


def test_circle_marker_becomes_a_circle_layer():
    style = Style.from_dict(
        {
            "stylingRules": [
                {
                    "name": "pts",
                    "symbolizer": {
                        "marker": {
                            "elements": [
                                {
                                    "type": "Circle",
                                    "fill": {"color": "#f00"},
                                    "outline": {"color": "#000", "thickness": 1},
                                    "radius": 6,
                                }
                            ]
                        }
                    },
                }
            ]
        }
    )
    out = MaplibreWriter().write(style)
    layer = out["layers"][0]
    assert layer["type"] == "circle"
    assert layer["paint"] == {
        "circle-color": "#f00",
        "circle-stroke-color": "#000",
        "circle-stroke-width": 1,
        "circle-radius": 6,
    }
    assert_maplibre_valid(out)


def test_non_circle_marker_element_is_rejected():
    style = Style.from_dict(
        {
            "stylingRules": [
                {
                    "name": "pts",
                    "symbolizer": {"marker": {"elements": [{"type": "Dot"}]}},
                }
            ]
        }
    )
    with pytest.raises(NotImplementedError):
        MaplibreWriter().write(style)


def test_multi_element_marker_is_rejected():
    style = Style.from_dict(
        {
            "stylingRules": [
                {
                    "name": "pts",
                    "symbolizer": {
                        "marker": {"elements": [{"type": "Circle"}, {"type": "Circle"}]}
                    },
                }
            ]
        }
    )
    with pytest.raises(NotImplementedError):
        MaplibreWriter().write(style)


def test_text_marker_element_is_rejected():
    style = Style.from_dict(
        {
            "stylingRules": [
                {
                    "name": "t",
                    "symbolizer": {
                        "marker": {"elements": [{"type": "Text", "text": "x"}]}
                    },
                }
            ]
        }
    )
    with pytest.raises(NotImplementedError):
        MaplibreWriter().write(style)


def test_rule_selector_becomes_layer_filter():
    style = Style.from_dict(
        {
            "stylingRules": [
                {
                    "name": "x",
                    "selector": {"op": "=", "args": [{"property": "k"}, "v"]},
                    "symbolizer": {"fill": {"color": "red"}},
                }
            ]
        }
    )
    out = MaplibreWriter().write(style)
    assert out["layers"][0]["filter"] == ["==", ["get", "k"], "v"]
    assert list(out["layers"][0]) == ["id", "type", "source", "filter", "paint"]
    assert_maplibre_valid(out)


def test_sysid_selector_is_rejected():
    style = Style.from_dict(
        {
            "stylingRules": [
                {
                    "name": "x",
                    "selector": {"op": "=", "args": [{"sysId": "dataLayer.id"}, "L"]},
                    "symbolizer": {"fill": {"color": "red"}},
                }
            ]
        }
    )
    with pytest.raises(NotImplementedError):
        MaplibreWriter().write(style)


def test_fill_with_full_stroke_is_rejected():
    style = Style.from_dict(
        {
            "stylingRules": [
                {
                    "name": "x",
                    "symbolizer": {
                        "fill": {"color": "red"},
                        "stroke": {"color": "black", "width": 3},
                    },
                }
            ]
        }
    )
    with pytest.raises(NotImplementedError):
        MaplibreWriter().write(style)


def test_json_serialisable():
    style = MaplibreReader().read(_ATOMIC / "fill-color-literal.json")
    json.dumps(MaplibreWriter().write(style))
