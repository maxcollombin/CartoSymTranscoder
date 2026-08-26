"""
Symbolizer models for CartoSym.

Based on the JSON Schema definitions for symbolizer, fill, stroke, marker, label, etc.
"""

from typing import Optional, Union, List, Any, Dict
from pydantic import Field, field_validator, ConfigDict
from .base import BaseCartoSymModel, CommentMixin, AlterMixin
from .types import FlexibleColor, FlexibleOpacity, FlexibleAngle, UnitValue
from .expressions import BoolExpression, NumericExpression

def parse_flexible_unit_value(v):
    # Accept dicts like {"px": 2.0}
    if isinstance(v, dict) and len(v) == 1:
        unit, value = next(iter(v.items()))
        return UnitValue(value=value, unit=unit)
    return v

class Fill(BaseCartoSymModel, AlterMixin):
    """
    Fill symbolizer for polygons and areas.
    
    Based on the 'fill' definition in the JSON schema.
    Can be either an expression reference or a fill object.
    """
    # For now, using precise types from Phase B
    color: Optional[FlexibleColor] = Field(None, description="Fill color")
    opacity: Optional[FlexibleOpacity] = Field(None, description="Fill opacity (0.0-1.0)")
    
    # Pattern fills
    pattern: Optional[Dict[str, Any]] = Field(None, description="Fill pattern graphic (temporary)")
    hatch: Optional['Hatch'] = Field(None, description="Hatch pattern")
    dotpattern: Optional['DotPattern'] = Field(None, description="Dot pattern")
    stipple: Optional['Stipple'] = Field(None, description="Stipple pattern")


class Hatch(BaseCartoSymModel, AlterMixin):
    """
    Hatch pattern for fills.
    """
    width: Optional[Union[UnitValue, str, float]] = Field(None, description="Hatch line width")
    angle: Optional[FlexibleAngle] = Field(None, description="Hatch angle")
    distance: Optional[Union[UnitValue, str, float]] = Field(None, description="Distance between hatch lines")

    @field_validator('width', 'distance', mode='before')
    def validate_unit_fields(cls, v):
        return parse_flexible_unit_value(v)


class DotPattern(BaseCartoSymModel, AlterMixin):
    """
    Dot pattern for fills.
    """
    distance: Optional[Union[UnitValue, str, float]] = Field(None, description="Distance between dots")

    @field_validator('distance', mode='before')
    def validate_distance(cls, v):
        return parse_flexible_unit_value(v)


class Stipple(BaseCartoSymModel, AlterMixin):
    """
    Stipple pattern for fills.
    """
    ratio: Optional[Any] = Field(None, description="Stipple ratio (temporary - will be numericExpression)")


class StrokeStyling(BaseCartoSymModel, AlterMixin):
    """
    Basic stroke styling properties.
    """
    color: Optional[FlexibleColor] = Field(None, description="Stroke color")
    opacity: Optional[FlexibleOpacity] = Field(None, description="Stroke opacity (0.0-1.0)")
    width: Optional[Union[UnitValue, str, float]] = Field(None, description="Stroke width")

    @field_validator('width', mode='before')
    def validate_width(cls, v):
        return parse_flexible_unit_value(v)


class DashPattern(BaseCartoSymModel):
    """
    Dash pattern for strokes.
    
    Can be either an array of integers or an indexed value.
    """
    # This will be a Union type later, for now simplified
    pattern: Optional[List[int]] = Field(None, description="Dash pattern as array of integers")
    index: Optional[int] = Field(None, description="Index for indexed dash patterns")
    value: Optional[int] = Field(None, description="Value for indexed dash patterns")


