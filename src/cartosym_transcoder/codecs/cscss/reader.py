"""
CSCSS reader — parse CartoSym-CSS files into Style models.

Delegates to the existing :class:`~cartosym_transcoder.parser.CartoSymParser`.
"""

from pathlib import Path
from typing import Union

from ..base import CodecReader
from ...models.styles import Style
from ...parser import CartoSymParser


class CscssReader(CodecReader):
    """Read ``.cscss`` files (or raw CSCSS strings) into a Style model."""

    def __init__(self):
        self._parser = CartoSymParser()

    def read(self, source: Union[str, Path]) -> Style:
        """Parse *source* and return a validated Style.

        Parameters
        ----------
        source : str | Path
            A filesystem path to a ``.cscss`` file, or the raw CSCSS text.
        """
        if isinstance(source, Path):
            return self._parser.parse_file_to_pydantic(source)

        # Heuristic: short string without newlines that exists on disk → file path
        if (
            isinstance(source, str)
            and len(source) < 500
            and "\n" not in source
            and Path(source).exists()
        ):
            return self._parser.parse_file_to_pydantic(Path(source))

        # Otherwise treat it as raw CSCSS content
        return self._parser.parse_string_to_pydantic(source)
