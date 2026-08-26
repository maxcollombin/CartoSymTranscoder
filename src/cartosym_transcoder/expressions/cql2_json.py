"""
CQL2-JSON serialisation — conversion between expression models and CQL2-JSON dicts.

The CQL2-JSON serialisation is currently handled by:

* **Serialisation** (model → JSON dict): methods on the expression model classes
  (``to_cql2_json()``) and the ``ast_converter._convert_expression_to_json_selector()``.
* **Deserialisation** (JSON dict → model): the ``expression_parser`` when reading
  ``.cs.json`` files.

This module provides convenient public entry-points for both directions.
"""

from typing import Any, Dict

from ..expression_parser import ExpressionParser


def from_cql2_json(data: Dict[str, Any]):
    """Deserialise a CQL2-JSON expression dict into an expression model.

    Parameters
    ----------
    data : dict
        CQL2-JSON expression (e.g. ``{"op": "=", "args": [{"property": "x"}, 1]}``).

    Returns
    -------
    Expression
        Parsed expression model.
    """
    return ExpressionParser._parse_expression_text(str(data))


def to_cql2_json(expr) -> Dict[str, Any]:
    """Serialise an expression model to a CQL2-JSON dict.

    Parameters
    ----------
    expr : Expression | dict
        Expression model instance, or an already-serialised dict
        (returned as-is).

    Returns
    -------
    dict
        CQL2-JSON representation.
    """
    if isinstance(expr, dict):
        return expr
    if hasattr(expr, 'to_cql2_json'):
        return expr.to_cql2_json()
    # Fallback: if it's a Pydantic model, dump it
    if hasattr(expr, 'model_dump'):
        return expr.model_dump(exclude_none=True)
    return expr
