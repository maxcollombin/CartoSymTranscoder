"""Reader-direction tests for the SLD/SE codec (vector-only pass)."""

from pathlib import Path

import pytest

from cartosym_transcoder.codecs.sld_se.reader import SldSeReader

ROOT = Path(__file__).resolve().parent.parent
FIXTURES = ROOT / "examples" / "sld"


def _read(name):
    return SldSeReader().read(FIXTURES / name)


class TestReadBasicSymbolizers:
    def test_polygon_fill_stroke(self):
        style = _read("1-polygon-fill-stroke.sld")
        rule = style.styling_rules[0]
        sym = rule.symbolizer
        assert sym.fill.color == [128, 128, 128]
        assert sym.fill.opacity == 0.5
        assert sym.stroke.color == [32, 32, 32]
        assert sym.stroke.opacity == 1.0

    def test_line_stroke_dash(self):
        style = _read("2-line-stroke-dash.sld")
        sym = style.styling_rules[0].symbolizer
        assert sym.fill is None
        assert sym.stroke.color == [169, 169, 169]
        assert sym.stroke.dash_pattern.pattern == [4, 2]

    def test_point_dot_mark(self):
        style = _read("3-point-dot-mark.sld")
        sym = style.styling_rules[0].symbolizer
        elements = sym.marker.elements
        assert len(elements) == 2
        assert elements[0]["type"] == "Dot"
        assert elements[0]["color"] == [255, 255, 255]
        assert elements[1]["color"] == [255, 165, 0]

    def test_text_label(self):
        style = _read("4-text-label.sld")
        sym = style.styling_rules[0].symbolizer
        el = sym.label.elements[0]
        assert el.text == {"property": "Name"}
        assert el.font["face"] == "Arial"
        assert el.alignment == ["left", "middle"]
        assert el.position.x == 20

    def test_label_ogc_literal_is_read_as_plain_text(self):
        """se:Label is mixed content; some producers wrap literal text in
        <ogc:Literal> rather than as a bare text node.
        """
        xml = (
            '<StyledLayerDescriptor version="1.1.0" '
            'xmlns="http://www.opengis.net/sld" '
            'xmlns:se="http://www.opengis.net/se" '
            'xmlns:ogc="http://www.opengis.net/ogc">'
            "<NamedLayer><se:Name>x</se:Name><UserStyle>"
            "<se:FeatureTypeStyle><se:Rule><se:TextSymbolizer>"
            "<se:Label><ogc:Literal>myText</ogc:Literal></se:Label>"
            "</se:TextSymbolizer></se:Rule></se:FeatureTypeStyle>"
            "</UserStyle></NamedLayer></StyledLayerDescriptor>"
        )
        style = SldSeReader().read(xml)
        el = style.styling_rules[0].symbolizer.label.elements[0]
        assert el.text == "myText"


class TestReadFilter:
    def test_and_of_comparisons(self):
        style = _read("2-line-stroke-dash.sld")
        selector = style.styling_rules[0].selector
        assert selector["op"] == "and"
        # One conjunct is the dataLayer.id sugar, the other the RoadClass comparison.
        ops = {arg["op"] for arg in selector["args"]}
        assert ops == {"="}

    def test_filter_breadth(self):
        style = _read("8-comparisons.sld")
        selector = style.styling_rules[0].selector
        assert selector["op"] == "and"
        ops = [arg.get("op") for arg in selector["args"]]
        assert "between" in ops
        assert "like" in ops
        assert "not" in ops
        assert "or" in ops


