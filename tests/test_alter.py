"""Tests for the 'alter' flag on dot-notation and indexed element overrides (Phase 2.2)."""

import pytest
from pathlib import Path

from cartosym_transcoder.parser import CartoSymParser

INPUT_DIR = Path(__file__).resolve().parent.parent / "input"


class TestAlterFlag:
    """Verify that dot-notation properties produce alter: true on the parent sub-object."""

    def setup_method(self):
        self.parser = CartoSymParser()

    # ── fill.color in a nested rule ────────────────────────────────

    def test_fill_dot_color_sets_alter(self):
        """fill.color: darkGray  →  fill: { alter: true, color: 'darkGray' }"""
        cscss = """\
[Base]
{
   fill: {color: gray; opacity: 0.5};

   [FunctionCode = 'parking']
   {
      fill.color: darkGray;
   }
}
"""
        style = self.parser.parse_string_to_pydantic(cscss)
        # The nested rule's symbolizer should have fill.alter == True
        nested = style.styling_rules[0].nested_rules[0]
        sym = nested.symbolizer
        assert sym.fill is not None, "fill should be set"
        assert sym.fill.alter is True, "fill.color in nested rule must set alter=True"
        assert sym.fill.color == "darkGray"

    # ── stroke.color in a nested rule ──────────────────────────────

    def test_stroke_dot_color_sets_alter(self):
        """stroke.color: #202020  →  stroke: { alter: true, color: [32,32,32] }"""
        cscss = """\
[Base]
{
   stroke: {color: gray; width: 2.0 px; opacity: 1.0};

   [FunctionCode = 'parking']
   {
      stroke.color: #202020;
   }
}
"""
        style = self.parser.parse_string_to_pydantic(cscss)
        nested = style.styling_rules[0].nested_rules[0]
        sym = nested.symbolizer
        assert sym.stroke is not None, "stroke should be set"
        assert sym.stroke.alter is True, "stroke.color in nested rule must set alter=True"

    # ── stroke.width in a nested rule ──────────────────────────────

    def test_stroke_dot_width_sets_alter(self):
        """stroke.width: 4.0 px  →  stroke: { alter: true, width: {px: 4.0} }"""
        cscss = """\
[Base]
{
   stroke: {color: gray; width: 2.0 px};

   [viz.sd < 10000]
   {
      stroke.width: 4.0 px;
   }
}
"""
        style = self.parser.parse_string_to_pydantic(cscss)
        nested = style.styling_rules[0].nested_rules[0]
        sym = nested.symbolizer
        assert sym.stroke is not None, "stroke should be set"
        assert sym.stroke.alter is True, "stroke.width in nested rule must set alter=True"

    # ── fill.color + stroke.color combined ─────────────────────────

    def test_fill_and_stroke_dot_notation_both_alter(self):
        """Both fill.color and stroke.color should set alter on their respective objects."""
        cscss = """\
[Base]
{
   fill: {color: gray; opacity: 0.5};
   stroke: {color: gray; width: 2.0 px; opacity: 1.0};

   [FunctionCode = 'park']
   {
      fill.color: darkGreen;
      stroke.color: green;
   }
}
"""
        style = self.parser.parse_string_to_pydantic(cscss)
        nested = style.styling_rules[0].nested_rules[0]
        sym = nested.symbolizer
        assert sym.fill.alter is True
        assert sym.fill.color == "darkGreen"
        assert sym.stroke.alter is True
        assert sym.stroke.color == "green"

    # ── marker.elements[N] sets alter on marker ───────────────────

    def test_marker_elements_indexed_sets_alter(self):
        """marker.elements[1]: Image{...} → marker: { alter: true, elements: {index: 1, value: ...} }"""
        cscss = """\
[Base]
{
   marker: {elements: [Dot(size: 10 px; color: red)]};

   [FunctionCode = 'parking']
   {
      marker.elements[1]:
         Image {
            image: {uri: 'http://example.com/icon'; path: 'icon.png'; id: 'parking'; type: 'image/png'; ext: 'png'};
            hotSpot: 50 pc 50 pc; tint: white; blackTint: blue; alphaThreshold: 0.1;
         };
   }
}
"""
        style = self.parser.parse_string_to_pydantic(cscss)
        nested = style.styling_rules[0].nested_rules[0]
        sym = nested.symbolizer
        assert sym.marker is not None, "marker should be set"
        assert sym.marker.alter is True, "marker.elements[N] must set alter=True on marker"

    # ── No alter when property is set directly (not dot notation) ──

    def test_no_alter_on_direct_fill(self):
        """fill: {color: gray; opacity: 0.5} should NOT set alter."""
        cscss = """\
[Base]
{
   fill: {color: gray; opacity: 0.5};
}
"""
        style = self.parser.parse_string_to_pydantic(cscss)
        sym = style.styling_rules[0].symbolizer
        assert sym.fill is not None
        assert sym.fill.alter is None or sym.fill.alter is False, \
            "Direct fill assignment should not set alter"

    # ── Real file: example 2 should have alter on nested fill/stroke

    def test_example2_alter_flags(self):
        """Example 2 (vector-polygon) nested rules should have alter on fill/stroke."""
        style = self.parser.parse_file_to_pydantic(INPUT_DIR / '2-vector-polygon.cscss')
        # Navigate: stylingRules[0] → nestedRules[0] (the zoom rule) → nestedRules[0..2] (FunctionCode rules)
        base_rule = style.styling_rules[0]
        zoom_rule = base_rule.nested_rules[0]
        # The first 3 nested rules use fill.color / stroke.color
        for i in range(3):
            rule = zoom_rule.nested_rules[i]
            sym = rule.symbolizer
            assert sym.fill is not None, f"nestedRules[{i}] should have fill"
            assert sym.fill.alter is True, f"nestedRules[{i}].fill should have alter=True"
            assert sym.stroke is not None, f"nestedRules[{i}] should have stroke"
            assert sym.stroke.alter is True, f"nestedRules[{i}].stroke should have alter=True"
