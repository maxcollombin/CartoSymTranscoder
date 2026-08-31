"""MapLibre reader — fill / line / circle / symbol / background layers.

In scope this pass: ``fill`` / ``line`` / ``circle`` / ``symbol`` /
``background`` layers whose paint / layout values are constants, or one
of the six MapLibre value-expression operators covered by
``codecs.maplibre._expressions`` (``circle`` → a ``marker`` with one
``Circle``; ``symbol`` → a ``label`` with one ``Text`` and/or a
``marker`` with one ``Image``; ``background`` → a ``Fill`` symbolizer
tagged ``vendor.maplibre.layer-type: "background"``). ``raster`` layers,
a layer's ``minzoom``/``maxzoom``, legacy zoom/property functions, any
other expression operator, and symbol constructs this pass does not
cover (a multi-family ``text-font`` stack, ``symbol-placement: line``,
…) must raise ``NotImplementedError`` (a clean rejection — never another
exception type).
"""

from __future__ import annotations

from pathlib import Path

import pytest

from pycartosym.codecs.maplibre import MaplibreReader
from pycartosym.models.styles import Style

_ATOMIC = Path(__file__).parent / "fixtures" / "maplibre" / "atomic"

# fixture stem -> the styling rules its layers should produce
IN_SCOPE: dict[str, list[dict]] = {
    "fill-opacity-default": [{"name": "fill", "symbolizer": {"fill": {}}}],
    "fill-color-literal": [{"name": "fill", "symbolizer": {"fill": {"color": "blue"}}}],
    "fill-outline-color-default": [
        {
            "name": "fill",
            "symbolizer": {"fill": {"color": "rgba(0,0,0,0)"}},
        }
    ],
    "fill-outline-color-literal": [
        {
            "name": "fill",
            "symbolizer": {
                "fill": {"color": "rgba(0,0,0,0)"},
                "stroke": {"color": "blue"},
            },
        }
    ],
    "line-simple": [{"name": "line", "symbolizer": {"stroke": {"width": 8.0}}}],
    "line-opacity-literal": [
        {
            "name": "line",
            "symbolizer": {"stroke": {"opacity": 0.3, "width": 8.0}},
        }
    ],
    "circle-radius-literal": [
        {
            "name": "circle",
            "symbolizer": {"marker": {"elements": [{"type": "Circle", "radius": 8}]}},
        }
    ],
    "circle-color-literal": [
        {
            "name": "circle",
            "symbolizer": {
                "marker": {
                    "elements": [
                        {"type": "Circle", "fill": {"color": "blue"}, "radius": 10}
                    ]
                }
            },
        }
    ],
    "circle-stroke-width-default": [
        {
            "name": "circle",
            "symbolizer": {
                "marker": {"elements": [{"type": "Circle", "fill": {"color": "#fff"}}]}
            },
        }
    ],
    "circle-stroke-literal": [
        {
            "name": "circle",
            "symbolizer": {
                "marker": {
                    "elements": [
                        {
                            "type": "Circle",
                            "fill": {"color": "#fff"},
                            "outline": {"color": "blue", "thickness": 2},
                        }
                    ]
                }
            },
        }
    ],
    "icon-image-literal": [
        {
            "name": "text",
            "symbolizer": {
                "marker": {
                    "elements": [
                        {
                            "type": "Image",
                            "image": {"id": "dot.sdf"},
                            "position": {"x": 0, "y": 0},
                        }
                    ]
                }
            },
        }
    ],
    "background-color-literal": [
        {
            "name": "background",
            "symbolizer": {
                "fill": {"color": "red"},
                "vendor.maplibre.layer-type": "background",
            },
        }
    ],
    "line-color-literal": [
        {
            "name": "background",
            "symbolizer": {
                "fill": {"color": "white"},
                "vendor.maplibre.layer-type": "background",
            },
        },
        {
            "name": "road",
            "symbolizer": {"stroke": {"color": "blue", "width": 10.0}},
        },
    ],
}

OUT_OF_SCOPE = {
    "text-field-literal": "multi-family text-font stack",
    "fill-pattern-literal": "fill-pattern paint",
    "line-width-function": "legacy zoom function on line-width",
}


@pytest.mark.parametrize("stem, expected", list(IN_SCOPE.items()))
def test_in_scope_fixture_reads(stem: str, expected: list[dict]):
    style = MaplibreReader().read(_ATOMIC / f"{stem}.json")
    assert isinstance(style, Style)
    assert style.to_dict()["stylingRules"] == expected


