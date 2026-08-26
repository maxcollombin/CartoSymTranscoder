"""
SLD/SE reader — parse OGC Styled Layer Descriptor / Symbology Encoding XML
into Style models.

.. note::
   This is a **stub**. Implementation is tracked in ROADMAP §3.3.
"""

from pathlib import Path
from typing import Union

from ..base import CodecReader
from ...models.styles import Style


class SldSeReader(CodecReader):
    """Read ``.sld`` / ``.se`` XML files into a Style model.

    .. warning:: Not yet implemented — raises :exc:`NotImplementedError`.
    """

    def read(self, source: Union[str, Path]) -> Style:
        raise NotImplementedError(
            "SLD/SE reader is not yet implemented (see ROADMAP §3.3)"
        )
