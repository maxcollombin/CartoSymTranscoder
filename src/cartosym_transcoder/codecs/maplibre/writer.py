"""MapLibre / MapBox GL Style writer — CartoSym Style models → style JSON.

The inverse of :mod:`.reader`, and with the same scope: a ``fill`` or
``line`` symbolizer with constant values maps to one MapLibre layer.
Markers, labels, raster symbolizers, rule selectors, and non-literal
values raise :exc:`NotImplementedError`.

A CartoSym style has no data-source concept, so the output declares one
synthetic empty GeoJSON source (``cartosym``) that every layer references
— enough to satisfy the MapLibre style specification.
"""

from __future__ import annotations

from typing import Any

from ...models.styles import Style
from ..base import CodecWriter

_SOURCE = "cartosym"

# Symbolizer parts with no mapping in this pass — presence is an error,
# not a silent drop.
_UNSUPPORTED_SYMBOLIZER_PARTS = (
    "marker",
    "label",
    "color_channels",
    "alpha_channel",
    "single_channel",
    "color_map",
    "opacity_map",
    "hill_shading",
)


def _literal(value: Any, prop: str) -> Any:
    """Return a plain string / number / bool, or raise for a model / expression."""
    if isinstance(value, (str, int, float, bool)):
        return value
    raise NotImplementedError(
        f"{prop}: only literal values map to MapLibre in this codec (got "
        f"{type(value).__name__})"
    )


def _reject_stroke_extras(stroke: Any, ctx: str) -> None:
    for attr in ("casing", "center_line", "dash_pattern", "pattern", "alter"):
        if getattr(stroke, attr, None) is not None:
            raise NotImplementedError(
                f"{ctx}: stroke.{attr} has no MapLibre mapping in this codec"
            )


def _fill_layer(layer_id: str, fill: Any, stroke: Any) -> dict[str, Any]:
    for attr in ("pattern", "hatch", "dotpattern", "stipple", "alter"):
        if getattr(fill, attr, None) is not None:
            raise NotImplementedError(
                f"fill.{attr} has no MapLibre mapping in this codec"
            )

    paint: dict[str, Any] = {}
    if fill.color is not None:
        paint["fill-color"] = _literal(fill.color, "fill.color")
    if fill.opacity is not None:
        paint["fill-opacity"] = _literal(fill.opacity, "fill.opacity")

    if stroke is not None:
        _reject_stroke_extras(stroke, "fill symbolizer")
        if stroke.width is not None or stroke.opacity is not None:
            raise NotImplementedError(
                "a fill symbolizer with a full stroke needs a separate MapLibre "
                "line layer — not supported yet (only a plain outline colour is)"
            )
        if stroke.color is not None:
            paint["fill-outline-color"] = _literal(stroke.color, "stroke.color")

    return {"id": layer_id, "type": "fill", "source": _SOURCE, "paint": paint}


def _line_layer(layer_id: str, stroke: Any) -> dict[str, Any]:
    _reject_stroke_extras(stroke, "line symbolizer")
    paint: dict[str, Any] = {}
    if stroke.color is not None:
        paint["line-color"] = _literal(stroke.color, "stroke.color")
    if stroke.width is not None:
        paint["line-width"] = _literal(stroke.width, "stroke.width")
    if stroke.opacity is not None:
        paint["line-opacity"] = _literal(stroke.opacity, "stroke.opacity")
    return {"id": layer_id, "type": "line", "source": _SOURCE, "paint": paint}


def _rule_to_layer(rule: Any) -> dict[str, Any]:
    if rule.selector is not None:
        raise NotImplementedError(
            "styling-rule selector → MapLibre layer filter is not mapped yet"
        )
    sym = rule.symbolizer
    if sym is None:
        raise NotImplementedError("styling rule without a symbolizer")
    for part in _UNSUPPORTED_SYMBOLIZER_PARTS:
        if getattr(sym, part, None) is not None:
            raise NotImplementedError(
                f"symbolizer.{part} has no MapLibre mapping in this codec"
            )

    layer_id = rule.name or rule.styling_rule_name
    if not layer_id:
        raise NotImplementedError("styling rule without a name → MapLibre layer id")

    if sym.fill is not None:
        layer = _fill_layer(layer_id, sym.fill, sym.stroke)
    elif sym.stroke is not None:
        layer = _line_layer(layer_id, sym.stroke)
    else:
        raise NotImplementedError(
            "symbolizer with neither fill nor stroke has no MapLibre mapping"
        )

    if sym.visibility is False:
        layer["layout"] = {"visibility": "none"}
    elif sym.visibility is not None:
        raise NotImplementedError(
            "non-constant symbolizer.visibility → MapLibre is not mapped yet"
        )
    return layer


class MaplibreWriter(CodecWriter):
    """Serialise a :class:`Style` as a MapLibre GL style ``dict``."""

    def write(self, style: Style) -> dict[str, Any]:
        """Return the MapLibre style JSON for *style*.

        Raises:
            NotImplementedError: the style uses a construct this codec
                does not map yet (see the module docstring).
        """
        layers = [_rule_to_layer(rule) for rule in style.styling_rules]
        sources: dict[str, Any] = {}
        if layers:
            sources[_SOURCE] = {
                "type": "geojson",
                "data": {"type": "FeatureCollection", "features": []},
            }
        return {"version": 8, "sources": sources, "layers": layers}
