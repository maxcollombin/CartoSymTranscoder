"""MapLibre / MapBox GL Style writer — CartoSym Style models → style JSON.

The inverse of :mod:`.reader`, and with the same scope: a ``fill`` /
``line`` / ``marker`` (single ``Circle`` or ``Image``) / ``label``
(single ``Text``) symbolizer with constant values maps to one MapLibre
layer (``fill`` / ``line`` / ``circle`` / ``symbol``); a rule selector
maps to the layer ``filter``, except any ``viz.sd`` conjuncts that match
MapLibre's own zoom-range shape, which map to ``minzoom``/``maxzoom``
instead (see :mod:`._zoom`). A fill-only symbolizer carrying the
``vendor.maplibre.layer-type: "background"`` extension (see
:mod:`._layers`) maps to a ``background`` layer instead of ``fill``.
Raster symbolizers, multi-element markers/labels, other graphic types,
and non-literal values raise :exc:`NotImplementedError`.

``StylingRule.nestedRules`` (a cascading refinement, e.g.
``[attr = value] { ... }`` narrowing a parent rule) has no MapLibre
nesting equivalent — ``layers`` is a flat list — so it is flattened into
independent rules first (see :func:`_flatten_rules`, reusing
:mod:`..._cascade`); a flattened rule with no name of its own inherits
its nearest named ancestor's, disambiguated with a positional suffix. A
rule that draws nothing (visibility/opacity/zOrder only — typically a
cascade's base/gate rule) is dropped rather than raising (see
:func:`_is_empty_of_paint`); one that instead carries unsupported
(raster) content still raises.

A CartoSym style has no data-source concept, so the output declares one
synthetic empty GeoJSON source (``cartosym``) that every layer references
— enough to satisfy the MapLibre style specification.
"""

from __future__ import annotations

from typing import Any

from ...models.styles import Style, StylingRule
from .._cascade import flatten_cascade_rules
from ..base import CodecWriter
from ._expressions import value_to_maplibre_expr
from ._filter import selector_to_filter
from ._layers import _ANCHOR_TO_ALIGNMENT
from ._zoom import extract_zoom_range

_SOURCE = "cartosym"

# CartoSym (hAlignment, vAlignment) -> MapLibre text-anchor token.
_ALIGNMENT_TO_ANCHOR = {v: k for k, v in _ANCHOR_TO_ALIGNMENT.items()}

# Symbolizer parts with no mapping in this pass — presence is an error,
# not a silent drop.
_UNSUPPORTED_SYMBOLIZER_PARTS = (
    "color_channels",
    "alpha_channel",
    "single_channel",
    "color_map",
    "opacity_map",
    "hill_shading",
)


def _literal(value: Any, prop: str) -> Any:
    """Return a plain string / number / bool, or a mapped MapLibre expression.

    A :mod:`...models.value_expressions` model (``PropertyRef``,
    ``CaseExpression``, …) round-trips back to its MapLibre array via
    :func:`._expressions.value_to_maplibre_expr`; anything else this codec
    does not map (a precise ``Color``/``UnitValue`` model, …) raises.
    """
    if isinstance(value, (str, int, float, bool)):
        return value
    return value_to_maplibre_expr(value, prop)


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


def _vendor_layer_type(sym: Any) -> str | None:
    """Return the symbolizer's ``vendor.maplibre.layer-type`` extra, if any.

    Raises on any other ``vendor.*`` extra (no other one is understood by
    this codec) or an unrecognised ``layer-type`` value — an unknown
    vendor extension must never be silently dropped.
    """
    extras = getattr(sym, "__pydantic_extra__", None) or {}
    layer_type = extras.get("vendor.maplibre.layer-type")
    unknown = [k for k in extras if k != "vendor.maplibre.layer-type"]
    if unknown:
        raise NotImplementedError(
            f"vendor extension {unknown[0]!r} has no MapLibre mapping in this codec"
        )
    if layer_type is not None and layer_type != "background":
        raise NotImplementedError(
            f"vendor.maplibre.layer-type {layer_type!r} is not a recognised value"
        )
    return layer_type


def _background_layer(layer_id: str, fill: Any, stroke: Any) -> dict[str, Any]:
    """A ``Fill`` symbolizer tagged ``vendor.maplibre.layer-type: background``.

    See :func:`._layers._background_symbolizer` for why the tag exists: a
    ``background`` layer's paint is structurally identical to a ``fill``
    layer's, so this is the only way back to the right MapLibre layer
    type. Unlike ``fill``, a ``background`` layer has no ``source`` and
    no outline.
    """
    for attr in ("pattern", "hatch", "dotpattern", "stipple", "alter"):
        if getattr(fill, attr, None) is not None:
            raise NotImplementedError(
                f"fill.{attr} has no MapLibre mapping in this codec"
            )
    if stroke is not None:
        raise NotImplementedError(
            "a background layer has no outline — a stroke on a "
            "vendor.maplibre.layer-type=background symbolizer has no MapLibre "
            "mapping"
        )

    paint: dict[str, Any] = {}
    if fill.color is not None:
        paint["background-color"] = _literal(fill.color, "fill.color")
    if fill.opacity is not None:
        paint["background-opacity"] = _literal(fill.opacity, "fill.opacity")

    return {"id": layer_id, "type": "background", "paint": paint}


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


