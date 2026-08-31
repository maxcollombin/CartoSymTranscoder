"""Tests for CartoSym nested-rule cascade flattening (``codecs/_cascade.py``).

Shared by any codec whose target format has no cascade concept of its own
(SLD/SE, MapLibre). A selector-bearing ``nestedRules`` entry is a
cascading refinement: its selector is AND-ed with the parent's and its
symbolizer is merged onto the parent's.
"""

from pycartosym.codecs._cascade import flatten_cascade_rules


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
