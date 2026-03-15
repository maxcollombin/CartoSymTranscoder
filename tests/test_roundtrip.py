"""Round-trip and forward-conversion tests for all input examples (Phase 4.1).

Forward test:   input/*.cscss  →  converter  →  compare with output/*.cs.json
Write-back:     output/*.cs.json  →  csjson_to_cscss  →  re-parse without error
"""

import json
import pytest
from pathlib import Path

from cartosym_transcoder.converter import Converter

ROOT = Path(__file__).resolve().parent.parent
INPUT_DIR = ROOT / "input"
OUTPUT_DIR = ROOT / "output"

# All .cscss inputs that have a matching expected .cs.json output
_FORWARD_CASES = sorted(
    f.stem
    for f in INPUT_DIR.glob("*.cscss")
    if (OUTPUT_DIR / f"{f.stem}.cs.json").exists()
)


# ---------------------------------------------------------------------------
# Forward conversion:  .cscss → .cs.json  must match expected output
# ---------------------------------------------------------------------------

class TestForwardConversion:
    """Parse each input .cscss and compare JSON output with expected file."""

    def setup_method(self):
        self.converter = Converter()

    @pytest.mark.parametrize("stem", _FORWARD_CASES, ids=_FORWARD_CASES)
    def test_cscss_to_csjson_matches_expected(self, stem):
        """converter.cscss_to_csjson(input/<stem>.cscss) == output/<stem>.cs.json"""
        cscss_path = INPUT_DIR / f"{stem}.cscss"
        expected_path = OUTPUT_DIR / f"{stem}.cs.json"

        result = self.converter.cscss_to_csjson(cscss_path)
        with open(expected_path, encoding="utf-8") as f:
            expected = json.load(f)

        assert result == expected, (
            f"Mismatch for {stem}.cscss — "
            f"re-run `python -c \"...\"` to see diffs or regenerate expected output"
        )


# ---------------------------------------------------------------------------
# Structural round-trip:  .cs.json → .cscss → .cs.json  (re-parseable)
# ---------------------------------------------------------------------------

class TestRoundTripFidelity:
    """Full round-trip fidelity: CSCSS → JSON → CSCSS → JSON must match.

    For each input .cscss file:
    1. Forward-parse the original CSCSS to JSON (json1)
    2. Write-back the expected JSON to CSCSS
    3. Re-parse that CSCSS back to JSON (json2)
    4. Assert json1 == json2  (nothing lost in the two successive conversions)
    """

    def setup_method(self):
        self.converter = Converter()

    @pytest.mark.parametrize("stem", _FORWARD_CASES, ids=_FORWARD_CASES)
    def test_round_trip_semantic_equality(self, stem):
        """CSCSS → JSON vs CSCSS → JSON → CSCSS → JSON must be identical."""
        cscss_path = INPUT_DIR / f"{stem}.cscss"
        expected_path = OUTPUT_DIR / f"{stem}.cs.json"

        # Step 1: Forward parse
        json1 = self.converter.cscss_to_csjson(cscss_path)

        # Step 2: Write-back
        cscss_wb = self.converter.csjson_to_cscss(expected_path)
        assert isinstance(cscss_wb, str) and len(cscss_wb) > 0, (
            "write-back produced empty CSCSS"
        )

        # Step 3: Re-parse
        json2 = self.converter.cscss_to_csjson(cscss_wb)

        # Step 4: Full semantic equality
        assert json1 == json2, (
            f"Round-trip mismatch for {stem}.cscss — "
            f"the write-back CSCSS re-parses differently from the original"
        )


# ---------------------------------------------------------------------------
# Targeted parsing tests — selectors, properties, expressions
# ---------------------------------------------------------------------------

