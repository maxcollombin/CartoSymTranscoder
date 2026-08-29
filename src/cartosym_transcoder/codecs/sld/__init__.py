"""OGC SLD / Symbology Encoding codec.

The reader and writer are dialect-parametrised (:class:`._dialect.SldDialect`).

* ``sld`` — reads either dialect (auto-detected from the root ``version``
  attribute) and **writes** SLD 1.1.0 / SE 1.1.0.
* ``sld:1.0.0`` — reads/writes SLD 1.0.0 (the dialect GeoServer and QGIS
  emit by default). ``sld:1.1.0`` is an explicit alias of ``sld``.
"""

from __future__ import annotations

from ..base import Codec
from ._dialect import SE_1_1_0, SLD_1_0_0, SldDialect
from .reader import SldReader
from .writer import SldWriter

codec = Codec(
    format_name="sld",
    extensions=[".sld", ".se"],
    reader=SldReader(),  # auto-detect 1.0.0 vs 1.1.0 from the document
    writer=SldWriter(SE_1_1_0),
)

codec_sld_1_1_0 = Codec(
    format_name="sld:1.1.0",
    extensions=[],
    reader=SldReader(SE_1_1_0),
    writer=SldWriter(SE_1_1_0),
)

codec_sld_1_0_0 = Codec(
    format_name="sld:1.0.0",
    extensions=[],
    reader=SldReader(SLD_1_0_0),
    writer=SldWriter(SLD_1_0_0),
)

__all__ = [
    "codec",
    "codec_sld_1_1_0",
    "codec_sld_1_0_0",
    "SldReader",
    "SldWriter",
    "SldDialect",
    "SE_1_1_0",
    "SLD_1_0_0",
]
