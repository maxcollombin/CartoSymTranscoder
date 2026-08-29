"""The ``Symbolizer`` model accepts vendor-extension keys and nothing else.

The conceptual model defines a generic vendor-extension mechanism: a
symbolizer property named ``vendor.<vendorName>.<propertyName>``, of any
datatype, which a consumer ignores when it does not understand it. The
model permits exactly those extra keys (so e.g. GeoServer ``<VendorOption>``
values survive a CS-JSON round-trip) and rejects any other unknown key as
a likely typo.
"""

import pytest
from pydantic import ValidationError

from cartosym_transcoder.models.symbolizers import Symbolizer


@pytest.mark.parametrize(
    "key",
    [
        "vendor.geoserver.autoWrap",
        "vendor.geoserver.group",
        "vendor.my-vendor.some_prop",
        "vendor.x.a.b.c",
    ],
)
def test_vendor_extension_keys_are_accepted_and_round_trip(key):
    sym = Symbolizer.from_dict({"fill": {"color": "#ffffff"}, key: 42})
    assert sym.to_dict()[key] == 42


def test_vendor_extension_value_keeps_its_datatype():
    sym = Symbolizer.from_dict(
        {
            "vendor.geoserver.group": True,
            "vendor.geoserver.autoWrap": 100,
            "vendor.geoserver.labelAllGroup": "true",
        }
    )
    dumped = sym.to_dict()
    assert dumped["vendor.geoserver.group"] is True
    assert dumped["vendor.geoserver.autoWrap"] == 100
    assert dumped["vendor.geoserver.labelAllGroup"] == "true"


@pytest.mark.parametrize(
    "key",
    [
        "bogus",
        "fil",  # typo of "fill"
        "vendor",
        "vendor.geoserver",  # no property part
        "vendor..autoWrap",  # empty vendor name
        "vendorX.geoserver.autoWrap",
    ],
)
def test_non_vendor_extra_keys_are_rejected(key):
    with pytest.raises(ValidationError):
        Symbolizer.from_dict({key: 1})


def test_known_fields_still_validated_normally():
    sym = Symbolizer.from_dict({"fill": {"color": "#abcabc"}})
    assert sym.fill is not None
