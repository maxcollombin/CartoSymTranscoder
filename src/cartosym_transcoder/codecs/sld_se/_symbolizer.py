"""
CartoSym ``Symbolizer`` <-> SLD/SE ``{Point,Line,Polygon,Text,Raster}Symbolizer``
mapping, both directions.

Scope: vector symbolizers plus basic Part-1 raster/coverage styling
(channels, color map, shaded relief) — see
``docs/sld_se_mapping_issues.md`` issues #3/#24/#25/#31/#32/#33 for the
exact boundary. ``Fill.hatch/dotpattern/stipple``, ``Stroke.casing/centerLine``,
``Label.placement``, ``Symbolizer.alphaChannel``, ``Symbolizer.opacityMap``,
and ``HillShading.sun``/``colorMap``/``opacityMap`` are all out of scope
and raise :exc:`NotImplementedError` naming the field — per this project's
lossless-transcoding requirement, out-of-scope content must fail loudly
rather than silently drop data.

``Dot``, ``Image``, and ``Text`` graphic elements (found in either
``Symbolizer.marker.elements`` or ``Symbolizer.label.elements`` — CartoSym
allows Text under either) are in scope (``Shape``/``Circle``/``Rectangle``
are not, see mapping-issues issue #8); on read, an ``se:Mark``/
``se:ExternalGraphic`` always reconstructs into ``marker.elements`` and an
``se:TextSymbolizer`` always reconstructs into ``label.elements`` (SLD/SE
has no construct distinguishing CartoSym's separate marker-text vs
label-text concepts — see mapping-issues issue on this asymmetry).
"""

from typing import Any, List, Optional

from lxml import etree

from ._types import (
    format_color,
    format_number,
    format_opacity,
    format_unit_value,
    parse_color,
    parse_number,
    parse_opacity,
    parse_unit_value,
)
from ._xml_helpers import (
    OGC,
    XLINK,
    find_se_direct,
    get_svg_param,
    local_name,
    se_el,
    svg_param,
)

_ANCHOR_X = {"left": "0", "center": "0.5", "right": "1"}
_ANCHOR_Y = {"top": "1", "middle": "0.5", "bottom": "0"}
_ANCHOR_X_TO_H = {"0": "left", "0.5": "center", "1": "right"}
_ANCHOR_Y_TO_V = {"1": "top", "0.5": "middle", "0": "bottom"}


def _g(obj: Any, key: str, default: Any = None) -> Any:
    """Get *key* from *obj*, whether it's a plain dict or a Pydantic model."""
    if obj is None:
        return default
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


def _number_of(value: Any) -> Optional[float]:
    if value is None:
        return None
    if hasattr(value, "value"):
        return value.value
    if isinstance(value, dict) and len(value) == 1:
        return next(iter(value.values()))
    if isinstance(value, (int, float)):
        return value
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _unit_point_xy(position: Any):
    return _number_of(_g(position, "x")), _number_of(_g(position, "y"))


# ---------------------------------------------------------------------------
# Writer direction: Symbolizer -> SLD/SE symbolizer elements
# ---------------------------------------------------------------------------

_RASTER_FIELD_ATTRS = (
    "color_channels",
    "alpha_channel",
    "single_channel",
    "color_map",
    "opacity_map",
    "hill_shading",
)


def _has_raster_fields(sym: Any) -> bool:
    return any(_g(sym, attr) is not None for attr in _RASTER_FIELD_ATTRS)


def symbolizer_to_elements(sym: Any) -> List[etree._Element]:
    """Convert one CartoSym ``Symbolizer`` into 1..N sibling SLD/SE elements."""
    elements: List[etree._Element] = []
    fill = _g(sym, "fill")
    stroke = _g(sym, "stroke")
    marker = _g(sym, "marker")
    label = _g(sym, "label")

    if fill is not None:
        elements.append(_build_polygon_symbolizer(fill, stroke))
    elif stroke is not None:
        elements.append(_build_line_symbolizer(stroke))

    if _has_raster_fields(sym):
        elements.append(_build_raster_symbolizer(sym))

    if marker is not None:
        elements.extend(_graphic_elements_to_symbolizers(_g(marker, "elements")))

    if label is not None:
        if _g(label, "placement") is not None:
            raise NotImplementedError(
                "Label.placement (line placement / priority / spacing) has "
                "no SLD/SE mapping in this codec (see mapping-issues issue #18)"
            )
        elements.extend(_graphic_elements_to_symbolizers(_g(label, "elements")))

    return elements


