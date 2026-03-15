"""
CQL2-Text serialisation — write-back of expressions to CQL2-Text syntax.

The CQL2-Text write-back logic is currently implemented inline in
:meth:`~cartosym_transcoder.converter.Converter._format_selector_expr`.
This module provides a public entry-point that delegates to that method.
"""

from typing import Any

from ..converter import Converter

# Singleton converter used for serialisation (stateless, so safe to share).
_converter = Converter()


def to_cql2_text(expr: Any) -> str:
    """Serialise a selector expression dict to CQL2-Text.

    Parameters
    ----------
    expr : dict | str | Any
        The selector expression in CQL2-JSON-like dict form (``{"op": …, "args": …}``),
        or a plain string.

    Returns
    -------
    str
        CQL2-Text representation.
    """
    return _converter._format_selector_expr(expr)


def selector_to_cscss(selector: Any) -> str:
    """Serialise a full selector (possibly with ``dataLayer.id`` wrapper)
    back to CSCSS syntax (``[filter]`` or bare identifier).

    Parameters
    ----------
    selector : dict | list | str
        The selector value from a StylingRule.

    Returns
    -------
    str
        CSCSS selector string.
    """
    return _converter._selector_to_cscss(selector)
