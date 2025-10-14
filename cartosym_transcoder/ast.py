"""
Abstract Syntax Tree (AST) classes for CartoSym CSS.

This module contains the data structures representing parsed CartoSym CSS.
"""

from dataclasses import dataclass
from typing import List, Optional, Any, Dict
from enum import Enum


@dataclass
class StyleSheet:
    """Root node of a CartoSym CSS stylesheet."""
    metadata: List['Metadata'] = None
    styling_rules: Optional['StylingRuleList'] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = []


@dataclass
class Metadata:
    """Metadata entry in a stylesheet."""
    key: str
    value: str


@dataclass
class StylingRuleList:
    """Collection of styling rules."""
    rules: List['StylingRule']
    
    def __post_init__(self):
        if self.rules is None:
            self.rules = []


@dataclass
class StylingRule:
    """Individual styling rule with selector and properties."""
    name: Optional[str] = None
    selector: Optional['Selector'] = None
    symbolizer: Optional['Symbolizer'] = None
    nested_rules: List['StylingRule'] = None
    
    def __post_init__(self):
        if self.nested_rules is None:
            self.nested_rules = []


@dataclass
class Selector:
    """Selector for filtering features."""
    expression: Optional['Expression'] = None


@dataclass
class Symbolizer:
    """Symbolizer defining how features are rendered."""
    # Basic properties
    visibility: Optional[bool] = None
    opacity: Optional[float] = None
    z_order: Optional[int] = None
    
    # Vector symbolizers
    fill: Optional['Fill'] = None
    stroke: Optional['Stroke'] = None
    marker: Optional['Marker'] = None
    label: Optional['Label'] = None
    
    # Coverage/Raster properties (Phase B Priority 1)
    single_channel: Optional[str] = None  # e.g., "elevation"
    singleChannel: Optional[str] = None   # camelCase alternative
    color_channels: Optional[Any] = None  # RGB color channels
    colorChannels: Optional[Any] = None   # camelCase alternative
    alpha_channel: Optional[Any] = None   # Alpha channel
    alphaChannel: Optional[Any] = None    # camelCase alternative
    color_map: Optional[Any] = None       # Color mapping
    colorMap: Optional[Any] = None        # camelCase alternative
    opacity_map: Optional[Any] = None     # Opacity mapping
    opacityMap: Optional[Any] = None      # camelCase alternative
    hill_shading: Optional[Dict[str, Any]] = None  # Hill shading config
    hillShading: Optional[Dict[str, Any]] = None   # camelCase alternative


@dataclass
class Expression:
    """Base class for expressions."""
    pass


@dataclass
class PropertyAssignment:
    """Assignment of a value to a property."""
    property_name: str
    value: Any


@dataclass
class PropertyAssignmentList:
    """Collection of property assignments."""
    assignments: List[PropertyAssignment]
    
    def __post_init__(self):
        if self.assignments is None:
            self.assignments = []


@dataclass
class Fill:
    """Fill styling properties."""
    color: Optional[str] = None
    opacity: Optional[float] = None


@dataclass
class Stroke:
    """Stroke styling properties."""
    color: Optional[str] = None
    width: Optional[float] = None
    opacity: Optional[float] = None


@dataclass
class Marker:
    """Marker styling properties."""
    pass


@dataclass
class Label:
    """Label styling properties."""
    pass
