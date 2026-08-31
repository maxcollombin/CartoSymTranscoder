"""Spatial-relation predicate mapping in the SLD/SE codec's Filter layer.

Covers the outcome of the ``3-geometry`` Annex B audit: the named CQL2
spatial predicates map 1:1 to Filter 1.1.0 ``ogc:BinarySpatialOpType``
elements —
*not* to ``<ogc:Function>`` as Annex B claims — and ``s_equals`` is one of
them (Annex B wrongly marks it N/A). ``s_covers``/``s_coveredBy`` have no
Filter 1.1.0 element and stay unmapped.
"""

import pytest
from lxml import etree

from pycartosym.codecs.sld._filter import (
    filter_xml_to_selector,
    selector_to_filter_xml,
)

NS = {"ogc": "http://www.opengis.net/ogc"}

_NAMED = [
    ("s_intersects", "Intersects"),
    ("s_within", "Within"),
    ("s_contains", "Contains"),
    ("s_disjoint", "Disjoint"),
    ("s_touches", "Touches"),
    ("s_overlaps", "Overlaps"),
    ("s_crosses", "Crosses"),
    ("s_equals", "Equals"),
]


@pytest.mark.parametrize("op,tag", _NAMED)
def test_named_spatial_predicate_maps_to_filter_operator_element(op, tag):
    selector = {"op": op, "args": [{"property": "geom"}, {"property": "aoi"}]}
    filt = selector_to_filter_xml(selector)
    assert filt is not None
    el = filt.find(f"ogc:{tag}", NS)
    assert el is not None, f"{op} should emit <ogc:{tag}>"
    # never a generic <ogc:Function> (Annex B #41)
    assert filt.find(".//ogc:Function", NS) is None
    # round-trips back to the same selector
    assert filter_xml_to_selector(filt) == selector


def test_s_equals_reads_back_from_ogc_equals():
    xml = (
        '<ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">'
        "<ogc:Equals><ogc:PropertyName>a</ogc:PropertyName>"
        "<ogc:PropertyName>b</ogc:PropertyName></ogc:Equals></ogc:Filter>"
    )
    selector = filter_xml_to_selector(etree.fromstring(xml))
    assert selector == {
        "op": "s_equals",
        "args": [{"property": "a"}, {"property": "b"}],
    }


@pytest.mark.parametrize("op", ["s_covers", "s_coveredBy"])
def test_covers_family_has_no_filter_1_1_mapping(op):
    selector = {"op": op, "args": [{"property": "geom"}, {"property": "aoi"}]}
    with pytest.raises(NotImplementedError):
        selector_to_filter_xml(selector)
