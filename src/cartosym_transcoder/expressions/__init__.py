"""
Expressions sub-package for CartoSym Transcoder.

Provides:
- ``model`` — Pydantic expression models (re-exported from ``models.expressions``)
- ``cql2_text`` — CQL2-Text serialisation
- ``cql2_json`` — CQL2-JSON serialisation / deserialisation

Usage::

    from cartosym_transcoder.expressions.model import Expression, BinaryOperator
    from cartosym_transcoder.expressions.cql2_text import to_cql2_text
    from cartosym_transcoder.expressions.cql2_json import to_cql2_json, from_cql2_json
"""

from .cql2_text import to_cql2_text, selector_to_cscss
from .cql2_json import to_cql2_json, from_cql2_json

__all__ = [
    "to_cql2_text",
    "selector_to_cscss",
    "to_cql2_json",
    "from_cql2_json",
]