def _graphic_elements_to_symbolizers(elements: Any) -> List[etree._Element]:
    if elements is None:
        return []
    if isinstance(elements, dict) and "index" in elements and "value" in elements:
        raise NotImplementedError(
            "Indexed marker/label element overrides ({index, value}) are "
            "not supported by this codec — the rule's element list must "
            "already be fully resolved before conversion to SLD/SE"
        )
    if not isinstance(elements, list):
        elements = [elements]
    result = []
    for el in elements:
        el_type = _g(el, "type")
        if el_type == "Dot":
            result.append(_build_point_symbolizer(el))
        elif el_type == "Image":
            result.append(_build_image_symbolizer(el))
        elif el_type == "Text":
            result.append(_build_text_symbolizer(el))
        else:
            raise NotImplementedError(
                f"Graphic element type {el_type!r} has no SLD/SE mapping in "
                "this codec's scope (Shape/Circle/Rectangle — see "
                "mapping-issues issue #8)"
            )
    return result


def _raise_if_fill_out_of_scope(fill: Any) -> None:
    for attr in ("hatch", "dotpattern", "stipple", "pattern"):
        if _g(fill, attr) is not None:
            raise NotImplementedError(
                f"Fill.{attr} has no SLD/SE mapping in this codec (see "
                "mapping-issues issue #7)"
            )


def _build_fill_element(fill: Any) -> etree._Element:
    _raise_if_fill_out_of_scope(fill)
    el = se_el("Fill")
    color = _g(fill, "color")
    opacity = _g(fill, "opacity")
    if color is not None:
        svg_param(el, "fill", format_color(color))
    if opacity is not None:
        svg_param(el, "fill-opacity", format_opacity(opacity))
    return el


def _raise_if_stroke_out_of_scope(stroke: Any) -> None:
    if _g(stroke, "casing") is not None:
        raise NotImplementedError(
            "Stroke.casing has no SLD/SE mapping in this codec (see "
            "mapping-issues issue #8)"
        )
    if _g(stroke, "center_line") is not None:
        raise NotImplementedError(
            "Stroke.centerLine has no SLD/SE mapping in this codec (see "
            "mapping-issues issue #8)"
        )
    if _g(stroke, "pattern") is not None:
        raise NotImplementedError(
            "Stroke.pattern (graphic stroke) has no SLD/SE mapping in this "
            "codec (see mapping-issues issue #8)"
        )


def _build_stroke_element(stroke: Any) -> etree._Element:
    _raise_if_stroke_out_of_scope(stroke)
    el = se_el("Stroke")
    color = _g(stroke, "color")
    width = _g(stroke, "width")
    opacity = _g(stroke, "opacity")
    dash_pattern = _g(stroke, "dash_pattern")
    if color is not None:
        svg_param(el, "stroke", format_color(color))
    if width is not None:
        svg_param(el, "stroke-width", format_unit_value(width))
    if opacity is not None:
        svg_param(el, "stroke-opacity", format_opacity(opacity))
    if dash_pattern is not None:
        pattern = _g(dash_pattern, "pattern")
        if pattern:
            svg_param(el, "stroke-dasharray", " ".join(str(int(p)) for p in pattern))
    return el


def _build_polygon_symbolizer(fill: Any, stroke: Any) -> etree._Element:
    el = se_el("PolygonSymbolizer")
    if fill is not None:
        el.append(_build_fill_element(fill))
    if stroke is not None:
        el.append(_build_stroke_element(stroke))
    return el


def _build_line_symbolizer(stroke: Any) -> etree._Element:
    el = se_el("LineSymbolizer")
    el.append(_build_stroke_element(stroke))
    return el


def _g2(obj: Any, snake: str, camel: str, default: Any = None) -> Any:
    """Like :func:`_g`, but for raster sub-dicts (``hillShading``, ...)
    that are always raw ``Any``-typed dicts with camelCase JSON keys —
    never alias-normalized by Pydantic — so both spellings must be tried.
    """
    if obj is None:
        return default
    if isinstance(obj, dict):
        return obj[snake] if snake in obj else obj.get(camel, default)
    return getattr(obj, snake, default)


def _channel_source_name(channel_expr: Any, field_label: str) -> str:
    """Return the plain band/property name for one ``colorChannels``/
    ``singleChannel`` entry. Only a bare ``{"property": X}`` reference
    maps to ``se:SourceChannelName`` — a plain-string XSD type, unable to
    hold an arithmetic expression (e.g. an NDVI formula) at all.
    """
    if isinstance(channel_expr, dict) and set(channel_expr) == {"property"}:
        return str(channel_expr["property"])
    raise NotImplementedError(
        f"Symbolizer.{field_label} entries other than a bare property "
        f"reference ({{'property': X}}) have no se:SourceChannelName "
        f"mapping in this codec (got {channel_expr!r}; see mapping-issues "
        "issue #32)"
    )