class TestSelectorParsing:
    """Verify various selector patterns are parsed correctly."""

    def setup_method(self):
        self.converter = Converter()

    def test_equality_selector(self):
        cscss = "[dataLayer.id = Rivers]\n{ visibility: true; }"
        result = self.converter.cscss_to_csjson(cscss)
        sel = result["stylingRules"][0]["selector"]
        assert sel["op"] == "="
        assert sel["args"][1] == "Rivers"

    def test_inequality_selector(self):
        cscss = "[population != 0]\n{ visibility: true; }"
        result = self.converter.cscss_to_csjson(cscss)
        sel = result["stylingRules"][0]["selector"]
        assert sel["op"] == "!="

    def test_less_than_selector(self):
        cscss = "[viz.sd < 50000]\n{ visibility: true; }"
        result = self.converter.cscss_to_csjson(cscss)
        sel = result["stylingRules"][0]["selector"]
        assert sel["op"] == "<"

    def test_compound_and_selector(self):
        cscss = "[a = 1 and b = 2]\n{ visibility: true; }"
        result = self.converter.cscss_to_csjson(cscss)
        sel = result["stylingRules"][0]["selector"]
        assert sel["op"] == "and"
        assert len(sel["args"]) == 2

    def test_compound_or_selector(self):
        cscss = "[a = 1 or b = 2]\n{ visibility: true; }"
        result = self.converter.cscss_to_csjson(cscss)
        sel = result["stylingRules"][0]["selector"]
        assert sel["op"] == "or"

    def test_sysid_in_selector(self):
        """dataLayer.id, viz.sd etc. should produce sysId references."""
        cscss = "[dataLayer.id = Foo]\n{ visibility: true; }"
        result = self.converter.cscss_to_csjson(cscss)
        sel = result["stylingRules"][0]["selector"]
        assert sel["args"][0] == {"sysId": "dataLayer.id"}

    def test_named_rule_selector(self):
        """A named rule like 'RuleName[selector]' should produce name + selector."""
        cscss = "Cities[dataLayer.id = Cities]\n{ visibility: true; }"
        result = self.converter.cscss_to_csjson(cscss)
        rule = result["stylingRules"][0]
        assert rule.get("name") == "Cities"
        # Named rules produce a compound selector
        assert "op" in rule["selector"]


# ---------------------------------------------------------------------------
# Targeted property tests
# ---------------------------------------------------------------------------

class TestPropertyParsing:
    """Verify symbolizer properties are parsed correctly."""

    def setup_method(self):
        self.converter = Converter()

    def test_visibility_false(self):
        result = self.converter.cscss_to_csjson("[Base]\n{ visibility: false; }")
        sym = result["stylingRules"][0]["symbolizer"]
        assert sym["visibility"] is False

    def test_visibility_true(self):
        result = self.converter.cscss_to_csjson("[Base]\n{ visibility: true; }")
        sym = result["stylingRules"][0]["symbolizer"]
        assert sym["visibility"] is True

    def test_opacity_float(self):
        result = self.converter.cscss_to_csjson("[Base]\n{ opacity: 0.5; }")
        sym = result["stylingRules"][0]["symbolizer"]
        assert sym["opacity"] == 0.5

    def test_zorder_int(self):
        result = self.converter.cscss_to_csjson("[Base]\n{ zOrder: 3; }")
        sym = result["stylingRules"][0]["symbolizer"]
        assert sym["zOrder"] == 3

    def test_fill_object(self):
        result = self.converter.cscss_to_csjson("[Base]\n{ fill: {color: red; opacity: 0.8}; }")
        fill = result["stylingRules"][0]["symbolizer"]["fill"]
        assert fill["color"] == "red"
        assert fill["opacity"] == 0.8

    def test_stroke_with_unit_width(self):
        result = self.converter.cscss_to_csjson("[Base]\n{ stroke: {color: blue; width: 3.0 px}; }")
        stroke = result["stylingRules"][0]["symbolizer"]["stroke"]
        assert stroke["color"] == "blue"
        assert stroke["width"] == {"px": 3.0}

    def test_fill_color_hex(self):
        """Hex colors like #FF0000 should be parsed to RGB arrays."""
        result = self.converter.cscss_to_csjson("[Base]\n{ fill: {color: #FF0000}; }")
        fill = result["stylingRules"][0]["symbolizer"]["fill"]
        assert fill["color"] == [255, 0, 0]

    def test_nested_rules(self):
        """Nested selector blocks should produce nestedRules."""
        cscss = """\
[Base]
{
   visibility: false;
   [sub = 1]
   {
      visibility: true;
   }
}
"""
        result = self.converter.cscss_to_csjson(cscss)
        rule = result["stylingRules"][0]
        assert rule["symbolizer"]["visibility"] is False
        assert "nestedRules" in rule
        assert len(rule["nestedRules"]) == 1
        assert rule["nestedRules"][0]["symbolizer"]["visibility"] is True