def _attr(obj: Any, key: str) -> Any:
    """Read *key* from a graphic element, which may be a dict or a Pydantic model."""
    if isinstance(obj, dict):
        return obj.get(key)
    return getattr(obj, key, None)


def _circle_layer(layer_id: str, marker: Any) -> dict[str, Any]:
    elements = marker.elements
    if not isinstance(elements, list) or len(elements) != 1:
        raise NotImplementedError(
            "MapLibre has no multi-graphic marker — exactly one Circle element "
            "maps to a circle layer"
        )
    circle = elements[0]
    if _attr(circle, "type") != "Circle":
        raise NotImplementedError(
            f"marker element {_attr(circle, 'type')!r} → MapLibre "
            "(only a shapes Circle maps, to a circle layer)"
        )

    paint: dict[str, Any] = {}
    fill = _attr(circle, "fill")
    if fill is not None and _attr(fill, "color") is not None:
        paint["circle-color"] = _literal(_attr(fill, "color"), "Circle.fill.color")

    outline = _attr(circle, "outline")
    if outline is not None:
        for cs_key, mb_key in (
            ("color", "circle-stroke-color"),
            ("thickness", "circle-stroke-width"),
            ("opacity", "circle-stroke-opacity"),
        ):
            value = _attr(outline, cs_key)
            if value is not None:
                paint[mb_key] = _literal(value, f"Circle.outline.{cs_key}")

    radius = _attr(circle, "radius")
    if radius is not None:
        paint["circle-radius"] = _literal(radius, "Circle.radius")

    opacity = _attr(circle, "opacity")
    if opacity is not None:
        paint["circle-opacity"] = _literal(opacity, "Circle.opacity")

    return {"id": layer_id, "type": "circle", "source": _SOURCE, "paint": paint}


def _position_axis_number(value: Any, ctx: str) -> float:
    """A ``Graphic.position`` axis as a bare number for ``text-offset``.

    ``UnitPoint.x``/``.y`` is ``UnitValue | str | float`` once validated;
    only a bare number round-trips (see the reader's matching comment —
    the CartoSym-JSON unit tag does not survive validation on this field).
    """
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return value
    raise NotImplementedError(
        f"{ctx}: only a unit-less Text.position axis maps to MapLibre "
        "text-offset (an em) in this codec"
    )


def _text_layer_layout_paint(text_el: Any) -> tuple[dict[str, Any], dict[str, Any]]:
    layout: dict[str, Any] = {}
    paint: dict[str, Any] = {}

    text = _attr(text_el, "text")
    if isinstance(text, dict) and "property" in text:
        layout["text-field"] = "{" + text["property"] + "}"
    elif isinstance(text, str):
        layout["text-field"] = text
    else:
        raise NotImplementedError(
            f"Text.text {text!r}: only a literal string or a {{property: …}} "
            "reference maps to MapLibre text-field in this codec"
        )

    position = _attr(text_el, "position")
    if position is not None:
        px = _position_axis_number(_attr(position, "x"), "Text.position.x")
        py = _position_axis_number(_attr(position, "y"), "Text.position.y")
        if px != 0 or py != 0:
            layout["text-offset"] = [px, py]

    alignment = _attr(text_el, "alignment")
    if alignment is not None:
        if isinstance(alignment, (list, tuple)) and len(alignment) == 2:
            h, v = alignment[0], alignment[1]
        else:
            h = _attr(alignment, "h_alignment") or _attr(alignment, "hAlignment")
            v = _attr(alignment, "v_alignment") or _attr(alignment, "vAlignment")
        anchor = _ALIGNMENT_TO_ANCHOR.get((h, v))
        if anchor is None:
            raise NotImplementedError(f"Text.alignment {(h, v)!r} is not mapped")
        layout["text-anchor"] = anchor

    font = _attr(text_el, "font")
    if font is not None:
        for attr in ("bold", "italic", "underline"):
            if _attr(font, attr) is not None:
                raise NotImplementedError(
                    f"Font.{attr} has no MapLibre mapping in this codec"
                )
        face = _attr(font, "face")
        if face is not None:
            layout["text-font"] = [_literal(face, "Font.face")]
        size = _attr(font, "size")
        if size is not None:
            layout["text-size"] = _literal(size, "Font.size")
        color = _attr(font, "color")
        if color is not None:
            paint["text-color"] = _literal(color, "Font.color")
        opacity = _attr(font, "opacity")
        if opacity is not None:
            paint["text-opacity"] = _literal(opacity, "Font.opacity")

        outline = _attr(font, "outline")
        if outline is not None:
            outline_color = _attr(outline, "color")
            if outline_color is not None:
                paint["text-halo-color"] = _literal(outline_color, "Font.outline.color")
            outline_size = _attr(outline, "size")
            if outline_size is not None:
                paint["text-halo-width"] = _literal(outline_size, "Font.outline.size")

    return layout, paint


