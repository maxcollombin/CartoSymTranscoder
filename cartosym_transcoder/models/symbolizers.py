"""
Symbolizer models for CartoSym.

Based on the JSON Schema definitions for symbolizer, fill, stroke, marker, label, etc.
"""

from typing import Optional, Union, List, Any, Dict
from pydantic import Field
from .base import BaseCartoSymModel, CommentMixin, AlterMixin
from .types import FlexibleColor, FlexibleUnitValue, FlexibleOpacity, FlexibleAngle
from .expressions import BoolExpression, NumericExpression


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
    width: Optional[FlexibleUnitValue] = Field(None, description="Hatch line width")
    angle: Optional[FlexibleAngle] = Field(None, description="Hatch angle")
    distance: Optional[FlexibleUnitValue] = Field(None, description="Distance between hatch lines")


class DotPattern(BaseCartoSymModel, AlterMixin):
    """
    Dot pattern for fills.
    """
    distance: Optional[FlexibleUnitValue] = Field(None, description="Distance between dots")


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
    width: Optional[FlexibleUnitValue] = Field(None, description="Stroke width")


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
    width: Optional[FlexibleUnitValue] = Field(None, description="Stroke width")
    
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


class Marker(BaseCartoSymModel):
    """
    Marker symbolizer for points.
    
    Based on the 'marker' definition (multiGraphic) in the JSON schema.
    """
    # Enhanced with proper structure
    alter: Optional[bool] = Field(None, description="Alter behavior flag")
    position: Optional['UnitPoint'] = Field(None, description="Marker position")
    opacity: Optional[FlexibleOpacity] = Field(None, description="Marker opacity")
    elements: Optional[List['Graphic']] = Field(None, description="Graphic elements in marker")


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


# Graphic system classes
class UnitPoint(BaseCartoSymModel):
    """Point with unit values: [x, y] or {x: value, y: value}"""
    x: FlexibleUnitValue
    y: FlexibleUnitValue


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
    size: Optional[FlexibleUnitValue] = Field(None, description="Font size")
    bold: Optional[bool] = Field(None, description="Bold weight")
    italic: Optional[bool] = Field(None, description="Italic style")
    underline: Optional[bool] = Field(None, description="Underline decoration")


class FontOutline(BaseCartoSymModel):
    """Font outline styling."""
    color: Optional[FlexibleColor] = Field(None, description="Outline color")
    width: Optional[FlexibleUnitValue] = Field(None, description="Outline width")


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
    min_spacing: Optional[FlexibleUnitValue] = Field(None, alias="minSpacing", description="Minimum spacing")
    max_spacing: Optional[FlexibleUnitValue] = Field(None, alias="maxSpacing", description="Maximum spacing")


# Abstract base for graphics
class AbstractGraphic(BaseCartoSymModel, AlterMixin):
    """Base class for all graphic elements."""
    position: Optional[UnitPoint] = Field(None, description="Graphic position")
    opacity: Optional[FlexibleOpacity] = Field(None, description="Graphic opacity")


class Graphic(AbstractGraphic):
    """Base graphic element - can be Image, Text, Shape, etc."""
    type: Optional[str] = Field(None, description="Graphic type: Image, Text, Shape, etc.")


class ImageGraphic(Graphic):
    """Image graphic element."""
    type: str = Field("Image", description="Graphic type")
    image: Resource = Field(..., description="Image resource")
    hot_spot: Optional[UnitPoint] = Field(None, alias="hotSpot", description="Hot spot position")
    tint: Optional[FlexibleColor] = Field(None, description="Tint color")
    black_tint: Optional[FlexibleColor] = Field(None, alias="blackTint", description="Black tint color")
    alpha_threshold: Optional[FlexibleOpacity] = Field(None, alias="alphaThreshold", description="Alpha threshold")


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
    size: Optional[FlexibleUnitValue] = Field(None, description="Shape size")
    outline: Optional[Stroke] = Field(None, description="Shape outline")


class CircleGraphic(ShapeGraphic):
    """Circle shape graphic."""
    radius: FlexibleUnitValue = Field(..., description="Circle radius")


class RectangleGraphic(ShapeGraphic):
    """Rectangle shape graphic."""
    width: FlexibleUnitValue = Field(..., description="Rectangle width")
    height: FlexibleUnitValue = Field(..., description="Rectangle height")


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
