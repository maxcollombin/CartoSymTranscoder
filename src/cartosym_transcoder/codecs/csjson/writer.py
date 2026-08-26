"""
CS-JSON writer — serialise Style models to CartoSym-JSON.

Delegates to :meth:`~cartosym_transcoder.converter.Converter.cscss_to_csjson`
(which accepts a Style model directly and produces a validated dict).
"""

import json
from typing import Any, Union

from ..base import CodecWriter
from ...models.styles import Style
from ...converter import Converter


class CsjsonWriter(CodecWriter):
    """Write a Style model as a CS-JSON dict (or JSON string)."""

    def __init__(self):
        self._converter = Converter()

    def write(self, style: Style, *, as_string: bool = False) -> Union[dict, str]:
        """Return the CS-JSON representation of *style*.

        Parameters
        ----------
        style : Style
            Pydantic Style model.
        as_string : bool
            If *True*, return a pretty-printed JSON string instead of a dict.

        Returns
        -------
        dict | str
        """
        result = self._converter.cscss_to_csjson(style)
        if as_string:
            return json.dumps(result, indent=2, ensure_ascii=False)
        return result
