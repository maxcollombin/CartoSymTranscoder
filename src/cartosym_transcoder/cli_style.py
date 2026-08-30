"""Terminal output helpers for the ``cartosym`` CLI.

A tiny, dependency-free styling layer: coloured, streamed, structured
diagnostics without pulling in ``rich`` or ``click``. Colour is emitted
only when stderr is a TTY and ``NO_COLOR`` is unset (https://no-color.org).

The module exposes:

* :data:`ExitCode` — distinct process exit statuses.
* :func:`info` / :func:`success` / :func:`warn` / :func:`error` /
  :func:`hint` — one-line diagnostics on the right stream.
* :func:`format_syntax_errors` — render collected parser errors with a
  source caret.
* :data:`QUIET` — set by ``--quiet`` to silence ``info`` / ``success``.
"""

from __future__ import annotations

import os
import sys
from enum import IntEnum

__all__ = [
    "ExitCode",
    "COLOR",
    "QUIET",
    "set_quiet",
    "info",
    "success",
    "warn",
    "error",
    "hint",
    "format_syntax_errors",
]


class ExitCode(IntEnum):
    """Process exit statuses, so callers can branch on the failure kind."""

    OK = 0
    USAGE = 1  # bad arguments / nothing to do
    NOT_FOUND = 2  # an input file does not exist
    INPUT_INVALID = 3  # input fails to parse or validate
    UNSUPPORTED = 4  # no codec path for the requested formats
    TRANSCODE_GAP = 5  # a codec raised NotImplementedError


def _color_enabled() -> bool:
    if os.environ.get("NO_COLOR") is not None:
        return False
    if os.environ.get("CARTOSYM_FORCE_COLOR") is not None:
        return True
    return sys.stderr.isatty()


COLOR: bool = _color_enabled()
QUIET: bool = False

_CODES = {
    "reset": "\033[0m",
    "red": "\033[31m",
    "yellow": "\033[33m",
    "green": "\033[32m",
    "cyan": "\033[36m",
    "dim": "\033[2m",
    "bold": "\033[1m",
}


def set_quiet(value: bool) -> None:
    """Toggle suppression of ``info`` / ``success`` output (``--quiet``)."""
    global QUIET
    QUIET = value


def _paint(text: str, *names: str) -> str:
    if not COLOR or not names:
        return text
    prefix = "".join(_CODES[n] for n in names)
    return f"{prefix}{text}{_CODES['reset']}"


def _emit(stream, label: str, label_colors: tuple[str, ...], msg: str) -> None:
    stream.write(f"{_paint(label, *label_colors)} {msg}\n")


def info(msg: str) -> None:
    """Progress note on stdout (suppressed by ``--quiet``)."""
    if not QUIET:
        sys.stdout.write(f"{msg}\n")


def success(msg: str) -> None:
    """Completion note on stdout (suppressed by ``--quiet``)."""
    if not QUIET:
        _emit(sys.stdout, "ok:", ("green", "bold"), msg)


def warn(msg: str) -> None:
    """Non-fatal warning on stderr."""
    _emit(sys.stderr, "warning:", ("yellow", "bold"), msg)


def error(msg: str) -> None:
    """Fatal error on stderr."""
    _emit(sys.stderr, "error:", ("red", "bold"), msg)


def hint(msg: str) -> None:
    """Indented follow-up line on stderr (a detail under an ``error``)."""
    sys.stderr.write(f"  {_paint('→', 'dim')} {msg}\n")


def format_syntax_errors(
    errors: list[tuple[int, int, str]],
    source_lines: list[str],
    path: str,
) -> str:
    """Render ``(line, column, message)`` tuples with a source caret.

    Args:
        errors: Collected parser errors, 1-based line, 0-based column.
        source_lines: The input split on newlines (no trailing newline).
        path: The file path, shown in the location prefix.

    Returns:
        A multi-line string ready to hand to :func:`hint` line by line, or
        to write as-is.
    """
    out: list[str] = []
    for line, col, msg in errors:
        loc = _paint(f"{path}:{line}:{col + 1}", "cyan")
        out.append(f"  {loc} {msg}")
        if 1 <= line <= len(source_lines):
            src = source_lines[line - 1]
            out.append(f"    {src}")
            out.append(f"    {' ' * col}{_paint('^', 'red', 'bold')}")
    return "\n".join(out)
