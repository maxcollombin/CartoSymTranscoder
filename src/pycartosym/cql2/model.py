"""Expression system for CartoSym-CSS and the CartoSym-JSON schema.

Supports complex expressions, conditions, function calls, and JSON Schema
expression types.
"""

from __future__ import annotations

from abc import ABC
from enum import Enum
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from ..models.base import BaseCartoSymModel


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
    NULL = "null"
    # Additional expression-type discriminants
    NUMERIC = "numeric"
    OBJECT = "object"
    PREDICATE = "predicate"


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

    model_config = ConfigDict(use_enum_values=True)

    type: ExpressionType


class IdentifierExpression(Expression):
    """Simple identifier like 'dataLayer' or 'FunctionCode'."""

    type: ExpressionType = ExpressionType.IDENTIFIER
    name: str


class ConstantExpression(Expression):
    """Constant value (number, boolean, etc.)."""

    type: ExpressionType = ExpressionType.CONSTANT
    value: int | float | bool | str
    unit: str | None = None  # For values like "2.0 px"


class StringExpression(Expression):
    """String literal."""

    type: ExpressionType = ExpressionType.STRING
    value: str


class NullLiteral(Expression):
    """SQL ``NULL`` literal (CQL2 ``x IS NULL``).

    A distinct type so consumers test ``isinstance(expr, NullLiteral)`` rather
    than sniffing an identifier name. Serialises to JSON ``null``.
    """

    type: ExpressionType = ExpressionType.NULL

    def to_cql2_json(self) -> None:
        """Serialise to CQL2-JSON: SQL ``NULL`` becomes JSON ``null``."""
        return None


class MemberAccessExpression(Expression):
    """Member access like 'dataLayer.type' or 'viz.timeInterval.start.date'."""

    type: ExpressionType = ExpressionType.MEMBER_ACCESS
    object: Expression
    member: str


class FunctionCallExpression(Expression):
    """Function call like 'Text(...)' or 'Image(...)'."""

    type: ExpressionType = ExpressionType.FUNCTION_CALL
    function_name: str
    arguments: list[Expression]


class BinaryOperationExpression(Expression):
    """Binary operation like 'a + b' or 'x = y'."""

    type: ExpressionType = ExpressionType.BINARY_OP
    left: Expression
    operator: BinaryOperator
    right: Expression


class UnaryOperationExpression(Expression):
    """Unary operation like '-x' or 'not y'."""

    type: ExpressionType = ExpressionType.UNARY_OP
    operator: UnaryOperator
    operand: Expression


class ConditionalExpression(Expression):
    """Ternary conditional like 'condition ? true_value : false_value'."""

    type: ExpressionType = ExpressionType.CONDITIONAL
    condition: Expression
    true_value: Expression
    false_value: Expression


class ArrayExpression(Expression):
    """Array literal like '[a, b, c]'."""

    type: ExpressionType = ExpressionType.ARRAY
    elements: list[Expression]


class PropertyAssignment(BaseModel):
    """Property assignment within an instance."""

    property: str
    value: Expression


class InstanceExpression(Expression):
    """Instance creation like '{color: red; opacity: 0.5}' or 'Text(...)'."""

    type: ExpressionType = ExpressionType.INSTANCE
    class_name: str | None = None  # For Text(...) vs {...}
    properties: list[PropertyAssignment] = []


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

    name: str | None = None  # Simple name like "Landuse"
    conditions: list[Expression] = []  # Conditions like [dataLayer.type = vector]

    def is_simple(self) -> bool:
        """Check if this is a simple selector (name only)."""
        return self.name is not None and len(self.conditions) == 0


# Enhanced styling rule
class StylingRuleExpression(BaseModel):
    """Styling rule that can contain expressions and nested rules."""

    selectors: list[Selector] = []
    properties: dict[str, Expression] = {}  # property_name -> expression
    nested_rules: list[StylingRuleExpression] = []


# Update forward reference
StylingRuleExpression.model_rebuild()


# =====================================================
# JSON Schema Expression Types (from CartoSym schema)
# =====================================================


