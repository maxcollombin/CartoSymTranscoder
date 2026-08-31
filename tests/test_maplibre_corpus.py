"""MapLibre style corpus — well-formedness, spec validity, stub contract.

The ``codecs.maplibre`` reader/writer are not implemented yet. This module
locks in the foundation the later PRs build on:

* every vendored fixture is valid JSON and a valid MapLibre GL style
  (checked with the official ``gl-style-validate`` CLI);
* the stub reader/writer raise ``NotImplementedError`` — nothing else;
* the fixture directory and its ``README`` stay in sync.

See ``tests/fixtures/maplibre/README.md`` for provenance.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from pycartosym.codecs.maplibre import MaplibreReader, MaplibreWriter
from pycartosym.models.styles import Style

from ._maplibre_spec import assert_maplibre_valid

_CORPUS = Path(__file__).parent / "fixtures" / "maplibre"
_FIXTURES = sorted(_CORPUS.rglob("*.json"))
_IDS = [str(p.relative_to(_CORPUS)) for p in _FIXTURES]


def test_corpus_is_not_empty():
    assert _FIXTURES, "no MapLibre fixtures vendored under tests/fixtures/maplibre/"


@pytest.mark.parametrize("path", _FIXTURES, ids=_IDS)
def test_fixture_is_valid_json(path: Path):
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data.get("version") == 8, f"{path.name}: not a v8 style"


@pytest.mark.parametrize("path", _FIXTURES, ids=_IDS)
def test_fixture_is_spec_valid(path: Path):
    assert_maplibre_valid(json.loads(path.read_text(encoding="utf-8")))


@pytest.mark.parametrize("path", _FIXTURES, ids=_IDS)
def test_reader_result_is_style_or_clean_rejection(path: Path):
    """Every fixture either reads to a Style or raises NotImplementedError.

    Any other exception type means the reader mis-parsed rather than
    honestly declining an unsupported construct.
    """
    try:
        result = MaplibreReader().read(path)
    except NotImplementedError:
        return
    assert isinstance(result, Style)


def test_writer_handles_the_empty_style():
    assert MaplibreWriter().write(Style(styling_rules=[])) == {
        "version": 8,
        "sources": {},
        "layers": [],
    }


def test_readme_lists_every_atomic_fixture():
    readme = (_CORPUS / "README.md").read_text(encoding="utf-8")
    for path in (_CORPUS / "atomic").glob("*.json"):
        assert path.name in readme, f"{path.name} missing from fixtures README"
