"""MapLibre GL layer → CartoSym styling-rule mapping (reader side).

Scope of this pass: ``fill`` / ``line`` / ``circle`` / ``symbol`` /
``background`` layers whose paint / layout scalar values are constants,
or one of six MapLibre value-expression operators — ``get`` / ``case`` /
``match`` / ``interpolate`` / ``step`` / ``coalesce`` (see
:mod:`._expressions`). Anything else — ``raster`` layers, legacy
zoom/property functions (``{"stops": …}``), or any other expression
operator — raises :exc:`NotImplementedError`. A partial mapping would
silently drop styling, which this project does not do. Layer ``filter``
maps to ``rule.selector`` (see :mod:`._filter`); a layer's
``minzoom``/``maxzoom`` also merge into ``rule.selector``, as ``viz.sd``
conjuncts (see :mod:`._zoom`).

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
from ._zoom import merge_zoom_range

# Paint/layout keys that carry no CartoSym-symbology meaning and are
# dropped rather than rejected, regardless of value — checked in both
# `paint` and `layout` (see `_reject_unknown`).
# `line-blur`/`text-halo-blur`/`icon-halo-blur` are a rendering-only blur
# radius, same category as `fill-antialias` — neither Stroke nor
# FontOutline has a blur field to hold them.
# `symbol-spacing` only affects symbol-placement `line`/`line-center`
# (MapLibre spec) — inert here, since this codec only maps
# `symbol-placement: point` (anything else already raises elsewhere).
# `text-padding` is collision-detection sizing (whether a label is hidden
# next to another one) — it never changes one label's own rendered
# appearance, so it carries no portrayal content for this codec's purposes.
# `text-rotate`/`icon-rotate` have no CartoSym field, same open question as
# `se:Graphic/se:Rotation` on the SLD/SE side (see `codecs/sld/_symbolizer.py`
# — "pending a mapping decision"), so dropped the same way for consistency
# across codecs rather than raised here alone.
_IGNORED_PAINT: frozenset[str] = frozenset(
    {
        "fill-antialias",
        "line-blur",
        "text-halo-blur",
        "icon-halo-blur",
        "symbol-spacing",
        "text-padding",
        "text-rotate",
        "icon-rotate",
    }
)

# Layout/paint properties whose spec default is a portrayal no-op (the
# same as the property being absent) — anything else raises, since there
# is no CartoSym field for the non-default effect. See `_reject_if_non_default`.
_LAYOUT_DEFAULTS: dict[str, Any] = {
    "icon-size": 1,
    "text-justify": "center",
    "text-max-width": 10,
}
_PAINT_DEFAULTS: dict[str, Any] = {"line-offset": 0}

_FILL_PAINT: frozenset[str] = frozenset(
    {"fill-color", "fill-opacity", "fill-outline-color", "fill-pattern"}
)
_LINE_PAINT: frozenset[str] = frozenset(
    {"line-color", "line-opacity", "line-width", "line-offset", "line-dasharray"}
)
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
    {
        "text-color",
        "text-opacity",
        "text-halo-color",
        "text-halo-width",
        "icon-opacity",
        "icon-color",
    }
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
        "icon-size",
        "text-justify",
        "text-max-width",
    }
)
_BACKGROUND_PAINT: frozenset[str] = frozenset(
    {"background-color", "background-opacity"}
)

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
    """Build a literal 2-number ``[x, y]`` array for an array-*typed* property.

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


def _reject_if_non_default(value: Any, prop: str, defaults: dict[str, Any]) -> None:
    """Raise unless *value* equals ``defaults[prop]`` — a spec no-op.

    ``defaults`` (see ``_LAYOUT_DEFAULTS``/``_PAINT_DEFAULTS``) holds the
    MapLibre spec default for a property this codec has no CartoSym field
    for. Writing that literal default is equivalent to omitting the
    property — nothing is lost passing it through silently — but any
    other literal, or an expression, has real portrayal content this
    codec cannot represent and must raise instead of dropping.
    """
    default = defaults[prop]
    if value != default:
        raise NotImplementedError(
            f"{prop} {value!r} (not the spec default {default!r}) has no "
            "CartoSym mapping in this codec"
        )


def _visibility(layer: dict[str, Any]) -> bool | None:
    vis = layer.get("layout", {}).get("visibility")
    if vis in (None, "visible"):
        return None
    if vis == "none":
        return False
    raise NotImplementedError(f"unexpected layout.visibility {vis!r}")


def _fill_pattern_to_graphic(value: Any) -> dict[str, Any]:
    """Turn a MapLibre ``fill-pattern`` value into a CartoSym Image graphic.

    Only a literal sprite-id string maps — MapLibre also allows a
    data-driven expression here (this codec's own target corpus has one,
    a ``match`` on a numeric weight property), but CartoSym's
    ``Resource.id`` is a plain string with no data-driven equivalent to
    hold an expression.
    """
    if not isinstance(value, str):
        raise NotImplementedError(
            f"fill-pattern {value!r}: only a literal sprite-id string maps "
            "to a CartoSym Image graphic in this codec"
        )
    return {"type": "Image", "image": {"id": value}}


