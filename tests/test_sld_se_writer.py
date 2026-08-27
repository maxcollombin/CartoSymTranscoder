"""Writer-direction tests for the SLD/SE codec (vector + Part-1 raster).

Builds small Style/Symbolizer objects in-code and asserts on the parsed-back
XML tree (not raw string matching, to avoid whitespace/attribute-order
brittleness).
"""

import json
from pathlib import Path

import pytest
from lxml import etree

from cartosym_transcoder.codecs.sld_se._symbolizer import symbolizer_to_elements
from cartosym_transcoder.codecs.sld_se.writer import SldSeWriter
from cartosym_transcoder.models.styles import Style

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT / "output"

NS = {
    "sld": "http://www.opengis.net/sld",
    "se": "http://www.opengis.net/se",
    "ogc": "http://www.opengis.net/ogc",
    "gml": "http://www.opengis.net/gml",
    "xlink": "http://www.w3.org/1999/xlink",
}


def _write(style_dict) -> etree._Element:
    style = Style.from_dict(style_dict)
    xml = SldSeWriter().write(style)
    return etree.fromstring(xml.encode("utf-8"))


def _rule_style(symbolizer, selector=None, nested_rules=None):
    rule = {"name": "R", "symbolizer": symbolizer}
    if selector is not None:
        rule["selector"] = selector
    if nested_rules is not None:
        rule["nestedRules"] = nested_rules
    return {"stylingRules": [rule]}


class TestWriteBasicSymbolizers:
    def test_fill_and_stroke_produce_polygon_symbolizer(self):
        root = _write(
            _rule_style(
                {
                    "fill": {"color": "gray", "opacity": 0.5},
                    "stroke": {"color": "#202020", "width": {"px": 2.0}},
                }
            )
        )
        poly = root.find(".//se:PolygonSymbolizer", NS)
        assert poly is not None
        assert root.find(".//se:LineSymbolizer", NS) is None
        fill_params = {
            p.get("name"): p.text for p in poly.findall("se:Fill/se:SvgParameter", NS)
        }
        assert fill_params["fill"] == "#808080"
        assert fill_params["fill-opacity"] == "0.5"
        stroke_params = {
            p.get("name"): p.text for p in poly.findall("se:Stroke/se:SvgParameter", NS)
        }
        assert stroke_params["stroke"] == "#202020"
        assert stroke_params["stroke-width"] == "2"

    def test_stroke_only_produces_line_symbolizer(self):
        root = _write(_rule_style({"stroke": {"color": "red", "width": {"px": 3.0}}}))
        assert root.find(".//se:PolygonSymbolizer", NS) is None
        line = root.find(".//se:LineSymbolizer", NS)
        assert line is not None
        stroke_params = {
            p.get("name"): p.text for p in line.findall("se:Stroke/se:SvgParameter", NS)
        }
        assert stroke_params["stroke"] == "#ff0000"

    def test_stroke_width_as_raw_unit_string_is_parsed(self):
        """CscssReader bypasses Converter._fix_unit_values, so some
        UnitValue fields reach this codec as a raw 'N unit' string (e.g.
        input/3-vector-line.cscss's alter-overridden width) rather than a
        {unit: value} dict — must still parse, not raise issue #11."""
        root = _write(_rule_style({"stroke": {"color": "red", "width": "8.0 m"}}))
        line = root.find(".//se:LineSymbolizer", NS)
        stroke_params = {
            p.get("name"): p.text for p in line.findall("se:Stroke/se:SvgParameter", NS)
        }
        assert stroke_params["stroke-width"] == "8"

    def test_marker_dot_produces_point_symbolizer(self):
        root = _write(
            _rule_style(
                {
                    "marker": {
                        "elements": [
                            {
                                "type": "Dot",
                                "size": {"px": 10},
                                "position": {"x": 0, "y": 0},
                                "color": "white",
                            }
                        ]
                    }
                }
            )
        )
        point = root.find(".//se:PointSymbolizer", NS)
        assert point is not None
        wkn = point.find("se:Graphic/se:Mark/se:WellKnownName", NS)
        assert wkn.text == "circle"
        size = point.find("se:Graphic/se:Size", NS)
        assert size.text == "10"

    def test_label_text_produces_text_symbolizer(self):
        root = _write(
            _rule_style(
                {
                    "label": {
                        "elements": [
                            {
                                "type": "Text",
                                "text": {"property": "Name"},
                                "position": {"x": 0, "y": 0},
                            }
                        ]
                    }
                }
            )
        )
        text_sym = root.find(".//se:TextSymbolizer", NS)
        assert text_sym is not None
        prop = text_sym.find("se:Label/ogc:PropertyName", NS)
        assert prop.text == "Name"

    def test_multiple_dots_produce_sibling_point_symbolizers(self):
        root = _write(
            _rule_style(
                {
                    "marker": {
                        "elements": [
                            {
                                "type": "Dot",
                                "size": {"px": 10},
                                "position": {"x": 0, "y": 0},
                                "color": "white",
                            },
                            {
                                "type": "Dot",
                                "size": {"px": 8},
                                "position": {"x": 0, "y": 0},
                                "color": "orange",
                            },
                        ]
                    }
                }
            )
        )
        points = root.findall(".//se:PointSymbolizer", NS)
        assert len(points) == 2


