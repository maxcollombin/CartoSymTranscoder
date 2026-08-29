"""
Symbolizer models for CartoSym.

Based on the JSON Schema definitions for symbolizer, fill, stroke, marker, label, etc.
"""

from typing import Any, Optional

from pydantic import ConfigDict, Field, field_validator, model_validator

from ..cql2.model import BoolExpression, NumericExpression
from .base import AlterMixin, BaseCartoSymModel, CommentMixin
from .types import FlexibleAngle, FlexibleColor, FlexibleOpacity, UnitValue


def parse_flexible_unit_value(v):
    # Accept dicts like {"px": 2.0}
    if isinstance(v, dict) and len(v) == 1:
        unit, value = next(iter(v.items()))
        return UnitValue(value=value, unit=unit)
    return v


def _coerce_numeric_str(v: str):
    """Convert a numeric string to int/float, leaving it as-is if it isn't one."""
    try:
        return int(v)
    except ValueError:
        try:
            return float(v)
        except ValueError:
            return v


class Fill(BaseCartoSymModel, AlterMixin):
    """
    Fill symbolizer for polygons and areas.

    Based on the 'fill' definition in the JSON schema.
    Can be either an expression reference or a fill object.
    """

    # For now, using precise types from Phase B
    color: FlexibleColor | None = Field(None, description="Fill color")
    opacity: FlexibleOpacity | None = Field(None, description="Fill opacity (0.0-1.0)")

    # Pattern fills
    pattern: dict[str, Any] | None = Field(
        None, description="Fill pattern graphic (temporary)"
    )
    hatch: Optional["Hatch"] = Field(None, description="Hatch pattern")
    dotpattern: Optional["DotPattern"] = Field(None, description="Dot pattern")
    stipple: Optional["Stipple"] = Field(None, description="Stipple pattern")


class Hatch(BaseCartoSymModel, AlterMixin):
    """
    Hatch pattern for fills.
    """

    width: UnitValue | str | float | None = Field(None, description="Hatch line width")
    angle: FlexibleAngle | None = Field(None, description="Hatch angle")
    distance: UnitValue | str | float | None = Field(
        None, description="Distance between hatch lines"
    )

    @field_validator("width", "distance", mode="before")
    def validate_unit_fields(cls, v):
        return parse_flexible_unit_value(v)


class DotPattern(BaseCartoSymModel, AlterMixin):
    """
    Dot pattern for fills.
    """

    distance: UnitValue | str | float | None = Field(
        None, description="Distance between dots"
    )

    @field_validator("distance", mode="before")
    def validate_distance(cls, v):
        return parse_flexible_unit_value(v)


class Stipple(BaseCartoSymModel, AlterMixin):
    """
    Stipple pattern for fills.
    """

    ratio: Any | None = Field(
        None, description="Stipple ratio (temporary - will be numericExpression)"
    )


class StrokeStyling(BaseCartoSymModel, AlterMixin):
    """
    Basic stroke styling properties.
    """

    color: FlexibleColor | None = Field(None, description="Stroke color")
    opacity: FlexibleOpacity | None = Field(
        None, description="Stroke opacity (0.0-1.0)"
    )
    width: UnitValue | str | float | None = Field(None, description="Stroke width")

    @field_validator("width", mode="before")
    def validate_width(cls, v):
        return parse_flexible_unit_value(v)


class DashPattern(BaseCartoSymModel):
    """
    Dash pattern for strokes.

    Can be either an array of integers or an indexed value.
    """

    # This will be a Union type later, for now simplified
    pattern: list[int] | None = Field(
        None, description="Dash pattern as array of integers"
    )
    index: int | None = Field(None, description="Index for indexed dash patterns")
    value: int | None = Field(None, description="Value for indexed dash patterns")