def _build_channel_selection_rgb(color_channels: Any) -> etree._Element:
    if not isinstance(color_channels, list) or len(color_channels) != 3:
        raise NotImplementedError(
            "Symbolizer.colorChannels must be a 3-element [R, G, B] list "
            f"(got {color_channels!r})"
        )
    cs = se_el("ChannelSelection")
    for tag, expr in zip(("RedChannel", "GreenChannel", "BlueChannel"), color_channels):
        name = _channel_source_name(expr, "colorChannels")
        channel_el = se_el(tag, parent=cs)
        se_el("SourceChannelName", parent=channel_el, text=name)
    return cs


def _build_channel_selection_gray(single_channel: Any) -> etree._Element:
    name = _channel_source_name(single_channel, "singleChannel")
    cs = se_el("ChannelSelection")
    gray_el = se_el("GrayChannel", parent=cs)
    se_el("SourceChannelName", parent=gray_el, text=name)
    return cs


def _validated_map_pairs(value: Any, field_label: str) -> list:
    if not isinstance(value, list) or not value:
        raise NotImplementedError(
            f"Symbolizer.{field_label} must be a non-empty list of "
            f"[threshold, value] pairs (got {value!r})"
        )
    for pair in value:
        if not isinstance(pair, (list, tuple)) or len(pair) < 2:
            raise NotImplementedError(
                f"Symbolizer.{field_label} entries must be [threshold, "
                f"value] pairs (got {pair!r})"
            )
    return value


def _build_categorize(pairs: list) -> etree._Element:
    """Build ``se:Categorize`` from ``[threshold, color]`` pairs.

    Per ``se:Categorize``'s own semantics, the first ``se:Value`` has no
    preceding ``se:Threshold`` (it's the below/at-first-value bucket) —
    ``pairs[0][0]`` is therefore never written (mapping-issues issue #33).
    """
    categorize = se_el("Categorize")
    # fallbackValue is required on se:FunctionType (SE 1.1.0). It is the
    # value returned for an uncategorisable input; the below-first-
    # threshold colour is the natural choice. Ignored on read (regenerated
    # deterministically, so the round trip stays stable).
    categorize.set("fallbackValue", format_color(pairs[0][1]))
    se_el("LookupValue", parent=categorize, text="Rasterdata")
    se_el("Value", parent=categorize, text=format_color(pairs[0][1]))
    for threshold, value in pairs[1:]:
        se_el("Threshold", parent=categorize, text=format_number(threshold))
        se_el("Value", parent=categorize, text=format_color(value))
    return categorize


def _build_color_map(color_map: Any) -> etree._Element:
    pairs = _validated_map_pairs(color_map, "colorMap")
    cm = se_el("ColorMap")
    cm.append(_build_categorize(pairs))
    return cm


def _build_shaded_relief(hill_shading: Any) -> etree._Element:
    if _g2(hill_shading, "sun", "sun") is not None:
        raise NotImplementedError(
            "HillShading.sun (azimuth/elevation) has no SE 1.1.0 "
            "se:ShadedRelief mapping — confirmed N/A by Annex B, a "
            "permanent gap (see mapping-issues issue #25)"
        )
    if _g2(hill_shading, "color_map", "colorMap") is not None:
        raise NotImplementedError(
            "HillShading.colorMap has no documented SE 1.1.0 mapping — "
            "Annex B is silent (see mapping-issues issue #25)"
        )
    if _g2(hill_shading, "opacity_map", "opacityMap") is not None:
        raise NotImplementedError(
            "HillShading.opacityMap has no documented SE 1.1.0 mapping — "
            "Annex B is silent (see mapping-issues issue #25)"
        )
    sr = se_el("ShadedRelief")
    factor = _g2(hill_shading, "factor", "factor")
    if factor is not None:
        se_el("ReliefFactor", parent=sr, text=format_number(factor))
    return sr


