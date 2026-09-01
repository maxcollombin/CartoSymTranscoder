"""Pydantic models for CartoSym CSS/JSON structures.

This module contains the complete data model based on the OGC CartoSym specification,
implemented using Pydantic for validation, serialization, and documentation.
"""

from __future__ import annotations

from .base import AlterMixin, BaseCartoSymModel, CommentMixin
from .styles import Metadata, Style, StylingRule
from .symbolizers import (
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
    FlexibleSize,
    FlexibleUnitValue,
    Percent,
    RGBColor,
    RGBColorNormalized,
    UnitType,
    UnitValue,
    WebColorName,
    ZeroToOne,
)
from .value_expressions import (
    CaseExpression,
    CoalesceExpression,
    InterpolateExpression,
    MatchExpression,
    PropertyRef,
    StepExpression,
    ValueExpression,
)

__all__ = [
    # Base types
    "BaseCartoSymModel",
    "CommentMixin",
    "AlterMixin",
    # Core models
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
    "FlexibleSize",
    "AngleUnit",
    "Angle",
    "FlexibleAngle",
    "ZeroToOne",
    "Percent",
    "ColorComponent255",
    "FlexibleOpacity",
    # Value expressions (data-driven property values)
    "ValueExpression",
    "PropertyRef",
    "CaseExpression",
    "MatchExpression",
    "StepExpression",
    "InterpolateExpression",
    "CoalesceExpression",
    # Symbolizer models
    "Symbolizer",
    "Fill",
    "Stroke",
    "Marker",
    "Label",
    "StrokeStyling",
    "Hatch",
    "DotPattern",
    "Stipple",
]
