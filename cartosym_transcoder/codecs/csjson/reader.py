"""
CS-JSON reader — parse CartoSym-JSON files into Style models.

Delegates to :meth:`~cartosym_transcoder.converter.Converter.csjson_to_style`.
"""

from pathlib import Path
from typing import Union

from ..base import CodecReader
from ...models.styles import Style
from ...converter import Converter


class CsjsonReader(CodecReader):
    """Read ``.cs.json`` files (or raw JSON strings / dicts) into a Style model."""

    def __init__(self):
        self._converter = Converter()

    def read(self, source: Union[str, Path, dict]) -> Style:
        """Parse *source* and return a validated Style.

        Parameters
        ----------
        source : str | Path | dict
            A filesystem path to a ``.cs.json`` file, a JSON string, or an
            already-parsed dictionary.
        """
        return self._converter.csjson_to_style(source)