def _build_raster_symbolizer(sym: Any) -> etree._Element:
    rs = se_el("RasterSymbolizer")

    color_channels = _g(sym, "color_channels")
    single_channel = _g(sym, "single_channel")
    if color_channels is not None and single_channel is not None:
        raise NotImplementedError(
            "Symbolizer.colorChannels and Symbolizer.singleChannel cannot "
            "both be set — se:ChannelSelection is RGB *or* Gray, not both"
        )
    if color_channels is not None:
        rs.append(_build_channel_selection_rgb(color_channels))
    elif single_channel is not None:
        rs.append(_build_channel_selection_gray(single_channel))

    if _g(sym, "alpha_channel") is not None:
        raise NotImplementedError(
            "Symbolizer.alphaChannel has no SE 1.1.0 RasterSymbolizer "
            "construct — confirmed N/A by Annex B, a permanent gap (see "
            "mapping-issues issue #24)"
        )
    if _g(sym, "opacity_map") is not None:
        raise NotImplementedError(
            "Symbolizer.opacityMap has no clear SE 1.1.0 mapping — Annex "
            "B's own table is self-contradictory here (see mapping-issues "
            "issues #24/#28)"
        )

    color_map = _g(sym, "color_map")
    if color_map is not None:
        rs.append(_build_color_map(color_map))

    hill_shading = _g(sym, "hill_shading")
    if hill_shading is not None:
        rs.append(_build_shaded_relief(hill_shading))

    return rs


def _build_point_symbolizer(dot: Any) -> etree._Element:
    ps = se_el("PointSymbolizer")
    graphic = se_el("Graphic", parent=ps)
    mark = se_el("Mark", parent=graphic)
    se_el("WellKnownName", parent=mark, text="circle")

    color = _g(dot, "color")
    if color is not None:
        fill_el = se_el("Fill", parent=mark)
        svg_param(fill_el, "fill", format_color(color))

    size = _g(dot, "size")
    if size is not None:
        se_el("Size", parent=graphic, text=format_unit_value(size))

    position = _g(dot, "position")
    if position is not None:
        px, py = _unit_point_xy(position)
        if (px or 0) != 0 or (py or 0) != 0:
            raise NotImplementedError(
                "Non-zero Dot.position (offset) has no verified SLD/SE "
                "PointSymbolizer displacement mapping in this codec (see "
                "mapping-issues issue #15)"
            )
    return ps


def _percent_to_fraction(value: Any) -> float:
    if isinstance(value, dict) and set(value) == {"pc"}:
        return value["pc"] / 100
    raise NotImplementedError(
        f"ImageGraphic.hotSpot component {value!r} is not a percent (pc) "
        "unit value — only pc-unit hotSpot maps to se:AnchorPoint in this "
        "codec (see mapping-issues issue #35)"
    )


def _hot_spot_to_anchor_fraction(hot_spot: Any):
    if isinstance(hot_spot, (list, tuple)) and len(hot_spot) == 2:
        x_raw, y_raw = hot_spot
    elif isinstance(hot_spot, dict) and "x" in hot_spot and "y" in hot_spot:
        x_raw, y_raw = hot_spot["x"], hot_spot["y"]
    else:
        raise NotImplementedError(
            f"Unsupported ImageGraphic.hotSpot shape: {hot_spot!r}"
        )
    return _percent_to_fraction(x_raw), _percent_to_fraction(y_raw)


def _raise_if_image_out_of_scope(image_graphic: Any) -> None:
    for attr in ("tint", "blackTint", "alphaThreshold"):
        if _g(image_graphic, attr) is not None:
            raise NotImplementedError(
                f"ImageGraphic.{attr} has no SLD/SE mapping in this codec "
                "— Annex B is silent on it entirely (see mapping-issues "
                "issue #34)"
            )


def _build_image_symbolizer(image_graphic: Any) -> etree._Element:
    _raise_if_image_out_of_scope(image_graphic)

    resource = _g(image_graphic, "image")
    if resource is None:
        raise NotImplementedError("ImageGraphic.image (Resource) is required")
    uri = _g(resource, "uri")
    if uri is None:
        raise NotImplementedError(
            "Resource.path-only images (no uri) have no SLD/SE mapping in "
            "this codec — no local-file resolution (see mapping-issues "
            "issue #34)"
        )
    mime_type = _g(resource, "type")

    ps = se_el("PointSymbolizer")
    graphic = se_el("Graphic", parent=ps)
    ext_graphic = se_el("ExternalGraphic", parent=graphic)
    online_resource = se_el("OnlineResource", parent=ext_graphic)
    online_resource.set(f"{XLINK}type", "simple")
    online_resource.set(f"{XLINK}href", uri)
    if mime_type is not None:
        se_el("Format", parent=ext_graphic, text=mime_type)

    position = _g(image_graphic, "position")
    if position is not None:
        px, py = _unit_point_xy(position)
        if (px or 0) != 0 or (py or 0) != 0:
            raise NotImplementedError(
                "Non-zero ImageGraphic.position (offset) has no verified "
                "SLD/SE PointSymbolizer displacement mapping in this codec "
                "(see mapping-issues issue #15)"
            )

    hot_spot = _g(image_graphic, "hotSpot")
    if hot_spot is not None:
        fx, fy = _hot_spot_to_anchor_fraction(hot_spot)
        anchor_el = se_el("AnchorPoint", parent=ps)
        se_el("AnchorPointX", parent=anchor_el, text=format_number(fx))
        se_el("AnchorPointY", parent=anchor_el, text=format_number(fy))

    return ps