class TestReadScaleDenominator:
    _RULE = """<?xml version="1.0"?>
<StyledLayerDescriptor version="1.1.0"
    xmlns="http://www.opengis.net/sld"
    xmlns:se="http://www.opengis.net/se"
    xmlns:ogc="http://www.opengis.net/ogc">
  <NamedLayer><se:Name>L</se:Name><UserStyle><se:Name>S</se:Name>
    <se:FeatureTypeStyle>
      <se:Rule>
        <se:Name>R</se:Name>
        {filter}
        {min}
        {max}
        <se:PointSymbolizer><se:Graphic><se:Mark>
          <se:WellKnownName>circle</se:WellKnownName>
          <se:Fill><se:SvgParameter name="fill">#FF0000</se:SvgParameter></se:Fill>
        </se:Mark></se:Graphic></se:PointSymbolizer>
      </se:Rule>
    </se:FeatureTypeStyle>
  </UserStyle></NamedLayer>
</StyledLayerDescriptor>"""

    def _read(self, *, filter="", min="", max=""):
        xml = self._RULE.format(filter=filter, min=min, max=max)
        return SldSeReader().read(xml).styling_rules[0].selector

    def test_min_and_max_become_viz_sd_range(self):
        selector = self._read(
            min="<se:MinScaleDenominator>10000</se:MinScaleDenominator>",
            max="<se:MaxScaleDenominator>20000</se:MaxScaleDenominator>",
        )
        assert selector == {
            "op": "and",
            "args": [
                {"op": ">=", "args": [{"sysId": "viz.sd"}, 10000]},
                {"op": "<", "args": [{"sysId": "viz.sd"}, 20000]},
            ],
        }

    def test_max_only(self):
        selector = self._read(
            max="<se:MaxScaleDenominator>200000</se:MaxScaleDenominator>"
        )
        assert selector == {"op": "<", "args": [{"sysId": "viz.sd"}, 200000]}

    def test_zero_min_is_dropped(self):
        selector = self._read(
            min="<se:MinScaleDenominator>0</se:MinScaleDenominator>",
            max="<se:MaxScaleDenominator>500000</se:MaxScaleDenominator>",
        )
        assert selector == {"op": "<", "args": [{"sysId": "viz.sd"}, 500000]}

    def test_merged_ahead_of_ogc_filter(self):
        selector = self._read(
            filter=(
                "<ogc:Filter><ogc:PropertyIsEqualTo>"
                "<ogc:PropertyName>NAME</ogc:PropertyName>"
                "<ogc:Literal>NY</ogc:Literal>"
                "</ogc:PropertyIsEqualTo></ogc:Filter>"
            ),
            max="<se:MaxScaleDenominator>20000</se:MaxScaleDenominator>",
        )
        assert selector == {
            "op": "and",
            "args": [
                {"op": "<", "args": [{"sysId": "viz.sd"}, 20000]},
                {"op": "=", "args": [{"property": "NAME"}, "NY"]},
            ],
        }


class TestReadElseRule:
    def test_nested_rules_populated(self):
        style = _read("5-else-rule.sld")
        rule = style.styling_rules[0]
        assert rule.nested_rules is not None
        assert len(rule.nested_rules) == 1
        assert rule.nested_rules[0].symbolizer.stroke.color == [128, 128, 128]


class TestReadFeatureTypeName:
    def test_selector_contains_datalayer_id(self):
        style = _read("6-feature-type-name.sld")
        selector = style.styling_rules[0].selector
        assert selector == {
            "op": "=",
            "args": [{"sysId": "dataLayer.id"}, "Buildings"],
        }


class TestReadMultiSymbolizerRule:
    def test_single_symbolizer_has_fill_stroke_and_label(self):
        style = _read("7-multi-symbolizer-rule.sld")
        sym = style.styling_rules[0].symbolizer
        assert sym.fill is not None
        assert sym.stroke is not None
        assert sym.label is not None
        assert sym.marker is None


class TestReadMetadata:
    def test_title_and_abstract(self):
        style = _read("9-metadata.sld")
        assert style.metadata.title == "Metadata-only style"
        assert style.metadata.abstract == (
            "SLD/SE codec fixture: se:Description/Title/Abstract mapping"
        )


