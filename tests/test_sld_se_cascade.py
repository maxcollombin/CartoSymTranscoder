"""Tests for CartoSym nested-rule cascade flattening in the SLD/SE writer
(``codecs/sld_se/_cascade.py``, mapping-issues issue #19).

A selector-bearing ``nestedRules`` entry is a cascading refinement: its
selector is AND-ed with the parent's and its symbolizer is merged onto the
parent's. SE 1.1.0 has no cascade, so the writer pre-flattens each subtree
into independent ``se:Rule``s.
"""

from lxml import etree

from cartosym_transcoder.codecs.sld_se._cascade import flatten_cascade_rules
from cartosym_transcoder.codecs.sld_se.writer import SldSeWriter
from cartosym_transcoder.models.styles import Style

NS = {
    "sld": "http://www.opengis.net/sld",
    "se": "http://www.opengis.net/se",
    "ogc": "http://www.opengis.net/ogc",
}


class TestFlattenCascadeRules:
    def test_selector_is_and_merged_down_the_tree(self):
        flat = flatten_cascade_rules(
            [
                {
                    "selector": {"op": "=", "args": [{"property": "A"}, 1]},
                    "symbolizer": {"fill": {"color": "gray"}},
                    "nestedRules": [
                        {
                            "selector": {"op": "=", "args": [{"property": "B"}, 2]},
                            "symbolizer": {"fill": {"color": "red"}},
                        }
                    ],
                }
            ]
        )
        assert len(flat) == 2
        assert flat[0]["selector"] == {"op": "=", "args": [{"property": "A"}, 1]}
        assert flat[1]["selector"] == {
            "op": "and",
            "args": [
                {"op": "=", "args": [{"property": "A"}, 1]},
                {"op": "=", "args": [{"property": "B"}, 2]},
            ],
        }

    def test_symbolizer_partial_override_is_deep_merged(self):
        flat = flatten_cascade_rules(
            [
                {
                    "selector": {"op": "=", "args": [{"property": "A"}, 1]},
                    "symbolizer": {
                        "fill": {"color": "gray", "opacity": 0.5},
                        "stroke": {"color": "gray", "width": {"px": 2}},
                    },
                    "nestedRules": [
                        {
                            "selector": {"op": "=", "args": [{"property": "K"}, "x"]},
                            "symbolizer": {"fill": {"color": "darkGreen"}},
                        }
                    ],
                }
            ]
        )
        child = flat[1]["symbolizer"]
        # overridden key wins, siblings inherited
        assert child["fill"] == {"color": "darkGreen", "opacity": 0.5}
        assert child["stroke"] == {"color": "gray", "width": {"px": 2}}

    def test_indexed_element_override_replaces_one_inherited_element(self):
        flat = flatten_cascade_rules(
            [
                {
                    "selector": {"op": "=", "args": [{"property": "A"}, 1]},
                    "symbolizer": {
                        "marker": {
                            "elements": [
                                {"type": "Dot", "color": "white"},
                                {"type": "Dot", "color": "orange"},
                            ]
                        }
                    },
                    "nestedRules": [
                        {
                            "selector": {"op": "=", "args": [{"property": "K"}, "x"]},
                            "symbolizer": {
                                "marker": {
                                    "alter": True,
                                    "elements": {
                                        "index": 1,
                                        "value": {"type": "Text", "text": "hi"},
                                    },
                                }
                            },
                        }
                    ],
                }
            ]
        )
        elements = flat[1]["symbolizer"]["marker"]["elements"]
        assert elements == [
            {"type": "Dot", "color": "white"},
            {"type": "Text", "text": "hi"},
        ]
        assert "alter" not in flat[1]["symbolizer"]["marker"]

    def test_selectorless_nested_rule_stays_nested_as_else(self):
        flat = flatten_cascade_rules(
            [
                {
                    "selector": {"op": "=", "args": [{"property": "A"}, 1]},
                    "symbolizer": {"stroke": {"color": "red"}},
                    "nestedRules": [
                        {"symbolizer": {"stroke": {"color": "gray"}}},
                    ],
                }
            ]
        )
        assert len(flat) == 1
        assert "selector" not in flat[0]["nestedRules"][0]
        # else-rule symbolizer is merged onto its ancestor's
        assert flat[0]["nestedRules"][0]["symbolizer"]["stroke"] == {"color": "gray"}

    def test_symbolizerless_base_node_still_emits_a_row_but_writer_drops_it(self):
        flat = flatten_cascade_rules(
            [
                {
                    "selector": {"op": "=", "args": [{"property": "A"}, 1]},
                    "symbolizer": {"visibility": False},
                    "nestedRules": [
                        {
                            "selector": {
                                "op": "<",
                                "args": [{"sysId": "viz.sd"}, 5000],
                            },
                            "symbolizer": {
                                "visibility": True,
                                "fill": {"color": "gray"},
                            },
                        }
                    ],
                }
            ]
        )
        assert flat[0]["symbolizer"] == {"visibility": False}
        assert flat[1]["symbolizer"]["visibility"] is True