def _alignment_hv(alignment: Any):
    if isinstance(alignment, (list, tuple)) and len(alignment) == 2:
        return alignment[0], alignment[1]
    if isinstance(alignment, dict):
        h = alignment.get("hAlignment") or alignment.get("h_alignment")
        v = alignment.get("vAlignment") or alignment.get("v_alignment")
        return h, v
    h = _g(alignment, "h_alignment")
    v = _g(alignment, "v_alignment")
    return h, v


def _build_text_symbolizer(text_graphic: Any) -> etree._Element:
    ts = se_el("TextSymbolizer")

    text = _g(text_graphic, "text")
    label_el = se_el("Label", parent=ts)
    if isinstance(text, dict) and "property" in text:
        etree.SubElement(label_el, f"{OGC}PropertyName").text = text["property"]
    elif isinstance(text, str):
        label_el.text = text
    else:
        raise NotImplementedError(f"Unsupported Text.text shape: {text!r}")

    # Font color/opacity map to se:Fill, but SE's TextSymbolizerType fixes
    # the child order as Label, Font, LabelPlacement, Halo, Fill — so the
    # Fill element is built last, after the placement block below.
    font_color = None
    font_opacity = None
    font = _g(text_graphic, "font")
    if font is not None:
        if _g(font, "underline"):
            raise NotImplementedError(
                "Font.underline has no se:Font mapping in this codec (see "
                "mapping-issues issue #16)"
            )
        font_el = se_el("Font", parent=ts)
        face = _g(font, "face")
        size = _g(font, "size")
        bold = _g(font, "bold")
        italic = _g(font, "italic")
        if face is not None:
            svg_param(font_el, "font-family", str(face))
        if size is not None:
            svg_param(font_el, "font-size", format_unit_value(size))
        if bold is not None:
            svg_param(font_el, "font-weight", "bold" if bold else "normal")
        if italic is not None:
            svg_param(font_el, "font-style", "italic" if italic else "normal")

        font_color = _g(font, "color")
        font_opacity = _g(font, "opacity")

    alignment = _g(text_graphic, "alignment")
    position = _g(text_graphic, "position")
    px, py = _unit_point_xy(position) if position is not None else (None, None)
    has_displacement = (px or 0) != 0 or (py or 0) != 0

    if alignment is not None or has_displacement:
        placement_el = se_el("LabelPlacement", parent=ts)
        point_placement_el = se_el("PointPlacement", parent=placement_el)
        if alignment is not None:
            h, v = _alignment_hv(alignment)
            anchor_el = se_el("AnchorPoint", parent=point_placement_el)
            se_el("AnchorPointX", parent=anchor_el, text=_ANCHOR_X.get(h, "0.5"))
            se_el("AnchorPointY", parent=anchor_el, text=_ANCHOR_Y.get(v, "0.5"))
        if has_displacement:
            disp_el = se_el("Displacement", parent=point_placement_el)
            se_el("DisplacementX", parent=disp_el, text=format_unit_value(px or 0))
            se_el("DisplacementY", parent=disp_el, text=format_unit_value(py or 0))

    if font_color is not None or font_opacity is not None:
        fill_el = se_el("Fill", parent=ts)
        if font_color is not None:
            svg_param(fill_el, "fill", format_color(font_color))
        if font_opacity is not None:
            svg_param(fill_el, "fill-opacity", format_opacity(font_opacity))

    return ts


# ---------------------------------------------------------------------------
# Reader direction: SLD/SE symbolizer elements -> Symbolizer dict
# ---------------------------------------------------------------------------


