"""
SLD/SE writer — serialise Style models to OGC Styled Layer Descriptor /
Symbology Encoding XML.

.. note::
   This is a **stub**. Implementation is tracked in ROADMAP §3.3.
"""

from ..base import CodecWriter
from ...models.styles import Style


class SldSeWriter(CodecWriter):
    """Write a Style model as SLD/SE XML.

    .. warning:: Not yet implemented — raises :exc:`NotImplementedError`.
    """

    def write(self, style: Style) -> str:
        raise NotImplementedError(
            "SLD/SE writer is not yet implemented (see ROADMAP §3.3)"
        )