# Boolean Expressions (JSON Schema: boolExpression)
class BoolExpression(BaseExpression, Expression):
    """Base class for boolean expressions from JSON schema.

    Also an :class:`Expression` (multiple inheritance, not a plain
    ``BaseExpression``) — predicates (``IsLikePredicate``,
    ``SpatialPredicate``, ``NotExpression``…) need to slot into the generic
    ``Expression`` tree wherever CQL2-Text combines them with AND/OR/NOT
    (:class:`BinaryOperationExpression`/:class:`UnaryOperationExpression`
    from :mod:`.from_cql2text`). ``BaseExpression`` is listed first so its
    (``BaseCartoSymModel``) stricter ``model_config`` — ``extra="forbid"``
    in particular — wins over ``Expression``'s plainer one.
    """

    type: ExpressionType = ExpressionType.PREDICATE


class AndOrExpression(BoolExpression):
    """Logical AND/OR expression: {"op": "and|or", "args": [...]}."""

    op: Literal["and", "or"]
    args: list[BoolExpression] = Field(min_length=2)


class NotExpression(BoolExpression):
    """Logical NOT expression: {"op": "not", "args": [...]}."""

    op: Literal["not"] = "not"
    args: list[BoolExpression] = Field(min_length=1, max_length=1)


# Numeric Expressions (JSON Schema: numericExpression)
class NumericExpression(BaseExpression):
    """Base class for numeric expressions from JSON schema."""

    type: str | None = None


class ArithmeticExpression(NumericExpression):
    """Arithmetic expression: {"op": "+|-|*|/|%|**", "args": [...]}."""

    op: Literal["+", "-", "*", "/", "%", "**"]
    args: list[NumericExpression] = Field(min_length=2)


class ArithmeticOperands(NumericExpression):
    """Advanced arithmetic operands with multiple operations."""

    operations: list[ArithmeticExpression]

    @property
    def result_type(self) -> str:
        """Static result type of this expression (always ``"numeric"``)."""
        return "numeric"


class ScalarOperands(Expression):
    """Scalar operands for various operations on single values."""

    op: str
    args: list[NumericExpression | ScalarExpression] = Field(min_length=1)


class BitwiseLogical(NumericExpression):
    """Bitwise logical: {"op": "&|||^", "args": [...]}."""

    op: Literal["&", "|", "^"]
    args: list[NumericExpression] = Field(min_length=2)


class BitwiseShift(NumericExpression):
    """Bitwise shift: {"op": "<<|>>", "args": [...]}."""

    op: Literal["<<", ">>"]
    args: list[NumericExpression] = Field(min_length=2)


class BitwiseNot(NumericExpression):
    """Bitwise NOT: {"op": "~", "args": [...]}."""

    op: Literal["~"] = "~"
    args: list[NumericExpression] = Field(min_length=1, max_length=1)


# Comparison Predicates
class ComparisonPredicate(BoolExpression):
    """Base class for comparison predicates."""

    pass


class BinaryComparisonPredicate(ComparisonPredicate):
    """Binary comparison: {"op": "=|!=|<|<=|>|>=", "args": [...]}."""

    op: Literal["=", "!=", "<", "<=", ">", ">="]
    args: list[NumericExpression | ScalarExpression] = Field(min_length=2, max_length=2)


class IsNullPredicate(ComparisonPredicate):
    """Null check: {"op": "isNull", "args": [...]}."""

    op: Literal["isNull"] = "isNull"
    args: list[Expression] = Field(min_length=1, max_length=1)


class IsInListPredicate(ComparisonPredicate):
    """In list check: {"op": "in", "args": [...]}."""

    op: Literal["in"] = "in"
    args: list[Expression | list[Expression]] = Field(min_length=2)


class IsBetweenPredicate(ComparisonPredicate):
    """Between check: {"op": "between", "args": [...]}."""

    op: Literal["between"] = "between"
    args: list[Expression] = Field(min_length=3, max_length=3)  # [value, min, max]


