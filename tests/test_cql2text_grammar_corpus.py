"""CQL2-Text grammar corpus — parses without a syntax error.

The standalone `CQL2Text.g4` grammar (`vendor/cartosymcss-grammar/CQL2Text.g4`,
generated into `pycartosym.grammar.generated.cql2text`) is exercised here
against the official OGC CQL2-Text example corpus. This is a grammar-only
conformance check — see `test_cql2text_treewalker.py` for the tree-walker
built on top of it (`cql2/from_cql2text.py`, now `cql2/from_text.py`'s
primary parsing path).

See `tests/fixtures/cql2/text/README.md` for provenance.
"""

from __future__ import annotations

from pathlib import Path

import pytest
from antlr4 import CommonTokenStream, InputStream
from antlr4.error.ErrorListener import ErrorListener

from pycartosym.grammar.generated.cql2text import CQL2TextLexer, CQL2TextParser

_CORPUS = Path(__file__).parent / "fixtures" / "cql2" / "text"
_FIXTURES = sorted(_CORPUS.glob("*.txt"))
_IDS = [p.name for p in _FIXTURES]


class _CollectingErrorListener(ErrorListener):
    """Collects ANTLR syntax errors instead of printing them to stderr."""

    def __init__(self) -> None:
        self.errors: list[str] = []

    def syntaxError(  # noqa: N802 (ANTLR's own method name)
        self, recognizer, offending_symbol, line, column, msg, e
    ) -> None:
        self.errors.append(f"{line}:{column} {msg}")


def _parse_errors(text: str) -> list[str]:
    lexer = CQL2TextLexer(InputStream(text))
    lexer.removeErrorListeners()
    lexer_errors = _CollectingErrorListener()
    lexer.addErrorListener(lexer_errors)

    parser = CQL2TextParser(CommonTokenStream(lexer))
    parser.removeErrorListeners()
    parser_errors = _CollectingErrorListener()
    parser.addErrorListener(parser_errors)

    parser.cql2Text()
    return lexer_errors.errors + parser_errors.errors


def test_corpus_is_not_empty():
    assert _FIXTURES, "no CQL2-Text fixtures vendored under tests/fixtures/cql2/text/"


@pytest.mark.parametrize("path", _FIXTURES, ids=_IDS)
def test_official_example_parses(path: Path):
    text = path.read_text(encoding="utf-8")
    errors = _parse_errors(text)
    assert not errors, f"{path.name}: {text.strip()!r}\n" + "\n".join(errors)


@pytest.mark.parametrize(
    "text",
    [
        "a = b =",
        "a AND",
        "(a",
        "a IN ()",
        "S_INTERSECTS(a)",
        "1 +",
        '"unterminated',
        "'unterminated",
        "a LIKE",
        "BETWEEN 1 AND 2",
    ],
)
def test_invalid_text_is_rejected(text: str):
    """The grammar must reject malformed input, not just accept valid input."""
    assert _parse_errors(text), f"expected a syntax error for {text!r}"