def elements_to_symbolizer(sym_elements: List[etree._Element]) -> dict:
    """Convert the SLD/SE symbolizer elements of one ``se:Rule`` into a
    CartoSym ``symbolizer`` dict (CS-JSON shape, ready for ``Style.from_dict``).
    """
    result: dict = {}
    marker_elements: List[dict] = []
    label_elements: List[dict] = []

    for el in sym_elements:
        tag = local_name(el)
        if tag == "PolygonSymbolizer":
            fill_el = find_se_direct(el, "Fill")
            stroke_el = find_se_direct(el, "Stroke")
            if fill_el is not None:
                result["fill"] = _parse_fill_element(fill_el)
            if stroke_el is not None:
                result["stroke"] = _parse_stroke_element(stroke_el)
        elif tag == "LineSymbolizer":
            stroke_el = find_se_direct(el, "Stroke")
            if stroke_el is None:
                raise NotImplementedError(
                    "se:LineSymbolizer without se:Stroke is not supported"
                )
            result["stroke"] = _parse_stroke_element(stroke_el)
        elif tag == "PointSymbolizer":
            marker_elements.append(_parse_point_symbolizer(el))
        elif tag == "TextSymbolizer":
            label_elements.append(_parse_text_symbolizer(el))
        elif tag == "RasterSymbolizer":
            result.update(_parse_raster_symbolizer(el))
        else:
            raise NotImplementedError(f"Unsupported symbolizer element <{tag}>")

    if marker_elements:
        result["marker"] = {"elements": marker_elements}
    if label_elements:
        result["label"] = {"elements": label_elements}
    return result


def _parse_fill_element(fill_el: etree._Element) -> dict:
    if find_se_direct(fill_el, "GraphicFill") is not None:
        raise NotImplementedError(
            "se:Fill/se:GraphicFill (hatch/pattern fills) is out of scope "
            "for this codec (see mapping-issues issue #7)"
        )
    result: dict = {}
    color = get_svg_param(fill_el, "fill")
    opacity = get_svg_param(fill_el, "fill-opacity")
    if color is not None:
        result["color"] = parse_color(color)
    if opacity is not None:
        result["opacity"] = parse_opacity(opacity)
    return result


def _parse_stroke_element(stroke_el: etree._Element) -> dict:
    if (
        find_se_direct(stroke_el, "GraphicStroke") is not None
        or find_se_direct(stroke_el, "GraphicFill") is not None
    ):
        raise NotImplementedError(
            "se:Stroke graphic-fill/-stroke patterns are out of scope for "
            "this codec (see mapping-issues issue #8)"
        )
    result: dict = {}
    color = get_svg_param(stroke_el, "stroke")
    width = get_svg_param(stroke_el, "stroke-width")
    opacity = get_svg_param(stroke_el, "stroke-opacity")
    dasharray = get_svg_param(stroke_el, "stroke-dasharray")
    if color is not None:
        result["color"] = parse_color(color)
    if width is not None:
        result["width"] = parse_unit_value(width)
    if opacity is not None:
        result["opacity"] = parse_opacity(opacity)
    if dasharray is not None:
        result["dashPattern"] = {"pattern": [int(float(p)) for p in dasharray.split()]}
    return result


_UNSUPPORTED_RASTER_CHILDREN = (
    "OverlapBehavior",
    "ContrastEnhancement",
    "ImageOutline",
)


def _parse_selected_channel(channel_el: etree._Element) -> dict:
    if find_se_direct(channel_el, "ContrastEnhancement") is not None:
        raise NotImplementedError(
            "se:SelectedChannelType/se:ContrastEnhancement has no "
            "CartoSym mapping in this codec's scope (see mapping-issues "
            "issue #26)"
        )
    name_el = find_se_direct(channel_el, "SourceChannelName")
    if name_el is None or not (name_el.text and name_el.text.strip()):
        raise NotImplementedError(
            "se:SourceChannelName is required and must have text content"
        )
    return {"property": name_el.text.strip()}


def _parse_channel_selection(cs_el: etree._Element) -> dict:
    red = find_se_direct(cs_el, "RedChannel")
    green = find_se_direct(cs_el, "GreenChannel")
    blue = find_se_direct(cs_el, "BlueChannel")
    gray = find_se_direct(cs_el, "GrayChannel")
    if red is not None and green is not None and blue is not None:
        return {
            "colorChannels": [
                _parse_selected_channel(red),
                _parse_selected_channel(green),
                _parse_selected_channel(blue),
            ]
        }
    if gray is not None:
        return {"singleChannel": _parse_selected_channel(gray)}
    raise NotImplementedError(
        "se:ChannelSelection without a full RGB triple or a GrayChannel is "
        "not supported"
    )


