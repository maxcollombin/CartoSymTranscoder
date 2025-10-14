"""
Complete Expression System for CartoSym CSS and JSON Schema
Supports complex expressions, conditions, function calls, and JSON Schema expression types.
"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, List, Optional, Union, Dict, Literal
from pydantic import BaseModel, Field, field_validator
from .base import BaseCartoSymModel


class BaseExpression(BaseCartoSymModel):
    """Base class for all expressions with minimal required fields."""
    pass


class ExpressionType(str, Enum):
    """Types of expressions in CartoSym CSS."""
    IDENTIFIER = "identifier"
    CONSTANT = "constant"
    STRING = "string"
    MEMBER_ACCESS = "member_access"
    FUNCTION_CALL = "function_call"
    BINARY_OP = "binary_operation"
    UNARY_OP = "unary_operation"
    CONDITIONAL = "conditional"
    ARRAY = "array"
    INSTANCE = "instance"
    # Additional types for Phase C
    NUMERIC = "numeric"
    OBJECT = "object"


class BinaryOperator(str, Enum):
    """Binary operators."""
    # Arithmetic
    ADD = "+"
    SUBTRACT = "-"
    MULTIPLY = "*"
    DIVIDE = "/"
    INTEGER_DIVIDE = "//"
    MODULO = "%"
    POWER = "**"
    
    # Relational
    EQUAL = "="
    NOT_EQUAL = "!="
    LESS_THAN = "<"
    LESS_EQUAL = "<="
    GREATER_THAN = ">"
    GREATER_EQUAL = ">="
    IN = "in"
    NOT_IN = "not in"
    IS = "is"
    IS_NOT = "is not"
    LIKE = "like"
    NOT_LIKE = "not like"
    
    # Logical
    AND = "and"
    OR = "or"
    
    # Special
    BETWEEN = "between"
    NOT_BETWEEN = "not between"


class UnaryOperator(str, Enum):
    """Unary operators."""
    PLUS = "+"
    MINUS = "-"
    NOT = "not"


class Expression(BaseModel, ABC):
    """Base class for all expressions."""
    type: ExpressionType
    
    class Config:
        use_enum_values = True


class IdentifierExpression(Expression):
    """Simple identifier like 'dataLayer' or 'FunctionCode'."""
    type: ExpressionType = ExpressionType.IDENTIFIER
    name: str


class ConstantExpression(Expression):
    """Constant value (number, boolean, etc.)."""
    type: ExpressionType = ExpressionType.CONSTANT
    value: Union[int, float, bool, str]
    unit: Optional[str] = None  # For values like "2.0 px"


class StringExpression(Expression):
    """String literal."""
    type: ExpressionType = ExpressionType.STRING
    value: str


class MemberAccessExpression(Expression):
    """Member access like 'dataLayer.type' or 'viz.timeInterval.start.date'."""
    type: ExpressionType = ExpressionType.MEMBER_ACCESS
    object: 'Expression'
    member: str


class FunctionCallExpression(Expression):
    """Function call like 'Text(...)' or 'Image(...)'."""
    type: ExpressionType = ExpressionType.FUNCTION_CALL
    function_name: str
    arguments: List['Expression']


class BinaryOperationExpression(Expression):
    """Binary operation like 'a + b' or 'x = y'."""
    type: ExpressionType = ExpressionType.BINARY_OP
    left: 'Expression'
    operator: BinaryOperator
    right: 'Expression'


class UnaryOperationExpression(Expression):
    """Unary operation like '-x' or 'not y'."""
    type: ExpressionType = ExpressionType.UNARY_OP
    operator: UnaryOperator
    operand: 'Expression'


class ConditionalExpression(Expression):
    """Ternary conditional like 'condition ? true_value : false_value'."""
    type: ExpressionType = ExpressionType.CONDITIONAL
    condition: 'Expression'
    true_value: 'Expression'
    false_value: 'Expression'


class ArrayExpression(Expression):
    """Array literal like '[a, b, c]'."""
    type: ExpressionType = ExpressionType.ARRAY
    elements: List['Expression']


class PropertyAssignment(BaseModel):
    """Property assignment within an instance."""
    property: str
    value: 'Expression'


class InstanceExpression(Expression):
    """Instance creation like '{color: red; opacity: 0.5}' or 'Text(...)'."""
    type: ExpressionType = ExpressionType.INSTANCE
    class_name: Optional[str] = None  # For Text(...) vs {...}
    properties: List[PropertyAssignment] = []


# Update forward references
MemberAccessExpression.model_rebuild()
FunctionCallExpression.model_rebuild()
BinaryOperationExpression.model_rebuild()
UnaryOperationExpression.model_rebuild()
ConditionalExpression.model_rebuild()
ArrayExpression.model_rebuild()
PropertyAssignment.model_rebuild()


# Selector with expressions
class Selector(BaseModel):
    """Enhanced selector that can include expressions."""
    name: Optional[str] = None  # Simple name like "Landuse"
    conditions: List[Expression] = []  # Conditions like [dataLayer.type = vector]
    
    def is_simple(self) -> bool:
        """Check if this is a simple selector (name only)."""
        return self.name is not None and len(self.conditions) == 0


# Enhanced styling rule
class StylingRuleExpression(BaseModel):
    """Styling rule that can contain expressions and nested rules."""
    selectors: List[Selector] = []
    properties: Dict[str, Expression] = {}  # property_name -> expression
    nested_rules: List['StylingRuleExpression'] = []


# Update forward reference
StylingRuleExpression.model_rebuild()


# =====================================================
# JSON Schema Expression Types (from CartoSym schema)
# =====================================================

# Boolean Expressions (JSON Schema: boolExpression)
class BoolExpression(BaseExpression):
    """Base class for boolean expressions from JSON schema."""
    type: Optional[str] = None


class AndOrExpression(BoolExpression):
    """Logical AND/OR expression: {"op": "and|or", "args": [...]}"""
    op: Literal["and", "or"]
    args: List[BoolExpression] = Field(min_length=2)


class NotExpression(BoolExpression):
    """Logical NOT expression: {"op": "not", "args": [...]}"""
    op: Literal["not"] = "not"
    args: List[BoolExpression] = Field(min_length=1, max_length=1)


# Numeric Expressions (JSON Schema: numericExpression)
class NumericExpression(BaseExpression):
    """Base class for numeric expressions from JSON schema."""
    type: Optional[str] = None


class ArithmeticExpression(NumericExpression):
    """Arithmetic expression: {"op": "+|-|*|/|%|**", "args": [...]}"""
    op: Literal["+", "-", "*", "/", "%", "**"]
    args: List[NumericExpression] = Field(min_length=2)


class ArithmeticOperands(NumericExpression):
    """Advanced arithmetic operands with multiple operations (Phase B Priority 4)."""
    operations: List[ArithmeticExpression]
    
    @property
    def result_type(self) -> str:
        return "numeric"


class ScalarOperands(Expression):
    """Scalar operands for various operations on single values."""
    op: str
    args: List[Union[NumericExpression, 'ScalarExpression']] = Field(min_length=1)


class BitwiseLogical(NumericExpression):
    """Bitwise logical: {"op": "&|||^", "args": [...]}"""
    op: Literal["&", "|", "^"]
    args: List[NumericExpression] = Field(min_length=2)


class BitwiseShift(NumericExpression):
    """Bitwise shift: {"op": "<<|>>", "args": [...]}"""
    op: Literal["<<", ">>"]
    args: List[NumericExpression] = Field(min_length=2)


class BitwiseNot(NumericExpression):
    """Bitwise NOT: {"op": "~", "args": [...]}"""
    op: Literal["~"] = "~"
    args: List[NumericExpression] = Field(min_length=1, max_length=1)


# Comparison Predicates
class ComparisonPredicate(BoolExpression):
    """Base class for comparison predicates."""
    pass


class BinaryComparisonPredicate(ComparisonPredicate):
    """Binary comparison: {"op": "=|!=|<|<=|>|>=", "args": [...]}"""
    op: Literal["=", "!=", "<", "<=", ">", ">="]
    args: List[Union[NumericExpression, 'ScalarExpression']] = Field(min_length=2, max_length=2)


class IsNullPredicate(ComparisonPredicate):
    """Null check: {"op": "isNull", "args": [...]}"""
    op: Literal["isNull"] = "isNull"
    args: List['ScalarExpression'] = Field(min_length=1, max_length=1)


class IsInListPredicate(ComparisonPredicate):
    """In list check: {"op": "in", "args": [...]}"""
    op: Literal["in"] = "in"
    args: List[Union['ScalarExpression', List['ScalarExpression']]] = Field(min_length=2)


class IsBetweenPredicate(ComparisonPredicate):
    """Between check: {"op": "between", "args": [...]}"""
    op: Literal["between"] = "between"
    args: List['ScalarExpression'] = Field(min_length=3, max_length=3)  # [value, min, max]


class IsLikePredicate(ComparisonPredicate):
    """Pattern matching: {"op": "like|ilike", "args": [...]}"""
    op: Literal["like", "ilike"]
    args: List['ScalarExpression'] = Field(min_length=2, max_length=3)  # [value, pattern, escape?]


# Property and System References
class PropertyRef(Expression):
    """Property reference: {"property": "propertyName"}"""
    property: str


class SystemIdentifier(Expression):
    """System identifier: {"sysId": "identifier"}"""
    sysId: str


# Scalar Expressions
class ScalarExpression(Expression):
    """Base class for scalar expressions."""
    pass


class ScalarLiteral(ScalarExpression):
    """Scalar literal value."""
    value: Union[str, int, float, bool]


# Enhanced Function Calls (JSON Schema format)
class FunctionCallJSON(Expression):
    """JSON Schema function call: {"op": "functionName", "args": [...]}"""
    op: str  # Function name
    args: List[Expression] = Field(default_factory=list)


# Enhanced Conditional Expressions (JSON Schema format)
class ConditionalExpressionJSON(Expression):
    """JSON Schema conditional: {"op": "if", "args": [condition, trueValue, falseValue]}"""
    op: Literal["if"] = "if"
    args: List[Expression] = Field(min_length=3, max_length=3)


# Temporal Expressions (for date/time)
class TemporalExpression(Expression):
    """Base class for temporal expressions (Phase B Priority 4)."""
    type: ExpressionType = ExpressionType.FUNCTION_CALL  # Default type for temporal functions


class DateInstant(TemporalExpression):
    """Date instant: {"op": "date", "args": [year, month, day]}"""
    op: Literal["date"] = "date"
    args: List[Union[int, float]] = Field(min_length=3, max_length=3)  # [year, month, day] - use simple types


class TimestampInstant(TemporalExpression):
    """Timestamp instant: {"op": "timestamp", "args": [year, month, day, hour, minute, second]}"""
    op: Literal["timestamp"] = "timestamp"
    args: List[NumericExpression] = Field(min_length=6, max_length=7)  # [y,m,d,h,min,s,ms?]


class DateString(TemporalExpression):
    """Date from string: {"op": "dateString", "args": [dateString, format?]}"""
    op: Literal["dateString"] = "dateString"
    args: List[Expression] = Field(min_length=1, max_length=2)


class TimestampString(TemporalExpression):
    """Timestamp from string: {"op": "timestampString", "args": [timestampString, format?]}"""
    op: Literal["timestampString"] = "timestampString"
    args: List[Expression] = Field(min_length=1, max_length=2)


class InstantInstance(TemporalExpression):
    """Generic instant instance for temporal operations."""
    instant_type: Literal["date", "timestamp"]
    value: Union[str, int, float]


class IntervalInstance(TemporalExpression):
    """Time interval instance: {"start": instant, "end": instant}"""
    start: TemporalExpression
    end: TemporalExpression


class IntervalArray(TemporalExpression):
    """Array of time intervals."""
    intervals: List[IntervalInstance]


class TemporalInstantExpression(TemporalExpression):
    """Complex temporal instant with operations."""
    op: str
    args: List[TemporalExpression]


class TemporalOperands(Expression):
    """Temporal operands for arithmetic operations on time values."""
    op: Literal["add", "subtract", "duration"]
    args: List[TemporalExpression] = Field(min_length=2)


class TemporalPredicate(BoolExpression):
    """Temporal predicate for time-based comparisons."""
    op: Literal["before", "after", "during", "meets", "overlaps"]
    args: List[TemporalExpression]


# Spatial Expressions (for geometry)
class SpatialPredicate(BoolExpression):
    """Spatial predicate for geometry-based comparisons (Phase B Priority 3)."""
    op: Literal["intersects", "contains", "within", "touches", "crosses", "disjoint", "overlaps", "equals"]
    args: List['GeometryExpression']


class GeometryExpression(Expression):
    """Base class for geometry expressions (Phase B Priority 3)."""
    type: ExpressionType = ExpressionType.INSTANCE  # Default type for geometry instances


class GeometryBuffer(GeometryExpression):
    """Geometry buffer operation: {"op": "buffer", "args": [geometry, distance]}"""
    op: Literal["buffer"] = "buffer"
    args: List[Expression] = Field(min_length=2, max_length=2)  # [geometry, distance]


class GeometryManipulationUnary(GeometryExpression):
    """Unary geometry operations: {"op": "centroid|envelope|convexHull|boundary", "args": [geometry]}"""
    op: Literal["centroid", "envelope", "convexHull", "boundary"]
    args: List[GeometryExpression] = Field(min_length=1, max_length=1)


class GeometryManipulationBinary(GeometryExpression):
    """Binary geometry operations: {"op": "union|intersection|difference|symDifference", "args": [geom1, geom2]}"""
    op: Literal["union", "intersection", "difference", "symDifference"]
    args: List[GeometryExpression] = Field(min_length=2, max_length=2)


class SpatialInstance(GeometryExpression):
    """Spatial geometry instance with coordinates."""
    geometry_type: Literal["Point", "LineString", "Polygon", "MultiPoint", "MultiLineString", "MultiPolygon"]
    coordinates: List[Any]  # Coordinate arrays, structure depends on geometry type
    crs: Optional[str] = Field(None, description="Coordinate Reference System")


class AzimuthElevation(Expression):
    """Azimuth and elevation for directional calculations."""
    azimuth: Union[float, NumericExpression]
    elevation: Union[float, NumericExpression]


# =====================================================
# Color and Graphics Expressions (Phase B Priority 4)
# =====================================================

class ColorExpression(Expression):
    """Base class for color expressions."""
    type: ExpressionType = ExpressionType.CONSTANT  # Default type for color constants


class Color0to1(ColorExpression):
    """Color with components in 0-1 range: {"r": 0.5, "g": 0.3, "b": 0.8, "a"?: 1.0}"""
    r: Union[float, int] = Field(ge=0.0, le=1.0)
    g: Union[float, int] = Field(ge=0.0, le=1.0)  
    b: Union[float, int] = Field(ge=0.0, le=1.0)
    a: Optional[Union[float, int]] = Field(None, ge=0.0, le=1.0)


class ColorComponent0to255(ColorExpression):
    """Color with components in 0-255 range: {"r": 128, "g": 76, "b": 204, "a"?: 255}"""
    r: Union[int, NumericExpression] = Field(ge=0, le=255)
    g: Union[int, NumericExpression] = Field(ge=0, le=255)
    b: Union[int, NumericExpression] = Field(ge=0, le=255)
    a: Optional[Union[int, NumericExpression]] = Field(None, ge=0, le=255)


class HexNumber(ColorExpression):
    """Hexadecimal color: {"hex": "#FF5733"}"""
    hex: str = Field(pattern=r'^#[0-9A-Fa-f]{6}([0-9A-Fa-f]{2})?$')


class ZeroToOne(NumericExpression):
    """Numeric value constrained to 0-1 range."""
    value: Union[float, NumericExpression] = Field(ge=0.0, le=1.0)


class Shape(Expression):
    """Shape definition for graphics."""
    shape_type: Literal["circle", "square", "triangle", "star", "cross", "diamond"]
    size: Optional[Union[float, NumericExpression]] = None
    properties: Optional[Dict[str, Any]] = None


# =====================================================
# Alignment and Layout Expressions (Phase B Priority 4)
# =====================================================

class HAlignment(Expression):
    """Horizontal alignment: left, center, right."""
    value: Literal["left", "center", "right"]


class VAlignment(Expression):
    """Vertical alignment: top, middle, bottom."""
    value: Literal["top", "middle", "bottom"]


class Horizontal(Expression):
    """Horizontal positioning/direction."""
    value: Union[float, str, NumericExpression]


class Vertical(Expression):
    """Vertical positioning/direction."""
    value: Union[float, str, NumericExpression]


class Dot(Expression):
    """Dot notation access for nested properties."""
    path: List[str] = Field(min_length=2)  # e.g., ['dataLayer', 'type']
    
    def to_string(self) -> str:
        return '.'.join(self.path)


# Array Expressions
class ArrayPredicate(BoolExpression):
    """Array-based predicates."""
    op: str
    args: List[Expression]


# =====================================================
# Character Expression Types (Phase B Priority 2)
# =====================================================


class AnyExpressionWrapper(Expression):
    """Wrapper for AnyExpression with proper Pydantic handling."""
    type: ExpressionType = ExpressionType.IDENTIFIER
    expression: Any = Field(..., description="Wrapped expression of any type")
    
    def get_expression_type(self) -> str:
        """Get the actual type of the wrapped expression."""
        return type(self.expression).__name__

class CharacterExpression(Expression):
    """Base class for character/string expressions from JSON schema."""
    type: ExpressionType = ExpressionType.FUNCTION_CALL  # Default type for function-like expressions


class CaseiExpression(CharacterExpression):
    """Case-insensitive string expression: {"op": "casei", "args": [string]}"""
    op: Literal["casei"] = "casei"
    args: List[Expression] = Field(min_length=1, max_length=1)


class AccentiExpression(CharacterExpression):
    """Accent-insensitive string expression: {"op": "accenti", "args": [string]}"""
    op: Literal["accenti"] = "accenti"
    args: List[Expression] = Field(min_length=1, max_length=1)


class ConcatenateExpression(CharacterExpression):
    """String concatenation: {"op": "concatenate", "args": [str1, str2, ...]}"""
    op: Literal["concatenate"] = "concatenate"
    args: List[Expression] = Field(min_length=2)


class FormatExpression(CharacterExpression):
    """String formatting: {"op": "format", "args": [format_string, ...values]}"""
    op: Literal["format"] = "format"
    args: List[Expression] = Field(min_length=1)


class SubstituteExpression(CharacterExpression):
    """String substitution: {"op": "substitute", "args": [string, pattern, replacement]}"""
    op: Literal["substitute"] = "substitute"
    args: List[Expression] = Field(min_length=3, max_length=3)


class LowerUpperCaseExpression(CharacterExpression):
    """Case conversion: {"op": "upper|lower", "args": [string]}"""
    op: Literal["upper", "lower"]
    args: List[Expression] = Field(min_length=1, max_length=1)


class PatternExpression(CharacterExpression):
    """Pattern matching expression for advanced text operations."""
    type: ExpressionType = ExpressionType.STRING
    pattern: str
    flags: Optional[List[str]] = None


class TextOpPredicate(BoolExpression):
    """Text operation predicates for string comparisons."""
    op: Literal["matches", "startsWith", "endsWith", "contains"]
    args: List[CharacterExpression] = Field(min_length=2, max_length=2)


# Update forward references
BinaryComparisonPredicate.model_rebuild()
IsNullPredicate.model_rebuild()
IsInListPredicate.model_rebuild()
IsBetweenPredicate.model_rebuild()
IsLikePredicate.model_rebuild()
TemporalPredicate.model_rebuild()
SpatialPredicate.model_rebuild()


__all__ = [
    # Original CSCSS expressions
    'Expression', 'ExpressionType', 'BinaryOperator', 'UnaryOperator',
    'IdentifierExpression', 'ConstantExpression', 'StringExpression',
    'MemberAccessExpression', 'FunctionCallExpression', 'BinaryOperationExpression',
    'UnaryOperationExpression', 'ConditionalExpression', 'ArrayExpression',
    'PropertyAssignment', 'InstanceExpression', 'Selector', 'StylingRuleExpression',
    
    # JSON Schema expressions
    'BoolExpression', 'AndOrExpression', 'NotExpression',
    'NumericExpression', 'ArithmeticExpression', 'BitwiseLogical', 'BitwiseShift', 'BitwiseNot',
    'ComparisonPredicate', 'BinaryComparisonPredicate', 'IsNullPredicate', 'IsInListPredicate',
    'IsBetweenPredicate', 'IsLikePredicate',
    'PropertyRef', 'SystemIdentifier', 'ScalarExpression', 'ScalarLiteral',
    'FunctionCallJSON', 'ConditionalExpressionJSON',
    
    # Character expressions (Phase B Priority 2)
    'CharacterExpression', 'CaseiExpression', 'AccentiExpression', 'ConcatenateExpression',
    'FormatExpression', 'SubstituteExpression', 'LowerUpperCaseExpression',
    'PatternExpression', 'TextOpPredicate',
    
    # Spatial expressions (Phase B Priority 3)
    'SpatialPredicate', 'GeometryExpression', 'GeometryBuffer', 'GeometryManipulationUnary',
    'GeometryManipulationBinary', 'SpatialInstance', 'AzimuthElevation',
    
    # Temporal expressions (Phase B Priority 4)
    'TemporalExpression', 'TemporalPredicate', 'DateInstant', 'TimestampInstant',
    'DateString', 'TimestampString', 'InstantInstance', 'IntervalInstance', 'IntervalArray',
    'TemporalInstantExpression', 'TemporalOperands',
    
    # Arithmetic expressions (Phase B Priority 4)
    'ArithmeticOperands', 'ScalarOperands',
    
    # Color and graphics expressions (Phase B Priority 4)
    'ColorExpression', 'Color0to1', 'ColorComponent0to255', 'HexNumber', 'ZeroToOne', 'Shape',
    
    # Alignment and layout expressions (Phase B Priority 4)
    'HAlignment', 'VAlignment', 'Horizontal', 'Vertical', 'Dot',
    
    # Miscellaneous
    'ArrayPredicate',
    
    # Polymorphic expressions (Phase C Priority 1)
    'AnyExpressionType', 'AnyExpressionWrapper', 'TypedArray', 'IdOrFnExpression',
    
    # Font expressions (Phase C Priority 2.1)
    'FontFamily', 'FontSize', 'FontWeight', 'FontStyle', 'FontExpression',
    
    # Geometry transformations (Phase C Priority 2.2)
    'TransformationMatrix', 'RotationTransform', 'ScaleTransform', 
    'TranslationTransform', 'GeometryTransformation',
    
    # DateTime calendar expressions (Phase C Priority 2.3)
    'CalendarField', 'DateTimeFormat', 'CalendarInterval', 'DateTimeCalendar',
    
    # Unit/Measure expressions (Phase C Priority 2.4)
    'UnitType', 'UnitConversion', 'MeasureExpression', 'UnitRange', 'ResponsiveUnit',
]


# =====================================================
# Polymorphic Expressions (Phase C Priority 1)
# =====================================================

class AnyExpressionWrapper(Expression):
    """
    Wrapper for AnyExpression with proper Pydantic handling.
    This allows storing any expression type polymorphically.
    """
    type: ExpressionType = ExpressionType.IDENTIFIER
    expression: Any = Field(..., description="Wrapped expression of any type")
    
    def get_expression_type(self) -> str:
        """Get the actual type of the wrapped expression."""
        return type(self.expression).__name__


### **1.3 TypedArray - Arrays typés avec validation**

class TypedArray(Expression):
    """
    Typed array with validation constraints.
    Provides strict validation of array elements with type checking.
    """
    type: ExpressionType = ExpressionType.ARRAY
    element_type: str = Field(..., description="Expected type of array elements")
    elements: List[Any] = Field(default_factory=list, description="Array elements")
    min_length: Optional[int] = Field(None, ge=0, description="Minimum array length")
    max_length: Optional[int] = Field(None, ge=0, description="Maximum array length")
    
    def validate_elements(self) -> bool:
        """Validate that all elements match the expected type."""
        if not self.elements:
            return True
            
        for element in self.elements:
            if self.element_type and not isinstance(element, eval(self.element_type)):
                return False
        return True
    
    def add_element(self, element: Any) -> bool:
        """Add an element with type validation."""
        if self.max_length and len(self.elements) >= self.max_length:
            return False
            
        if self.element_type and not isinstance(element, eval(self.element_type)):
            return False
            
        self.elements.append(element)
        return True


### **1.4 IdOrFnExpression - Union identifier/fonction**

class IdOrFnExpressionWrapper(Expression):
    """
    Wrapper for identifier or function call expressions.
    Provides flexible syntax for identifiants vs function calls.
    """
    type: ExpressionType = ExpressionType.IDENTIFIER
    expression: Union[IdentifierExpression, FunctionCallExpression] = Field(..., description="Identifier or function call")
    
    def is_function_call(self) -> bool:
        """Check if this is a function call rather than identifier."""
        return isinstance(self.expression, FunctionCallExpression)
    
    def get_name(self) -> str:
        """Get the name (identifier name or function name)."""
        if isinstance(self.expression, IdentifierExpression):
            return self.expression.name
        elif isinstance(self.expression, FunctionCallExpression):
            return self.expression.function_name
        return "unknown"


# Define type aliases at the end of the file for proper forward references
AnyExpressionType = Union[
    # Basic expressions
    IdentifierExpression,
    ConstantExpression, 
    StringExpression,
    MemberAccessExpression,
    
    # Function and operation expressions
    FunctionCallExpression,
    BinaryOperationExpression,
    UnaryOperationExpression,
    ConditionalExpression,
    
    # Collection expressions
    ArrayExpression,
    InstanceExpression,
    
    # JSON Schema expressions
    BoolExpression,
    NumericExpression,
    ArithmeticExpression,
    ComparisonPredicate,
    
    # Character expressions
    CharacterExpression,
    ConcatenateExpression,
    FormatExpression,
    
    # Spatial expressions
    SpatialPredicate,
    GeometryExpression,
    
    # Temporal expressions
    TemporalExpression,
    DateInstant,
    
    # Color expressions
    ColorExpression,
    Color0to1,
    HexNumber,
]

# Convenience type aliases
IdOrFnExpression = Union[IdentifierExpression, FunctionCallExpression]


# =====================================================
# Phase C Priority 2.1 - Font Expressions
# =====================================================

class FontFamily(Expression):
    """
    Font family specification for text rendering.
    Supports system fonts, web fonts, and fallback chains.
    """
    type: ExpressionType = ExpressionType.STRING
    family_name: str = Field(..., description="Primary font family name")
    fallback_families: List[str] = Field(default_factory=list, description="Fallback font families")
    font_type: Optional[str] = Field(None, description="Font type: system, web, embedded")
    
    def get_css_font_family(self) -> str:
        """Get CSS-compatible font-family string."""
        all_families = [self.family_name] + self.fallback_families
        return ", ".join(f'"{family}"' if " " in family else family for family in all_families)


class FontSize(Expression):
    """
    Font size specification with unit support.
    Supports absolute (px, pt, pc) and relative (em, rem, %) units.
    """
    type: ExpressionType = ExpressionType.NUMERIC
    value: float = Field(..., ge=0, description="Font size value")
    unit: str = Field("px", description="Size unit: px, pt, em, rem, %")
    
    def to_pixels(self, base_size: float = 16.0) -> float:
        """Convert font size to pixels for rendering calculations."""
        if self.unit == "px":
            return self.value
        elif self.unit == "pt":
            return self.value * 1.333  # 1pt = 1.333px
        elif self.unit == "pc":
            return self.value * 16.0   # 1pc = 16px
        elif self.unit == "em":
            return self.value * base_size
        elif self.unit == "rem":
            return self.value * 16.0   # Assuming 16px root
        elif self.unit == "%":
            return (self.value / 100.0) * base_size
        return self.value


class FontWeight(Expression):
    """
    Font weight specification.
    Supports numeric weights (100-900) and named weights.
    """
    type: ExpressionType = ExpressionType.STRING
    weight: Union[int, str] = Field(..., description="Font weight")
    
    @field_validator('weight')
    def validate_weight(cls, v):
        """Validate font weight values."""
        if isinstance(v, int):
            if not (100 <= v <= 900 and v % 100 == 0):
                raise ValueError("Numeric weight must be 100-900 in increments of 100")
        elif isinstance(v, str):
            valid_names = ["normal", "bold", "bolder", "lighter"]
            if v not in valid_names:
                raise ValueError(f"Named weight must be one of: {valid_names}")
        else:
            raise ValueError("Weight must be int (100-900) or str")
        return v
    
    def to_numeric(self) -> int:
        """Convert named weight to numeric equivalent."""
        if isinstance(self.weight, int):
            return self.weight
        
        name_to_numeric = {
            "normal": 400,
            "bold": 700,
            "bolder": 700,  # Context-dependent, defaulting to 700
            "lighter": 300  # Context-dependent, defaulting to 300
        }
        return name_to_numeric.get(str(self.weight), 400)


class FontStyle(Expression):
    """
    Font style specification.
    Supports italic, oblique, and normal styles.
    """
    type: ExpressionType = ExpressionType.STRING
    style: str = Field("normal", description="Font style")
    oblique_angle: Optional[float] = Field(None, description="Oblique angle in degrees")
    
    @field_validator('style')
    def validate_style(cls, v):
        """Validate font style values."""
        valid_styles = ["normal", "italic", "oblique"]
        if v not in valid_styles:
            raise ValueError(f"Style must be one of: {valid_styles}")
        return v


class FontExpression(Expression):
    """
    Complete font specification combining family, size, weight, and style.
    Provides comprehensive font definition for text rendering.
    """
    type: ExpressionType = ExpressionType.OBJECT
    family: FontFamily = Field(..., description="Font family specification")
    size: FontSize = Field(..., description="Font size specification")
    weight: Optional[FontWeight] = Field(None, description="Font weight specification")
    style: Optional[FontStyle] = Field(None, description="Font style specification")
    line_height: Optional[float] = Field(None, ge=0, description="Line height multiplier")
    
    def get_css_font(self) -> str:
        """Generate CSS font shorthand property."""
        parts = []
        
        # Font style and weight
        if self.style and self.style.style != "normal":
            parts.append(self.style.style)
        if self.weight and self.weight.weight != "normal":
            parts.append(str(self.weight.weight))
        
        # Font size and line height
        size_part = f"{self.size.value}{self.size.unit}"
        if self.line_height:
            size_part += f"/{self.line_height}"
        parts.append(size_part)
        
        # Font family
        parts.append(self.family.get_css_font_family())
        
        return " ".join(parts)
    
    def is_system_font(self) -> bool:
        """Check if this uses system font families."""
        system_fonts = ["system-ui", "serif", "sans-serif", "monospace", "cursive", "fantasy"]
        return self.family.family_name in system_fonts or any(
            font in system_fonts for font in self.family.fallback_families
        )


# =====================================================
# Phase C Priority 2.2 - Geometry Transformations  
# =====================================================

class TransformationMatrix(Expression):
    """
    2D transformation matrix for geometric operations.
    Represents affine transformations with 6-parameter matrix [a,b,c,d,e,f].
    """
    type: ExpressionType = ExpressionType.ARRAY
    matrix: List[float] = Field(..., min_length=6, max_length=6, 
                               description="Transformation matrix [a,b,c,d,e,f]")
    
    @field_validator('matrix')
    def validate_matrix(cls, v):
        """Validate transformation matrix values."""
        if len(v) != 6:
            raise ValueError("Transformation matrix must have exactly 6 values")
        return v
    
    def get_css_transform(self) -> str:
        """Generate CSS transform matrix() function."""
        return f"matrix({','.join(map(str, self.matrix))})"
    
    def compose(self, other: 'TransformationMatrix') -> 'TransformationMatrix':
        """Compose this transformation with another transformation."""
        a1, b1, c1, d1, e1, f1 = self.matrix
        a2, b2, c2, d2, e2, f2 = other.matrix
        
        # Matrix multiplication for 2D affine transformations
        return TransformationMatrix(matrix=[
            a1 * a2 + b1 * c2,      # a
            a1 * b2 + b1 * d2,      # b  
            c1 * a2 + d1 * c2,      # c
            c1 * b2 + d1 * d2,      # d
            e1 * a2 + f1 * c2 + e2, # e
            e1 * b2 + f1 * d2 + f2  # f
        ])


class RotationTransform(Expression):
    """
    Rotation transformation around a point.
    Supports angle in degrees or radians with optional center point.
    """
    type: ExpressionType = ExpressionType.OBJECT
    angle: float = Field(..., description="Rotation angle")
    angle_unit: str = Field("deg", description="Angle unit: deg or rad")
    center_x: float = Field(0.0, description="Rotation center X coordinate")
    center_y: float = Field(0.0, description="Rotation center Y coordinate")
    
    @field_validator('angle_unit')
    def validate_angle_unit(cls, v):
        """Validate angle unit."""
        if v not in ["deg", "rad"]:
            raise ValueError("Angle unit must be 'deg' or 'rad'")
        return v
    
    def to_radians(self) -> float:
        """Convert angle to radians."""
        if self.angle_unit == "rad":
            return self.angle
        return self.angle * 3.14159265359 / 180.0
    
    def to_matrix(self) -> TransformationMatrix:
        """Convert rotation to transformation matrix."""
        import math
        rad = self.to_radians()
        cos_a = math.cos(rad)
        sin_a = math.sin(rad)
        
        # Translation to origin, rotation, translation back
        cx, cy = self.center_x, self.center_y
        
        return TransformationMatrix(matrix=[
            cos_a, sin_a, -sin_a, cos_a,
            cx * (1 - cos_a) + cy * sin_a,
            cy * (1 - cos_a) - cx * sin_a
        ])
    
    def get_css_transform(self) -> str:
        """Generate CSS rotate() function."""
        if self.center_x == 0 and self.center_y == 0:
            return f"rotate({self.angle}{self.angle_unit})"
        else:
            return f"rotate({self.angle}{self.angle_unit} {self.center_x}px {self.center_y}px)"


class ScaleTransform(Expression):
    """
    Scale transformation with independent X and Y scaling.
    Supports uniform and non-uniform scaling with optional center point.
    """
    type: ExpressionType = ExpressionType.OBJECT
    scale_x: float = Field(1.0, gt=0, description="X-axis scale factor")
    scale_y: Optional[float] = Field(None, gt=0, description="Y-axis scale factor (defaults to scale_x)")
    center_x: float = Field(0.0, description="Scale center X coordinate")
    center_y: float = Field(0.0, description="Scale center Y coordinate")
    
    def get_scale_y(self) -> float:
        """Get effective Y scale factor."""
        return self.scale_y if self.scale_y is not None else self.scale_x
    
    def is_uniform(self) -> bool:
        """Check if this is uniform scaling."""
        return self.scale_y is None or abs(self.scale_x - self.scale_y) < 1e-10
    
    def to_matrix(self) -> TransformationMatrix:
        """Convert scale to transformation matrix."""
        sx, sy = self.scale_x, self.get_scale_y()
        cx, cy = self.center_x, self.center_y
        
        return TransformationMatrix(matrix=[
            sx, 0, 0, sy,
            cx * (1 - sx),
            cy * (1 - sy)
        ])
    
    def get_css_transform(self) -> str:
        """Generate CSS scale() function."""
        if self.is_uniform():
            scale_func = f"scale({self.scale_x})"
        else:
            scale_func = f"scale({self.scale_x}, {self.get_scale_y()})"
        
        if self.center_x == 0 and self.center_y == 0:
            return scale_func
        else:
            return f"translate({self.center_x}px, {self.center_y}px) {scale_func} translate({-self.center_x}px, {-self.center_y}px)"


class TranslationTransform(Expression):
    """
    Translation transformation.
    Moves geometry by specified X and Y offsets.
    """
    type: ExpressionType = ExpressionType.OBJECT
    offset_x: float = Field(0.0, description="X-axis translation offset")
    offset_y: float = Field(0.0, description="Y-axis translation offset")
    unit: str = Field("px", description="Translation unit")
    
    def to_matrix(self) -> TransformationMatrix:
        """Convert translation to transformation matrix."""
        return TransformationMatrix(matrix=[
            1.0, 0.0, 0.0, 1.0,
            self.offset_x, self.offset_y
        ])
    
    def get_css_transform(self) -> str:
        """Generate CSS translate() function."""
        return f"translate({self.offset_x}{self.unit}, {self.offset_y}{self.unit})"


class GeometryTransformation(Expression):
    """
    Complete geometry transformation combining multiple operations.
    Supports composition of rotation, scaling, and translation transforms.
    """
    type: ExpressionType = ExpressionType.OBJECT
    rotation: Optional[RotationTransform] = Field(None, description="Rotation transformation")
    scale: Optional[ScaleTransform] = Field(None, description="Scale transformation")  
    translation: Optional[TranslationTransform] = Field(None, description="Translation transformation")
    custom_matrix: Optional[TransformationMatrix] = Field(None, description="Custom transformation matrix")
    
    def get_combined_matrix(self) -> TransformationMatrix:
        """Get combined transformation matrix from all operations."""
        # Start with identity matrix
        result = TransformationMatrix(matrix=[1.0, 0.0, 0.0, 1.0, 0.0, 0.0])
        
        # Apply transformations in order: scale -> rotate -> translate
        if self.scale:
            result = result.compose(self.scale.to_matrix())
        
        if self.rotation:
            result = result.compose(self.rotation.to_matrix())
            
        if self.translation:
            result = result.compose(self.translation.to_matrix())
            
        if self.custom_matrix:
            result = result.compose(self.custom_matrix)
            
        return result
    
    def get_css_transforms(self) -> List[str]:
        """Get list of CSS transform functions."""
        transforms = []
        
        if self.translation:
            transforms.append(self.translation.get_css_transform())
        
        if self.rotation:
            transforms.append(self.rotation.get_css_transform())
            
        if self.scale:
            transforms.append(self.scale.get_css_transform())
            
        if self.custom_matrix:
            transforms.append(self.custom_matrix.get_css_transform())
            
        return transforms
    
    def get_css_transform(self) -> str:
        """Generate complete CSS transform property."""
        transforms = self.get_css_transforms()
        return " ".join(transforms) if transforms else "none"


# =====================================================
# Phase C Priority 2.3 - DateTime Calendar Expressions
# =====================================================

class CalendarField(Expression):
    """
    Calendar field extraction from date/time values.
    Supports year, month, day, hour, minute, second, day of week, etc.
    """
    type: ExpressionType = ExpressionType.STRING
    field_type: str = Field(..., description="Calendar field type")
    source_expression: Any = Field(..., description="Source date/time expression")
    
    @field_validator('field_type')
    def validate_field_type(cls, v):
        """Validate calendar field types."""
        valid_fields = [
            "year", "month", "day", "hour", "minute", "second",
            "dayOfWeek", "dayOfYear", "weekOfYear", "quarter",
            "millisecond", "timezone", "era"
        ]
        if v not in valid_fields:
            raise ValueError(f"Field type must be one of: {valid_fields}")
        return v
    
    def extract_field(self, date_value: Any) -> int:
        """Extract calendar field from date value."""
        # This would be implemented with actual date parsing
        # For now, return a placeholder
        return 0


class DateTimeFormat(Expression):
    """
    DateTime formatting expression with pattern support.
    Supports ICU/Java style date format patterns.
    """
    type: ExpressionType = ExpressionType.STRING
    pattern: str = Field(..., description="Date format pattern")
    locale: str = Field("en", description="Locale for formatting")
    timezone: Optional[str] = Field(None, description="Timezone identifier")
    
    def format_datetime(self, datetime_value: Any) -> str:
        """Format datetime value according to pattern."""
        # Implementation would use datetime.strftime or babel
        return str(datetime_value)
    
    def get_pattern_components(self) -> List[str]:
        """Extract components from format pattern."""
        # Simple pattern analysis (full implementation would be more complex)
        components = []
        if "yyyy" in self.pattern or "YYYY" in self.pattern:
            components.append("year")
        if "MM" in self.pattern:
            components.append("month")
        if "dd" in self.pattern or "DD" in self.pattern:
            components.append("day")
        if "HH" in self.pattern or "hh" in self.pattern:
            components.append("hour")
        if "mm" in self.pattern:
            components.append("minute")
        if "ss" in self.pattern:
            components.append("second")
        return components


class CalendarInterval(Expression):
    """
    Calendar interval for date range operations.
    Supports various interval types (days, months, years, etc.).
    """
    type: ExpressionType = ExpressionType.OBJECT
    interval_type: str = Field(..., description="Interval type")
    amount: int = Field(..., description="Interval amount")
    
    @field_validator('interval_type')
    def validate_interval_type(cls, v):
        """Validate interval types."""
        valid_intervals = [
            "millisecond", "second", "minute", "hour", "day",
            "week", "month", "quarter", "year"
        ]
        if v not in valid_intervals:
            raise ValueError(f"Interval type must be one of: {valid_intervals}")
        return v
    
    def to_timedelta_kwargs(self) -> Dict[str, int]:
        """Convert to Python timedelta kwargs."""
        mapping = {
            "day": "days",
            "week": "weeks", 
            "hour": "hours",
            "minute": "minutes",
            "second": "seconds",
            "millisecond": "milliseconds"
        }
        
        if self.interval_type in mapping:
            return {mapping[self.interval_type]: self.amount}
        else:
            # For month/quarter/year, would need more complex handling
            return {"days": self.amount * 30}  # Approximation


class DateTimeCalendar(Expression):
    """
    Complete datetime calendar system with field extraction, formatting, and intervals.
    Provides comprehensive date/time manipulation for CartoSym expressions.
    """
    type: ExpressionType = ExpressionType.OBJECT
    source_datetime: Any = Field(..., description="Source datetime expression")
    field_extractions: List[CalendarField] = Field(default_factory=list, 
                                                  description="Calendar field extractions")
    formatting: Optional[DateTimeFormat] = Field(None, description="DateTime formatting")
    intervals: List[CalendarInterval] = Field(default_factory=list,
                                            description="Calendar intervals")
    
    def extract_fields(self) -> Dict[str, int]:
        """Extract all configured calendar fields."""
        return {field.field_type: field.extract_field(self.source_datetime) 
                for field in self.field_extractions}
    
    def format_output(self) -> str:
        """Format datetime according to configured formatting."""
        if self.formatting:
            return self.formatting.format_datetime(self.source_datetime)
        return str(self.source_datetime)
    
    def add_intervals(self) -> Any:
        """Add all configured intervals to source datetime."""
        # Implementation would use datetime arithmetic
        return self.source_datetime
    
    def is_business_day(self) -> bool:
        """Check if the datetime falls on a business day."""
        # Would extract day of week and check if Monday-Friday
        return True
    
    def get_quarter(self) -> int:
        """Get quarter (1-4) for the datetime."""
        # Would extract month and calculate quarter
        return 1


# =====================================================
# Phase C Priority 2.4 - Unit/Measure Expressions
# =====================================================

class UnitType(str, Enum):
    """Enumeration of supported unit types."""
    # Length units
    PX = "px"      # Pixels
    PT = "pt"      # Points
    PC = "pc"      # Picas  
    MM = "mm"      # Millimeters
    CM = "cm"      # Centimeters
    IN = "in"      # Inches
    
    # Relative units
    EM = "em"      # Relative to font size
    REM = "rem"    # Relative to root font size
    EX = "ex"      # Relative to x-height
    CH = "ch"      # Relative to character width
    
    # Percentage and viewport units
    PERCENT = "%"  # Percentage
    VW = "vw"      # Viewport width
    VH = "vh"      # Viewport height
    VMIN = "vmin"  # Viewport minimum
    VMAX = "vmax"  # Viewport maximum
    
    # Angular units
    DEG = "deg"    # Degrees
    RAD = "rad"    # Radians
    GRAD = "grad"  # Gradians
    TURN = "turn"  # Turns


class UnitConversion:
    """Unit conversion utilities for different measurement systems."""
    
    # Conversion factors to pixels (assuming 96 DPI, 16px base font)
    TO_PIXELS = {
        UnitType.PX: 1.0,
        UnitType.PT: 4.0/3.0,     # 1pt = 4/3 px at 96 DPI
        UnitType.PC: 16.0,        # 1pc = 16px
        UnitType.MM: 96.0/25.4,   # 1mm = 96/25.4 px at 96 DPI
        UnitType.CM: 96.0/2.54,   # 1cm = 96/2.54 px at 96 DPI  
        UnitType.IN: 96.0,        # 1in = 96px at 96 DPI
        UnitType.EM: 16.0,        # 1em = 16px (default)
        UnitType.REM: 16.0,       # 1rem = 16px (default)
        UnitType.EX: 8.0,         # 1ex ≈ 0.5em (approximation)
        UnitType.CH: 8.0,         # 1ch ≈ 0.5em (approximation)
    }
    
    # Angular conversion to radians
    TO_RADIANS = {
        UnitType.RAD: 1.0,
        UnitType.DEG: 3.14159265359 / 180.0,
        UnitType.GRAD: 3.14159265359 / 200.0,
        UnitType.TURN: 2 * 3.14159265359,
    }
    
    @classmethod
    def to_pixels(cls, value: float, unit: UnitType, context_size: float = 16.0) -> float:
        """Convert value to pixels."""
        if unit in cls.TO_PIXELS:
            factor = cls.TO_PIXELS[unit]
            if unit in [UnitType.EM, UnitType.EX, UnitType.CH]:
                return value * context_size * (factor / 16.0)
            return value * factor
        return value
    
    @classmethod
    def to_radians(cls, value: float, unit: UnitType) -> float:
        """Convert angular value to radians."""
        return value * cls.TO_RADIANS.get(unit, 1.0)


class MeasureExpression(Expression):
    """
    Measurement expression with unit support.
    Provides value with associated unit and conversion capabilities.
    """
    type: ExpressionType = ExpressionType.NUMERIC
    value: float = Field(..., description="Numeric value")
    unit: UnitType = Field(UnitType.PX, description="Measurement unit")
    
    def to_pixels(self, context_size: float = 16.0) -> float:
        """Convert measurement to pixels."""
        return UnitConversion.to_pixels(self.value, self.unit, context_size)
    
    def to_radians(self) -> float:
        """Convert angular measurement to radians."""
        return UnitConversion.to_radians(self.value, self.unit)
    
    def convert_to(self, target_unit: UnitType, context_size: float = 16.0) -> 'MeasureExpression':
        """Convert to target unit."""
        if self.unit == target_unit:
            return self
        
        # Convert via pixels for length units
        if target_unit in UnitConversion.TO_PIXELS:
            pixels = self.to_pixels(context_size)
            target_factor = UnitConversion.TO_PIXELS[target_unit]
            if target_unit in [UnitType.EM, UnitType.EX, UnitType.CH]:
                target_factor = target_factor / 16.0 * context_size
            new_value = pixels / target_factor
            return MeasureExpression(value=new_value, unit=target_unit)
        
        return self
    
    def is_absolute(self) -> bool:
        """Check if this is an absolute unit."""
        absolute_units = {UnitType.PX, UnitType.PT, UnitType.PC, 
                         UnitType.MM, UnitType.CM, UnitType.IN}
        return self.unit in absolute_units
    
    def is_relative(self) -> bool:
        """Check if this is a relative unit."""
        relative_units = {UnitType.EM, UnitType.REM, UnitType.EX, UnitType.CH, UnitType.PERCENT}
        return self.unit in relative_units
    
    def is_viewport(self) -> bool:
        """Check if this is a viewport unit."""
        viewport_units = {UnitType.VW, UnitType.VH, UnitType.VMIN, UnitType.VMAX}
        return self.unit in viewport_units
    
    def is_angular(self) -> bool:
        """Check if this is an angular unit."""
        angular_units = {UnitType.DEG, UnitType.RAD, UnitType.GRAD, UnitType.TURN}
        return self.unit in angular_units
    
    def __str__(self) -> str:
        """String representation with unit."""
        unit_str = self.unit.value if hasattr(self.unit, 'value') else str(self.unit)
        return f"{self.value}{unit_str}"


class UnitRange(Expression):
    """
    Range of measurements with min/max constraints.
    Useful for responsive design and adaptive styling.
    """
    type: ExpressionType = ExpressionType.OBJECT
    min_value: MeasureExpression = Field(..., description="Minimum value")
    max_value: MeasureExpression = Field(..., description="Maximum value")
    current_value: Optional[MeasureExpression] = Field(None, description="Current value in range")
    
    def contains(self, value: MeasureExpression, context_size: float = 16.0) -> bool:
        """Check if value is within range."""
        min_px = self.min_value.to_pixels(context_size)
        max_px = self.max_value.to_pixels(context_size)
        val_px = value.to_pixels(context_size)
        return min_px <= val_px <= max_px
    
    def clamp(self, value: MeasureExpression, context_size: float = 16.0) -> MeasureExpression:
        """Clamp value to range bounds."""
        min_px = self.min_value.to_pixels(context_size)
        max_px = self.max_value.to_pixels(context_size)
        val_px = value.to_pixels(context_size)
        
        clamped_px = max(min_px, min(max_px, val_px))
        
        # Convert back to original unit
        if clamped_px == min_px:
            return self.min_value
        elif clamped_px == max_px:
            return self.max_value
        else:
            return value
    
    def get_percentage(self, value: MeasureExpression, context_size: float = 16.0) -> float:
        """Get percentage position of value within range."""
        min_px = self.min_value.to_pixels(context_size)
        max_px = self.max_value.to_pixels(context_size)
        val_px = value.to_pixels(context_size)
        
        if max_px == min_px:
            return 0.0
        
        return (val_px - min_px) / (max_px - min_px)


class ResponsiveUnit(Expression):
    """
    Responsive unit that adapts based on context (viewport, container, etc.).
    Supports fluid scaling between breakpoints.
    """
    type: ExpressionType = ExpressionType.OBJECT
    base_value: MeasureExpression = Field(..., description="Base measurement value")
    scale_factor: float = Field(1.0, description="Scale factor for adaptation")
    min_constraint: Optional[MeasureExpression] = Field(None, description="Minimum constraint")
    max_constraint: Optional[MeasureExpression] = Field(None, description="Maximum constraint")
    viewport_basis: str = Field("width", description="Viewport dimension for scaling")
    
    @field_validator('viewport_basis')
    def validate_viewport_basis(cls, v):
        """Validate viewport basis."""
        if v not in ["width", "height", "min", "max"]:
            raise ValueError("Viewport basis must be: width, height, min, or max")
        return v
    
    def calculate_responsive_value(self, viewport_width: float, viewport_height: float, 
                                  context_size: float = 16.0) -> MeasureExpression:
        """Calculate responsive value based on viewport."""
        # Determine basis dimension
        if self.viewport_basis == "width":
            basis = viewport_width
        elif self.viewport_basis == "height":
            basis = viewport_height
        elif self.viewport_basis == "min":
            basis = min(viewport_width, viewport_height)
        else:  # max
            basis = max(viewport_width, viewport_height)
        
        # Scale base value
        base_px = self.base_value.to_pixels(context_size)
        scaled_px = base_px * self.scale_factor * (basis / 1920.0)  # 1920px reference
        
        # Create scaled measurement
        scaled_measure = MeasureExpression(value=scaled_px, unit=UnitType.PX)
        
        # Apply constraints
        if self.min_constraint and scaled_px < self.min_constraint.to_pixels(context_size):
            return self.min_constraint
        if self.max_constraint and scaled_px > self.max_constraint.to_pixels(context_size):
            return self.max_constraint
        
        return scaled_measure