class TestWriteFilter:
    def test_comparison_operators(self):
        for op, tag in [
            ("=", "PropertyIsEqualTo"),
            ("!=", "PropertyIsNotEqualTo"),
            ("<", "PropertyIsLessThan"),
            (">", "PropertyIsGreaterThan"),
            ("<=", "PropertyIsLessThanOrEqualTo"),
            (">=", "PropertyIsGreaterThanOrEqualTo"),
        ]:
            root = _write(
                _rule_style(
                    {"fill": {"color": "red"}},
                    selector={"op": op, "args": [{"property": "X"}, 1]},
                )
            )
            assert (
                root.find(f".//ogc:{tag}", NS) is not None
            ), f"missing {tag} for op {op}"

    def test_and_or_not(self):
        root = _write(
            _rule_style(
                {"fill": {"color": "red"}},
                selector={
                    "op": "and",
                    "args": [
                        {"op": "=", "args": [{"property": "A"}, 1]},
                        {
                            "op": "or",
                            "args": [
                                {"op": "=", "args": [{"property": "B"}, 2]},
                                {
                                    "op": "not",
                                    "args": [
                                        {"op": "=", "args": [{"property": "C"}, 3]}
                                    ],
                                },
                            ],
                        },
                    ],
                },
            )
        )
        assert root.find(".//ogc:And", NS) is not None
        assert root.find(".//ogc:Or", NS) is not None
        assert root.find(".//ogc:Not", NS) is not None

    def test_between_like_isnull(self):
        root = _write(
            _rule_style(
                {"fill": {"color": "red"}},
                selector={
                    "op": "and",
                    "args": [
                        {"op": "between", "args": [{"property": "P"}, 1, 5]},
                        {"op": "like", "args": [{"property": "N"}, "%x%"]},
                        {"op": "isnull", "args": [{"property": "Q"}]},
                    ],
                },
            )
        )
        assert root.find(".//ogc:PropertyIsBetween", NS) is not None
        assert root.find(".//ogc:PropertyIsLike", NS) is not None
        assert root.find(".//ogc:PropertyIsNull", NS) is not None

    def test_datalayer_id_consumed_not_emitted_as_filter(self):
        root = _write(
            _rule_style(
                {"fill": {"color": "red"}},
                selector={"op": "=", "args": [{"sysId": "dataLayer.id"}, "Landuse"]},
            )
        )
        assert root.find(".//se:FeatureTypeName", NS).text == "Landuse"
        assert root.find(".//ogc:Filter", NS) is None


class TestWriteElseRule:
    def test_else_filter_uses_se_namespace(self):
        root = _write(
            _rule_style(
                {"fill": {"color": "red"}},
                nested_rules=[{"symbolizer": {"fill": {"color": "gray"}}}],
            )
        )
        rules = root.findall(".//se:Rule", NS)
        assert len(rules) == 2
        assert rules[0].find("se:ElseFilter", NS) is None
        assert rules[1].find("se:ElseFilter", NS) is not None
        # Regression guard for mapping-issues issue #1: never ogc:ElseFilter.
        assert root.find(".//ogc:ElseFilter", NS) is None


