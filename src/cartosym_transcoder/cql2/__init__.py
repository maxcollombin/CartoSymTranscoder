"""CQL2 — the OGC Common Query Language expression sublanguage.

CQL2 (OGC 21-065r2) is a standalone standard that CartoSym-CSS embeds in
selectors (``[ filter ]``) and CS-JSON encodes as ``{"op": …, "args": …}``.
This package is its designated home in the transcoder:

* :mod:`.vocab` — operator / predicate / function vocabulary, **derived from
  the Pydantic models** (:mod:`.model`) rather than hand-listed.
* :mod:`.model` — Pydantic models for the expression AST.
* :mod:`.from_text` — CQL2-Text / an ANTLR parse tree → expression models.
* :mod:`.to_json` — expression models → CQL2-JSON selector dict.
* :mod:`.to_text` — CQL2-JSON selector dict → CartoSym-CSS filter text.

The functions below are the stable entry points; import them from here
rather than from the implementation submodules. ``ast_converter`` and
``converter`` still call into ``to_json`` / ``to_text`` directly for the
pipeline's internal wiring.
"""

from __future__ import annotations

from typing import Any

from . import vocab

__all__ = ["vocab", "parse_text", "parse_tree", "to_cql2_json", "to_cql2_text"]


def parse_text(text: str) -> Any:
    """Parse a CQL2-Text expression string into an expression model."""
    from .from_text import ExpressionParser

    return ExpressionParser._parse_expression_text(text)


def parse_tree(ctx: Any) -> Any:
    """Convert an ANTLR ``expression`` parse-tree node into an expression model."""
    from .from_text import ExpressionParser

    return ExpressionParser.parse_expression_ctx(ctx)


def to_cql2_json(expr: Any) -> Any:
    """Serialise an expression model (or selector dict) to CQL2-JSON."""
    from .to_json import expression_to_json, post_process_selector

    if isinstance(expr, dict):
        return expr
    return post_process_selector(expression_to_json(expr))


def to_cql2_text(expr: Any) -> str:
    """Serialise a CQL2-JSON-shaped selector dict to CQL2-Text."""
    from .to_text import expression_to_text

    return expression_to_text(expr)
