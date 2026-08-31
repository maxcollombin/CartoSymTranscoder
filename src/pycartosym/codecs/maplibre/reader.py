"""MapLibre / MapBox GL Style reader — style JSON → CartoSym Style models.

Scope: ``fill`` / ``line`` / ``circle`` layers with constant paint values
and layer ``filter`` (see ``_layers`` / ``_filter``). Everything else
raises :exc:`NotImplementedError` rather than being silently dropped, per
this project's lossless-transcoding requirement. Symbol layers and
MapLibre value expressions land in later passes.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, cast

from ...models.styles import Style
from ..base import CodecReader
from ._layers import layer_to_styling_rule


class MaplibreReader(CodecReader):
    """Read a MapLibre GL style (``.json`` file, path, string, or dict)."""

    def read(self, source: str | Path | dict[str, Any]) -> Style:
        """Parse *source* into a validated :class:`Style`.

        Args:
            source: a filesystem path, the raw JSON text, or an
                already-parsed style ``dict``.

        Returns:
            The validated CartoSym Style model.

        Raises:
            NotImplementedError: the style uses a construct this codec
                does not map yet (see the module docstring).
        """
        style = self._load(source)

        version = style.get("version")
        if version != 8:
            raise NotImplementedError(
                f"MapLibre style version {version!r} is not supported (expected 8)"
            )

        rules = [layer_to_styling_rule(layer) for layer in style.get("layers", [])]
        return Style(styling_rules=rules)

    @staticmethod
    def _load(source: str | Path | dict[str, Any]) -> dict[str, Any]:
        if isinstance(source, dict):
            return source
        if isinstance(source, Path):
            text = source.read_text(encoding="utf-8")
        else:
            # A str is JSON text, or a path to a file.
            text = source
            if "\n" not in source and len(source) < 4096:
                candidate = Path(source)
                if candidate.is_file():
                    text = candidate.read_text(encoding="utf-8")
        return cast("dict[str, Any]", json.loads(text))
