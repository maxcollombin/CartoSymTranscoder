"""
MapLibre / MapBox GL Style writer — serialise Style models to MapLibre
style JSON.

.. note::
   This is a **stub**. Implementation is tracked in ROADMAP §3.4.
"""

from ..base import CodecWriter
from ...models.styles import Style


class MaplibreWriter(CodecWriter):
    """Write a Style model as MapLibre / MapBox GL Style JSON.

    .. warning:: Not yet implemented — raises :exc:`NotImplementedError`.
    """

    def write(self, style: Style) -> dict:
        raise NotImplementedError(
            "MapLibre writer is not yet implemented (see ROADMAP §3.4)"
        )