class TestWriteFeatureTypeName:
    def test_rules_with_different_ids_get_separate_feature_type_styles(self):
        style_dict = {
            "stylingRules": [
                {
                    "name": "A",
                    "selector": {
                        "op": "=",
                        "args": [{"sysId": "dataLayer.id"}, "Landuse"],
                    },
                    "symbolizer": {"fill": {"color": "red"}},
                },
                {
                    "name": "B",
                    "selector": {
                        "op": "=",
                        "args": [{"sysId": "dataLayer.id"}, "Roads"],
                    },
                    "symbolizer": {"stroke": {"color": "black", "width": {"px": 1.0}}},
                },
            ]
        }
        root = _write(style_dict)
        fts_list = root.findall(".//se:FeatureTypeStyle", NS)
        assert len(fts_list) == 2
        names = {fts.find("se:FeatureTypeName", NS).text for fts in fts_list}
        assert names == {"Landuse", "Roads"}

    def test_datalayer_type_and_dims_conjuncts_stripped_leaves_no_filter(self):
        root = _write(
            _rule_style(
                {"fill": {"color": "gray"}},
                selector={
                    "op": "and",
                    "args": [
                        {"op": "=", "args": [{"sysId": "dataLayer.id"}, "Landuse"]},
                        {
                            "op": "and",
                            "args": [
                                {
                                    "op": "=",
                                    "args": [{"sysId": "dataLayer.type"}, "vector"],
                                },
                                {
                                    "op": "=",
                                    "args": [
                                        {
                                            "sysId": "dataLayer.featuresGeometryDimensions"  # noqa: E501
                                        },
                                        2,
                                    ],
                                },
                            ],
                        },
                    ],
                },
            )
        )
        assert root.find(".//se:FeatureTypeName", NS).text == "Landuse"
        assert root.find(".//ogc:Filter", NS) is None

    def test_datalayer_type_dims_stripped_leaves_other_conjunct_as_filter(self):
        root = _write(
            _rule_style(
                {"fill": {"color": "gray"}},
                selector={
                    "op": "and",
                    "args": [
                        {"op": "=", "args": [{"sysId": "dataLayer.id"}, "Landuse"]},
                        {"op": "=", "args": [{"sysId": "dataLayer.type"}, "vector"]},
                        {
                            "op": "=",
                            "args": [
                                {"sysId": "dataLayer.featuresGeometryDimensions"},
                                2,
                            ],
                        },
                        {"op": "=", "args": [{"property": "FunctionCode"}, "parking"]},
                    ],
                },
            )
        )
        assert root.find(".//se:FeatureTypeName", NS).text == "Landuse"
        filt = root.find(".//ogc:Filter", NS)
        assert filt is not None
        assert filt.find(".//ogc:PropertyIsEqualTo", NS) is not None
        assert filt.find(".//ogc:PropertyName", NS).text == "FunctionCode"


class TestWriteAlwaysSvgParameter:
    def test_no_css_parameter_anywhere(self):
        root = _write(
            _rule_style(
                {
                    "fill": {"color": "gray", "opacity": 0.5},
                    "stroke": {"color": "black", "width": {"px": 1.0}},
                }
            )
        )
        assert root.findall(".//se:CssParameter", NS) == []
        assert root.findall(".//CssParameter") == []


