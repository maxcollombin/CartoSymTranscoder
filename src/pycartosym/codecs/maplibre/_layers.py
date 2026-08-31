"""MapLibre GL layer → CartoSym styling-rule mapping (reader side).

Scope of this pass: ``fill`` / ``line`` / ``circle`` / ``symbol`` /
``background`` layers whose paint / layout scalar values are constants,
or one of six MapLibre value-expression operators — ``get`` / ``case`` /
``match`` / ``interpolate`` / ``step`` / ``coalesce`` (see
:mod:`._expressions`). Anything else — ``raster`` layers, a layer's
``minzoom``/``maxzoom`` (zoom-range visibility has no CartoSym mapping in
this codec), legacy zoom/property functions (``{"stops": …}``), or any
other expression operator — raises :exc:`NotImplementedError`. A partial
mapping would silently drop styling, which this project does not do.
Layer ``filter`` maps to ``rule.selector`` (see :mod:`._filter`).

A ``symbol`` layer maps to a ``label`` (from ``text-field``) and/or a
``marker`` holding one ``Image`` (from ``icon-image``). A ``background``
layer maps to a ``Fill`` symbolizer tagged
``vendor.maplibre.layer-type: "background"`` — its paint is structurally
identical to a ``fill`` layer's, so this vendor-extension tag (SymCore
§7) is the only way the writer can reconstruct the right MapLibre layer
type on the way back.

Each function returns a plain ``dict`` shaped like a CartoSym
``stylingRule`` / ``symbolizer``; the caller feeds it to the Pydantic
``Style`` model, which validates and coerces.
"""

from __future__ import annotations

from typing import Any

from ._expressions import maplibre_expr_to_value
from ._filter import filter_to_selector

# Paint keys that carry no CartoSym-symbology meaning and are dropped
# rather than rejected: they tune rasteriser quality, not the portrayal.
_IGNORED_PAINT: frozenset[str] = frozenset({"fill-antialias"})

_FILL_PAINT: frozenset[str] = frozenset(
    {"fill-color", "fill-opacity", "fill-outline-color"}
)
_LINE_PAINT: frozenset[str] = frozenset({"line-color", "line-opacity", "line-width"})
_CIRCLE_PAINT: frozenset[str] = frozenset(
    {
        "circle-color",
        "circle-opacity",
        "circle-radius",
        "circle-stroke-color",
        "circle-stroke-width",
        "circle-stroke-opacity",
    }
)
_SYMBOL_PAINT: frozenset[str] = frozenset(
    {"text-color", "text-opacity", "text-halo-color", "text-halo-width", "icon-opacity"}
)
_SYMBOL_LAYOUT: frozenset[str] = frozenset(
    {
        "text-field",
        "text-font",
        "text-size",
        "text-transform",
        "text-anchor",
        "text-offset",
        "icon-image",
        "symbol-placement",
        "visibility",
    }
)
_BACKGROUND_PAINT: frozenset[str] = frozenset(
    {"background-color", "background-opacity"}
)

# Layer keys with no CartoSym mapping in this codec — presence raises
# rather than being silently dropped.
_UNSUPPORTED_LAYER_KEYS: frozenset[str] = frozenset({"minzoom", "maxzoom"})

# MapLibre text-anchor token → CartoSym (hAlignment, vAlignment).
_ANCHOR_TO_ALIGNMENT: dict[str, tuple[str, str]] = {
    "center": ("center", "middle"),
    "left": ("left", "middle"),
    "right": ("right", "middle"),
    "top": ("center", "top"),
    "bottom": ("center", "bottom"),
    "top-left": ("left", "top"),
    "top-right": ("right", "top"),
    "bottom-left": ("left", "bottom"),
    "bottom-right": ("right", "bottom"),
}


def _constant(value: Any, prop: str) -> Any:
    """Return *value*, mapping a MapLibre expression to its CartoSym form.

    A ``list`` is a MapLibre expression (``["get", "x"]`` …) — mapped via
    :func:`._expressions.maplibre_expr_to_value` for the six operators it
    covers, and rejected for anything else. A ``dict`` is a legacy
    zoom/property function (``{"stops": …}``) — out of scope, always
    rejected.
    """
    if isinstance(value, dict):
        raise NotImplementedError(
            f"{prop}: legacy zoom/property functions ({{'stops': …}}) are "
            "not mapped by this codec"
        )
    return maplibre_expr_to_value(value, prop)


