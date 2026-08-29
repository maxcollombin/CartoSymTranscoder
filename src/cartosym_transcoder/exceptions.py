"""Exception types for CartoSym transcoding.

Kept in a leaf module (no intra-package imports) so any module can raise
these without creating an import cycle.
"""

from __future__ import annotations


class CartoSymError(Exception):
    """Base class for all CartoSym transcoder errors."""


class CartoSymSyntaxError(CartoSymError, ValueError):
    """Raised when CartoSym-CSS source contains lexer/parser syntax errors.

    Subclasses :class:`ValueError` so existing ``except ValueError`` call
    sites keep catching malformed input.

    Attributes:
        errors: the individual ``"line L:C message"`` strings, in source order.
    """

    def __init__(self, errors: list[str]) -> None:
        self.errors = list(errors)
        n = len(self.errors)
        joined = "\n  ".join(self.errors)
        super().__init__(
            f"{n} CartoSym-CSS syntax error{'s' if n != 1 else ''}:\n  {joined}"
        )
