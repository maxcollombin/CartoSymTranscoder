"""Robustness tests for the text-based expression parser
(`expression_parser.py`) — the cases that its hand-rolled operator
scanners historically mishandled:

* logical/relational operators **inside string literals** were split on
  (``name = 'a and b'`` became an AND);
* parentheses wrapping a whole sub-expression were read as a function call
  (``a = 1 and (b = 2 or c = 3)``);
* a leading ``not`` was silently dropped.

Checked both at the parser level and end-to-end through
``Converter.cscss_to_csjson`` (selectors) + write-back.
"""

import pytest

from pycartosym.converter import Converter
from pycartosym.cql2.from_text import ExpressionParser
from pycartosym.cql2.model import (
    BinaryOperationExpression,
    UnaryOperationExpression,
)


@pytest.fixture
def converter():
    return Converter()


def _sel(converter, condition):
    src = f"[{condition}]\n{{ visibility: true; }}"
    return converter.cscss_to_csjson(src)["stylingRules"][0].get("selector")


class TestOperatorsInsideStringLiterals:
    def test_and_inside_string_is_not_split(self):
        expr = ExpressionParser.parse_expression("name = 'a and b'")
        assert isinstance(expr, BinaryOperationExpression)
        assert str(expr.operator) in ("=", "BinaryOperator.EQUAL")
        assert expr.right.value == "a and b"

    def test_or_inside_string_with_real_top_level_and(self):
        expr = ExpressionParser.parse_expression("name = 'x or y' and cat = 2")
        assert isinstance(expr, BinaryOperationExpression)
        assert "AND" in str(expr.operator).upper() or expr.operator == "and"

    def test_equals_inside_string_is_not_split(self, converter):
        assert _sel(converter, "label = 'has = sign'") == {
            "op": "=",
            "args": [{"property": "label"}, "has = sign"],
        }


class TestParenthesisedSubExpressions:
    def test_parenthesised_or_on_the_right(self, converter):
        assert _sel(converter, "a = 1 and (b = 2 or c = 3)") == {
            "op": "and",
            "args": [
                {"op": "=", "args": [{"property": "a"}, 1]},
                {
                    "op": "or",
                    "args": [
                        {"op": "=", "args": [{"property": "b"}, 2]},
                        {"op": "=", "args": [{"property": "c"}, 3]},
                    ],
                },
            ],
        }

    def test_fully_wrapped_expression(self):
        expr = ExpressionParser.parse_expression("(population = 0)")
        assert isinstance(expr, BinaryOperationExpression)


class TestLeadingNot:
    def test_not_parenthesised_predicate(self):
        expr = ExpressionParser.parse_expression("not (FunctionCode = 'park')")
        assert isinstance(expr, UnaryOperationExpression)
        assert str(expr.operator).endswith("not") or expr.operator == "not"
        assert isinstance(expr.operand, BinaryOperationExpression)

    def test_not_bare_predicate(self):
        expr = ExpressionParser.parse_expression("not FunctionCode = 'park'")
        assert isinstance(expr, UnaryOperationExpression)

    @pytest.mark.parametrize(
        "condition",
        ["not (FunctionCode = 'park')", "not FunctionCode = 'park'"],
    )
    def test_not_selector_end_to_end_is_cql2_json(self, converter, condition):
        assert _sel(converter, condition) == {
            "op": "not",
            "args": [{"op": "=", "args": [{"property": "FunctionCode"}, "park"]}],
        }

    def test_not_selector_round_trips(self, converter):
        j1 = converter.cscss_to_csjson(
            "[not (FunctionCode = 'park')]\n{ visibility: true; }"
        )
        j2 = converter.cscss_to_csjson(converter.csjson_to_cscss(j1))
        assert j1 == j2