class Stroke(BaseCartoSymModel, AlterMixin):
    """
    Stroke symbolizer for lines and outlines.

    Based on the 'stroke' definition in the JSON schema.
    """

    # Basic stroke properties with precise types from Phase B
    color: FlexibleColor | None = Field(None, description="Stroke color")
    opacity: FlexibleOpacity | None = Field(
        None, description="Stroke opacity (0.0-1.0)"
    )
    width: UnitValue | str | float | None = Field(None, description="Stroke width")

    # Extended stroke properties
    casing: Optional["StrokeStyling"] = Field(None, description="Stroke casing")
    center_line: Optional["StrokeStyling"] = Field(
        None, alias="centerLine", description="Center line styling"
    )
    dash_pattern: Optional["DashPattern"] = Field(
        None, alias="dashPattern", description="Dash pattern"
    )
    pattern: dict[str, Any] | None = Field(
        None, description="Stroke pattern graphic (temporary)"
    )

    @field_validator("width", mode="before")
    def validate_width(cls, v):
        return parse_flexible_unit_value(v)


class Marker(BaseCartoSymModel):
    """
    Marker symbolizer for points.

    Based on the 'marker' definition (multiGraphic) in the JSON schema.
    """

    # Enhanced with proper structure
    alter: bool | None = Field(None, description="Alter behavior flag")
    position: Optional["UnitPoint"] = Field(None, description="Marker position")
    opacity: FlexibleOpacity | None = Field(None, description="Marker opacity")
    elements: Any | None = Field(
        None,
        description=(
            "Graphic elements in marker (list) or indexed override " "{index, value}"
        ),
    )

    @field_validator("elements", mode="before")
    def ensure_elements_list(cls, v):
        # Preserve indexed override form {"index": N, "value": graphic} as-is
        if isinstance(v, dict) and "index" in v and "value" in v:
            return v
        # Accept dicts like {"value": ...} without index and convert to list
        if isinstance(v, dict) and "value" in v:
            return [v["value"]]
        if isinstance(v, dict):
            # If dict is a single graphic, wrap in list
            return [v]
        if not isinstance(v, list) and v is not None:
            return [v]
        return v


class Label(BaseCartoSymModel):
    """
    Label symbolizer for text labels.

    Based on the 'label' definition in the JSON schema.
    Extends multiGraphic with label placement.
    """

    # Enhanced with proper structure
    alter: bool | None = Field(None, description="Alter behavior flag")
    position: Optional["UnitPoint"] = Field(None, description="Label position")
    opacity: FlexibleOpacity | None = Field(None, description="Label opacity")
    elements: list["Graphic"] | None = Field(
        None, description="Graphic elements in label"
    )
    placement: Optional["LabelPlacement"] = Field(
        None, description="Label placement configuration"
    )

    @field_validator("elements", mode="before")
    def ensure_elements_list(cls, v):
        if isinstance(v, dict) and "value" in v:
            return [v["value"]]
        if isinstance(v, dict):
            return [v]
        if not isinstance(v, list) and v is not None:
            return [v]
        return v


# Graphic system classes
class UnitPoint(BaseCartoSymModel):
    """Point with unit values: [x, y], {x: value, y: value}, or "x y"."""

    x: UnitValue | str | float
    y: UnitValue | str | float

    @model_validator(mode="before")
    @classmethod
    def parse_unit_point(cls, v):
        # Accept a bare "x y" string (as written by the CSCSS writer, e.g.
        # for `position`) or a [x, y] list, in addition to the normal
        # {x: ..., y: ...} dict form.
        if isinstance(v, str):
            parts = v.strip().split()
            if len(parts) == 2:
                return {
                    "x": _coerce_numeric_str(parts[0]),
                    "y": _coerce_numeric_str(parts[1]),
                }
        elif isinstance(v, (list, tuple)) and len(v) == 2:
            return {"x": v[0], "y": v[1]}
        return v


class Resource(BaseCartoSymModel):
    """Resource reference (file, URL, etc.)"""

    uri: str | None = Field(None, description="Resource URI")
    path: str | None = Field(None, description="File path")
    id: str | None = Field(None, description="Resource ID")
    type: str | None = Field(None, description="MIME type")
    ext: str | None = Field(None, description="File extension")


