"""Tests for ANTLR-based marker/label element extraction (Phase 2.4)."""

import pytest
from pathlib import Path

from cartosym_transcoder.parser import CartoSymParser


INPUT_DIR = Path(__file__).resolve().parent.parent / "input"


class TestMarkerAntlrExtraction:
    """Verify that marker and label elements are extracted via the ANTLR tree."""

    def setup_method(self):
        self.parser = CartoSymParser()

    # ── Simple marker: single Dot element ──────────────────────────

    def test_simple_marker_dot(self):
        """A marker with a single Dot element should be correctly extracted."""
        cscss = """\
[Roads]
{
   marker: { elements: [
      Dot {
         size: 10 m;
         color: white;
      }
   ]};
}
"""
        style = self.parser.parse_string_to_pydantic(cscss)
        rules = style.styling_rules
        assert rules is not None
        # Find the rule with a marker
        marker = None
        for rule in rules:
            sym = getattr(rule, 'symbolizer', None)
            if sym and getattr(sym, 'marker', None):
                marker = sym.marker
                break
        assert marker is not None, "No marker found"
        assert marker.elements is not None
        assert len(marker.elements) == 1
        el = marker.elements[0]
        assert el['type'] == 'Dot'
        assert el['size'] == '10 m'
        assert el['color'] == 'white'

    # ── Multiple Dot elements ──────────────────────────────────────

    def test_multiple_dot_elements(self):
        """A marker with two Dot elements should extract both."""
        cscss = """\
[Points]
{
   marker: { elements: [
      Dot {
         size: 10 px;
         color: white;
      },
      Dot {
         size: 8 px;
         color: orange;
      }
   ]};
}
"""
        style = self.parser.parse_string_to_pydantic(cscss)
        marker = None
        for rule in style.styling_rules:
            sym = getattr(rule, 'symbolizer', None)
            if sym and getattr(sym, 'marker', None):
                marker = sym.marker
                break
        assert marker is not None
        assert len(marker.elements) == 2
        assert marker.elements[0]['type'] == 'Dot'
        assert marker.elements[0]['color'] == 'white'
        assert marker.elements[1]['type'] == 'Dot'
        assert marker.elements[1]['color'] == 'orange'

    # ── Text element with nested font object ──────────────────────

    def test_text_element_with_font(self):
        """A Text element with a nested font:{...} should produce a structured dict."""
        cscss = """\
[Labels]
{
   marker: { elements: [
      Text(
         text: Name;
         font: {
            face: 'Arial';
            size: 14;
            bold: true;
         };
      )
   ]};
}
"""
        style = self.parser.parse_string_to_pydantic(cscss)
        marker = None
        for rule in style.styling_rules:
            sym = getattr(rule, 'symbolizer', None)
            if sym and getattr(sym, 'marker', None):
                marker = sym.marker
                break
        assert marker is not None
        assert len(marker.elements) == 1
        el = marker.elements[0]
        assert el['type'] == 'Text'
        # 'Name' is parsed as an identifier (property reference), not a string literal
        assert el['text'] == 'Name' or el['text'] == {'property': 'Name'}
        # Font should be a structured dict (ANTLR extraction), not a raw string
        font = el['font']
        assert isinstance(font, dict), f"font should be dict, got {type(font)}"
        assert font['face'] == 'Arial'
        assert font['size'] == 14
        assert font['bold'] is True

    # ── Image element with nested image object ────────────────────

    def test_image_element_nested_object(self):
        """An Image element with image:{...} should have structured properties."""
        cscss = """\
[Icons]
{
   marker: { elements: [
      Image {
         image: {
            uri: 'http://example.com/icon';
            path: 'icon.png';
            type: 'image/png';
         };
         hotSpot: 50 pc 50 pc;
      }
   ]};
}
"""
        style = self.parser.parse_string_to_pydantic(cscss)
        marker = None
        for rule in style.styling_rules:
            sym = getattr(rule, 'symbolizer', None)
            if sym and getattr(sym, 'marker', None):
                marker = sym.marker
                break
        assert marker is not None
        assert len(marker.elements) == 1
        el = marker.elements[0]
        assert el['type'] == 'Image'
        # Image should be a nested dict
        image = el['image']
        assert isinstance(image, dict), f"image should be dict, got {type(image)}"
        assert image['uri'] == 'http://example.com/icon'
        assert image['path'] == 'icon.png'
        assert image['type'] == 'image/png'

    # ── Label elements ────────────────────────────────────────────

    def test_label_extraction(self):
        """Label with elements should be extracted like marker."""
        cscss = """\
[CityLabels]
{
   label: { elements: [
      Text(
         text: name;
         font: {
            face: 'Verdana';
            size: 12;
         };
      )
   ]};
}
"""
        style = self.parser.parse_string_to_pydantic(cscss)
        label = None
        for rule in style.styling_rules:
            sym = getattr(rule, 'symbolizer', None)
            if sym and getattr(sym, 'label', None):
                label = sym.label
                break
        assert label is not None
        assert label.elements is not None
        assert len(label.elements) == 1
        el = label.elements[0]
        # Label.elements is List[Graphic] — Pydantic converts dicts to Graphic objects
        # Graphic uses ConfigDict(extra="allow"), so fields are attributes
        if isinstance(el, dict):
            assert el['type'] == 'Text'
            font = el['font']
        else:
            assert el.type == 'Text'
            font = el.font
        # font may be a dict or a Pydantic model
        if isinstance(font, dict):
            assert font['face'] == 'Verdana'
        else:
            assert font.face == 'Verdana'

    # ── Real file: example 3 (vector-line) ────────────────────────

    def test_example3_marker(self):
        """Example 3 (vector-line) should parse marker elements correctly."""
        style = self.parser.parse_file_to_pydantic(INPUT_DIR / '3-vector-line.cscss')
        # Find a marker somewhere in the rule tree
        found = _find_markers_recursive(style.styling_rules)
        assert len(found) >= 1, "Expected at least one marker in example 3"
        # First marker should have a Dot element
        marker = found[0]
        assert marker.elements is not None
        assert any(el.get('type') == 'Dot' for el in marker.elements)

    # ── Real file: example 4 (vector-point) ───────────────────────

    def test_example4_markers(self):
        """Example 4 (vector-point) should parse multiple Dot markers."""
        style = self.parser.parse_file_to_pydantic(INPUT_DIR / '4-vector-point.cscss')
        found = _find_markers_recursive(style.styling_rules)
        assert len(found) >= 1, "Expected at least one marker in example 4"
        # First marker should have 2 Dot elements (white and orange)
        marker = found[0]
        assert marker.elements is not None
        assert len(marker.elements) == 2
        types = [el.get('type') for el in marker.elements]
        assert types == ['Dot', 'Dot']


def _find_markers_recursive(rules):
    """Recursively find all markers in a rule tree."""
    markers = []
    if rules is None:
        return markers
    for rule in rules:
        sym = getattr(rule, 'symbolizer', None)
        if sym and getattr(sym, 'marker', None):
            m = sym.marker
            if m.elements is not None:
                markers.append(m)
        nested = getattr(rule, 'nested_rules', None)
        if nested:
            markers.extend(_find_markers_recursive(nested))
    return markers