def _literal_offset(value: Any, prop: str) -> list:
    """A literal 2-number ``[x, y]`` array for an array-*typed* property.

    Unlike a scalar property (where any ``list`` is a MapLibre expression,
    see :func:`_constant`), an array-typed property like ``text-offset``
    is legitimately a plain ``[x, y]`` literal — but a MapLibre expression
    evaluating to an array (``["literal", [...]]``, ``["interpolate", ...]``,
    a legacy ``{"stops": ...}`` function, …) is still out of scope here.
    """
    if (
        isinstance(value, list)
        and len(value) == 2
        and all(isinstance(v, (int, float)) and not isinstance(v, bool) for v in value)
    ):
        return value
    raise NotImplementedError(
        f"{prop}: only a literal [x, y] array maps in this codec (data-driven "
        "/ zoom values and MapLibre expressions are not mapped yet)"
    )


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


def _circle_symbolizer(layer: dict[str, Any]) -> dict[str, Any]:
    """A ``circle`` layer → a ``marker`` with a single ``Circle`` element.

    A MapLibre circle carries an interior colour, an outline colour/width
    and a radius independently — a filled, outlined, sized circle. The
    faithful CartoSym target is the "shapes" ``Circle``
    (``ClosedShape.fill`` + ``abstractShape.outline`` + ``radius``); a
    ``1-core`` ``Dot`` (stroke only, by design) cannot hold all three.
    ``circle-radius`` and ``radius`` are both radii — mapped directly.
    """
    paint = layer.get("paint", {})
    _reject_unknown(paint, _CIRCLE_PAINT, "circle")
    _reject_unknown(layer.get("layout", {}), frozenset({"visibility"}), "circle layout")

    circle: dict[str, Any] = {"type": "Circle"}
    if "circle-opacity" in paint:
        circle["opacity"] = _constant(paint["circle-opacity"], "circle-opacity")
    if "circle-color" in paint:
        circle["fill"] = {"color": _constant(paint["circle-color"], "circle-color")}

    outline: dict[str, Any] = {}
    for mb_key, cs_key in (
        ("circle-stroke-color", "color"),
        ("circle-stroke-width", "thickness"),
        ("circle-stroke-opacity", "opacity"),
    ):
        if mb_key in paint:
            outline[cs_key] = _constant(paint[mb_key], mb_key)
    if outline:
        circle["outline"] = outline

    if "circle-radius" in paint:
        circle["radius"] = _constant(paint["circle-radius"], "circle-radius")

    return {"marker": {"elements": [circle]}}


def _background_symbolizer(layer: dict[str, Any]) -> dict[str, Any]:
    """A ``background`` layer → a ``Fill`` symbolizer tagged for round-trip.

    A ``background`` layer paints the whole map viewport — it has no
    ``source``/``source-layer`` and no feature geometry, so there is no
    CartoSym geometry-bound concept for it. Its paint
    (``background-color``/``background-opacity``) is structurally
    identical to a ``fill`` layer's ``Fill``; see the module docstring
    for why the vendor-extension tag exists.
    """
    paint = layer.get("paint", {})
    _reject_unknown(paint, _BACKGROUND_PAINT, "background")

    fill: dict[str, Any] = {}
    if "background-color" in paint:
        fill["color"] = _constant(paint["background-color"], "background-color")
    if "background-opacity" in paint:
        fill["opacity"] = _constant(paint["background-opacity"], "background-opacity")

    return {"fill": fill, "vendor.maplibre.layer-type": "background"}


def _text_field_to_text(value: Any) -> Any:
    """``"{name}"`` → ``{"property": "name"}``; ``"Foo"`` → ``"Foo"``.

    A ``text-field`` that is a MapLibre expression, or a template mixing
    literal text with ``{token}`` substitutions, has no single-value
    CartoSym ``Text.text`` mapping and is rejected.
    """
    if not isinstance(value, str):
        raise NotImplementedError(
            "text-field: only a literal string or a single {property} token "
            "maps to CartoSym Text in this codec"
        )
    stripped = value.strip()
    if stripped.startswith("{") and stripped.endswith("}") and stripped.count("{") == 1:
        return {"property": stripped[1:-1]}
    if "{" in value or "}" in value:
        raise NotImplementedError(
            f"text-field template {value!r} (literal text mixed with tokens) "
            "has no CartoSym Text.text mapping in this codec"
        )
    return value