class IsLikePredicate(ComparisonPredicate):
    """Pattern matching: {"op": "like|ilike", "args": [...]}."""

    op: Literal["like", "ilike"]
    args: list[Expression] = Field(
        min_length=2, max_length=3
    )  # [value, pattern, escape?]


# Property and System References
class PropertyRef(Expression):
    """Property reference: {"property": "propertyName"}."""

    property: str


class SystemIdentifier(Expression):
    """System identifier: {"sysId": "identifier"}."""

    sysId: str


# Scalar Expressions
class ScalarExpression(Expression):
    """Base class for scalar expressions."""

    pass


class ScalarLiteral(ScalarExpression):
    """Scalar literal value."""

    value: str | int | float | bool


# Enhanced Function Calls (JSON Schema format)
class FunctionCallJSON(Expression):
    """JSON Schema function call: {"op": "functionName", "args": [...]}."""

    op: str  # Function name
    args: list[Expression] = Field(default_factory=list)


# Enhanced Conditional Expressions (JSON Schema format)
class ConditionalExpressionJSON(Expression):
    """JSON Schema conditional.

    ``{"op": "if", "args": [condition, trueValue, falseValue]}``
    """

    op: Literal["if"] = "if"
    args: list[Expression] = Field(min_length=3, max_length=3)


# Temporal Expressions (for date/time)
class TemporalExpression(Expression):
    """Base class for temporal expressions."""

    type: ExpressionType = (
        ExpressionType.FUNCTION_CALL
    )  # Default type for temporal functions


class DateInstant(TemporalExpression):
    """Date instant: {"op": "date", "args": [year, month, day]}."""

    op: Literal["date"] = "date"
    args: list[int | float] = Field(
        min_length=3, max_length=3
    )  # [year, month, day] - use simple types


class TimestampInstant(TemporalExpression):
    """Timestamp instant.

    ``{"op": "timestamp", "args": [year, month, day, hour, minute, second]}``
    """

    op: Literal["timestamp"] = "timestamp"
    args: list[NumericExpression] = Field(
        min_length=6, max_length=7
    )  # [y,m,d,h,min,s,ms?]


class DateString(TemporalExpression):
    """Date from string: {"op": "dateString", "args": [dateString, format?]}."""

    op: Literal["dateString"] = "dateString"
    args: list[Expression] = Field(min_length=1, max_length=2)


class TimestampString(TemporalExpression):
    """Timestamp from string.

    ``{"op": "timestampString", "args": [timestampString, format?]}``
    """

    op: Literal["timestampString"] = "timestampString"
    args: list[Expression] = Field(min_length=1, max_length=2)


class InstantInstance(TemporalExpression):
    """Generic instant instance for temporal operations."""

    instant_type: Literal["date", "timestamp"]
    value: str | int | float


class IntervalInstance(TemporalExpression):
    """Time interval instance: {"start": instant, "end": instant}."""

    start: TemporalExpression
    end: TemporalExpression


class IntervalArray(TemporalExpression):
    """Array of time intervals."""

    intervals: list[IntervalInstance]


class TemporalInstantExpression(TemporalExpression):
    """Complex temporal instant with operations."""

    op: str
    args: list[TemporalExpression]


class TemporalOperands(Expression):
    """Temporal operands for arithmetic operations on time values."""

    op: Literal["add", "subtract", "duration"]
    args: list[TemporalExpression] = Field(min_length=2)


class TemporalPredicate(BoolExpression):
    """Temporal predicate for time-based comparisons.

    OGC CQL2-JSON format: {"op": "t_before", "args": [instantA, instantB]}
    Reference: ecere/libCartoSym CQL2Expressions.ec (DATE/TIMESTAMP/INTERVAL handling).
    """

    op: Literal[
        "t_before",
        "t_after",
        "t_meets",
        "t_metby",
        "t_overlaps",
        "t_overlappedby",
        # OGC 21-065r2's Allen-relation names are "starts"/"startedby" and
        # "finishes"/"finishedby" (matching `T_STARTS`/`T_STARTEDBY`/
        # `T_FINISHES`/`T_FINISHEDBY` in the CQL2-Text grammar) — this
        # Literal previously spelled them "begins"/"begunby"/"ends"/
        # "endedby", which no CQL2-Text/JSON producer ever emits.
        "t_starts",
        "t_startedby",
        "t_during",
        "t_contains",
        "t_finishes",
        "t_finishedby",
        "t_equals",
        "t_intersects",
        "t_disjoint",
        # Legacy bare names
        "before",
        "after",
        "during",
        "meets",
        "overlaps",
    ]
    args: list[Expression]

    def normalised_op(self) -> str:
        """Return the CQL2-standard t_ prefixed operator name."""
        if self.op.startswith("t_"):
            return self.op
        return f"t_{self.op}"


