"""OGC SLD / Symbology Encoding codec.

The reader and writer are dialect-parametrised (:class:`._dialect.SldDialect`);
this package wires the default ``"sld"`` codec to SE 1.1.0. SLD 1.0.0 wiring
lives in a separate sub-package.
"""

from __future__ import annotations

from ..base import Codec
from ._dialect import SE_1_1_0, SLD_1_0_0, SldDialect
from .reader import SldReader
from .writer import SldWriter

codec = Codec(
    format_name="sld",
    extensions=[".sld", ".se"],
    reader=SldReader(SE_1_1_0),
    writer=SldWriter(SE_1_1_0),
)

__all__ = [
    "codec",
    "SldReader",
    "SldWriter",
    "SldDialect",
    "SE_1_1_0",
    "SLD_1_0_0",
]