class TestReadSymbolizerGeometry:
    """se:Geometry (symbolizer geometry, 3-geometry) has no CartoSym
    conceptual-model representation yet — the reader must raise, not drop
    it silently.
    """

    def test_se_geometry_child_raises(self):
        xml = (
            '<StyledLayerDescriptor version="1.1.0" '
            'xmlns="http://www.opengis.net/sld" '
            'xmlns:se="http://www.opengis.net/se" '
            'xmlns:ogc="http://www.opengis.net/ogc">'
            "<NamedLayer><se:Name>L</se:Name><UserStyle><se:Name>S</se:Name>"
            "<se:FeatureTypeStyle><se:Rule><se:LineSymbolizer>"
            "<se:Geometry><ogc:PropertyName>centerline</ogc:PropertyName>"
            "</se:Geometry>"
            '<se:Stroke><se:SvgParameter name="stroke">#000000</se:SvgParameter>'
            "</se:Stroke></se:LineSymbolizer>"
            "</se:Rule></se:FeatureTypeStyle></UserStyle></NamedLayer>"
            "</StyledLayerDescriptor>"
        )
        with pytest.raises(NotImplementedError, match="symbolizer geometry"):
            SldSeReader().read(xml)


class TestReadOutOfScopeRaises:
    def test_raster_symbolizer_contrast_enhancement_raises(self):
        with pytest.raises(NotImplementedError):
            _read("10-out-of-scope-raster.sld")

    def _read_string(self, xml):
        return SldSeReader().read(xml)

    def test_graphic_fill_raises(self):
        xml = """<?xml version='1.0' encoding='UTF-8'?>
<StyledLayerDescriptor
    xmlns="http://www.opengis.net/sld"
    xmlns:se="http://www.opengis.net/se"
    xmlns:ogc="http://www.opengis.net/ogc"
    version="1.1.0">
  <NamedLayer><UserStyle><se:FeatureTypeStyle><se:Rule>
    <se:PolygonSymbolizer><se:Fill>
      <se:GraphicFill><se:Graphic/></se:GraphicFill>
    </se:Fill></se:PolygonSymbolizer>
  </se:Rule></se:FeatureTypeStyle></UserStyle></NamedLayer>
</StyledLayerDescriptor>"""
        with pytest.raises(NotImplementedError):
            self._read_string(xml)

    def test_external_graphic_without_online_resource_raises(self):
        xml = """<?xml version='1.0' encoding='UTF-8'?>
<StyledLayerDescriptor
    xmlns="http://www.opengis.net/sld"
    xmlns:se="http://www.opengis.net/se"
    xmlns:ogc="http://www.opengis.net/ogc"
    version="1.1.0">
  <NamedLayer><UserStyle><se:FeatureTypeStyle><se:Rule>
    <se:PointSymbolizer><se:Graphic><se:ExternalGraphic>
      <se:Format>image/png</se:Format>
    </se:ExternalGraphic></se:Graphic></se:PointSymbolizer>
  </se:Rule></se:FeatureTypeStyle></UserStyle></NamedLayer>
</StyledLayerDescriptor>"""
        with pytest.raises(NotImplementedError):
            self._read_string(xml)

    def test_incomplete_rgb_channel_triple_raises(self):
        xml = """<?xml version='1.0' encoding='UTF-8'?>
<StyledLayerDescriptor
    xmlns="http://www.opengis.net/sld"
    xmlns:se="http://www.opengis.net/se"
    version="1.1.0">
  <NamedLayer><UserStyle><se:FeatureTypeStyle><se:Rule>
    <se:RasterSymbolizer><se:ChannelSelection>
      <se:RedChannel><se:SourceChannelName>B04</se:SourceChannelName></se:RedChannel>
      <se:GreenChannel><se:SourceChannelName>B03</se:SourceChannelName></se:GreenChannel>
    </se:ChannelSelection></se:RasterSymbolizer>
  </se:Rule></se:FeatureTypeStyle></UserStyle></NamedLayer>
</StyledLayerDescriptor>"""
        with pytest.raises(NotImplementedError):
            self._read_string(xml)

    def test_selected_channel_contrast_enhancement_raises(self):
        xml = """<?xml version='1.0' encoding='UTF-8'?>
<StyledLayerDescriptor
    xmlns="http://www.opengis.net/sld"
    xmlns:se="http://www.opengis.net/se"
    version="1.1.0">
  <NamedLayer><UserStyle><se:FeatureTypeStyle><se:Rule>
    <se:RasterSymbolizer><se:ChannelSelection>
      <se:GrayChannel>
        <se:SourceChannelName>elevation</se:SourceChannelName>
        <se:ContrastEnhancement><se:Normalize/></se:ContrastEnhancement>
      </se:GrayChannel>
    </se:ChannelSelection></se:RasterSymbolizer>
  </se:Rule></se:FeatureTypeStyle></UserStyle></NamedLayer>
</StyledLayerDescriptor>"""
        with pytest.raises(NotImplementedError):
            self._read_string(xml)

    def test_colormap_interpolate_raises(self):
        xml = """<?xml version='1.0' encoding='UTF-8'?>
<StyledLayerDescriptor
    xmlns="http://www.opengis.net/sld"
    xmlns:se="http://www.opengis.net/se"
    version="1.1.0">
  <NamedLayer><UserStyle><se:FeatureTypeStyle><se:Rule>
    <se:RasterSymbolizer><se:ColorMap>
      <se:Interpolate><se:LookupValue>Rasterdata</se:LookupValue></se:Interpolate>
    </se:ColorMap></se:RasterSymbolizer>
  </se:Rule></se:FeatureTypeStyle></UserStyle></NamedLayer>
</StyledLayerDescriptor>"""
        with pytest.raises(NotImplementedError):
            self._read_string(xml)

    def test_shaded_relief_brightness_only_raises(self):
        xml = """<?xml version='1.0' encoding='UTF-8'?>
<StyledLayerDescriptor
    xmlns="http://www.opengis.net/sld"
    xmlns:se="http://www.opengis.net/se"
    version="1.1.0">
  <NamedLayer><UserStyle><se:FeatureTypeStyle><se:Rule>
    <se:RasterSymbolizer><se:ShadedRelief>
      <se:BrightnessOnly/>
    </se:ShadedRelief></se:RasterSymbolizer>
  </se:Rule></se:FeatureTypeStyle></UserStyle></NamedLayer>
</StyledLayerDescriptor>"""
        with pytest.raises(NotImplementedError):
            self._read_string(xml)