# Spatial Expressions (for geometry)
class SpatialPredicate(BoolExpression):
    """Spatial predicate for geometry-based comparisons.

    OGC CQL2-JSON format: {"op": "s_intersects", "args": [geomA, geomB]}
    Inspired by CQL2ExpCall in ecere/libCartoSym CQL2Expressions.ec.
    """

    op: Literal[
        "s_intersects",
        "s_contains",
        "s_within",
        "s_touches",
        "s_crosses",
        "s_disjoint",
        "s_overlaps",
        "s_equals",
        "s_covers",
        "s_coveredBy",
        # Legacy bare names (accepted on input, normalised to s_ prefix on output)
        "intersects",
        "contains",
        "within",
        "touches",
        "crosses",
        "disjoint",
        "overlaps",
        "equals",
        "covers",
        "coveredBy",
    ]
    args: list[Expression]

    def normalised_op(self) -> str:
        """Return the CQL2-standard s_ prefixed operator name."""
        if self.op.startswith("s_"):
            return self.op
        return f"s_{self.op}"


class SpatialRelatePredicate(BoolExpression):
    """DE-9IM relate predicate: {"op": "s_relate", "args": [geomA, geomB, pattern]}.

    The pattern is a 9-character DE-9IM matrix string (e.g. "T*F**FFF*").
    See models/de9im.py for predicate↔pattern mapping and README for
    a description of the DE-9IM model.
    """

    op: Literal["s_relate"] = "s_relate"
    args: list[Expression] = Field(min_length=2, max_length=2)
    pattern: str = Field(
        ...,
        min_length=9,
        max_length=9,
        description="DE-9IM intersection matrix pattern",
    )

    @field_validator("pattern")
    def _validate_de9im_pattern(cls, v: str) -> str:
        """Reject a ``pattern`` that is not a well-formed DE-9IM pattern.

        Delegates to :func:`pycartosym.models.de9im.is_valid_de9im_pattern`
        so the pattern alphabet (``0 1 2 T F *``) lives in one place.
        """
        from ..models.de9im import is_valid_de9im_pattern

        if not is_valid_de9im_pattern(v):
            raise ValueError(
                f"{v!r} is not a valid DE-9IM pattern "
                "(9 characters, each one of 0 1 2 T F *)"
            )
        return v


class GeometryExpression(Expression):
    """Base class for geometry expressions."""

    type: ExpressionType = (
        ExpressionType.INSTANCE
    )  # Default type for geometry instances


class GeometryBuffer(GeometryExpression):
    """Geometry buffer operation: {"op": "s_buffer", "args": [geometry, distance]}."""

    op: Literal["buffer", "s_buffer"] = "s_buffer"
    args: list[Expression] = Field(min_length=2, max_length=2)  # [geometry, distance]


class GeometryManipulationUnary(GeometryExpression):
    """Unary geometry operations.

    ``{"op": "s_convexHull|s_envelope|centroid|boundary", "args": [geometry]}``
    """

    op: Literal[
        "centroid", "envelope", "convexHull", "boundary", "s_convexHull", "s_envelope"
    ]
    args: list[Expression] = Field(min_length=1, max_length=1)


class GeometryManipulationBinary(GeometryExpression):
    """Binary geometry operations.

    ``{"op": "s_intersection|s_union|s_difference|s_symDifference",
    "args": [geom1, geom2]}``
    """

    op: Literal[
        "union",
        "intersection",
        "difference",
        "symDifference",
        "s_intersection",
        "s_union",
        "s_difference",
        "s_symDifference",
    ]
    args: list[Expression] = Field(min_length=2, max_length=2)