class Font(BaseCartoSymModel):
    """Font specification."""

    face: str | None = Field(None, description="Font family name")
    size: UnitValue | str | float | None = Field(None, description="Font size")
    bold: bool | None = Field(None, description="Bold weight")
    italic: bool | None = Field(None, description="Italic style")
    underline: bool | None = Field(None, description="Underline decoration")


class FontOutline(BaseCartoSymModel):
    """Font outline styling."""

    color: FlexibleColor | None = Field(None, description="Outline color")
    width: UnitValue | str | float | None = Field(None, description="Outline width")


class TextAlignment(BaseCartoSymModel):
    """Text alignment configuration."""

    h_alignment: str | None = Field(
        None,
        alias="hAlignment",
        description="Horizontal alignment: left, center, right",
    )
    v_alignment: str | None = Field(
        None, alias="vAlignment", description="Vertical alignment: top, middle, bottom"
    )
    alter: bool | None = Field(None, description="Alter behavior flag")


class LabelPlacement(BaseCartoSymModel):
    """Label placement configuration."""

    placement_type: str | None = Field(
        None, alias="type", description="Placement algorithm type"
    )
    # Additional placement properties would go here
    priority: NumericExpression | None = Field(None, description="Label priority")
    min_spacing: UnitValue | str | float | None = Field(
        None, alias="minSpacing", description="Minimum spacing"
    )
    max_spacing: UnitValue | str | float | None = Field(
        None, alias="maxSpacing", description="Maximum spacing"
    )


# Abstract base for graphics
class AbstractGraphic(BaseCartoSymModel, AlterMixin):
    """Base class for all graphic elements."""

    position: UnitPoint | None = Field(None, description="Graphic position")
    opacity: FlexibleOpacity | None = Field(None, description="Graphic opacity")

    @field_validator("position", mode="before")
    def validate_position(cls, v):
        if isinstance(v, list) and len(v) == 2:
            return UnitPoint(x=v[0], y=v[1])
        return v


class Graphic(AbstractGraphic):
    """Base graphic element - can be Image, Text, Shape, etc."""

    type: str | None = Field(None, description="Graphic type: Image, Text, Shape, etc.")
    model_config = ConfigDict(extra="allow")


class ImageGraphic(Graphic):
    """Image graphic element."""

    type: str = Field("Image", description="Graphic type")
    image: Resource = Field(..., description="Image resource")
    hot_spot: UnitPoint | None = Field(
        None, alias="hotSpot", description="Hot spot position"
    )
    tint: FlexibleColor | None = Field(None, description="Tint color")
    black_tint: FlexibleColor | None = Field(
        None, alias="blackTint", description="Black tint color"
    )
    alpha_threshold: FlexibleOpacity | None = Field(
        None, alias="alphaThreshold", description="Alpha threshold"
    )
    model_config = ConfigDict(extra="allow")


class TextGraphic(Graphic):
    """Text graphic element."""

    type: str = Field("Text", description="Graphic type")
    text: str | Any = Field(
        ..., description="Text content or expression"
    )  # Should be characterExpression
    font: Font | None = Field(None, description="Font specification")
    alignment: TextAlignment | None = Field(None, description="Text alignment")


# Shape classes (simplified)
class ShapeGraphic(Graphic):
    """Base class for shape graphics."""

    type: str = Field("Shape", description="Graphic type")
    size: UnitValue | str | float | None = Field(None, description="Shape size")
    outline: Stroke | None = Field(None, description="Shape outline")


class CircleGraphic(ShapeGraphic):
    """Circle shape graphic."""

    radius: UnitValue | str | float = Field(..., description="Circle radius")


class RectangleGraphic(ShapeGraphic):
    """Rectangle shape graphic."""

    width: UnitValue | str | float = Field(..., description="Rectangle width")
    height: UnitValue | str | float = Field(..., description="Rectangle height")


class ColorMap(BaseCartoSymModel):
    """Color mapping for raster/coverage data."""

    # Simplified for now - would contain color ramp definitions
    colors: list[FlexibleColor] | None = Field(None, description="Color ramp")
    values: list[NumericExpression] | None = Field(None, description="Value stops")


