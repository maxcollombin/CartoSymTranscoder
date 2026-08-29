"""Stricter round-trip / conformance checks for the CSCSS ↔ CS-JSON core
(complements ``test_roundtrip.py``):

* every generated **and** every golden ``.cs.json`` validates against
  the bundled ``CartoSym-JSON.schema.json`` (using the draft the schema
  declares — 2019-09 — which ``jsonschema.validate`` auto-selects);
* the CSCSS write-back is **idempotent** at the string level
  (json → cscss → json → cscss produces the same cscss twice);
* whitespace-/comment-only input is a valid empty style, not an error.
"""

import json
from pathlib import Path

import pytest
from jsonschema import validate as jsonschema_validate

from cartosym_transcoder.converter import Converter

ROOT = Path(__file__).resolve().parent.parent
EXAMPLES_DIR = ROOT / "examples"
EXPECTED_DIR = ROOT / "tests" / "fixtures" / "expected"
SCHEMA_PATH = (
    ROOT / "src" / "cartosym_transcoder" / "schemas" / "CartoSym-JSON.schema.json"
)

_SCHEMA = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
_CSCSS = sorted(f.stem for f in EXAMPLES_DIR.glob("*.cscss"))
_GOLDEN_JSON = sorted(f.name for f in EXPECTED_DIR.glob("*.cs.json"))


@pytest.fixture
def converter():
    return Converter()


class TestSchemaConformance:
    @pytest.mark.parametrize("stem", _CSCSS, ids=_CSCSS)
    def test_generated_csjson_is_schema_valid(self, converter, stem):
        data = converter.cscss_to_csjson(EXAMPLES_DIR / f"{stem}.cscss")
        jsonschema_validate(instance=data, schema=_SCHEMA)

    @pytest.mark.parametrize("name", _GOLDEN_JSON, ids=_GOLDEN_JSON)
    def test_golden_csjson_fixture_is_schema_valid(self, name):
        data = json.loads((EXPECTED_DIR / name).read_text(encoding="utf-8"))
        jsonschema_validate(instance=data, schema=_SCHEMA)


class TestWriteBackIdempotence:
    @pytest.mark.parametrize("stem", _CSCSS, ids=_CSCSS)
    def test_cscss_writeback_is_string_idempotent(self, converter, stem):
        """json → cscss → json → cscss: the two CSCSS renderings match
        exactly (the writer has reached a fixed point, not just a
        semantic one).
        """
        expected_json = EXPECTED_DIR / f"{stem}.cs.json"
        cscss_1 = converter.csjson_to_cscss(expected_json)
        json_2 = converter.cscss_to_csjson(cscss_1)
        cscss_2 = converter.csjson_to_cscss(json_2)

        assert cscss_1 == cscss_2, f"{stem}: write-back is not string-idempotent"


class TestEmptyAndDegenerateInput:
    @pytest.mark.parametrize(
        "src", ["", "   ", "\n\t  \n", "// just a comment\n", "/* block */"]
    )
    def test_blank_or_comment_only_cscss_is_an_empty_style(self, converter, src):
        assert converter.cscss_to_csjson(src) == {"stylingRules": []}

    def test_empty_style_dict_round_trips(self, converter):
        cscss = converter.csjson_to_cscss({"stylingRules": []})
        assert isinstance(cscss, str)
        assert converter.cscss_to_csjson(cscss) == {"stylingRules": []}

    def test_malformed_cscss_raises(self, converter):
        from cartosym_transcoder.exceptions import CartoSymSyntaxError

        with pytest.raises(CartoSymSyntaxError):
            converter.cscss_to_csjson("this is definitely not cscss !!!")