@pytest.mark.parametrize("stem", list(OUT_OF_SCOPE))
def test_out_of_scope_fixture_raises_not_implemented(stem: str):
    with pytest.raises(NotImplementedError):
        MaplibreReader().read(_ATOMIC / f"{stem}.json")


def test_every_atomic_fixture_is_classified():
    stems = {p.stem for p in _ATOMIC.glob("*.json")}
    assert stems == set(IN_SCOPE) | set(OUT_OF_SCOPE)


def test_reads_from_dict_and_string():
    style_dict = {
        "version": 8,
        "sources": {},
        "layers": [
            {"id": "l", "type": "line", "source": "s", "paint": {"line-color": "red"}}
        ],
    }
    from_dict = MaplibreReader().read(style_dict)
    import json

    from_str = MaplibreReader().read(json.dumps(style_dict))
    assert from_dict.to_dict() == from_str.to_dict()
    assert from_dict.to_dict()["stylingRules"][0]["symbolizer"]["stroke"] == {
        "color": "red"
    }


def test_style_with_no_layers_is_empty():
    style = MaplibreReader().read({"version": 8, "sources": {}, "layers": []})
    assert style.to_dict()["stylingRules"] == []


def test_non_v8_version_raises():
    with pytest.raises(NotImplementedError):
        MaplibreReader().read({"version": 7, "layers": []})


def test_layer_filter_maps_to_selector():
    style = MaplibreReader().read(
        {
            "version": 8,
            "sources": {},
            "layers": [
                {
                    "id": "l",
                    "type": "fill",
                    "source": "s",
                    "filter": ["==", "class", "water"],
                    "paint": {"fill-color": "blue"},
                }
            ],
        }
    )
    rule = style.to_dict()["stylingRules"][0]
    assert rule["selector"] == {
        "op": "=",
        "args": [{"property": "class"}, "water"],
    }


def test_unsupported_filter_key_raises():
    with pytest.raises(NotImplementedError):
        MaplibreReader().read(
            {
                "version": 8,
                "sources": {},
                "layers": [
                    {
                        "id": "l",
                        "type": "fill",
                        "source": "s",
                        "filter": ["==", "$type", "Polygon"],
                        "paint": {"fill-color": "blue"},
                    }
                ],
            }
        )


def test_get_expression_maps_to_property_ref():
    """['get', 'colour'] is one of the six in-scope value expressions."""
    style = MaplibreReader().read(
        {
            "version": 8,
            "sources": {},
            "layers": [
                {
                    "id": "l",
                    "type": "fill",
                    "source": "s",
                    "paint": {"fill-color": ["get", "colour"]},
                }
            ],
        }
    )
    fill = style.styling_rules[0].symbolizer.fill
    assert fill.color.property == "colour"


def test_legacy_zoom_function_raises():
    with pytest.raises(NotImplementedError):
        MaplibreReader().read(
            {
                "version": 8,
                "sources": {},
                "layers": [
                    {
                        "id": "l",
                        "type": "fill",
                        "source": "s",
                        "paint": {"fill-color": {"stops": [[0, "blue"], [10, "red"]]}},
                    }
                ],
            }
        )


def test_out_of_scope_expression_operator_raises():
    """A comparison/arithmetic expression is real MapLibre syntax, but not
    one of the six operators this codec's value-expression pass covers.
    """
    with pytest.raises(NotImplementedError):
        MaplibreReader().read(
            {
                "version": 8,
                "sources": {},
                "layers": [
                    {
                        "id": "l",
                        "type": "fill",
                        "source": "s",
                        "paint": {"fill-opacity": ["+", ["get", "a"], 1]},
                    }
                ],
            }
        )


def test_visibility_none_maps_to_false():
    style = MaplibreReader().read(
        {
            "version": 8,
            "sources": {},
            "layers": [
                {
                    "id": "l",
                    "type": "fill",
                    "source": "s",
                    "layout": {"visibility": "none"},
                    "paint": {"fill-color": "blue"},
                }
            ],
        }
    )
    sym = style.to_dict()["stylingRules"][0]["symbolizer"]
    assert sym["visibility"] is False


# ---------------------------------------------------------------------------
# symbol layer (label / marker)
# ---------------------------------------------------------------------------


def _symbol_layer(layout: dict, paint: dict | None = None) -> dict:
    return {
        "version": 8,
        "sources": {},
        "layers": [
            {
                "id": "l",
                "type": "symbol",
                "source": "s",
                "layout": layout,
                "paint": paint or {},
            }
        ],
    }


