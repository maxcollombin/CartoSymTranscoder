"""
MapLibre / MapBox GL Style reader — parse MapLibre style JSON into Style models.

.. note::
   This is a **stub**. Implementation is tracked in ROADMAP §3.4.
"""

from pathlib import Path
from typing import Union

from ..base import CodecReader
from ...models.styles import Style


class MaplibreReader(CodecReader):
    """Read MapLibre / MapBox GL Style JSON files into a Style model.

    .. warning:: Not yet implemented — raises :exc:`NotImplementedError`.
    """

    def read(self, source: Union[str, Path]) -> Style:
        raise NotImplementedError(
            "MapLibre reader is not yet implemented (see ROADMAP §3.4)"
        )