def _parse_color_map(cm_el: etree._Element) -> list:
    categorize_el = find_se_direct(cm_el, "Categorize")
    if categorize_el is None:
        raise NotImplementedError(
            "se:ColorMap without se:Categorize (se:Interpolate, or the "
            "SLD 1.0.0-only se:ColorMapEntry form) is out of scope for "
            "this codec (see mapping-issues issue #3)"
        )
    children = [
        c
        for c in categorize_el
        if isinstance(c.tag, str) and local_name(c) != "LookupValue"
    ]
    if not children or local_name(children[0]) != "Value":
        raise NotImplementedError(
            "se:Categorize must start with a se:Value (the below-first-"
            "threshold color)"
        )
    values = [c.text for c in children if local_name(c) == "Value"]
    thresholds = [c.text for c in children if local_name(c) == "Threshold"]
    if len(thresholds) != len(values) - 1:
        raise NotImplementedError(
            "se:Categorize Value/Threshold count mismatch (expected "
            "exactly one more se:Value than se:Threshold)"
        )
    colors = [parse_color(v) for v in values]
    numeric_thresholds = [parse_number(t) for t in thresholds]

    # colorMap[0][0] has no XML representation (mapping-issues issue #33)
    # — synthesized as a duplicate of the first real threshold, a
    # deterministic, round-trip-stable, but explicitly arbitrary
    # convention.
    first_threshold = numeric_thresholds[0] if numeric_thresholds else 0
    pairs = [[first_threshold, colors[0]]]
    pairs.extend([t, c] for t, c in zip(numeric_thresholds, colors[1:]))
    return pairs


def _parse_shaded_relief(sr_el: etree._Element) -> dict:
    if find_se_direct(sr_el, "BrightnessOnly") is not None:
        raise NotImplementedError(
            "se:ShadedRelief/se:BrightnessOnly has no CartoSym HillShading "
            "mapping in this codec's scope (see mapping-issues issue #25)"
        )
    result: dict = {}
    factor_el = find_se_direct(sr_el, "ReliefFactor")
    if factor_el is not None and factor_el.text:
        result["factor"] = parse_number(factor_el.text)
    return result


def _parse_raster_symbolizer(el: etree._Element) -> dict:
    for tag in _UNSUPPORTED_RASTER_CHILDREN:
        if find_se_direct(el, tag) is not None:
            raise NotImplementedError(
                f"se:RasterSymbolizer/se:{tag} has no CartoSym mapping in "
                "this codec's scope (see mapping-issues issue #26)"
            )
    result: dict = {}
    cs_el = find_se_direct(el, "ChannelSelection")
    if cs_el is not None:
        result.update(_parse_channel_selection(cs_el))
    cm_el = find_se_direct(el, "ColorMap")
    if cm_el is not None:
        result["colorMap"] = _parse_color_map(cm_el)
    sr_el = find_se_direct(el, "ShadedRelief")
    if sr_el is not None:
        result["hillShading"] = _parse_shaded_relief(sr_el)
    return result


def _parse_point_symbolizer(ps_el: etree._Element) -> dict:
    graphic_el = find_se_direct(ps_el, "Graphic")
    if graphic_el is None:
        raise NotImplementedError(
            "se:PointSymbolizer without se:Graphic is not supported"
        )
    mark_el = find_se_direct(graphic_el, "Mark")
    if mark_el is not None:
        return _parse_mark(mark_el, graphic_el)
    ext_el = find_se_direct(graphic_el, "ExternalGraphic")
    if ext_el is not None:
        return _parse_external_graphic(ext_el, ps_el)
    raise NotImplementedError(
        "se:Graphic without se:Mark or se:ExternalGraphic is not supported"
    )


def _parse_mark(mark_el: etree._Element, graphic_el: etree._Element) -> dict:
    wkn_el = find_se_direct(mark_el, "WellKnownName")
    wkn = wkn_el.text if wkn_el is not None else None
    if wkn != "circle":
        raise NotImplementedError(
            f"se:Mark/se:WellKnownName {wkn!r} is out of scope for this "
            "codec (only 'circle' / Dot is supported)"
        )

    result: dict = {"type": "Dot", "position": {"x": 0, "y": 0}}
    fill_el = find_se_direct(mark_el, "Fill")
    if fill_el is not None:
        color = get_svg_param(fill_el, "fill")
        if color is not None:
            result["color"] = parse_color(color)
    size_el = find_se_direct(graphic_el, "Size")
    if size_el is not None:
        result["size"] = parse_unit_value(size_el.text)
    return result


