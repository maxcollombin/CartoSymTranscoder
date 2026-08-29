"""CS-JSON reader — parse CartoSym-JSON files into Style models.

Delegates to :meth:`~cartosym_transcoder.converter.Converter.csjson_to_style`.
"""

from __future__ import annotations

from pathlib import Path

from ...converter import Converter
from ...models.styles import Style
from ..base import CodecReader


class CsjsonReader(CodecReader):
    """Read ``.cs.json`` files (or raw JSON strings / dicts) into a Style model."""

    def __init__(self) -> None:
        """Create the reader with a fresh :class:`Converter`."""
        self._converter = Converter()

    def read(self, source: str | Path | dict) -> Style:
        """Parse *source* and return a validated Style.

        Parameters
        ----------
        source : str | Path | dict
            A filesystem path to a ``.cs.json`` file, a JSON string, or an
            already-parsed dictionary.
        """
        return self._converter.csjson_to_style(source)
