"""
MapLibre / MapBox GL Style reader — parse MapLibre style JSON into Style models.

.. note::
   This is a **stub** — not yet implemented.
"""

from __future__ import annotations

from pathlib import Path

from ...models.styles import Style
from ..base import CodecReader


class MaplibreReader(CodecReader):
    """Read MapLibre / MapBox GL Style JSON files into a Style model.

    .. warning:: Not yet implemented — raises :exc:`NotImplementedError`.
    """

    def read(self, source: str | Path) -> Style:
        raise NotImplementedError("MapLibre reader is not yet implemented")