class Stroke(BaseCartoSymModel, AlterMixin):
    """
    Stroke symbolizer for lines and outlines.
    
    Based on the 'stroke' definition in the JSON schema.
    """
    # Basic stroke properties with precise types from Phase B
    color: Optional[FlexibleColor] = Field(None, description="Stroke color")
    opacity: Optional[FlexibleOpacity] = Field(None, description="Stroke opacity (0.0-1.0)")
    width: Optional[Union[UnitValue, str, float]] = Field(None, description="Stroke width")
    
    # Extended stroke properties
    casing: Optional['StrokeStyling'] = Field(None, description="Stroke casing")
    center_line: Optional['StrokeStyling'] = Field(
        None, 
        alias="centerLine", 
        description="Center line styling"
    )
    dash_pattern: Optional['DashPattern'] = Field(
        None,
        alias="dashPattern", 
        description="Dash pattern"
    )
    pattern: Optional[Dict[str, Any]] = Field(None, description="Stroke pattern graphic (temporary)")

    @field_validator('width', mode='before')
    def validate_width(cls, v):
        return parse_flexible_unit_value(v)


class Marker(BaseCartoSymModel):
    """
    Marker symbolizer for points.
    
    Based on the 'marker' definition (multiGraphic) in the JSON schema.
    """
    # Enhanced with proper structure
    alter: Optional[bool] = Field(None, description="Alter behavior flag")
    position: Optional['UnitPoint'] = Field(None, description="Marker position")
    opacity: Optional[FlexibleOpacity] = Field(None, description="Marker opacity")
    elements: Optional[Any] = Field(None, description="Graphic elements in marker (list) or indexed override {index, value}")

    @field_validator('elements', mode='before')
    def ensure_elements_list(cls, v):
        # Preserve indexed override form {"index": N, "value": graphic} as-is
        if isinstance(v, dict) and 'index' in v and 'value' in v:
            return v
        # Accept dicts like {"value": ...} without index and convert to list
        if isinstance(v, dict) and 'value' in v:
            return [v['value']]
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
    alter: Optional[bool] = Field(None, description="Alter behavior flag")
    position: Optional['UnitPoint'] = Field(None, description="Label position")
    opacity: Optional[FlexibleOpacity] = Field(None, description="Label opacity")
    elements: Optional[List['Graphic']] = Field(None, description="Graphic elements in label")
    placement: Optional['LabelPlacement'] = Field(None, description="Label placement configuration")

    @field_validator('elements', mode='before')
    def ensure_elements_list(cls, v):
        if isinstance(v, dict) and 'value' in v:
            return [v['value']]
        if isinstance(v, dict):
            return [v]
        if not isinstance(v, list) and v is not None:
            return [v]
        return v


# Graphic system classes
class UnitPoint(BaseCartoSymModel):
    """Point with unit values: [x, y] or {x: value, y: value}"""
    x: Union[UnitValue, str, float]
    y: Union[UnitValue, str, float]

    @classmethod
    def from_string(cls, v):
        # Accept string like '0 0' or '20 0'
        if isinstance(v, str):
            parts = v.strip().split()
            if len(parts) == 2:
                try:
                    x = float(parts[0]) if '.' in parts[0] else int(parts[0])
                    y = float(parts[1]) if '.' in parts[1] else int(parts[1])
                    return cls(x=x, y=y)
                except Exception:
                    pass
        return v

    @field_validator('x', 'y', mode='before')
    def parse_unit_point(cls, v, info):
        # Accept list like [x, y]
        if isinstance(v, list) and len(v) == 2:
            return v[info.field_index]
        # Accept string like '0 0' for position
        if isinstance(v, str):
            parts = v.strip().split()
            if len(parts) == 2:
                try:
                    return float(parts[info.field_index]) if '.' in parts[info.field_index] else int(parts[info.field_index])
                except Exception:
                    return v
        return v


class Resource(BaseCartoSymModel):
    """Resource reference (file, URL, etc.)"""
    uri: Optional[str] = Field(None, description="Resource URI")
    path: Optional[str] = Field(None, description="File path")
    id: Optional[str] = Field(None, description="Resource ID")
    type: Optional[str] = Field(None, description="MIME type")
    ext: Optional[str] = Field(None, description="File extension")


class Font(BaseCartoSymModel):
    """Font specification."""
    face: Optional[str] = Field(None, description="Font family name")
    size: Optional[Union[UnitValue, str, float]] = Field(None, description="Font size")
    bold: Optional[bool] = Field(None, description="Bold weight")
    italic: Optional[bool] = Field(None, description="Italic style")
    underline: Optional[bool] = Field(None, description="Underline decoration")


