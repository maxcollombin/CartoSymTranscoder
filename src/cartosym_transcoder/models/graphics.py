"""
Classes graphiques basées sur le JSON Schema CartoSym.
Gère les éléments visuels comme les graphiques, textes, images, etc.
"""

from typing import Any, List, Optional, Union, Dict, Literal
from pydantic import BaseModel, Field
from .base import BaseCartoSymModel, AlterMixin
from .types import UnitValue, FlexibleColor, FlexibleOpacity
from .expressions import Expression, BoolExpression, NumericExpression
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .symbolizers import Stroke


# Unit Point (position with units)
class UnitPoint(BaseCartoSymModel):
    """Point with unit values: [x, y] or {x: value, y: value}"""
    x: UnitValue
    y: UnitValue


class UnitPoint3D(BaseCartoSymModel):
    """3D point with unit values: [x, y, z] or {x: value, y: value, z: value}"""
    x: UnitValue
    y: UnitValue  
    z: UnitValue


# Scale definitions
class Scale2D(BaseCartoSymModel, AlterMixin):
    """2D scaling: [x, y] or {x: value, y: value}"""
    x: NumericExpression
    y: NumericExpression


class Scale3D(BaseCartoSymModel, AlterMixin):
    """3D scaling: [x, y, z] or {x: value, y: value, z: value}"""
    x: NumericExpression
    y: NumericExpression
    z: NumericExpression


class Orientation3D(BaseCartoSymModel, AlterMixin):
    """3D orientation: quaternion [x, y, z, w] or {yaw, pitch, roll}"""
    # Can be either quaternion or Euler angles
    yaw: Optional[NumericExpression] = None
    pitch: Optional[NumericExpression] = None
    roll: Optional[NumericExpression] = None
    # Or quaternion components
    x: Optional[NumericExpression] = None
    y: Optional[NumericExpression] = None
    z: Optional[NumericExpression] = None
    w: Optional[NumericExpression] = None


# Abstract base classes
class AbstractGraphic(BaseCartoSymModel, AlterMixin):
    """Base class for all graphic elements."""
    position: Optional[UnitPoint] = None
    opacity: Optional[FlexibleOpacity] = None


# Graphic elements
class Graphic(AbstractGraphic):
    """A single graphic element (shape, image, text, etc.)"""
    # This will be subclassed by specific graphic types
    pass


class GraphicArray(BaseCartoSymModel):
    """Array of graphic elements."""
    # Can be array of graphics or indexed access
    elements: Optional[List[Graphic]] = None
    index: Optional[int] = None
    value: Optional[Graphic] = None


class MultiGraphic(AbstractGraphic):
    """Multiple graphic elements container."""
    elements: GraphicArray


# Shape definitions (abstractShape from schema)
class AbstractShape(Graphic):
    """Base class for geometric shapes."""
    size: Optional[Union[UnitValue, Scale2D]] = None
    outline: Optional['Stroke'] = None  # Forward reference


# Specific shapes
class Circle(AbstractShape):
    """Circle shape."""
    radius: UnitValue


class Rectangle(AbstractShape):
    """Rectangle shape."""
    width: UnitValue
    height: UnitValue


class Ellipse(AbstractShape):
    """Ellipse shape."""
    width: UnitValue
    height: UnitValue


class Polygon(AbstractShape):
    """Polygon shape."""
    points: List[UnitPoint]


# Arc definition (abstractArc from schema)
class AbstractArc(AbstractShape):
    """Base class for arc shapes."""
    start_angle: NumericExpression = Field(alias="startAngle")
    delta_angle: NumericExpression = Field(alias="deltaAngle")


class Arc(AbstractArc):
    """Arc shape."""
    radius: UnitValue


# Text elements
class Font(BaseCartoSymModel):
    """Font specification."""
    face: Optional[str] = None  # Font family
    size: Optional[UnitValue] = None
    bold: Optional[bool] = None
    italic: Optional[bool] = None
    underline: Optional[bool] = None


class FontOutline(BaseCartoSymModel):
    """Font outline styling."""
    color: Optional[FlexibleColor] = None
    width: Optional[UnitValue] = None


class Text(Graphic):
    """Text graphic element."""
    text: Union[str, Expression]  # Can be literal or expression
    font: Optional[Font] = None
    color: Optional[FlexibleColor] = None
    outline: Optional[FontOutline] = None
    alignment: Optional[str] = None  # "left", "center", "right", etc.


# Image elements
class Resource(BaseCartoSymModel):
    """Resource reference (file, URL, etc.)"""
    uri: Optional[str] = None
    path: Optional[str] = None
    id: Optional[str] = None
    type: Optional[str] = None  # MIME type
    ext: Optional[str] = None   # File extension


class Image(Graphic):
    """Image graphic element."""
    image: Resource
    hot_spot: Optional[UnitPoint] = Field(None, alias="hotSpot")
    tint: Optional[FlexibleColor] = None
    black_tint: Optional[FlexibleColor] = Field(None, alias="blackTint")
    alpha_threshold: Optional[NumericExpression] = Field(None, alias="alphaThreshold")


# Label placement
class LabelPlacement(BaseCartoSymModel):
    """Label placement configuration."""
    # This would contain placement-specific properties
    # Simplified for now
    placement_type: Optional[str] = Field(None, alias="type")


# Update forward references  
AbstractShape.model_rebuild()


__all__ = [
    'UnitPoint', 'UnitPoint3D', 'Scale2D', 'Scale3D', 'Orientation3D',
    'AbstractGraphic', 'Graphic', 'GraphicArray', 'MultiGraphic',
    'AbstractShape', 'Circle', 'Rectangle', 'Ellipse', 'Polygon',
    'AbstractArc', 'Arc',
    'Font', 'FontOutline', 'Text',
    'Resource', 'Image',
    'LabelPlacement'
]
