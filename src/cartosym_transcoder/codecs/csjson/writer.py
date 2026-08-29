"""CS-JSON writer — serialise Style models to CartoSym-JSON.

Delegates to :meth:`~cartosym_transcoder.converter.Converter.cscss_to_csjson`
(which accepts a Style model directly and produces a validated dict).
"""

from __future__ import annotations

import json

from ...converter import Converter
from ...models.styles import Style
from ..base import CodecWriter


class CsjsonWriter(CodecWriter):
    """Write a Style model as a CS-JSON dict (or JSON string)."""

    def __init__(self) -> None:
        """Create the writer with a fresh :class:`Converter`."""
        self._converter = Converter()

    def write(self, style: Style, *, as_string: bool = False) -> dict | str:
        """Return the CS-JSON representation of *style*.

        Parameters
        ----------
        style : Style
            Pydantic Style model.
        as_string : bool
            If *True*, return a pretty-printed JSON string instead of a dict.

        Returns:
        -------
        dict | str
        """
        result = self._converter.cscss_to_csjson(style)
        if as_string:
            return json.dumps(result, indent=2, ensure_ascii=False)
        return result