class OpacityMap(BaseCartoSymModel):
    """Opacity mapping for raster/coverage data."""

    # Simplified for now - would contain opacity ramp definitions
    opacities: list[FlexibleOpacity] | None = Field(None, description="Opacity ramp")
    values: list[NumericExpression] | None = Field(None, description="Value stops")


class HillShading(BaseCartoSymModel):
    """Hill shading configuration for elevation data."""

    azimuth: FlexibleAngle | None = Field(None, description="Light source azimuth")
    elevation: FlexibleAngle | None = Field(None, description="Light source elevation")
    factor: NumericExpression | None = Field(None, description="Shading factor")


# Enhanced Symbolizer with all JSON schema properties
class SymbolizerEnhanced(BaseCartoSymModel, CommentMixin):
    """
    Enhanced symbolizer with all properties from JSON schema.
    """

    # Basic properties
    visibility: BoolExpression | None = Field(None, description="Visibility condition")
    opacity: FlexibleOpacity | None = Field(None, description="Overall opacity")
    z_order: NumericExpression | None = Field(
        None, alias="zOrder", description="Z-order for layering"
    )

    # Vector symbolizers
    fill: Fill | None = Field(None, description="Fill symbolizer")
    stroke: Stroke | None = Field(None, description="Stroke symbolizer")
    marker: Optional["Marker"] = Field(None, description="Marker symbolizer")
    label: Optional["Label"] = Field(None, description="Label symbolizer")

    # Raster/coverage symbolizers
    color_channels: FlexibleColor | None = Field(
        None, alias="colorChannels", description="RGB color channels"
    )
    alpha_channel: FlexibleOpacity | None = Field(
        None, alias="alphaChannel", description="Alpha channel"
    )
    single_channel: FlexibleOpacity | None = Field(
        None, alias="singleChannel", description="Single channel value"
    )
    color_map: ColorMap | None = Field(
        None, alias="colorMap", description="Color mapping"
    )
    opacity_map: OpacityMap | None = Field(
        None, alias="opacityMap", description="Opacity mapping"
    )

    # Elevation symbolizers
    hill_shading: HillShading | None = Field(
        None, alias="hillShading", description="Hill shading"
    )


class Symbolizer(BaseCartoSymModel, CommentMixin):
    """
    Main symbolizer containing all rendering properties.

    Based on the 'symbolizer' definition in the JSON schema.
    """

    # Core properties
    visibility: Any | None = Field(
        None, description="Visibility expression (temporary)"
    )
    opacity: Any | None = Field(
        None, description="Opacity value (temporary - will be zeroToOne)"
    )
    z_order: Any | None = Field(
        None,
        alias="zOrder",
        description="Z-order value (temporary - will be numericExpression)",
    )

    # Vector symbolizers
    fill: Fill | None = Field(None, description="Fill symbolizer")
    stroke: Stroke | None = Field(None, description="Stroke symbolizer")
    marker: Marker | None = Field(None, description="Marker symbolizer")
    label: Label | None = Field(None, description="Label symbolizer")

    # Raster symbolizers
    color_channels: Any | None = Field(
        None,
        alias="colorChannels",
        description="Color channels (temporary - will be color0to1)",
    )
    alpha_channel: Any | None = Field(
        None,
        alias="alphaChannel",
        description="Alpha channel (temporary - will be zeroToOne)",
    )
    single_channel: Any | None = Field(
        None,
        alias="singleChannel",
        description="Single channel (temporary - will be zeroToOne)",
    )
    color_map: Any | None = Field(
        None, alias="colorMap", description="Color map (temporary)"
    )
    opacity_map: Any | None = Field(
        None, alias="opacityMap", description="Opacity map (temporary)"
    )
    hill_shading: Any | None = Field(
        None, alias="hillShading", description="Hill shading (temporary)"
    )


# Enable forward references for nested types
Fill.model_rebuild()
Stroke.model_rebuild()
StrokeStyling.model_rebuild()
Marker.model_rebuild()
Label.model_rebuild()
AbstractGraphic.model_rebuild()
ImageGraphic.model_rebuild()
TextGraphic.model_rebuild()
ShapeGraphic.model_rebuild()