class SpatialInstance(GeometryExpression):
    """Spatial geometry instance with coordinates."""

    geometry_type: Literal[
        "Point",
        "LineString",
        "Polygon",
        "MultiPoint",
        "MultiLineString",
        "MultiPolygon",
    ]
    coordinates: list[Any]  # Coordinate arrays, structure depends on geometry type
    crs: str | None = Field(None, description="Coordinate Reference System")


class GeometryLiteral(GeometryExpression):
    """Inline geometry literal (WKT / GeoJSON).

    In CQL2-Text this is written as WKT: POINT(1 2), POLYGON((...)), etc.
    In CQL2-JSON this is serialised as a GeoJSON geometry object:
      {"type": "Point", "coordinates": [1, 2]}

    Inspired by CQL2ExpCall::readGeometryFromCQL2() and toCQL2JSON() in
    ecere/libCartoSym CQL2Expressions.ec.
    """

    geom_type: Literal[
        "Point",
        "LineString",
        "Polygon",
        "MultiPoint",
        "MultiLineString",
        "MultiPolygon",
        "GeometryCollection",
    ]
    coordinates: list[Any] | None = None
    geometries: list[GeometryLiteral] | None = None  # For GeometryCollection
    crs: str | None = None

    def to_geojson(self) -> dict[str, Any]:
        """Serialise as a GeoJSON geometry dict (for CQL2-JSON output)."""
        result: dict[str, Any] = {"type": self.geom_type}
        if self.geom_type == "GeometryCollection" and self.geometries:
            result["geometries"] = [g.to_geojson() for g in self.geometries]
        elif self.coordinates is not None:
            result["coordinates"] = self.coordinates
        return result

    @classmethod
    def from_geojson(cls, data: dict[str, Any]) -> GeometryLiteral:
        """Deserialise from a GeoJSON geometry dict."""
        geom_type = data["type"]
        if geom_type == "GeometryCollection":
            return cls(
                geom_type=geom_type,
                geometries=[cls.from_geojson(g) for g in data.get("geometries", [])],
            )
        return cls(geom_type=geom_type, coordinates=data.get("coordinates"))


class BboxLiteral(GeometryExpression):
    """Bounding box literal.

    CQL2-Text:  BBOX(geom, x1, y1, x2, y2)
    CQL2-JSON:  {"bbox": [x1, y1, x2, y2]}  (4 or 6 values)
    """

    bbox: list[float] = Field(min_length=4, max_length=6)

    def to_cql2_json(self) -> dict[str, Any]:
        """Serialise to a CQL2-JSON ``{"bbox": [...]}`` object."""
        return {"bbox": self.bbox}


class TemporalLiteral(TemporalExpression):
    """Temporal literal for DATE / TIMESTAMP / INTERVAL.

    CQL2-JSON format (from ecere/libCartoSym CQL2Expressions.ec toCQL2JSON):
      DATE       → {"date": "2020-01-01"}
      TIMESTAMP  → {"timestamp": "2020-01-01T00:00:00Z"}
      INTERVAL   → {"interval": ["2020-01-01", "2020-12-31"]}
    """

    temporal_type: Literal["date", "timestamp", "interval"]
    value: str | None = None  # For date / timestamp
    # For interval (2 values: start, end). A bound is usually a literal
    # string, but per the CQL2-JSON schema's `intervalArray` (each item
    # `oneOf` instantString / ".." / propertyRef / systemIdentifier /
    # functionCall / conditionalExpression) it may also be a property
    # reference or function call, e.g. `INTERVAL(starts_at, ends_at)` —
    # common in the official CQL2-Text corpus (T_DURING, T_CONTAINS…).
    interval: list[str | Expression] | None = None

    def to_cql2_json(self) -> dict[str, Any]:
        """Serialise as CQL2-JSON temporal literal."""
        if self.temporal_type == "interval" and self.interval:
            from .to_json import expression_to_json

            return {
                "interval": [
                    v if isinstance(v, str) else expression_to_json(v)
                    for v in self.interval
                ]
            }
        elif self.value:
            return {self.temporal_type: self.value}
        return {}

    @classmethod
    def from_cql2_json(cls, data: dict[str, Any]) -> TemporalLiteral:
        """Deserialise from a CQL2-JSON temporal literal."""
        if "date" in data:
            return cls(temporal_type="date", value=data["date"])
        elif "timestamp" in data:
            return cls(temporal_type="timestamp", value=data["timestamp"])
        elif "interval" in data:
            return cls(temporal_type="interval", interval=data["interval"])
        raise ValueError(f"Unknown temporal literal format: {data}")


