"""Back-compat shim — the expression models moved to ``cartosym_transcoder.cql2.model``.

CQL2 is a standalone OGC standard; its expression model now lives in the
:mod:`cartosym_transcoder.cql2` package. Import from there in new code::

    from cartosym_transcoder.cql2.model import Expression, BinaryOperator

This module re-exports every public name so existing
``from ...models.expressions import X`` imports keep working.
"""

from __future__ import annotations

from ..cql2 import model as _model
from ..cql2.model import *  # noqa: F401,F403


def __getattr__(name: str):  # PEP 562 — forward any name not caught by ``import *``
    try:
        return getattr(_model, name)
    except AttributeError as exc:  # pragma: no cover - mirrors normal ImportError
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}") from exc