class TestCascadeThroughWriter:
    def _write(self, style_dict):
        style = Style.from_dict(style_dict)
        return etree.fromstring(SldSeWriter().write(style).encode("utf-8"))

    def test_nested_scale_and_property_cascade_produces_independent_rules(self):
        root = self._write(
            {
                "stylingRules": [
                    {
                        "name": "Landuse",
                        "selector": {
                            "op": "=",
                            "args": [{"sysId": "dataLayer.id"}, "Landuse"],
                        },
                        "symbolizer": {"visibility": False},
                        "nestedRules": [
                            {
                                "selector": {
                                    "op": "<",
                                    "args": [{"sysId": "viz.sd"}, 200000],
                                },
                                "symbolizer": {
                                    "fill": {"color": "gray", "opacity": 0.5},
                                    "stroke": {"color": "gray", "width": {"px": 2}},
                                },
                                "nestedRules": [
                                    {
                                        "selector": {
                                            "op": "=",
                                            "args": [
                                                {"property": "FunctionCode"},
                                                "park",
                                            ],
                                        },
                                        "symbolizer": {"fill": {"color": "darkGreen"}},
                                    }
                                ],
                            }
                        ],
                    }
                ]
            }
        )
        rules = root.findall(".//se:Rule", NS)
        # base visibility:false rule is dropped; two renderable rules remain
        assert len(rules) == 2
        # both under one FeatureTypeName
        assert [e.text for e in root.findall(".//se:FeatureTypeName", NS)] == [
            "Landuse"
        ]
        # both carry the inherited MaxScaleDenominator
        assert all(r.find("se:MaxScaleDenominator", NS).text == "200000" for r in rules)
        # only the refined rule carries the FunctionCode filter
        filtered = [r for r in rules if r.find("ogc:Filter", NS) is not None]
        assert len(filtered) == 1
        assert filtered[0].find(".//ogc:Literal", NS).text == "park"
        # refined rule's fill is the override; parent rule's is gray
        fills = {
            r.find(".//se:PolygonSymbolizer/se:Fill/se:SvgParameter", NS).text
            for r in rules
        }
        assert fills == {"#808080", "#006400"}

    def test_selectorless_nested_rule_still_becomes_else_filter(self):
        root = self._write(
            {
                "stylingRules": [
                    {
                        "name": "Roads",
                        "selector": {
                            "op": "=",
                            "args": [{"property": "Class"}, "primary"],
                        },
                        "symbolizer": {"stroke": {"color": "red", "width": {"px": 3}}},
                        "nestedRules": [
                            {
                                "symbolizer": {
                                    "stroke": {"color": "gray", "width": {"px": 1}}
                                }
                            }
                        ],
                    }
                ]
            }
        )
        rules = root.findall(".//se:Rule", NS)
        assert len(rules) == 2
        assert rules[1].find("se:ElseFilter", NS) is not None
        assert root.find(".//ogc:ElseFilter", NS) is None