def _symbol_font(layout: dict[str, Any], paint: dict[str, Any]) -> dict[str, Any]:
    font: dict[str, Any] = {}
    if "text-font" in layout:
        stack = layout["text-font"]
        if (
            not isinstance(stack, list)
            or len(stack) != 1
            or not isinstance(stack[0], str)
        ):
            raise NotImplementedError(
                f"text-font {stack!r}: only a single-family list maps to "
                "CartoSym Font.face in this codec"
            )
        font["face"] = stack[0]
    if "text-size" in layout:
        # Kept as a bare number, like circle-radius/-stroke-width elsewhere
        # in this codec — MapLibre's own values carry no unit tag either.
        font["size"] = _constant(layout["text-size"], "text-size")
    if "text-transform" in layout:
        transform = _constant(layout["text-transform"], "text-transform")
        if transform != "none":
            raise NotImplementedError(
                f"text-transform {transform!r} has no CartoSym Font mapping "
                "(only 'none' is representable)"
            )
    if "text-color" in paint:
        font["color"] = _constant(paint["text-color"], "text-color")
    if "text-opacity" in paint:
        font["opacity"] = _constant(paint["text-opacity"], "text-opacity")

    outline: dict[str, Any] = {}
    if "text-halo-color" in paint:
        outline["color"] = _constant(paint["text-halo-color"], "text-halo-color")
    if "text-halo-width" in paint:
        outline["size"] = _constant(paint["text-halo-width"], "text-halo-width")
    if outline:
        font["outline"] = outline
    return font


def _symbol_symbolizer(layer: dict[str, Any]) -> dict[str, Any]:
    """A ``symbol`` layer → a ``label`` (text) and/or a ``marker`` (icon)."""
    paint = layer.get("paint", {})
    layout = layer.get("layout", {})
    _reject_unknown(paint, _SYMBOL_PAINT, "symbol")
    _reject_unknown(layout, _SYMBOL_LAYOUT, "symbol layout")

    placement = layout.get("symbol-placement", "point")
    if placement != "point":
        raise NotImplementedError(
            f"symbol-placement {placement!r} (line / line-center labelling) "
            "has no CartoSym mapping in this codec"
        )

    has_text = "text-field" in layout
    has_icon = "icon-image" in layout
    if not has_text and not has_icon:
        raise NotImplementedError(
            "symbol layer without text-field or icon-image has nothing to map"
        )

    symbolizer: dict[str, Any] = {}

    if has_text:
        text_el: dict[str, Any] = {
            "type": "Text",
            "text": _text_field_to_text(layout["text-field"]),
            "position": {"x": 0, "y": 0},
        }
        if "text-offset" in layout:
            offset = _literal_offset(layout["text-offset"], "text-offset")
            # text-offset is in ems, relative to the anchor. CartoSym's
            # Graphic.position (UnitPoint) has no per-axis unit tag once
            # validated (unlike marker/label elements' Any-typed dicts),
            # so — matching this codebase's existing implicit-unit
            # positions (e.g. SLD se:Displacement, always px) — the em
            # count is kept as a bare number.
            text_el["position"] = {"x": offset[0], "y": offset[1]}
        if "text-anchor" in layout:
            anchor = _constant(layout["text-anchor"], "text-anchor")
            if anchor not in _ANCHOR_TO_ALIGNMENT:
                raise NotImplementedError(f"unexpected text-anchor {anchor!r}")
            text_el["alignment"] = list(_ANCHOR_TO_ALIGNMENT[anchor])
        font = _symbol_font(layout, paint)
        if font:
            text_el["font"] = font
        symbolizer["label"] = {"elements": [text_el]}

    if has_icon:
        image_el: dict[str, Any] = {
            "type": "Image",
            "image": {"id": _constant(layout["icon-image"], "icon-image")},
            "position": {"x": 0, "y": 0},
        }
        if "icon-opacity" in paint:
            image_el["opacity"] = _constant(paint["icon-opacity"], "icon-opacity")
        symbolizer["marker"] = {"elements": [image_el]}
    elif "icon-opacity" in paint:
        raise NotImplementedError("icon-opacity without icon-image has nothing to map")

    return symbolizer


_HANDLERS = {
    "fill": _fill_symbolizer,
    "line": _line_symbolizer,
    "circle": _circle_symbolizer,
    "symbol": _symbol_symbolizer,
    "background": _background_symbolizer,
}


def layer_to_styling_rule(layer: dict[str, Any]) -> dict[str, Any]:
    """Convert one MapLibre layer to a CartoSym ``stylingRule`` dict.

    Raises:
        NotImplementedError: for a layer type, value, or property this
            pass does not map.
    """
    for key in _UNSUPPORTED_LAYER_KEYS:
        if key in layer:
            raise NotImplementedError(
                f"layer {key!r} (zoom-range visibility) has no CartoSym "
                "mapping in this codec"
            )

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
