"""
Pydantic models for CartoSym CSS/JSON structures.

This module contains the complete data model based on the OGC CartoSym specification,
implemented using Pydantic for validation, serialization, and documentation.
"""

from .base import BaseCartoSymModel, CommentMixin, AlterMixin
from .styles import Style, StylingRule, Metadata
from .types import (
    # Color types
    WebColorName, RGBColor, RGBColorNormalized, Color, ColorNormalized,
    FlexibleColor,
    # Unit types
    UnitType, UnitValue, UnitValueFlexible, FlexibleUnitValue,
    # Angle types
    AngleUnit, Angle, FlexibleAngle,
    # Range types
    ZeroToOne, Percent, ColorComponent255, FlexibleOpacity
)
from .symbolizers import (
    Symbolizer, Fill, Stroke, Marker, Label,
    StrokeStyling, DashPattern, Hatch, DotPattern, Stipple
)

# Import order will be important due to forward references
# from .expressions import *     # Phase 4

__all__ = [
    # Base types
    "BaseCartoSymModel",
    "CommentMixin", 
    "AlterMixin",
    
    # Core models (Phase 2)
    "Style", 
    "StylingRule", 
    "Metadata",
    
    # Phase B precise types
    "WebColorName", "RGBColor", "RGBColorNormalized", "Color", "ColorNormalized",
    "FlexibleColor",
    "UnitType", "UnitValue", "UnitValueFlexible", "FlexibleUnitValue",
    "AngleUnit", "Angle", "FlexibleAngle", 
    "ZeroToOne", "Percent", "ColorComponent255", "FlexibleOpacity",
    
    # Symbolizer models (Phase 3)
    "Symbolizer",
    "Fill",
    "Stroke", 
    "Marker",
    "Label",
    "StrokeStyling",
    "DashPattern",
    "Hatch",
    "DotPattern", 
    "Stipple",
]
