"""MapLibre / MapBox GL Style writer — Style models to MapLibre style JSON.

.. note::
   This is a **stub** — not yet implemented.
"""

from __future__ import annotations

from ...models.styles import Style
from ..base import CodecWriter


class MaplibreWriter(CodecWriter):
    """Write a Style model as MapLibre / MapBox GL Style JSON.

    .. warning:: Not yet implemented — raises :exc:`NotImplementedError`.
    """

    def write(self, style: Style) -> dict:
        """Serialise a Style model to MapLibre style JSON (not yet implemented)."""
        raise NotImplementedError("MapLibre writer is not yet implemented")
