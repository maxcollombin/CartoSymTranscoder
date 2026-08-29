"""
Pydantic models for CartoSym CSS/JSON structures.

This module contains the complete data model based on the OGC CartoSym specification,
implemented using Pydantic for validation, serialization, and documentation.
"""

from __future__ import annotations

from .base import AlterMixin, BaseCartoSymModel, CommentMixin
from .styles import Metadata, Style, StylingRule
from .symbolizers import (
    DashPattern,
    DotPattern,
    Fill,
    Hatch,
    Label,
    Marker,
    Stipple,
    Stroke,
    StrokeStyling,
    Symbolizer,
)
from .types import (  # Color types; Unit types; Angle types; Range types
    Angle,
    AngleUnit,
    Color,
    ColorComponent255,
    ColorNormalized,
    FlexibleAngle,
    FlexibleColor,
    FlexibleOpacity,
    FlexibleUnitValue,
    Percent,
    RGBColor,
    RGBColorNormalized,
    UnitType,
    UnitValue,
    WebColorName,
    ZeroToOne,
)

__all__ = [
    # Base types
    "BaseCartoSymModel",
    "CommentMixin",
    "AlterMixin",
    # Core models (Phase 2)
    "Style",
    "StylingRule",
    "Metadata",
    # Precise value types
    "WebColorName",
    "RGBColor",
    "RGBColorNormalized",
    "Color",
    "ColorNormalized",
    "FlexibleColor",
    "UnitType",
    "UnitValue",
    "FlexibleUnitValue",
    "AngleUnit",
    "Angle",
    "FlexibleAngle",
    "ZeroToOne",
    "Percent",
    "ColorComponent255",
    "FlexibleOpacity",
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
