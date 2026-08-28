"""Exercise the SLD/SE codec against the vendored third-party GeoStyler
SLD 1.1 corpus (``tests/fixtures/geostyler-sld-1.1/``, see its README).

The corpus is split into two explicit lists:

* ``IN_SCOPE`` — must ``read`` -> ``write`` -> XSD-validate -> ``read`` to a
  Pydantic-model fixed point.
* ``OUT_OF_SCOPE`` — must raise ``NotImplementedError`` (a clean rejection,
  never another exception type) on ``read`` or ``write``.

A file that changes category is a deliberate change: this test fails loudly
if a code change shifts one silently.
"""

from pathlib import Path

import pytest

from cartosym_transcoder.codecs.sld_se.reader import SldSeReader
from cartosym_transcoder.codecs.sld_se.writer import SldSeWriter

from ._xsd import assert_sld_valid

CORPUS = Path(__file__).resolve().parent / "fixtures" / "geostyler-sld-1.1"

IN_SCOPE = [
    "empty_filter",
    "function_nested",
    "line_groundUnitWidth",
    "line_perpendicularOffset",
    "line_pixelWidth",
    "line_simpleline",
    "multi_simplelineLabel",
    "point_externalgraphic",
    "point_externalgraphic_floatingPoint",
    "point_externalgraphic_svg",
    "point_externalgraphic_svg_displacement",
    "point_simpleLabel",
    "point_simpleLabel2",
    "point_simplepoint",
    "point_simplepoint_displacement",
    "point_simplepoint_oneline",
    "point_styledLabel_elementOrder",
    "point_styledLabel_literalPlaceholder",
    "point_styledlabel",
    "polygon_transparentpolygon",
    "text_newLine_expression",
    "text_pointplacement",
    "text_pointplacement_anchor",
    "unsupported_properties",
]

OUT_OF_SCOPE = [
    "function_filter",
    "function_filter_property_to_property",
    "function_label_round",
    "function_markSymbolizer",
    "line_graphicFill",
    "line_graphicFill_externalGraphic",
    "line_graphicStroke",
    "line_graphicStroke_externalGraphic",
    "point_externalgraphic_inlineContent",
    "point_fontglyph",
    "point_simplecross",
    "point_simplepoint_categorizefunctionfilter",
    "point_simplepoint_filter",
    "point_simplepoint_functionfilter",
    "point_simplepoint_nestedLogicalFilters",
    "point_simpleslash",
    "point_simplesquare",
    "point_simplestar",
    "point_simpletriangle",
    "point_simplex",
    "polygon_graphicFill",
    "polygon_graphicFill_externalGraphic",
    "raster_complexRaster",
    "raster_simpleRaster",
    "text_lineplacement",
    "text_lineplacement_offset",
    "text_lineplacement_repeat",
    "zero_values",
]


def test_corpus_fully_categorised():
    """Every .sld file in the corpus is in exactly one list."""
    on_disk = {p.stem for p in CORPUS.glob("*.sld")}
    listed = set(IN_SCOPE) | set(OUT_OF_SCOPE)
    assert on_disk == listed, f"uncategorised: {on_disk ^ listed}"
    assert not (set(IN_SCOPE) & set(OUT_OF_SCOPE))


@pytest.mark.parametrize("stem", IN_SCOPE)
def test_in_scope_round_trips_and_validates(stem):
    reader, writer = SldSeReader(), SldSeWriter()
    fixture = CORPUS / f"{stem}.sld"

    style1 = reader.read(fixture)
    xml = writer.write(style1)
    assert_sld_valid(xml, label=stem)
    style2 = reader.read(xml)
    assert style1 == style2, f"{stem}: read->write->read is not a fixed point"


@pytest.mark.parametrize("stem", OUT_OF_SCOPE)
def test_out_of_scope_raises_not_implemented(stem):
    reader, writer = SldSeReader(), SldSeWriter()
    fixture = CORPUS / f"{stem}.sld"
    with pytest.raises(NotImplementedError):
        style = reader.read(fixture)
        writer.write(style)