class TestReadImage:
    def test_image_marker_uri_format_and_anchor_point(self):
        style = _read("15-image-marker.sld")
        sym = style.styling_rules[0].symbolizer
        el = sym.marker.elements[0]
        assert el["type"] == "Image"
        assert el["image"] == {
            "uri": "http://example.com/parkingIcon.png",
            "type": "image/png",
        }
        assert el["hotSpot"] == [{"pc": 50}, {"pc": 50}]


class TestReadRaster:
    def test_single_channel_colormap(self):
        style = _read("11-raster-single-channel-colormap.sld")
        sym = style.styling_rules[0].symbolizer
        assert sym.single_channel == {"property": "elevation"}
        assert sym.color_map[0] == [900, [96, 136, 73]]
        assert sym.color_map[-1] == [2500, [250, 250, 250]]

    def test_color_channels_rgb(self):
        style = _read("12-raster-color-channels-rgb.sld")
        sym = style.styling_rules[0].symbolizer
        assert sym.color_channels == [
            {"property": "B04"},
            {"property": "B03"},
            {"property": "B02"},
        ]
        assert sym.alpha_channel is None

    def test_colormap_named_colors(self):
        style = _read("13-raster-colormap-named-colors.sld")
        sym = style.styling_rules[0].symbolizer
        assert sym.color_map[1] == [0.15, [128, 128, 128]]

    def test_shaded_relief_factor(self):
        style = _read("14-raster-shaded-relief.sld")
        sym = style.styling_rules[0].symbolizer
        assert sym.hill_shading == {"factor": 56}


class TestReadPathVsStringHeuristic:
    def test_path_and_raw_string_give_identical_results(self):
        path = FIXTURES / "1-polygon-fill-stroke.sld"
        from_path = SldSeReader().read(path)
        from_string = SldSeReader().read(path.read_text(encoding="utf-8"))
        assert from_path == from_string
