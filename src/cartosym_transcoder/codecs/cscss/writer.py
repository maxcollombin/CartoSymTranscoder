"""
CSCSS writer — serialise Style models to CartoSym-CSS text.

Delegates to :meth:`~cartosym_transcoder.converter.Converter.style_to_cscss`.
"""

from ..base import CodecWriter
from ...models.styles import Style
from ...converter import Converter


class CscssWriter(CodecWriter):
    """Write a Style model as ``.cscss`` text."""

    def __init__(self):
        self._converter = Converter()

    def write(self, style: Style) -> str:
        """Return the CSCSS string representation of *style*."""
        return self._converter.style_to_cscss(style)
