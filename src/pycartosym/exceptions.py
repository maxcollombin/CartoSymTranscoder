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
        error_tuples: the same errors as ``(line, column, message)`` tuples,
            for a caller that wants to render a source caret (e.g. the CLI's
            ``format_syntax_errors``) without re-parsing ``errors``' text.
            ``None`` if the raiser didn't have the structured form handy.
    """

    def __init__(
        self,
        errors: list[str],
        error_tuples: list[tuple[int, int, str]] | None = None,
    ) -> None:
        """Build the error from the list of ``"line L:C message"`` strings."""
        self.errors = list(errors)
        self.error_tuples = list(error_tuples) if error_tuples is not None else None
        n = len(self.errors)
        joined = "\n  ".join(self.errors)
        super().__init__(
            f"{n} CartoSym-CSS syntax error{'s' if n != 1 else ''}:\n  {joined}"
        )