class TestWriteOutOfScopeRaises:
    def test_raster_color_channels_raises(self):
        with pytest.raises(NotImplementedError):
            _write(_rule_style({"colorChannels": {"r": "R", "g": "G", "b": "B"}}))

    def test_fill_hatch_raises(self):
        with pytest.raises(NotImplementedError):
            _write(_rule_style({"fill": {"hatch": {"width": {"px": 1.0}}}}))

    def test_stroke_casing_raises(self):
        with pytest.raises(NotImplementedError):
            _write(
                _rule_style(
                    {"stroke": {"color": "black", "casing": {"color": "white"}}}
                )
            )

    def test_shape_graphic_raises(self):
        """Image is now supported (see TestWriteImage) — Shape/Circle/
        Rectangle remain the unsupported graphic types."""
        with pytest.raises(NotImplementedError):
            _write(
                _rule_style(
                    {
                        "marker": {
                            "elements": [
                                {
                                    "type": "Shape",
                                    "size": {"px": 5},
                                    "position": {"x": 0, "y": 0},
                                }
                            ]
                        }
                    }
                )
            )

    def test_metadata_authors_raises(self):
        style_dict = _rule_style({"fill": {"color": "red"}})
        style_dict["metadata"] = {"title": "T", "authors": ["Alice"]}
        with pytest.raises(NotImplementedError):
            _write(style_dict)

    def test_label_placement_raises(self):
        with pytest.raises(NotImplementedError):
            _write(
                _rule_style(
                    {
                        "label": {
                            "elements": [
                                {
                                    "type": "Text",
                                    "text": "X",
                                    "position": {"x": 0, "y": 0},
                                }
                            ],
                            "placement": {"type": "line"},
                        }
                    }
                )
            )


class TestWriteImage:
    def test_image_produces_external_graphic(self):
        root = _write(
            _rule_style(
                {
                    "marker": {
                        "elements": [
                            {
                                "type": "Image",
                                "image": {
                                    "uri": "http://example.com/x.png",
                                    "type": "image/png",
                                },
                            }
                        ]
                    }
                }
            )
        )
        point = root.find(".//se:PointSymbolizer", NS)
        assert point is not None
        online = point.find("se:Graphic/se:ExternalGraphic/se:OnlineResource", NS)
        assert online is not None
        assert online.get(f"{{{NS['xlink']}}}href") == "http://example.com/x.png"
        fmt = point.find("se:Graphic/se:ExternalGraphic/se:Format", NS)
        assert fmt is not None and fmt.text == "image/png"

    def test_image_hot_spot_produces_anchor_point(self):
        root = _write(
            _rule_style(
                {
                    "marker": {
                        "elements": [
                            {
                                "type": "Image",
                                "image": {"uri": "http://example.com/x.png"},
                                "hotSpot": [{"pc": 50}, {"pc": 50}],
                            }
                        ]
                    }
                }
            )
        )
        anchor = root.find(".//se:PointSymbolizer/se:AnchorPoint", NS)
        assert anchor is not None
        assert anchor.find("se:AnchorPointX", NS).text == "0.5"
        assert anchor.find("se:AnchorPointY", NS).text == "0.5"

    def test_image_hot_spot_non_percent_raises(self):
        with pytest.raises(NotImplementedError):
            _write(
                _rule_style(
                    {
                        "marker": {
                            "elements": [
                                {
                                    "type": "Image",
                                    "image": {"uri": "http://example.com/x.png"},
                                    "hotSpot": [{"px": 5}, {"px": 5}],
                                }
                            ]
                        }
                    }
                )
            )

    def test_image_without_uri_raises(self):
        with pytest.raises(NotImplementedError):
            _write(
                _rule_style(
                    {
                        "marker": {
                            "elements": [{"type": "Image", "image": {"path": "x.png"}}]
                        }
                    }
                )
            )

    def test_image_tint_always_raises(self):
        with pytest.raises(NotImplementedError):
            _write(
                _rule_style(
                    {
                        "marker": {
                            "elements": [
                                {
                                    "type": "Image",
                                    "image": {"uri": "http://example.com/x.png"},
                                    "tint": "white",
                                }
                            ]
                        }
                    }
                )
            )

    def test_image_non_zero_position_raises(self):
        with pytest.raises(NotImplementedError):
            _write(
                _rule_style(
                    {
                        "marker": {
                            "elements": [
                                {
                                    "type": "Image",
                                    "image": {"uri": "http://example.com/x.png"},
                                    "position": {"x": 10, "y": 0},
                                }
                            ]
                        }
                    }
                )
            )


