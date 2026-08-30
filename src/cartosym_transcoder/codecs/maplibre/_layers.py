"""MapLibre GL layer → CartoSym styling-rule mapping (reader side).

Scope of this pass: ``fill`` and ``line`` layers whose paint values are
**constants**. Anything else — ``circle`` / ``symbol`` / ``background`` /
``raster`` layers, MapLibre expressions or legacy interpolation functions
as values, and layer ``filter`` — raises :exc:`NotImplementedError`. A
partial mapping would silently drop styling, which this project does not
do.

Each function returns a plain ``dict`` shaped like a CartoSym
``stylingRule`` / ``symbolizer``; the caller feeds it to the Pydantic
``Style`` model, which validates and coerces.
"""

from __future__ import annotations

from typing import Any

from ._filter import filter_to_selector

# Paint keys that carry no CartoSym-symbology meaning and are dropped
# rather than rejected: they tune rasteriser quality, not the portrayal.
_IGNORED_PAINT: frozenset[str] = frozenset({"fill-antialias"})

_FILL_PAINT: frozenset[str] = frozenset(
    {"fill-color", "fill-opacity", "fill-outline-color"}
)
_LINE_PAINT: frozenset[str] = frozenset({"line-color", "line-opacity", "line-width"})


def _constant(value: Any, prop: str) -> Any:
    """Return *value*, or raise if it is a MapLibre expression / function.

    A ``list`` is a MapLibre expression (``["get", "x"]`` …); a ``dict`` is
    a legacy interpolation function (``{"stops": …}``). Both are deferred
    to the expression-mapping pass.
    """
    if isinstance(value, (list, dict)):
        raise NotImplementedError(
            f"{prop}: data-driven / zoom values (MapLibre expressions and "
            "legacy functions) are not mapped yet"
        )
    return value


def _reject_unknown(props: dict[str, Any], known: frozenset[str], ctx: str) -> None:
    for key in props:
        if key in known or key in _IGNORED_PAINT:
            continue
        raise NotImplementedError(
            f"MapLibre {ctx} property {key!r} is not supported by this codec"
        )


def _visibility(layer: dict[str, Any]) -> bool | None:
    vis = layer.get("layout", {}).get("visibility")
    if vis in (None, "visible"):
        return None
    if vis == "none":
        return False
    raise NotImplementedError(f"unexpected layout.visibility {vis!r}")


def _fill_symbolizer(layer: dict[str, Any]) -> dict[str, Any]:
    paint = layer.get("paint", {})
    _reject_unknown(paint, _FILL_PAINT, "fill")

    fill: dict[str, Any] = {}
    if "fill-color" in paint:
        fill["color"] = _constant(paint["fill-color"], "fill-color")
    if "fill-opacity" in paint:
        fill["opacity"] = _constant(paint["fill-opacity"], "fill-opacity")

    symbolizer: dict[str, Any] = {"fill": fill}
    if "fill-outline-color" in paint:
        # MapLibre draws the fill outline as a 1px stroke of this colour.
        symbolizer["stroke"] = {
            "color": _constant(paint["fill-outline-color"], "fill-outline-color")
        }
    return symbolizer


def _line_symbolizer(layer: dict[str, Any]) -> dict[str, Any]:
    paint = layer.get("paint", {})
    _reject_unknown(paint, _LINE_PAINT, "line")
    # line-cap / line-join / line-round-limit change rendered geometry with
    # no CartoSym Stroke field — reject rather than drop.
    _reject_unknown(layer.get("layout", {}), frozenset({"visibility"}), "line layout")

    stroke: dict[str, Any] = {}
    if "line-color" in paint:
        stroke["color"] = _constant(paint["line-color"], "line-color")
    if "line-width" in paint:
        stroke["width"] = _constant(paint["line-width"], "line-width")
    if "line-opacity" in paint:
        stroke["opacity"] = _constant(paint["line-opacity"], "line-opacity")
    return {"stroke": stroke}


_HANDLERS = {"fill": _fill_symbolizer, "line": _line_symbolizer}


def layer_to_styling_rule(layer: dict[str, Any]) -> dict[str, Any]:
    """Convert one MapLibre layer to a CartoSym ``stylingRule`` dict.

    Raises:
        NotImplementedError: for a layer type, value, or property this
            pass does not map.
    """
    layer_type = layer.get("type")
    handler = _HANDLERS.get(layer_type or "")
    if handler is None:
        raise NotImplementedError(
            f"MapLibre {layer_type!r} layer is not supported by this codec yet"
        )
    symbolizer = handler(layer)
    visibility = _visibility(layer)
    if visibility is not None:
        symbolizer["visibility"] = visibility

    rule: dict[str, Any] = {"name": layer["id"]}
    if "filter" in layer:
        rule["selector"] = filter_to_selector(layer["filter"])
    rule["symbolizer"] = symbolizer
    return rule
