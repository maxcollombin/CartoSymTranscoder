"""XML-Schema conformance tests for the SLD/SE codec.

Validates, against the vendored OGC SLD 1.1.0 / SE 1.1.0 schemas
(``tests/schemas/ogc-sld-se-1.1.0/``, see its ``README.md``):

* every hand-written ``examples/sld/*.sld`` fixture is itself valid SLD;
* the writer's output — both from the ``.sld`` fixtures (read -> write) and
  from the end-to-end-convertible ``examples/*.cscss`` examples — is valid SLD;
* ``.cscss`` styles with no SLD/SE-renderable content fail loudly rather
  than emit an invalid document.
"""

from pathlib import Path

import pytest

from pycartosym.codecs import get_codec
from pycartosym.codecs.sld.reader import SldReader
from pycartosym.codecs.sld.writer import SldWriter

from ._xsd import assert_sld_valid

ROOT = Path(__file__).resolve().parent.parent
SLD_FIXTURES = sorted((ROOT / "examples" / "sld").glob("*.sld"))

# .cscss examples whose SLD/SE conversion currently succeeds end-to-end.
CSCSS_CONVERTIBLE = ["5-coverage-dem", "11-natural_earth_continents"]
# .cscss examples that are valid CartoSym but have no SLD/SE-renderable
# content (visibility/opacity/zOrder-only rules) — must raise, not emit
# an invalid document (SE 1.1.0 forbids a se:Rule without a symbolizer).
CSCSS_NO_RENDERABLE_CONTENT = ["0-basic", "1-core"]


def _cscss_to_style(stem: str):
    return get_codec("cscss").read(ROOT / "examples" / f"{stem}.cscss")


@pytest.mark.parametrize("fixture", SLD_FIXTURES, ids=[f.name for f in SLD_FIXTURES])
def test_fixture_is_valid_sld(fixture):
    assert_sld_valid(fixture.read_text(), label=fixture.name)


@pytest.mark.parametrize("fixture", SLD_FIXTURES, ids=[f.name for f in SLD_FIXTURES])
def test_writer_output_from_fixture_is_valid_sld(fixture):
    try:
        style = SldReader().read(fixture)
    except NotImplementedError:
        pytest.skip(f"{fixture.name} is deliberately out of reader scope")
    xml = SldWriter().write(style)
    assert_sld_valid(xml, label=f"{fixture.name} (round-tripped)")


@pytest.mark.parametrize("stem", CSCSS_CONVERTIBLE)
def test_cscss_writer_output_is_valid_sld(stem):
    xml = SldWriter().write(_cscss_to_style(stem))
    assert_sld_valid(xml, label=f"{stem}.cscss -> SLD")


@pytest.mark.parametrize("stem", CSCSS_NO_RENDERABLE_CONTENT)
def test_cscss_without_renderable_content_raises(stem):
    with pytest.raises(NotImplementedError):
        SldWriter().write(_cscss_to_style(stem))
