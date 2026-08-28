"""CQL2 — the OGC Common Query Language expression sublanguage.

CQL2 (OGC 21-065r2) is a standalone standard that CartoSym-CSS embeds in
selectors (``[ filter ]``) and CS-JSON encodes as ``{"op": …, "args": …}``.
This package is its designated home in the transcoder:

* :mod:`.vocab` — operator / predicate / function vocabulary, **derived from
  the Pydantic models** (:mod:`.model`) rather than hand-listed.
* parsing — CQL2-Text / an ANTLR parse tree → expression models.
* serialisation — expression models → CQL2-JSON dict / CQL2-Text string.

The parsing and serialisation logic still physically lives in
``expression_parser`` / ``converter`` / ``ast_converter``; the functions
below are the stable entry points and will absorb that code over the
Palier 2 refactor (see ROADMAP). Import them from here, not from the
implementation modules.
"""

from __future__ import annotations

from typing import Any

from . import vocab

__all__ = ["vocab", "parse_text", "parse_tree", "to_cql2_json", "to_cql2_text"]


def parse_text(text: str) -> Any:
    """Parse a CQL2-Text expression string into an expression model."""
    from ..expression_parser import ExpressionParser

    return ExpressionParser._parse_expression_text(text)


def parse_tree(ctx: Any) -> Any:
    """Convert an ANTLR ``expression`` parse-tree node into an expression model."""
    from ..expression_parser import ExpressionParser

    return ExpressionParser.parse_expression_ctx(ctx)


def to_cql2_json(expr: Any) -> Any:
    """Serialise an expression model (or selector dict) to CQL2-JSON."""
    from ..ast_converter import AstToPydanticConverter

    if isinstance(expr, dict):
        return expr
    conv = AstToPydanticConverter()
    return conv._post_process_selector(conv._convert_expression_to_json_selector(expr))


def to_cql2_text(expr: Any) -> str:
    """Serialise a CQL2-JSON-shaped selector dict to CQL2-Text."""
    from ..converter import Converter

    return Converter._format_selector_expr(Converter.__new__(Converter), expr)