class AzimuthElevation(Expression):
    """Azimuth and elevation for directional calculations."""

    azimuth: float | NumericExpression
    elevation: float | NumericExpression


# =====================================================
# Color and Graphics Expressions
# =====================================================


class ColorExpression(Expression):
    """Base class for color expressions."""

    type: ExpressionType = ExpressionType.CONSTANT  # Default type for color constants


class Color0to1(ColorExpression):
    """Color with components in 0-1 range: {"r": 0.5, "g": 0.3, "b": 0.8, "a"?: 1.0}."""

    r: float | int = Field(ge=0.0, le=1.0)
    g: float | int = Field(ge=0.0, le=1.0)
    b: float | int = Field(ge=0.0, le=1.0)
    a: float | int | None = Field(None, ge=0.0, le=1.0)


class ColorComponent0to255(ColorExpression):
    """Color with 0-255 components: {"r": 128, "g": 76, "b": 204, "a"?: 255}."""

    r: int | NumericExpression = Field(ge=0, le=255)
    g: int | NumericExpression = Field(ge=0, le=255)
    b: int | NumericExpression = Field(ge=0, le=255)
    a: int | NumericExpression | None = Field(None, ge=0, le=255)


class HexNumber(ColorExpression):
    """Hexadecimal color: {"hex": "#FF5733"}."""

    hex: str = Field(pattern=r"^#[0-9A-Fa-f]{6}([0-9A-Fa-f]{2})?$")


class ZeroToOne(NumericExpression):
    """Numeric value constrained to 0-1 range."""

    value: float | NumericExpression = Field(ge=0.0, le=1.0)


class Shape(Expression):
    """Shape definition for graphics."""

    shape_type: Literal["circle", "square", "triangle", "star", "cross", "diamond"]
    size: float | NumericExpression | None = None
    properties: dict[str, Any] | None = None


# =====================================================
# Alignment and Layout Expressions
# =====================================================


class HAlignment(Expression):
    """Horizontal alignment: left, center, right."""

    value: Literal["left", "center", "right"]


class VAlignment(Expression):
    """Vertical alignment: top, middle, bottom."""

    value: Literal["top", "middle", "bottom"]


class Horizontal(Expression):
    """Horizontal positioning/direction."""

    value: float | str | NumericExpression


class Vertical(Expression):
    """Vertical positioning/direction."""

    value: float | str | NumericExpression


class Dot(Expression):
    """Dot notation access for nested properties."""

    path: list[str] = Field(min_length=2)  # e.g., ['dataLayer', 'type']

    def to_string(self) -> str:
        """Render the member path as a dotted string (e.g. ``dataLayer.type``)."""
        return ".".join(self.path)


# Array Expressions
class ArrayPredicate(BoolExpression):
    """Array-based predicates.

    OGC CQL2-JSON format: {"op": "a_contains", "args": [arrayA, arrayB]}
    """

    op: Literal[
        "a_equals",
        "a_contains",
        "a_containedby",
        "a_overlaps",
        # Legacy bare names
        "aequals",
        "acontains",
        "acontainedby",
        "aoverlaps",
    ]
    args: list[Expression]


# =====================================================
# Character Expression Types
# =====================================================
# AnyExpressionWrapper is defined below, under "Polymorphic Expressions".