class FontOutline(BaseCartoSymModel):
    """Font outline styling."""
    color: Optional[FlexibleColor] = Field(None, description="Outline color")
    width: Optional[Union[UnitValue, str, float]] = Field(None, description="Outline width")


class TextAlignment(BaseCartoSymModel):
    """Text alignment configuration."""
    h_alignment: Optional[str] = Field(None, alias="hAlignment", description="Horizontal alignment: left, center, right")
    v_alignment: Optional[str] = Field(None, alias="vAlignment", description="Vertical alignment: top, middle, bottom")
    alter: Optional[bool] = Field(None, description="Alter behavior flag")


class LabelPlacement(BaseCartoSymModel):
    """Label placement configuration."""
    placement_type: Optional[str] = Field(None, alias="type", description="Placement algorithm type")
    # Additional placement properties would go here
    priority: Optional[NumericExpression] = Field(None, description="Label priority")
    min_spacing: Optional[Union[UnitValue, str, float]] = Field(None, alias="minSpacing", description="Minimum spacing")
    max_spacing: Optional[Union[UnitValue, str, float]] = Field(None, alias="maxSpacing", description="Maximum spacing")


# Abstract base for graphics
class AbstractGraphic(BaseCartoSymModel, AlterMixin):
    """Base class for all graphic elements."""
    position: Optional[UnitPoint] = Field(None, description="Graphic position")
    opacity: Optional[FlexibleOpacity] = Field(None, description="Graphic opacity")

    @field_validator('position', mode='before')
    def validate_position(cls, v):
        if isinstance(v, list) and len(v) == 2:
            return UnitPoint(x=v[0], y=v[1])
        return v


class Graphic(AbstractGraphic):
    """Base graphic element - can be Image, Text, Shape, etc."""
    type: Optional[str] = Field(None, description="Graphic type: Image, Text, Shape, etc.")
    model_config = ConfigDict(extra="allow")


class ImageGraphic(Graphic):
    """Image graphic element."""
    type: str = Field("Image", description="Graphic type")
    image: Resource = Field(..., description="Image resource")
    hot_spot: Optional[UnitPoint] = Field(None, alias="hotSpot", description="Hot spot position")
    tint: Optional[FlexibleColor] = Field(None, description="Tint color")
    black_tint: Optional[FlexibleColor] = Field(None, alias="blackTint", description="Black tint color")
    alpha_threshold: Optional[FlexibleOpacity] = Field(None, alias="alphaThreshold", description="Alpha threshold")
    model_config = ConfigDict(extra="allow")


class TextGraphic(Graphic):
    """Text graphic element."""
    type: str = Field("Text", description="Graphic type")
    text: Union[str, Any] = Field(..., description="Text content or expression")  # Should be characterExpression
    font: Optional[Font] = Field(None, description="Font specification")
    alignment: Optional[TextAlignment] = Field(None, description="Text alignment")


# Shape classes (simplified)
class ShapeGraphic(Graphic):
    """Base class for shape graphics."""
    type: str = Field("Shape", description="Graphic type")
    size: Optional[Union[UnitValue, str, float]] = Field(None, description="Shape size")
    outline: Optional[Stroke] = Field(None, description="Shape outline")


class CircleGraphic(ShapeGraphic):
    """Circle shape graphic."""
    radius: Union[UnitValue, str, float] = Field(..., description="Circle radius")


class RectangleGraphic(ShapeGraphic):
    """Rectangle shape graphic."""
    width: Union[UnitValue, str, float] = Field(..., description="Rectangle width")
    height: Union[UnitValue, str, float] = Field(..., description="Rectangle height")


class ColorMap(BaseCartoSymModel):
    """Color mapping for raster/coverage data."""
    # Simplified for now - would contain color ramp definitions
    colors: Optional[List[FlexibleColor]] = Field(None, description="Color ramp")
    values: Optional[List[NumericExpression]] = Field(None, description="Value stops")


