"""MapLibre writer — Style → style JSON, and the read↔write round-trip.

Scope mirrors the reader: ``fill`` / ``line`` / ``marker`` (single
``Circle`` or ``Image``) / ``label`` (single ``Text``) symbolizers with
literal values. The round-trip checked here is a **model fixed point**
(``read → write → read`` yields the same Style); the emitted MapLibre is
not byte-identical to the input (a CartoSym Style has no sources / zoom /
metadata to round-trip).
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from pycartosym.codecs.maplibre import MaplibreReader, MaplibreWriter
from pycartosym.codecs.maplibre._zoom import (
    scale_denominator_from_zoom,
    zoom_from_scale_denominator,
)
from pycartosym.models.styles import Style

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


def test_zoom_range_round_trip_recovers_integer_zoom():
    layer = {
        "id": "fill",
        "type": "fill",
        "source": "cartosym",
        "minzoom": 10,
        "maxzoom": 14,
        "paint": {"fill-color": "red"},
    }
    read = MaplibreReader()
    style = read.read({"version": 8, "sources": {}, "layers": [layer]})
    out_layer = MaplibreWriter().write(style)["layers"][0]
    assert out_layer["minzoom"] == 10
    assert out_layer["maxzoom"] == 14
    assert isinstance(out_layer["minzoom"], int)
    assert isinstance(out_layer["maxzoom"], int)


def test_empty_style_has_no_sources():
    out = MaplibreWriter().write(Style(styling_rules=[]))
    assert out == {"version": 8, "sources": {}, "layers": []}


def test_stroke_width_unwraps_a_px_unit_value():
    """``stroke.width`` from CSCSS (``2.0 px``) validates into a
    ``UnitValue`` — MapLibre ``line-width`` needs a bare pixel number.
    """
    style = Style.from_dict(
        {
            "stylingRules": [
                {
                    "name": "roads",
                    "symbolizer": {"stroke": {"width": {"px": 2.0}}},
                }
            ]
        }
    )
    out = MaplibreWriter().write(style)
    assert out["layers"][0]["paint"]["line-width"] == 2.0
    assert_maplibre_valid(out)


def test_stroke_width_in_a_non_px_unit_is_rejected():
    style = Style.from_dict(
        {
            "stylingRules": [
                {
                    "name": "roads",
                    "symbolizer": {"stroke": {"width": {"mm": 2.0}}},
                }
            ]
        }
    )
    with pytest.raises(NotImplementedError):
        MaplibreWriter().write(style)


def test_circle_element_px_dict_fields_are_unwrapped():
    """A graphic element inside ``Marker.elements`` stays an untyped
    ``dict`` (see ``models/symbolizers.py``), so ``radius``/``thickness``
    arrive as a bare ``{"px": …}`` dict rather than a validated
    ``UnitValue`` — both shapes must unwrap the same way.
    """
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
                                    "outline": {"thickness": {"px": 1.5}},
                                    "radius": {"px": 6},
                                }
                            ]
                        }
                    },
                }
            ]
        }
    )
    out = MaplibreWriter().write(style)
    paint = out["layers"][0]["paint"]
    assert paint["circle-stroke-width"] == 1.5
    assert paint["circle-radius"] == 6
    assert_maplibre_valid(out)


def test_rgb_literal_color_becomes_hex():
    """CartoSym's ``Color`` accepts a ``[r, g, b]`` 0-255 literal (what a
    CSCSS ``#rrggbb`` hex literal actually parses into) — MapLibre needs
    a colour string.
    """
    style = Style.from_dict(
        {
            "stylingRules": [
                {"name": "areas", "symbolizer": {"fill": {"color": [32, 32, 32]}}}
            ]
        }
    )
    out = MaplibreWriter().write(style)
    assert out["layers"][0]["paint"]["fill-color"] == "#202020"
    assert_maplibre_valid(out)


def test_rgba_literal_color_becomes_hex():
    style = Style.from_dict(
        {
            "stylingRules": [
                {
                    "name": "areas",
                    "symbolizer": {"fill": {"color": [255, 0, 0, 128]}},
                }
            ]
        }
    )
    out = MaplibreWriter().write(style)
    assert out["layers"][0]["paint"]["fill-color"] == "#ff000080"
    assert_maplibre_valid(out)


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


def test_symbolizerless_rule_is_dropped_not_an_error():
    """A rule that draws nothing (visibility only) is safe to omit — the
    common case of a cascade's base/gate rule, but also holds standalone
    (no nesting involved). Mirrors the SLD/SE writer's identical policy.
    """
    style = Style.from_dict(
        {"stylingRules": [{"name": "gate", "symbolizer": {"visibility": False}}]}
    )
    out = MaplibreWriter().write(style)
    assert out["layers"] == []
    assert_maplibre_valid(out)


def test_raster_only_rule_still_raises_not_dropped():
    """Unlike a genuinely empty rule, one carrying unsupported (raster)
    content must still raise — dropping it would silently lose data.
    """
    style = Style.from_dict(
        {
            "stylingRules": [
                {"name": "dem", "symbolizer": {"singleChannel": "elevation"}}
            ]
        }
    )
    with pytest.raises(NotImplementedError, match="single_channel"):
        MaplibreWriter().write(style)


def test_nested_cascade_produces_independent_layers():
    """A cascading refinement (a selector-bearing nestedRules entry) has no
    MapLibre nesting equivalent — it must flatten into its own layer, AND-
    merged selector and merged symbolizer, same as the SLD/SE writer.
    """
    style = Style.from_dict(
        {
            "stylingRules": [
                {
                    "name": "Landuse",
                    "selector": {"op": "=", "args": [{"property": "type"}, "vector"]},
                    "symbolizer": {"visibility": False},
                    "nestedRules": [
                        {
                            "selector": {
                                "op": "=",
                                "args": [{"property": "FunctionCode"}, "park"],
                            },
                            "symbolizer": {"fill": {"color": "darkGreen"}},
                        }
                    ],
                }
            ]
        }
    )
    out = MaplibreWriter().write(style)
    # the empty base/gate rule is dropped; one layer remains
    assert len(out["layers"]) == 1
    layer = out["layers"][0]
    assert layer["paint"] == {"fill-color": "darkGreen"}
    assert layer["filter"] == [
        "all",
        ["==", ["get", "type"], "vector"],
        ["==", ["get", "FunctionCode"], "park"],
    ]
    assert_maplibre_valid(out)


def test_unnamed_cascade_children_get_synthesized_ids():
    """A refinement usually only narrows the selector and carries no name
    of its own — it inherits its nearest named ancestor's, disambiguated
    with a positional suffix (a MapLibre layer id must be unique).
    """
    style = Style.from_dict(
        {
            "stylingRules": [
                {
                    "name": "Landuse",
                    "symbolizer": {"visibility": False},
                    "nestedRules": [
                        {
                            "selector": {
                                "op": "=",
                                "args": [{"property": "K"}, "a"],
                            },
                            "symbolizer": {"fill": {"color": "red"}},
                        },
                        {
                            "selector": {
                                "op": "=",
                                "args": [{"property": "K"}, "b"],
                            },
                            "symbolizer": {"fill": {"color": "blue"}},
                        },
                    ],
                }
            ]
        }
    )
    out = MaplibreWriter().write(style)
    assert [lyr["id"] for lyr in out["layers"]] == ["Landuse-1", "Landuse-2"]
    assert_maplibre_valid(out)


def test_explicitly_named_cascade_child_keeps_its_own_name():
    style = Style.from_dict(
        {
            "stylingRules": [
                {
                    "name": "Landuse",
                    "symbolizer": {"visibility": False},
                    "nestedRules": [
                        {
                            "name": "Parks",
                            "selector": {
                                "op": "=",
                                "args": [{"property": "K"}, "park"],
                            },
                            "symbolizer": {"fill": {"color": "green"}},
                        }
                    ],
                }
            ]
        }
    )
    out = MaplibreWriter().write(style)
    assert [lyr["id"] for lyr in out["layers"]] == ["Parks"]


def test_selectorless_nested_rule_is_rejected():
    """A selector-less nestedRules entry is an OGC 'else' rule — MapLibre
    has no equivalent concept, so this must raise rather than be dropped.
    """
    style = Style.from_dict(
        {
            "stylingRules": [
                {
                    "name": "Roads",
                    "symbolizer": {"stroke": {"color": "red"}},
                    "nestedRules": [{"symbolizer": {"stroke": {"color": "gray"}}}],
                }
            ]
        }
    )
    with pytest.raises(NotImplementedError, match="'else' rule"):
        MaplibreWriter().write(style)


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


def test_label_text_becomes_a_symbol_layer():
    style = Style.from_dict(
        {
            "stylingRules": [
                {
                    "name": "labels",
                    "symbolizer": {
                        "label": {
                            "elements": [
                                {
                                    "type": "Text",
                                    "text": {"property": "name"},
                                    "position": {"x": 0, "y": 1.5},
                                    "alignment": ["center", "top"],
                                    "font": {
                                        "face": "Open Sans Semibold",
                                        "size": 12,
                                        "color": "#1077b0",
                                        "outline": {"color": "#fff", "size": 1},
                                    },
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
    assert layer["type"] == "symbol"
    assert layer["layout"] == {
        "text-field": "{name}",
        "text-offset": [0, 1.5],
        "text-anchor": "top",
        "text-font": ["Open Sans Semibold"],
        "text-size": 12,
    }
    assert layer["paint"] == {
        "text-color": "#1077b0",
        "text-halo-color": "#fff",
        "text-halo-width": 1,
    }
    assert_maplibre_valid(out)


def test_icon_marker_becomes_a_symbol_layer():
    style = Style.from_dict(
        {
            "stylingRules": [
                {
                    "name": "poi",
                    "symbolizer": {
                        "marker": {
                            "elements": [
                                {
                                    "type": "Image",
                                    "image": {"id": "dot.sdf"},
                                    "opacity": 0.8,
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
    assert layer["type"] == "symbol"
    assert layer["layout"] == {"icon-image": "dot.sdf"}
    assert layer["paint"] == {"icon-opacity": 0.8}
    assert_maplibre_valid(out)


def test_label_and_icon_marker_share_one_symbol_layer():
    style = Style.from_dict(
        {
            "stylingRules": [
                {
                    "name": "poi",
                    "symbolizer": {
                        "label": {"elements": [{"type": "Text", "text": "Foo"}]},
                        "marker": {
                            "elements": [{"type": "Image", "image": {"id": "dot.sdf"}}]
                        },
                    },
                }
            ]
        }
    )
    out = MaplibreWriter().write(style)
    assert len(out["layers"]) == 1
    layer = out["layers"][0]
    assert layer["type"] == "symbol"
    assert layer["layout"]["text-field"] == "Foo"
    assert layer["layout"]["icon-image"] == "dot.sdf"
    assert_maplibre_valid(out)


def test_multi_element_label_is_rejected():
    style = Style.from_dict(
        {
            "stylingRules": [
                {
                    "name": "labels",
                    "symbolizer": {
                        "label": {
                            "elements": [
                                {"type": "Text", "text": "a"},
                                {"type": "Text", "text": "b"},
                            ]
                        }
                    },
                }
            ]
        }
    )
    with pytest.raises(NotImplementedError):
        MaplibreWriter().write(style)


def test_non_text_label_element_is_rejected():
    style = Style.from_dict(
        {
            "stylingRules": [
                {
                    "name": "labels",
                    "symbolizer": {
                        "label": {"elements": [{"type": "Image", "image": {"id": "x"}}]}
                    },
                }
            ]
        }
    )
    with pytest.raises(NotImplementedError):
        MaplibreWriter().write(style)


def test_label_with_circle_marker_is_rejected():
    style = Style.from_dict(
        {
            "stylingRules": [
                {
                    "name": "labels",
                    "symbolizer": {
                        "label": {"elements": [{"type": "Text", "text": "a"}]},
                        "marker": {"elements": [{"type": "Circle", "radius": 5}]},
                    },
                }
            ]
        }
    )
    with pytest.raises(NotImplementedError):
        MaplibreWriter().write(style)


def test_label_with_fill_becomes_two_layers():
    """A symbolizer with both a label and a fill has no single-layer
    MapLibre equivalent — it expands to a ``fill`` layer and a ``symbol``
    layer, id-suffixed since the rule name alone is no longer unique.
    """
    style = Style.from_dict(
        {
            "stylingRules": [
                {
                    "name": "labels",
                    "symbolizer": {
                        "label": {"elements": [{"type": "Text", "text": "a"}]},
                        "fill": {"color": "red"},
                    },
                }
            ]
        }
    )
    out = MaplibreWriter().write(style)
    assert [(lyr["id"], lyr["type"]) for lyr in out["layers"]] == [
        ("labels-fill", "fill"),
        ("labels-symbol", "symbol"),
    ]
    assert out["layers"][0]["paint"] == {"fill-color": "red"}
    assert out["layers"][1]["layout"] == {"text-field": "a"}
    assert_maplibre_valid(out)


def test_font_bold_is_rejected():
    style = Style.from_dict(
        {
            "stylingRules": [
                {
                    "name": "labels",
                    "symbolizer": {
                        "label": {
                            "elements": [
                                {
                                    "type": "Text",
                                    "text": "a",
                                    "font": {"bold": True},
                                }
                            ]
                        }
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


def test_multi_layer_rule_shares_filter_and_visibility():
    """``filter``/``visibility`` apply identically to every layer a single
    rule expands into, not just the first.
    """
    style = Style.from_dict(
        {
            "stylingRules": [
                {
                    "name": "x",
                    "selector": {"op": "=", "args": [{"property": "k"}, "v"]},
                    "symbolizer": {
                        "visibility": False,
                        "fill": {"color": "red"},
                        "stroke": {"color": "black", "width": 3},
                    },
                }
            ]
        }
    )
    out = MaplibreWriter().write(style)
    assert len(out["layers"]) == 2
    for layer in out["layers"]:
        assert layer["filter"] == ["==", ["get", "k"], "v"]
        assert layer["layout"] == {"visibility": "none"}
    assert_maplibre_valid(out)


def test_datalayer_id_selector_is_dropped_not_an_error():
    """A ``sysId dataLayer.id = <name>`` conjunct is the implicit
    self-reference a CartoSym-CSS ``RuleName[...]`` rule always carries —
    redundant with the MapLibre layer's own ``id`` and with no
    data-source concept to bind to in this codec — dropped rather than
    raised on, unlike any other ``sysId``.
    """
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
    out = MaplibreWriter().write(style)
    assert "filter" not in out["layers"][0]
    assert_maplibre_valid(out)


def test_datalayer_id_conjunct_dropped_among_siblings():
    """The same conjunct, AND-combined with a real property predicate,
    is stripped out while the rest of the filter survives.
    """
    style = Style.from_dict(
        {
            "stylingRules": [
                {
                    "name": "x",
                    "selector": {
                        "op": "and",
                        "args": [
                            {"op": "=", "args": [{"sysId": "dataLayer.id"}, "L"]},
                            {"op": "=", "args": [{"property": "k"}, "v"]},
                        ],
                    },
                    "symbolizer": {"fill": {"color": "red"}},
                }
            ]
        }
    )
    out = MaplibreWriter().write(style)
    assert out["layers"][0]["filter"] == ["==", ["get", "k"], "v"]
    assert_maplibre_valid(out)


def test_other_sysid_selector_is_still_rejected():
    style = Style.from_dict(
        {
            "stylingRules": [
                {
                    "name": "x",
                    "selector": {
                        "op": "=",
                        "args": [{"sysId": "dataLayer.type"}, "vector"],
                    },
                    "symbolizer": {"fill": {"color": "red"}},
                }
            ]
        }
    )
    with pytest.raises(NotImplementedError):
        MaplibreWriter().write(style)


def test_fill_with_full_stroke_becomes_fill_and_line_layers():
    """A stroke with a ``width``/``opacity`` (not just a plain outline
    colour) has no ``fill-outline-color`` equivalent — it gets its own
    ``line`` layer alongside the ``fill`` one, id-suffixed.
    """
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
    out = MaplibreWriter().write(style)
    assert [(lyr["id"], lyr["type"]) for lyr in out["layers"]] == [
        ("x-fill", "fill"),
        ("x-line", "line"),
    ]
    assert out["layers"][0]["paint"] == {"fill-color": "red"}
    assert out["layers"][1]["paint"] == {"line-color": "black", "line-width": 3}
    assert_maplibre_valid(out)


def test_fill_with_plain_outline_stroke_stays_one_layer():
    """A stroke with only a ``color`` (no ``width``/``opacity``) still
    inlines into ``fill-outline-color`` — no split, unchanged behaviour.
    """
    style = Style.from_dict(
        {
            "stylingRules": [
                {
                    "name": "x",
                    "symbolizer": {
                        "fill": {"color": "red"},
                        "stroke": {"color": "black"},
                    },
                }
            ]
        }
    )
    out = MaplibreWriter().write(style)
    assert [(lyr["id"], lyr["type"]) for lyr in out["layers"]] == [("x", "fill")]
    assert out["layers"][0]["paint"] == {
        "fill-color": "red",
        "fill-outline-color": "black",
    }
    assert_maplibre_valid(out)


def test_circle_marker_with_fill_becomes_two_layers():
    """A symbolizer with both a marker and a fill/stroke needs several
    MapLibre layers too — same split, ``circle`` instead of ``symbol``.
    """
    style = Style.from_dict(
        {
            "stylingRules": [
                {
                    "name": "pts",
                    "symbolizer": {
                        "fill": {"color": "red"},
                        "marker": {"elements": [{"type": "Circle", "radius": 5}]},
                    },
                }
            ]
        }
    )
    out = MaplibreWriter().write(style)
    assert [(lyr["id"], lyr["type"]) for lyr in out["layers"]] == [
        ("pts-fill", "fill"),
        ("pts-circle", "circle"),
    ]
    assert_maplibre_valid(out)


def test_background_vendor_tag_becomes_background_layer():
    style = Style.from_dict(
        {
            "stylingRules": [
                {
                    "name": "bg",
                    "symbolizer": {
                        "fill": {"color": "red"},
                        "vendor.maplibre.layer-type": "background",
                    },
                }
            ]
        }
    )
    out = MaplibreWriter().write(style)
    assert out["sources"] == {}
    assert out["layers"] == [
        {"id": "bg", "type": "background", "paint": {"background-color": "red"}}
    ]
    assert_maplibre_valid(out)


def test_viz_sd_selector_becomes_zoom_range():
    style = Style.from_dict(
        {
            "stylingRules": [
                {
                    "name": "fill",
                    "selector": {
                        "op": "and",
                        "args": [
                            {
                                "op": "<=",
                                "args": [
                                    {"sysId": "viz.sd"},
                                    scale_denominator_from_zoom(10),
                                ],
                            },
                            {
                                "op": ">",
                                "args": [
                                    {"sysId": "viz.sd"},
                                    scale_denominator_from_zoom(12),
                                ],
                            },
                        ],
                    },
                    "symbolizer": {"fill": {"color": "red"}},
                }
            ]
        }
    )
    out = MaplibreWriter().write(style)
    layer = out["layers"][0]
    assert layer["minzoom"] == 10
    assert layer["maxzoom"] == 12
    assert "filter" not in layer
    assert_maplibre_valid(out)


def test_viz_sd_selector_merges_with_residual_filter():
    style = Style.from_dict(
        {
            "stylingRules": [
                {
                    "name": "fill",
                    "selector": {
                        "op": "and",
                        "args": [
                            {
                                "op": "<=",
                                "args": [
                                    {"sysId": "viz.sd"},
                                    scale_denominator_from_zoom(10),
                                ],
                            },
                            {"op": "=", "args": [{"property": "class"}, "water"]},
                        ],
                    },
                    "symbolizer": {"fill": {"color": "red"}},
                }
            ]
        }
    )
    layer = MaplibreWriter().write(style)["layers"][0]
    assert layer["minzoom"] == 10
    assert layer["filter"] == ["==", ["get", "class"], "water"]


def test_viz_sd_strict_lower_bound_becomes_a_zoom_filter():
    """``viz.sd < N`` has no minzoom/maxzoom shape (only ``<=``/``>`` do) —
    it becomes a ``["zoom"]`` filter conjunct instead (see
    ``_zoom.zoom_filter_conjunct``), not a minzoom/maxzoom layer property.
    """
    style = Style.from_dict(
        {
            "stylingRules": [
                {
                    "name": "fill",
                    "selector": {"op": "<", "args": [{"sysId": "viz.sd"}, 100000]},
                    "symbolizer": {"fill": {"color": "red"}},
                }
            ]
        }
    )
    layer = MaplibreWriter().write(style)["layers"][0]
    assert "minzoom" not in layer
    assert "maxzoom" not in layer
    assert layer["filter"] == [">", ["zoom"], zoom_from_scale_denominator(100000)]
    assert_maplibre_valid(MaplibreWriter().write(style))


def test_background_with_zoom_range_selector_is_kept():
    style = Style.from_dict(
        {
            "stylingRules": [
                {
                    "name": "bg",
                    "selector": {
                        "op": "<=",
                        "args": [{"sysId": "viz.sd"}, scale_denominator_from_zoom(5)],
                    },
                    "symbolizer": {
                        "fill": {"color": "red"},
                        "vendor.maplibre.layer-type": "background",
                    },
                }
            ]
        }
    )
    out = MaplibreWriter().write(style)
    layer = out["layers"][0]
    assert layer["minzoom"] == 5
    assert "filter" not in layer
    assert_maplibre_valid(out)


def test_background_with_stroke_is_rejected():
    style = Style.from_dict(
        {
            "stylingRules": [
                {
                    "name": "bg",
                    "symbolizer": {
                        "fill": {"color": "red"},
                        "stroke": {"color": "black"},
                        "vendor.maplibre.layer-type": "background",
                    },
                }
            ]
        }
    )
    with pytest.raises(NotImplementedError):
        MaplibreWriter().write(style)


def test_background_with_selector_is_rejected():
    style = Style.from_dict(
        {
            "stylingRules": [
                {
                    "name": "bg",
                    "selector": {"op": "=", "args": [{"property": "k"}, "v"]},
                    "symbolizer": {
                        "fill": {"color": "red"},
                        "vendor.maplibre.layer-type": "background",
                    },
                }
            ]
        }
    )
    with pytest.raises(NotImplementedError):
        MaplibreWriter().write(style)


def test_unrecognised_vendor_extension_is_rejected():
    style = Style.from_dict(
        {
            "stylingRules": [
                {
                    "name": "x",
                    "symbolizer": {
                        "fill": {"color": "red"},
                        "vendor.geoserver.group": "layers",
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


@pytest.mark.parametrize(
    "expr",
    [
        ["get", "cls"],
        ["case", ["get", "big"], "#f00", "#00f"],
        ["match", ["get", "cls"], "park", "#0f0", "water", "#00f", "#888"],
        ["step", ["get", "rank"], "#eee", 3, "#aaa", 6, "#444"],
        ["interpolate", ["linear"], ["get", "zoom"], 0, "#fff", 10, "#000"],
        ["coalesce", ["get", "override"], ["get", "cls"], "#888"],
    ],
)
def test_fill_layer_value_expression_round_trip(expr):
    """A value expression on fill-color read → write → read is a model
    fixed point, and the written-back style is spec-valid MapLibre.
    """
    read = MaplibreReader()
    style = read.read(
        {
            "version": 8,
            "sources": {},
            "layers": [
                {
                    "id": "areas",
                    "type": "fill",
                    "source": "s",
                    "paint": {"fill-color": expr},
                }
            ],
        }
    )
    out = MaplibreWriter().write(style)
    assert_maplibre_valid(out)
    again = read.read(out)
    assert again.to_dict() == style.to_dict()