class CharacterExpression(Expression):
    """Base class for character/string expressions from JSON schema."""

    type: ExpressionType = (
        ExpressionType.FUNCTION_CALL
    )  # Default type for function-like expressions


class CaseiExpression(CharacterExpression):
    """Case-insensitive string expression: {"op": "casei", "args": [string]}."""

    op: Literal["casei"] = "casei"
    args: list[Expression] = Field(min_length=1, max_length=1)


class AccentiExpression(CharacterExpression):
    """Accent-insensitive string expression: {"op": "accenti", "args": [string]}."""

    op: Literal["accenti"] = "accenti"
    args: list[Expression] = Field(min_length=1, max_length=1)


class ConcatenateExpression(CharacterExpression):
    """String concatenation: {"op": "concatenate", "args": [str1, str2, ...]}."""

    op: Literal["concatenate"] = "concatenate"
    args: list[Expression] = Field(min_length=2)


class FormatExpression(CharacterExpression):
    """String formatting: {"op": "format", "args": [format_string, ...values]}."""

    op: Literal["format"] = "format"
    args: list[Expression] = Field(min_length=1)


class SubstituteExpression(CharacterExpression):
    """String substitution.

    ``{"op": "substitute", "args": [string, pattern, replacement]}``
    """

    op: Literal["substitute"] = "substitute"
    args: list[Expression] = Field(min_length=3, max_length=3)


class LowerUpperCaseExpression(CharacterExpression):
    """Case conversion: {"op": "lowerCase|upperCase|upper|lower", "args": [string]}."""

    op: Literal["upper", "lower", "upperCase", "lowerCase"]
    args: list[Expression] = Field(min_length=1, max_length=1)


class PatternExpression(CharacterExpression):
    """Pattern matching expression for advanced text operations."""

    type: ExpressionType = ExpressionType.STRING
    pattern: str
    flags: list[str] | None = None


class TextOpPredicate(BoolExpression):
    """Text operation predicates for string comparisons.

    OGC CQL2-JSON: {"op": "contains|startsWith|endsWith", "args": [charExpr, charExpr]}
    """

    op: Literal["contains", "startsWith", "endsWith"]
    args: list[Expression] = Field(min_length=2, max_length=2)


# Update forward references
BinaryComparisonPredicate.model_rebuild()
IsNullPredicate.model_rebuild()
IsInListPredicate.model_rebuild()
IsBetweenPredicate.model_rebuild()
IsLikePredicate.model_rebuild()
TemporalPredicate.model_rebuild()
SpatialPredicate.model_rebuild()
SpatialRelatePredicate.model_rebuild()
GeometryLiteral.model_rebuild()
BboxLiteral.model_rebuild()
TemporalLiteral.model_rebuild()
# Re-rebuild models with Expression operands now that all subtypes are defined
UnaryOperationExpression.model_rebuild()
BinaryOperationExpression.model_rebuild()
ConditionalExpression.model_rebuild()