def test_text_field_property_token():
    style = MaplibreReader().read(_symbol_layer({"text-field": "{name}"}))
    el = style.styling_rules[0].symbolizer.label.elements[0]
    assert el.text == {"property": "name"}


def test_text_field_literal_string():
    style = MaplibreReader().read(_symbol_layer({"text-field": "Fixed label"}))
    el = style.styling_rules[0].symbolizer.label.elements[0]
    assert el.text == "Fixed label"


def test_text_field_mixed_template_raises():
    with pytest.raises(NotImplementedError):
        MaplibreReader().read(_symbol_layer({"text-field": "{name} ({code})"}))


def test_text_anchor_maps_to_alignment():
    style = MaplibreReader().read(
        _symbol_layer({"text-field": "x", "text-anchor": "bottom-left"})
    )
    el = style.styling_rules[0].symbolizer.label.elements[0]
    assert el.alignment == ["left", "bottom"]


def test_text_offset_maps_to_position():
    style = MaplibreReader().read(
        _symbol_layer({"text-field": "x", "text-offset": [1, -2]})
    )
    el = style.styling_rules[0].symbolizer.label.elements[0]
    assert (el.position.x, el.position.y) == (1, -2)


def test_text_transform_none_is_ignored():
    style = MaplibreReader().read(
        _symbol_layer({"text-field": "x", "text-transform": "none"})
    )
    el = style.styling_rules[0].symbolizer.label.elements[0]
    assert getattr(el, "font", None) is None


def test_text_transform_uppercase_raises():
    with pytest.raises(NotImplementedError):
        MaplibreReader().read(
            _symbol_layer({"text-field": "x", "text-transform": "uppercase"})
        )


def test_multi_family_text_font_raises():
    with pytest.raises(NotImplementedError):
        MaplibreReader().read(
            _symbol_layer({"text-field": "x", "text-font": ["A", "B"]})
        )


def test_symbol_placement_line_raises():
    with pytest.raises(NotImplementedError):
        MaplibreReader().read(
            _symbol_layer({"text-field": "x", "symbol-placement": "line"})
        )


def test_symbol_without_text_or_icon_raises():
    with pytest.raises(NotImplementedError):
        MaplibreReader().read(_symbol_layer({}))


def test_icon_opacity_without_icon_image_raises():
    with pytest.raises(NotImplementedError):
        MaplibreReader().read(_symbol_layer({}, {"icon-opacity": 0.5}))


def test_icon_image_maps_to_marker():
    style = MaplibreReader().read(_symbol_layer({"icon-image": "poi.png"}))
    sym = style.styling_rules[0].symbolizer
    assert sym.label is None
    assert sym.marker.elements[0]["image"] == {"id": "poi.png"}


def test_text_and_icon_together_produce_label_and_marker():
    style = MaplibreReader().read(
        _symbol_layer({"text-field": "x", "icon-image": "poi.png"})
    )
    sym = style.styling_rules[0].symbolizer
    assert sym.label is not None
    assert sym.marker is not None


def test_text_halo_maps_to_font_outline():
    style = MaplibreReader().read(
        _symbol_layer(
            {"text-field": "x"},
            {"text-halo-color": "#fff", "text-halo-width": 1.5},
        )
    )
    el = style.styling_rules[0].symbolizer.label.elements[0]
    assert el.font["outline"] == {"color": "#fff", "size": 1.5}


def test_unsupported_symbol_layout_key_raises():
    with pytest.raises(NotImplementedError):
        MaplibreReader().read(_symbol_layer({"text-field": "x", "text-max-width": 10}))


def _fill_style(layer: dict) -> dict:
    return {"version": 8, "sources": {}, "layers": [layer]}


def test_background_pattern_raises():
    layer = {"id": "bg", "type": "background", "paint": {"background-pattern": "p"}}
    with pytest.raises(NotImplementedError):
        MaplibreReader().read(_fill_style(layer))


@pytest.mark.parametrize("zoom_key", ["minzoom", "maxzoom"])
def test_layer_zoom_range_raises(zoom_key: str):
    layer = {
        "id": "fill",
        "type": "fill",
        "source": "s",
        "paint": {"fill-color": "red"},
        zoom_key: 10,
    }
    with pytest.raises(NotImplementedError):
        MaplibreReader().read(_fill_style(layer))
