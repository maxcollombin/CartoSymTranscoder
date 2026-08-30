"""MapLibre reader — fill / line / circle layers with constant paint values.

In scope this pass: ``fill`` / ``line`` / ``circle`` layers whose paint
values are constants (``circle`` → a ``marker`` with one ``Circle``). Symbol
/ background layers, MapLibre expressions and legacy functions must raise
``NotImplementedError`` (a clean rejection — never another exception type).
"""

from __future__ import annotations

from pathlib import Path

import pytest

from cartosym_transcoder.codecs.maplibre import MaplibreReader
from cartosym_transcoder.models.styles import Style

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
}

OUT_OF_SCOPE = {
    "background-color-literal": "background layer",
    "icon-image-literal": "symbol layer",
    "text-field-literal": "symbol layer",
    "fill-pattern-literal": "fill-pattern paint",
    "line-color-literal": "background layer sibling",
    "line-width-function": "background + legacy function",
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


def test_data_driven_value_raises():
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
                        "paint": {"fill-color": ["get", "colour"]},
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