__all__ = [
    # Original CSCSS expressions
    "Expression",
    "ExpressionType",
    "BinaryOperator",
    "UnaryOperator",
    "IdentifierExpression",
    "ConstantExpression",
    "StringExpression",
    "NullLiteral",
    "MemberAccessExpression",
    "FunctionCallExpression",
    "BinaryOperationExpression",
    "UnaryOperationExpression",
    "ConditionalExpression",
    "ArrayExpression",
    "PropertyAssignment",
    "InstanceExpression",
    "Selector",
    "StylingRuleExpression",
    # JSON Schema expressions
    "BoolExpression",
    "AndOrExpression",
    "NotExpression",
    "NumericExpression",
    "ArithmeticExpression",
    "BitwiseLogical",
    "BitwiseShift",
    "BitwiseNot",
    "ComparisonPredicate",
    "BinaryComparisonPredicate",
    "IsNullPredicate",
    "IsInListPredicate",
    "IsBetweenPredicate",
    "IsLikePredicate",
    "PropertyRef",
    "SystemIdentifier",
    "ScalarExpression",
    "ScalarLiteral",
    "FunctionCallJSON",
    "ConditionalExpressionJSON",
    # Character expressions
    "CharacterExpression",
    "CaseiExpression",
    "AccentiExpression",
    "ConcatenateExpression",
    "FormatExpression",
    "SubstituteExpression",
    "LowerUpperCaseExpression",
    "PatternExpression",
    "TextOpPredicate",
    # Spatial expressions
    "SpatialPredicate",
    "SpatialRelatePredicate",
    "GeometryExpression",
    "GeometryLiteral",
    "BboxLiteral",
    "GeometryBuffer",
    "GeometryManipulationUnary",
    "GeometryManipulationBinary",
    "SpatialInstance",
    "AzimuthElevation",
    # Temporal expressions
    "TemporalExpression",
    "TemporalPredicate",
    "TemporalLiteral",
    "DateInstant",
    "TimestampInstant",
    "DateString",
    "TimestampString",
    "InstantInstance",
    "IntervalInstance",
    "IntervalArray",
    "TemporalInstantExpression",
    "TemporalOperands",
    # Arithmetic expressions
    "ArithmeticOperands",
    "ScalarOperands",
    # Color and graphics expressions
    "ColorExpression",
    "Color0to1",
    "ColorComponent0to255",
    "HexNumber",
    "ZeroToOne",
    "Shape",
    # Alignment and layout expressions
    "HAlignment",
    "VAlignment",
    "Horizontal",
    "Vertical",
    "Dot",
    # Miscellaneous
    "ArrayPredicate",
    # Polymorphic expressions
    "AnyExpressionType",
    "AnyExpressionWrapper",
    "TypedArray",
    "IdOrFnExpression",
]


# =====================================================
# Polymorphic Expressions
# =====================================================


class AnyExpressionWrapper(Expression):
    """Wrapper for AnyExpression with proper Pydantic handling.

    This allows storing any expression type polymorphically.
    """

    type: ExpressionType = ExpressionType.IDENTIFIER
    expression: Any = Field(..., description="Wrapped expression of any type")

    def get_expression_type(self) -> str:
        """Get the actual type of the wrapped expression."""
        return type(self.expression).__name__


# 1.3 TypedArray - Arrays typés avec validation


class TypedArray(Expression):
    """Typed array with validation constraints.

    Provides strict validation of array elements with type checking.
    """

    type: ExpressionType = ExpressionType.ARRAY
    element_type: str = Field(..., description="Expected type of array elements")
    elements: list[Any] = Field(default_factory=list, description="Array elements")
    min_length: int | None = Field(None, ge=0, description="Minimum array length")
    max_length: int | None = Field(None, ge=0, description="Maximum array length")

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


# 1.4 IdOrFnExpression - Union identifier/fonction


class IdOrFnExpressionWrapper(Expression):
    """Wrapper for identifier or function call expressions.

    Provides flexible syntax for identifiants vs function calls.
    """

    type: ExpressionType = ExpressionType.IDENTIFIER
    expression: IdentifierExpression | FunctionCallExpression = Field(
        ..., description="Identifier or function call"
    )

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
AnyExpressionType = (
    # Basic expressions
    IdentifierExpression
    | ConstantExpression
    | StringExpression
    | MemberAccessExpression
    # Function and operation expressions
    | FunctionCallExpression
    | BinaryOperationExpression
    | UnaryOperationExpression
    | ConditionalExpression
    # Collection expressions
    | ArrayExpression
    | InstanceExpression
    # JSON Schema expressions
    | BoolExpression
    | NumericExpression
    | ArithmeticExpression
    | ComparisonPredicate
    # Character expressions
    | CharacterExpression
    | ConcatenateExpression
    | FormatExpression
    # Spatial expressions
    | SpatialPredicate
    | SpatialRelatePredicate
    | GeometryExpression
    | GeometryLiteral
    | BboxLiteral
    # Temporal expressions
    | TemporalExpression
    | TemporalLiteral
    | DateInstant
    # Color expressions
    | ColorExpression
    | Color0to1
    | HexNumber
)

# Convenience type aliases
IdOrFnExpression = IdentifierExpression | FunctionCallExpression