def _icon_layer_layout_paint(image_el: Any) -> tuple[dict[str, Any], dict[str, Any]]:
    for attr in (
        "hotSpot",
        "hot_spot",
        "tint",
        "blackTint",
        "black_tint",
        "alphaThreshold",
        "alpha_threshold",
    ):
        if _attr(image_el, attr) is not None:
            raise NotImplementedError(
                f"Image.{attr} has no MapLibre mapping in this codec"
            )
    image = _attr(image_el, "image")
    icon_id = _attr(image, "id") or _attr(image, "uri") or _attr(image, "path")
    if icon_id is None:
        raise NotImplementedError(
            "Image.image without id/uri/path has no MapLibre icon-image mapping"
        )
    layout: dict[str, Any] = {"icon-image": _literal(icon_id, "Image.image")}
    paint: dict[str, Any] = {}
    opacity = _attr(image_el, "opacity")
    if opacity is not None:
        paint["icon-opacity"] = _literal(opacity, "Image.opacity")
    return layout, paint


def _symbol_layer(layer_id: str, label: Any, marker: Any) -> dict[str, Any]:
    layout: dict[str, Any] = {}
    paint: dict[str, Any] = {}

    if label is not None:
        elements = label.elements
        if not isinstance(elements, list) or len(elements) != 1:
            raise NotImplementedError(
                "MapLibre has no multi-graphic label — exactly one Text "
                "element maps to a symbol layer"
            )
        text_el = elements[0]
        if _attr(text_el, "type") != "Text":
            raise NotImplementedError(
                f"label element {_attr(text_el, 'type')!r} → MapLibre "
                "(only Text maps, to a symbol layer)"
            )
        text_layout, text_paint = _text_layer_layout_paint(text_el)
        layout.update(text_layout)
        paint.update(text_paint)

    if marker is not None:
        elements = marker.elements
        if not isinstance(elements, list) or len(elements) != 1:
            raise NotImplementedError(
                "MapLibre has no multi-graphic marker — exactly one Image "
                "element maps into a symbol layer's icon-image"
            )
        image_el = elements[0]
        if _attr(image_el, "type") != "Image":
            raise NotImplementedError(
                f"marker element {_attr(image_el, 'type')!r} → MapLibre "
                "(only Image maps, into a symbol layer's icon-image)"
            )
        icon_layout, icon_paint = _icon_layer_layout_paint(image_el)
        layout.update(icon_layout)
        paint.update(icon_paint)

    return {
        "id": layer_id,
        "type": "symbol",
        "source": _SOURCE,
        "layout": layout,
        "paint": paint,
    }


def _flatten_rules(styling_rules: list[StylingRule]) -> list[StylingRule]:
    """Flatten CartoSym nested-rule cascades into independent rules.

    MapLibre's ``layers`` is a flat list — unlike ``StylingRule``, it has
    no nesting concept — so a cascading refinement
    (``[attr = value] { ... }`` under a parent rule) must become its own
    top-level entry before :func:`_rule_to_layer` can see it. Reuses the
    codec-agnostic :func:`~pycartosym.codecs._cascade.flatten_cascade_rules`
    (selector AND + symbolizer merge), one top-level rule's subtree at a
    time so a name synthesized below never leaks across siblings.

    A flattened rule with no ``name``/``stylingRuleName`` of its own — the
    common case for a refinement, which usually only narrows the selector
    — inherits its nearest named ancestor's name, disambiguated with a
    positional suffix (a MapLibre layer id must be unique, unlike an SE
    rule which needs no name at all).
    """
    if not any(rule.nested_rules for rule in styling_rules):
        return list(styling_rules)

    out: list[StylingRule] = []
    for rule in styling_rules:
        current_name: str | None = None
        counter = 0
        for flat in flatten_cascade_rules([rule.to_dict()]):
            if flat.get("nestedRules"):
                raise NotImplementedError(
                    "a selector-less nestedRules entry (OGC 'else' rule) has "
                    "no MapLibre mapping in this codec"
                )
            name = flat.get("name") or flat.get("stylingRuleName")
            if name:
                current_name = name
                counter = 0
            elif current_name is not None:
                counter += 1
                flat["name"] = f"{current_name}-{counter}"
            out.append(StylingRule.from_dict(flat))
    return out


