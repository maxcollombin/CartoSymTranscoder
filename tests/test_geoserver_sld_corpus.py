"""Guard the vendored GeoServer SLD corpus (``tests/fixtures/geoserver-sld/``).

There is no GeoServer codec yet — these checks just keep the vendored
files honest (count, SLD version, the handful that carry a
``<VendorOption>``) so the codec work has a stable, described starting
point. See the fixtures README.
"""

from pathlib import Path

import pytest

CORPUS = Path(__file__).resolve().parent / "fixtures" / "geoserver-sld"
FILES = sorted(p.name for p in CORPUS.glob("*.sld"))

# Files known to carry a GeoServer <VendorOption> (README table).
_WITH_VENDOR_OPTION = {
    "default_generic.sld",
    "pattern_polygon.sld",
    "poly_landmarks.sld",
    "tiger_roads.sld",
}


def test_corpus_present():
    assert len(FILES) == 24, FILES
    assert (CORPUS / "UPSTREAM").is_file()
    assert (CORPUS / "README.md").is_file()


@pytest.mark.parametrize("name", FILES)
def test_every_file_is_sld_1_0_0(name):
    text = (CORPUS / name).read_text(encoding="utf-8")
    assert 'version="1.0.0"' in text, f"{name}: expected an SLD 1.0.0 document"
    # SE 1.1.0 markers must be absent — this corpus is the 1.0 dialect.
    assert "SvgParameter" not in text
    assert "http://www.opengis.net/se" not in text


@pytest.mark.parametrize("name", FILES)
def test_vendor_option_classification(name):
    has_vo = "<VendorOption" in (CORPUS / name).read_text(encoding="utf-8")
    assert has_vo == (name in _WITH_VENDOR_OPTION), name