class TestWriteRaster:
    def test_color_channels_produce_channel_selection_rgb(self):
        root = _write(
            _rule_style(
                {
                    "colorChannels": [
                        {"property": "B04"},
                        {"property": "B03"},
                        {"property": "B02"},
                    ]
                }
            )
        )
        raster = root.find(".//se:RasterSymbolizer", NS)
        assert raster is not None
        assert (
            raster.find(
                "se:ChannelSelection/se:RedChannel/se:SourceChannelName", NS
            ).text
            == "B04"
        )
        assert (
            raster.find(
                "se:ChannelSelection/se:GreenChannel/se:SourceChannelName", NS
            ).text
            == "B03"
        )
        assert (
            raster.find(
                "se:ChannelSelection/se:BlueChannel/se:SourceChannelName", NS
            ).text
            == "B02"
        )

    def test_single_channel_produces_gray_channel(self):
        root = _write(_rule_style({"singleChannel": {"property": "elevation"}}))
        raster = root.find(".//se:RasterSymbolizer", NS)
        assert (
            raster.find(
                "se:ChannelSelection/se:GrayChannel/se:SourceChannelName", NS
            ).text
            == "elevation"
        )

    def test_single_channel_arithmetic_raises(self):
        with pytest.raises(NotImplementedError):
            _write(
                _rule_style(
                    {
                        "singleChannel": {
                            "op": "/",
                            "args": [
                                {
                                    "op": "-",
                                    "args": [
                                        {"property": "B08"},
                                        {"property": "B04"},
                                    ],
                                },
                                {
                                    "op": "+",
                                    "args": [
                                        {"property": "B08"},
                                        {"property": "B04"},
                                    ],
                                },
                            ],
                        }
                    }
                )
            )

    def test_color_channels_and_single_channel_mutually_exclusive_raises(self):
        with pytest.raises(NotImplementedError):
            _write(
                _rule_style(
                    {
                        "colorChannels": [
                            {"property": "R"},
                            {"property": "G"},
                            {"property": "B"},
                        ],
                        "singleChannel": {"property": "elevation"},
                    }
                )
            )

    def test_alpha_channel_always_raises(self):
        with pytest.raises(NotImplementedError):
            _write(
                _rule_style(
                    {
                        "colorChannels": [
                            {"property": "R"},
                            {"property": "G"},
                            {"property": "B"},
                        ],
                        "alphaChannel": 1.0,
                    }
                )
            )

    def test_opacity_map_always_raises(self):
        with pytest.raises(NotImplementedError):
            _write(
                _rule_style(
                    {
                        "singleChannel": {"property": "elevation"},
                        "opacityMap": [[0.0, 1.0], [1.0, 0.5]],
                    }
                )
            )

    def test_color_map_categorize_structure_array_colors(self):
        root = _write(
            _rule_style(
                {
                    "singleChannel": {"property": "elevation"},
                    "colorMap": [
                        [0.0, [96, 136, 73]],
                        [900.0, [226, 219, 167]],
                    ],
                }
            )
        )
        categorize = root.find(".//se:ColorMap/se:Categorize", NS)
        assert categorize is not None
        lookup = categorize.find("se:LookupValue", NS)
        assert lookup is not None and lookup.text == "Rasterdata"
        children = [c for c in categorize if c.tag != f"{{{NS['se']}}}LookupValue"]
        tags = [etree.QName(c).localname for c in children]
        assert tags == ["Value", "Threshold", "Value"]
        values = [c.text for c in children if etree.QName(c).localname == "Value"]
        assert values == ["#608849", "#e2dba7"]
        threshold = [c for c in children if etree.QName(c).localname == "Threshold"][0]
        assert threshold.text == "900"

    def test_color_map_categorize_named_colors(self):
        root = _write(
            _rule_style(
                {
                    "singleChannel": {"property": "hillshade"},
                    "colorMap": [[0.0, "black"], [0.15, "gray"]],
                }
            )
        )
        values = [v.text for v in root.findall(".//se:Categorize/se:Value", NS)]
        assert values == ["#000000", "#808080"]

    def test_hill_shading_factor_produces_shaded_relief(self):
        root = _write(
            _rule_style(
                {
                    "singleChannel": {"property": "elevation"},
                    "hillShading": {"factor": 56},
                }
            )
        )
        relief = root.find(".//se:ShadedRelief/se:ReliefFactor", NS)
        assert relief is not None
        assert relief.text == "56"

    def test_hill_shading_sun_always_raises(self):
        with pytest.raises(NotImplementedError):
            _write(
                _rule_style(
                    {
                        "singleChannel": {"property": "elevation"},
                        "hillShading": {
                            "factor": 56,
                            "sun": {"azimuth": 45.0, "elevation": 60.0},
                        },
                    }
                )
            )

    def test_hill_shading_nested_color_map_and_opacity_map_always_raise(self):
        with pytest.raises(NotImplementedError):
            _write(
                _rule_style(
                    {
                        "singleChannel": {"property": "hillshade"},
                        "hillShading": {
                            "colorMap": [[0.0, "black"], [0.15, "gray"]],
                        },
                    }
                )
            )
        with pytest.raises(NotImplementedError):
            _write(
                _rule_style(
                    {
                        "singleChannel": {"property": "hillshade"},
                        "hillShading": {
                            "opacityMap": [[0.0, 0.75], [0.15, 0.5]],
                        },
                    }
                )
            )

    def test_vector_and_raster_fields_coexist_as_sibling_symbolizers(self):
        root = _write(
            _rule_style(
                {
                    "fill": {"color": "gray"},
                    "singleChannel": {"property": "elevation"},
                }
            )
        )
        assert root.find(".//se:PolygonSymbolizer", NS) is not None
        assert root.find(".//se:RasterSymbolizer", NS) is not None