def _is_empty_of_paint(rule: Any) -> bool:
    """True if *rule* draws nothing and is safe to drop from ``layers``.

    Mirrors the SLD/SE writer's policy for a symbolizer-less rule (no
    symbolizer at all, or only ``visibility``/``opacity``/``zOrder`` —
    typically the base rule of a cascade, e.g. ``visibility: false`` gating
    scale-conditioned refinements): nothing is lost by omitting it. A rule
    that instead carries unsupported content (raster fields — see
    :data:`_UNSUPPORTED_SYMBOLIZER_PARTS`) is *not* empty — it still needs
    to reach :func:`_rule_to_layer` and raise there, not be silently
    dropped here.
    """
    sym = rule.symbolizer
    if sym is None:
        return True
    if any(
        getattr(sym, part, None) is not None for part in _UNSUPPORTED_SYMBOLIZER_PARTS
    ):
        return False
    return (
        sym.fill is None
        and sym.stroke is None
        and sym.marker is None
        and sym.label is None
    )


def _rule_to_layer(rule: Any) -> dict[str, Any]:
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

    minzoom, maxzoom, remaining_selector = extract_zoom_range(rule.selector)

    vendor_layer_type = _vendor_layer_type(sym)
    if vendor_layer_type == "background" and (
        sym.fill is None
        or sym.stroke is not None
        or sym.marker is not None
        or sym.label is not None
    ):
        raise NotImplementedError(
            "vendor.maplibre.layer-type=background requires a fill-only "
            "symbolizer (no stroke, marker, or label)"
        )
    if vendor_layer_type == "background" and remaining_selector is not None:
        raise NotImplementedError(
            "a background layer has no filter — rule.selector must reduce to "
            "nothing but viz.sd zoom-range conjuncts on a "
            "vendor.maplibre.layer-type=background symbolizer"
        )

    marker_type = None
    if sym.marker is not None:
        elements = sym.marker.elements
        if isinstance(elements, list) and len(elements) == 1:
            marker_type = _attr(elements[0], "type")

    if sym.label is not None or marker_type == "Image":
        if sym.fill is not None or sym.stroke is not None:
            raise NotImplementedError(
                "a symbolizer with both a label/icon marker and fill/stroke "
                "needs several MapLibre layers — not supported"
            )
        if sym.label is not None and marker_type not in (None, "Image"):
            raise NotImplementedError(
                "a symbolizer with both a label and a non-Image marker needs "
                "several MapLibre layers — not supported"
            )
        layer = _symbol_layer(layer_id, sym.label, sym.marker)
    elif sym.marker is not None:
        if sym.fill is not None or sym.stroke is not None:
            raise NotImplementedError(
                "a symbolizer with both a marker and fill/stroke needs several "
                "MapLibre layers — not supported"
            )
        layer = _circle_layer(layer_id, sym.marker)
    elif sym.fill is not None:
        if vendor_layer_type == "background":
            layer = _background_layer(layer_id, sym.fill, sym.stroke)
        else:
            layer = _fill_layer(layer_id, sym.fill, sym.stroke)
    elif sym.stroke is not None:
        layer = _line_layer(layer_id, sym.stroke)
    else:
        raise NotImplementedError(
            "symbolizer with no fill / stroke / marker has no MapLibre mapping"
        )

    if minzoom is not None or maxzoom is not None or remaining_selector is not None:
        # Re-key so `minzoom`/`maxzoom`/`filter` sit before `layout`/
        # `paint`, as styles are conventionally written.
        layout = layer.pop("layout", None)
        paint = layer.pop("paint")
        if minzoom is not None:
            layer["minzoom"] = minzoom
        if maxzoom is not None:
            layer["maxzoom"] = maxzoom
        if remaining_selector is not None:
            layer["filter"] = selector_to_filter(remaining_selector)
        if layout is not None:
            layer["layout"] = layout
        layer["paint"] = paint

    if sym.visibility is False:
        layer.setdefault("layout", {})["visibility"] = "none"
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
        rules = _flatten_rules(style.styling_rules)
        layers = [
            _rule_to_layer(rule) for rule in rules if not _is_empty_of_paint(rule)
        ]
        sources: dict[str, Any] = {}
        # A `background` layer has no `source` — only declare the synthetic
        # one when a layer actually references it.
        if any(layer.get("source") == _SOURCE for layer in layers):
            sources[_SOURCE] = {
                "type": "geojson",
                "data": {"type": "FeatureCollection", "features": []},
            }
        return {"version": 8, "sources": sources, "layers": layers}