def _parse_external_graphic(ext_el: etree._Element, ps_el: etree._Element) -> dict:
    online_resource_el = find_se_direct(ext_el, "OnlineResource")
    if online_resource_el is None:
        raise NotImplementedError(
            "se:ExternalGraphic without se:OnlineResource is not supported"
        )
    href = online_resource_el.get(f"{XLINK}href")
    if not href:
        raise NotImplementedError("se:OnlineResource must have a non-empty xlink:href")

    result: dict = {
        "type": "Image",
        "image": {"uri": href},
        "position": {"x": 0, "y": 0},
    }
    format_el = find_se_direct(ext_el, "Format")
    if format_el is not None and format_el.text:
        result["image"]["type"] = format_el.text.strip()

    anchor_el = find_se_direct(ps_el, "AnchorPoint")
    if anchor_el is not None:
        ax_el = find_se_direct(anchor_el, "AnchorPointX")
        ay_el = find_se_direct(anchor_el, "AnchorPointY")
        fx = _parsed_number_or(ax_el, 0.5)
        fy = _parsed_number_or(ay_el, 0.5)
        result["hotSpot"] = [
            {"pc": round(fx * 100)},
            {"pc": round(fy * 100)},
        ]
    return result


def _parsed_px_or_zero(el: Optional[etree._Element]) -> float:
    if el is None or el.text is None:
        return 0
    parsed = parse_unit_value(el.text)
    return parsed["px"] if parsed is not None else 0


def _parsed_number_or(el: Optional[etree._Element], default: float) -> float:
    if el is None or el.text is None:
        return default
    parsed = parse_number(el.text)
    return parsed if parsed is not None else default


def _parse_text_symbolizer(ts_el: etree._Element) -> dict:
    label_el = find_se_direct(ts_el, "Label")
    if label_el is None:
        raise NotImplementedError("se:TextSymbolizer without se:Label is not supported")
    prop_el = label_el.find(f"{OGC}PropertyName")
    if prop_el is not None:
        text: Any = {"property": prop_el.text}
    elif label_el.text and label_el.text.strip():
        text = label_el.text.strip()
    else:
        raise NotImplementedError(
            "se:Label with neither literal text nor ogc:PropertyName is "
            "not supported"
        )

    result: dict = {"type": "Text", "text": text, "position": {"x": 0, "y": 0}}

    font_el = find_se_direct(ts_el, "Font")
    font: dict = {}
    if font_el is not None:
        face = get_svg_param(font_el, "font-family")
        size = get_svg_param(font_el, "font-size")
        weight = get_svg_param(font_el, "font-weight")
        style = get_svg_param(font_el, "font-style")
        if face is not None:
            font["face"] = face
        if size is not None:
            font["size"] = parse_unit_value(size)
        if weight is not None:
            font["bold"] = weight == "bold"
        if style is not None:
            font["italic"] = style == "italic"

    fill_el = find_se_direct(ts_el, "Fill")
    if fill_el is not None:
        color = get_svg_param(fill_el, "fill")
        opacity = get_svg_param(fill_el, "fill-opacity")
        if color is not None:
            font["color"] = parse_color(color)
        if opacity is not None:
            font["opacity"] = parse_opacity(opacity)
    if font:
        result["font"] = font

    placement_el = find_se_direct(ts_el, "LabelPlacement")
    if placement_el is not None:
        point_placement_el = find_se_direct(placement_el, "PointPlacement")
        if point_placement_el is None:
            raise NotImplementedError(
                "se:LabelPlacement/se:LinePlacement is out of scope for "
                "this codec (see mapping-issues issue #18)"
            )
        anchor_el = find_se_direct(point_placement_el, "AnchorPoint")
        if anchor_el is not None:
            ax = find_se_direct(anchor_el, "AnchorPointX")
            ay = find_se_direct(anchor_el, "AnchorPointY")
            result["alignment"] = [
                _ANCHOR_X_TO_H.get(ax.text if ax is not None else "", "center"),
                _ANCHOR_Y_TO_V.get(ay.text if ay is not None else "", "middle"),
            ]
        disp_el = find_se_direct(point_placement_el, "Displacement")
        if disp_el is not None:
            dx = find_se_direct(disp_el, "DisplacementX")
            dy = find_se_direct(disp_el, "DisplacementY")
            result["position"] = {
                "x": _parsed_px_or_zero(dx),
                "y": _parsed_px_or_zero(dy),
            }

    return result