class OpacityMap(BaseCartoSymModel):
    """Opacity mapping for raster/coverage data."""
    # Simplified for now - would contain opacity ramp definitions
    opacities: Optional[List[FlexibleOpacity]] = Field(None, description="Opacity ramp") 
    values: Optional[List[NumericExpression]] = Field(None, description="Value stops")


class HillShading(BaseCartoSymModel):
    """Hill shading configuration for elevation data."""
    azimuth: Optional[FlexibleAngle] = Field(None, description="Light source azimuth")
    elevation: Optional[FlexibleAngle] = Field(None, description="Light source elevation")
    factor: Optional[NumericExpression] = Field(None, description="Shading factor")


# Enhanced Symbolizer with all JSON schema properties
class SymbolizerEnhanced(BaseCartoSymModel, CommentMixin):
    """
    Enhanced symbolizer with all properties from JSON schema.
    """
    # Basic properties
    visibility: Optional[BoolExpression] = Field(None, description="Visibility condition")
    opacity: Optional[FlexibleOpacity] = Field(None, description="Overall opacity")
    z_order: Optional[NumericExpression] = Field(None, alias="zOrder", description="Z-order for layering")
    
    # Vector symbolizers
    fill: Optional[Fill] = Field(None, description="Fill symbolizer")
    stroke: Optional[Stroke] = Field(None, description="Stroke symbolizer")
    marker: Optional['Marker'] = Field(None, description="Marker symbolizer")
    label: Optional['Label'] = Field(None, description="Label symbolizer")
    
    # Raster/coverage symbolizers  
    color_channels: Optional[FlexibleColor] = Field(None, alias="colorChannels", description="RGB color channels")
    alpha_channel: Optional[FlexibleOpacity] = Field(None, alias="alphaChannel", description="Alpha channel")
    single_channel: Optional[FlexibleOpacity] = Field(None, alias="singleChannel", description="Single channel value")
    color_map: Optional[ColorMap] = Field(None, alias="colorMap", description="Color mapping")
    opacity_map: Optional[OpacityMap] = Field(None, alias="opacityMap", description="Opacity mapping")
    
    # Elevation symbolizers
    hill_shading: Optional[HillShading] = Field(None, alias="hillShading", description="Hill shading")


class Symbolizer(BaseCartoSymModel, CommentMixin):
    """
    Main symbolizer containing all rendering properties.
    
    Based on the 'symbolizer' definition in the JSON schema.
    """
    # Core properties
    visibility: Optional[Any] = Field(None, description="Visibility expression (temporary)")
    opacity: Optional[Any] = Field(None, description="Opacity value (temporary - will be zeroToOne)")
    z_order: Optional[Any] = Field(
        None, 
        alias="zOrder", 
        description="Z-order value (temporary - will be numericExpression)"
    )
    
    # Vector symbolizers
    fill: Optional[Fill] = Field(None, description="Fill symbolizer")
    stroke: Optional[Stroke] = Field(None, description="Stroke symbolizer") 
    marker: Optional[Marker] = Field(None, description="Marker symbolizer")
    label: Optional[Label] = Field(None, description="Label symbolizer")
    
    # Raster symbolizers
    color_channels: Optional[Any] = Field(
        None,
        alias="colorChannels", 
        description="Color channels (temporary - will be color0to1)"
    )
    alpha_channel: Optional[Any] = Field(
        None,
        alias="alphaChannel",
        description="Alpha channel (temporary - will be zeroToOne)"
    )
    single_channel: Optional[Any] = Field(
        None,
        alias="singleChannel", 
        description="Single channel (temporary - will be zeroToOne)"
    )
    color_map: Optional[Any] = Field(
        None,
        alias="colorMap",
        description="Color map (temporary)"
    )
    opacity_map: Optional[Any] = Field(
        None,
        alias="opacityMap",
        description="Opacity map (temporary)"
    )
    hill_shading: Optional[Any] = Field(
        None,
        alias="hillShading",
        description="Hill shading (temporary)"
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