def _find_raster_symbolizer_dict(rules):
    """Recursively find the first nested-rule symbolizer dict carrying a
    raster field, in an output/*.cs.json-shaped stylingRules list."""
    raster_keys = (
        "colorChannels",
        "singleChannel",
        "alphaChannel",
        "colorMap",
        "hillShading",
    )
    for rule in rules:
        sym = rule.get("symbolizer")
        if isinstance(sym, dict) and any(k in sym for k in raster_keys):
            return sym
        nested = rule.get("nestedRules")
        if nested:
            found = _find_raster_symbolizer_dict(nested)
            if found is not None:
                return found
    return None


class TestRealRasterFixturesRegression:
    """Sanity-check the writer against real generated CS-JSON for the
    project's own raster fixtures (input/5..9-coverage-*.cscss). Only
    fixture 5 is expected to fully succeed after this pass — 6/7/8/9 each
    hit a distinct, correctly-documented out-of-scope construct. See the
    plan's Context section / docs/sld_se_mapping_issues.md #24/#25/#32."""

    def _symbolizer_for(self, stem):
        data = json.loads((OUTPUT_DIR / f"{stem}.cs.json").read_text(encoding="utf-8"))
        raw = _find_raster_symbolizer_dict(data["stylingRules"])
        assert raw is not None, f"no raster symbolizer found in {stem}.cs.json"
        style = Style.from_dict({"stylingRules": [{"symbolizer": raw}]})
        return style.styling_rules[0].symbolizer

    def test_dem_succeeds(self):
        sym = self._symbolizer_for("5-coverage-dem")
        elements = symbolizer_to_elements(sym)
        assert any(etree.QName(e).localname == "RasterSymbolizer" for e in elements)

    def test_sentinel2_raises_on_alpha_channel(self):
        sym = self._symbolizer_for("6-coverage-sentinel2")
        with pytest.raises(NotImplementedError, match="alphaChannel"):
            symbolizer_to_elements(sym)

    def test_ndvi_raises_on_arithmetic_single_channel(self):
        sym = self._symbolizer_for("7-coverage-ndvi")
        with pytest.raises(NotImplementedError, match="singleChannel"):
            symbolizer_to_elements(sym)

    def test_hillshading_raises_on_sun(self):
        sym = self._symbolizer_for("8-coverage-hillshading")
        with pytest.raises(NotImplementedError, match="sun"):
            symbolizer_to_elements(sym)

    def test_hillshading_opacity_raises_on_sun(self):
        sym = self._symbolizer_for("9-coverage-hillshading-opacity")
        with pytest.raises(NotImplementedError, match="sun"):
            symbolizer_to_elements(sym)
