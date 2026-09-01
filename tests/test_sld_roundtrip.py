"""Round-trip tests for the SLD/SE codec: read -> write -> read fixed point.

Compares Pydantic ``Style`` model instances directly (structural equality)
rather than ``model_dump()`` dicts — ``UnitValue.model_dump`` is only
correctly ``{unit: value}``-shaped when called directly on the submodel
(see ``UnitValue.model_dump`` override in ``models/types.py``); when
serializing as part of a parent model, Pydantic's core serializer bypasses
that Python-level override and dumps ``{value, unit}`` instead — a
pre-existing quirk of this codebase (worked around elsewhere via
``converter.py::_fix_unit_values``), not something to route around here.
Model-to-model equality sidesteps it entirely.
"""

import json
import subprocess
import sys
from pathlib import Path

import pytest
from jsonschema import validate as jsonschema_validate

from pycartosym.codecs.sld.reader import SldReader
from pycartosym.codecs.sld.writer import SldWriter
from pycartosym.models.styles import Style

ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = ROOT / "src" / "pycartosym" / "schemas" / "CartoSym-JSON.schema.json"
FIXTURES = sorted((ROOT / "examples" / "sld").glob("*.sld"))
# Fixture 10 is a deliberate out-of-scope negative case
# (RasterSymbolizer/ContrastEnhancement); it cannot round-trip since the
# reader raises on it. Filtered by filename convention rather than a
# hardcoded "10-" prefix so future out-of-scope fixtures are excluded too.
IN_SCOPE_FIXTURES = [f for f in FIXTURES if "out-of-scope" not in f.name]


class TestRoundTrip:
    @pytest.mark.parametrize(
        "fixture", IN_SCOPE_FIXTURES, ids=[f.name for f in IN_SCOPE_FIXTURES]
    )
    def test_read_write_read_fixed_point(self, fixture):
        reader = SldReader()
        writer = SldWriter()

        style1 = reader.read(fixture)
        xml2 = writer.write(style1)
        style2 = reader.read(xml2)

        assert style1 == style2


class TestDataLayerMetadataStripping:
    def test_datalayer_type_and_dims_conjuncts_are_dropped_not_round_tripped(self):
        """dataLayer.type/featuresGeometryDimensions have no SLD/SE
        representation — writing then reading back a selector that uses
        them, alongside dataLayer.id, drops them permanently rather than
        round-tripping.
        """
        style_dict = {
            "stylingRules": [
                {
                    "name": "Landuse",
                    "selector": {
                        "op": "and",
                        "args": [
                            {
                                "op": "=",
                                "args": [{"sysId": "dataLayer.id"}, "Landuse"],
                            },
                            {
                                "op": "and",
                                "args": [
                                    {
                                        "op": "=",
                                        "args": [
                                            {"sysId": "dataLayer.type"},
                                            "vector",
                                        ],
                                    },
                                    {
                                        "op": "=",
                                        "args": [
                                            {
                                                "sysId": "dataLayer.featuresGeometryDimensions"  # noqa: E501
                                            },
                                            2,
                                        ],
                                    },
                                ],
                            },
                        ],
                    },
                    "symbolizer": {"fill": {"color": "gray"}},
                }
            ]
        }
        style1 = Style.from_dict(style_dict)
        xml = SldWriter().write(style1)
        style2 = SldReader().read(xml)
        assert style2.styling_rules[0].selector == {
            "op": "=",
            "args": [{"sysId": "dataLayer.id"}, "Landuse"],
        }


class TestCliSmokeTest:
    def test_sld_to_csjson_and_back_via_cli(self, tmp_path):
        src = ROOT / "examples" / "sld" / "1-polygon-fill-stroke.sld"
        csjson_out = tmp_path / "out.cs.json"
        sld_out = tmp_path / "out.sld"

        result1 = subprocess.run(
            [
                sys.executable,
                "-m",
                "pycartosym.cli",
                str(src),
                "-o",
                str(csjson_out),
                "--force",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        assert result1.returncode == 0, result1.stderr
        assert csjson_out.exists()

        result2 = subprocess.run(
            [
                sys.executable,
                "-m",
                "pycartosym.cli",
                str(csjson_out),
                "-o",
                str(sld_out),
                "--force",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        assert result2.returncode == 0, result2.stderr
        assert sld_out.exists()
        assert b"PolygonSymbolizer" in sld_out.read_bytes()


# examples/*.cscss that convert cleanly all the way to SLD/SE (verified
# empirically, 2026-09-01) — the other 11 hit an already-documented gap
# partway through (dataLayer.type/keywords/singleChannel expressions/
# hillShading.sun, none new here) and are out of scope for this chain.
_CSCSS_TO_SLD_CLEAN = [
    "5-coverage-dem",
    "11-natural_earth_continents",
    "13-vector-point-circle",
]


class TestCscssToSldToCsjsonChain:
    """Full ``.cscss -> .sld -> .cs.json`` chain via the CLI.

    Complements ``TestCliSmokeTest`` (which starts from ``.sld``) and
    ``TestRoundTrip`` (which starts from ``.sld`` and stays in SLD/SE) by
    exercising the chain starting from CartoSym-CSS, the primary source
    format.
    """

    @pytest.mark.parametrize("stem", _CSCSS_TO_SLD_CLEAN, ids=_CSCSS_TO_SLD_CLEAN)
    def test_cscss_to_sld_to_csjson_via_cli(self, tmp_path, stem):
        src = ROOT / "examples" / f"{stem}.cscss"
        sld_out = tmp_path / "out.sld"
        csjson_out = tmp_path / "out.cs.json"

        result1 = subprocess.run(
            [sys.executable, "-m", "pycartosym.cli", str(src), "-o", str(sld_out)],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        assert result1.returncode == 0, result1.stderr
        assert sld_out.exists()

        result2 = subprocess.run(
            [
                sys.executable,
                "-m",
                "pycartosym.cli",
                str(sld_out),
                "-o",
                str(csjson_out),
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        assert result2.returncode == 0, result2.stderr
        assert csjson_out.exists()

        data = json.loads(csjson_out.read_text(encoding="utf-8"))
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        jsonschema_validate(instance=data, schema=schema)
        assert data["stylingRules"]