# ---------------------------------------------------------------------------
# Coverage-specific tests (DEM, NDVI, Sentinel-2, etc.)
# ---------------------------------------------------------------------------

class TestCoverageProperties:
    """Verify coverage-specific properties: colorMap, channels, etc."""

    def setup_method(self):
        self.converter = Converter()

    def _find_key_in_rules(self, rules, key):
        """Recursively search for a key in any symbolizer within rules."""
        for rule in rules:
            if key in rule.get("symbolizer", {}):
                return rule["symbolizer"][key]
            nested = rule.get("nestedRules", [])
            found = self._find_key_in_rules(nested, key)
            if found is not None:
                return found
        return None

    def test_dem_has_color_map(self):
        result = self.converter.cscss_to_csjson(INPUT_DIR / "5-coverage-dem.cscss")
        cm = self._find_key_in_rules(result["stylingRules"], "colorMap")
        assert cm is not None, "DEM example should have a colorMap"
        assert isinstance(cm, list), "colorMap should be an array"

    def test_sentinel2_has_channels(self):
        result = self.converter.cscss_to_csjson(INPUT_DIR / "6-coverage-sentinel2.cscss")
        ch = self._find_key_in_rules(result["stylingRules"], "colorChannels")
        assert ch is not None, "Sentinel-2 should have colorChannels"

    def test_ndvi_has_color_map(self):
        result = self.converter.cscss_to_csjson(INPUT_DIR / "7-coverage-ndvi.cscss")
        cm = self._find_key_in_rules(result["stylingRules"], "colorMap")
        assert cm is not None, "NDVI example should have a colorMap"

    def test_hillshading_has_hill_shading(self):
        result = self.converter.cscss_to_csjson(INPUT_DIR / "8-coverage-hillshading.cscss")
        hs = self._find_key_in_rules(result["stylingRules"], "hillShading")
        assert hs is not None, "Hillshading example should have hillShading"


# ---------------------------------------------------------------------------
# Metadata parsing
# ---------------------------------------------------------------------------

class TestMetadataParsing:
    """Verify .title, .abstract and other directives."""

    def setup_method(self):
        self.converter = Converter()

    def test_title_and_abstract(self):
        cscss = ".title 'My Style'\n.abstract 'A description'\n[Base]\n{ visibility: true; }"
        result = self.converter.cscss_to_csjson(cscss)
        meta = result.get("metadata", {})
        assert meta.get("title") == "My Style"
        assert meta.get("abstract") == "A description"

    def test_metadata_from_example3(self):
        result = self.converter.cscss_to_csjson(INPUT_DIR / "3-vector-line.cscss")
        meta = result.get("metadata", {})
        assert meta.get("title") == "Styling line vector features"
        assert "abstract" in meta


# ---------------------------------------------------------------------------
# Font and graphic element normalization (ast_converter)
# ---------------------------------------------------------------------------

class TestFontNormalization:
    """Verify font dict values are coerced to proper types."""

    def setup_method(self):
        from cartosym_transcoder.ast_converter import _coerce_font_dict
        self.coerce = _coerce_font_dict

    def test_size_string_to_int(self):
        font = {"size": "12"}
        self.coerce(font)
        assert font["size"] == 12
        assert isinstance(font["size"], int)

    def test_size_float_string(self):
        font = {"size": "12.5"}
        self.coerce(font)
        assert font["size"] == 12.5
        assert isinstance(font["size"], float)

    def test_bold_string_to_bool(self):
        font = {"bold": "true", "italic": "false"}
        self.coerce(font)
        assert font["bold"] is True
        assert font["italic"] is False

    def test_opacity_string_to_float(self):
        font = {"opacity": "0.75"}
        self.coerce(font)
        assert font["opacity"] == 0.75

    def test_color_preserved(self):
        font = {"color": "darkGray"}
        self.coerce(font)
        assert font["color"] == "darkGray"

    def test_outline_string_coerced(self):
        font = {"outline": "{ size: 3; opacity: 0.75; color: white }"}
        self.coerce(font)
        outline = font["outline"]
        assert isinstance(outline, dict)
        assert outline["size"] == 3
        assert outline["opacity"] == 0.75
        assert outline["color"] == "white"

    def test_already_coerced_values_untouched(self):
        """Values that are already the right type should not be altered."""
        font = {"size": 14, "bold": True, "opacity": 1.0}
        self.coerce(font)
        assert font["size"] == 14
        assert font["bold"] is True
        assert font["opacity"] == 1.0