def _fill_symbolizer(layer: dict[str, Any]) -> dict[str, Any]:
    paint = layer.get("paint", {})
    _reject_unknown(paint, _FILL_PAINT, "fill")

    fill: dict[str, Any] = {}
    if "fill-color" in paint:
        fill["color"] = _constant(paint["fill-color"], "fill-color")
    if "fill-opacity" in paint:
        fill["opacity"] = _constant(paint["fill-opacity"], "fill-opacity")
    if "fill-pattern" in paint:
        fill["pattern"] = _fill_pattern_to_graphic(paint["fill-pattern"])

    symbolizer: dict[str, Any] = {"fill": fill}
    if "fill-outline-color" in paint:
        # MapLibre draws the fill outline as a 1px stroke of this colour.
        symbolizer["stroke"] = {
            "color": _constant(paint["fill-outline-color"], "fill-outline-color")
        }
    return symbolizer


def _dash_pattern_from_array(dasharray: Any, width: Any, ctx: str) -> list[int]:
    """Turn a MapLibre ``line-dasharray`` into a CartoSym ``stroke.dashPattern``.

    Inverse of the writer's ``_dash_array``: ``line-dasharray`` is in
    multiples of the line's own width, ``dashPattern`` is absolute px —
    each length is multiplied by ``stroke.width`` in px, rounded to the
    nearest integer (``dashPattern``'s schema type). Only a literal array
    of numbers maps — a legacy ``{"stops": …}`` function or any other
    expression here is out of scope, same as elsewhere in this codec —
    and it needs a literal numeric ``line-width`` to scale by.
    """
    if not isinstance(dasharray, list) or not all(
        isinstance(v, (int, float)) and not isinstance(v, bool) for v in dasharray
    ):
        raise NotImplementedError(
            f"{ctx}: {dasharray!r} is not a literal array of numbers"
        )
    if not isinstance(width, (int, float)) or isinstance(width, bool):
        raise NotImplementedError(
            f"{ctx}: needs a literal line-width to convert into CartoSym's "
            "absolute-px stroke.dashPattern, which is missing or "
            "non-literal here"
        )
    return [round(v * width) for v in dasharray]


def _line_symbolizer(layer: dict[str, Any]) -> dict[str, Any]:
    paint = layer.get("paint", {})
    _reject_unknown(paint, _LINE_PAINT, "line")
    # line-cap / line-join / line-round-limit change rendered geometry with
    # no CartoSym Stroke field — reject rather than drop.
    _reject_unknown(layer.get("layout", {}), frozenset({"visibility"}), "line layout")
    if "line-offset" in paint:
        _reject_if_non_default(paint["line-offset"], "line-offset", _PAINT_DEFAULTS)

    stroke: dict[str, Any] = {}
    if "line-color" in paint:
        stroke["color"] = _constant(paint["line-color"], "line-color")
    if "line-width" in paint:
        stroke["width"] = _constant(paint["line-width"], "line-width")
    if "line-opacity" in paint:
        stroke["opacity"] = _constant(paint["line-opacity"], "line-opacity")
    if "line-dasharray" in paint:
        stroke["dashPattern"] = _dash_pattern_from_array(
            paint["line-dasharray"], stroke.get("width"), "line-dasharray"
        )
    return {"stroke": stroke}


def _circle_symbolizer(layer: dict[str, Any]) -> dict[str, Any]:
    """Turn a ``circle`` layer into a ``marker`` with a single ``Circle`` element.

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
    """Turn a ``background`` layer into a ``Fill`` symbolizer tagged for round-trip.

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
    """Turn a ``symbol`` layer into a ``label`` (text) and/or a ``marker`` (icon)."""
    paint = layer.get("paint", {})
    layout = layer.get("layout", {})
    _reject_unknown(paint, _SYMBOL_PAINT, "symbol")
    _reject_unknown(layout, _SYMBOL_LAYOUT, "symbol layout")
    for prop in ("icon-size", "text-justify", "text-max-width"):
        if prop in layout:
            _reject_if_non_default(layout[prop], prop, _LAYOUT_DEFAULTS)

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
        if "icon-color" in paint:
            # icon-color only recolours an SDF sprite in MapLibre — a
            # constraint this codec can't check (no access to the actual
            # sprite image), same caveat noted on the writer side
            # (._icon_layer_layout_paint).
            image_el["tint"] = _constant(paint["icon-color"], "icon-color")
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

    filter_selector = filter_to_selector(layer["filter"]) if "filter" in layer else None
    selector = merge_zoom_range(
        layer.get("minzoom"), layer.get("maxzoom"), filter_selector
    )

    rule: dict[str, Any] = {"name": layer["id"]}
    if selector is not None:
        rule["selector"] = selector
    rule["symbolizer"] = symbolizer
    return rule