class TestGraphicElementNormalization:
    """Verify _normalize_graphic_element handles text and alignment."""

    def setup_method(self):
        from cartosym_transcoder.ast_converter import _normalize_graphic_element
        self.normalize = _normalize_graphic_element

    def test_text_bare_identifier_becomes_property_ref(self):
        el = {"type": "Text", "text": "NAME"}
        self.normalize(el)
        assert el["text"] == {"property": "NAME"}

    def test_text_quoted_string_stays_literal(self):
        el = {"type": "Text", "text": "'Hello World'"}
        self.normalize(el)
        assert el["text"] == "Hello World"

    def test_alignment_space_separated(self):
        el = {"type": "Text", "text": "'X'", "alignment": "left middle"}
        self.normalize(el)
        assert el["alignment"] == ["left", "middle"]

    def test_alignment_braces_syntax(self):
        el = {"type": "Text", "text": "'X'", "alignment": "{ center, top }"}
        self.normalize(el)
        assert el["alignment"] == ["center", "top"]

    def test_opacity_string_to_float(self):
        el = {"type": "Dot", "opacity": "0.5"}
        self.normalize(el)
        assert el["opacity"] == 0.5

    def test_font_dict_coerced(self):
        el = {"type": "Text", "text": "'X'", "font": {"size": "10", "bold": "true"}}
        self.normalize(el)
        assert el["font"]["size"] == 10
        assert el["font"]["bold"] is True


# ---------------------------------------------------------------------------
# Color parsing (ast_converter)
# ---------------------------------------------------------------------------

class TestColorParsing:
    """Verify _parse_color_value handles various formats."""

    def setup_method(self):
        from cartosym_transcoder.ast_converter import _parse_color_value
        self.parse = _parse_color_value

    def test_named_color(self):
        assert self.parse("red") == "red"

    def test_hex_color_6_digits(self):
        assert self.parse("#FF0000") == [255, 0, 0]

    def test_hex_color_lowercase(self):
        assert self.parse("#00ff00") == [0, 255, 0]

    def test_hex_color_8_digits_passthrough(self):
        """8-digit hex colors are not yet parsed — returned as-is."""
        result = self.parse("#FF000080")
        assert result == "#FF000080"

    def test_hex_color_3_digits(self):
        result = self.parse("#F00")
        assert result == [255, 0, 0]


# ---------------------------------------------------------------------------
# Variable resolution
# ---------------------------------------------------------------------------

class TestVariableResolution:
    """Verify that @variable references are resolved during parsing."""

    def setup_method(self):
        self.converter = Converter()

    def test_variable_substitution_in_fill(self, tmp_path):
        """Variables are resolved during file pre-processing."""
        f = tmp_path / "vars.cscss"
        f.write_text("@baseColor = #336699;\n\nLanduse\n{\n   fill: {color: @baseColor};\n}\n")
        result = self.converter.cscss_to_csjson(f)
        fill = result["stylingRules"][0]["symbolizer"]["fill"]
        # Variable should be resolved to the hex color
        assert fill["color"] == [51, 102, 153]

    def test_variable_substitution_numeric(self, tmp_path):
        f = tmp_path / "vars.cscss"
        f.write_text("@baseOpacity = 0.7;\n\nLanduse\n{\n   opacity: @baseOpacity;\n}\n")
        result = self.converter.cscss_to_csjson(f)
        sym = result["stylingRules"][0]["symbolizer"]
        assert sym["opacity"] == 0.7
