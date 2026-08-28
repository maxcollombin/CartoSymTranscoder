"""CQL2 operator / function vocabulary — single source of truth.

The CartoSym-CSS grammar parses every function call as a generic
``IDENTIFIER LPAR arguments RPAR`` — it carries **no** CQL2 semantics. The
transcoder therefore needs its own notion of "which identifier names are
CQL2 predicates / functions". Rather than hand-maintaining string lists in
the parser (which drift from the standard), these sets are **derived from
the Pydantic models** in :mod:`.models.expressions`: every predicate model
declares its accepted ``op`` values as a ``typing.Literal``, and those
models are separately validated against the OGC CS-JSON schema
(``tests/test_csjson_strictness.py``). The models are thus the reconciled,
authoritative vocabulary.

Nothing here is a magic string except the two OGC primitives that are not
modelled as an ``op`` enum (WKT geometry type names / temporal-literal
constructors), and those are themselves derived from the relevant model
``Literal`` fields where possible.
"""

from __future__ import annotations

from typing import get_args

from .models.expressions import (
    AccentiExpression,
    ArrayPredicate,
    BinaryOperator,
    CaseiExpression,
    ConcatenateExpression,
    FormatExpression,
    GeometryBuffer,
    GeometryLiteral,
    GeometryManipulationBinary,
    GeometryManipulationUnary,
    LowerUpperCaseExpression,
    SpatialPredicate,
    SpatialRelatePredicate,
    SubstituteExpression,
    TemporalLiteral,
    TemporalPredicate,
    TextOpPredicate,
)


def _ops(model: type, prefix: str = "") -> frozenset[str]:
    """Lower-cased ``op`` ``Literal`` values declared by *model*.

    ``prefix`` restricts to the canonical CQL2 spelling (``s_`` / ``t_`` /
    ``a_``) and drops the models' back-compat bare aliases, which must not
    trigger predicate dispatch from raw CartoSym-CSS text.
    """
    return frozenset(
        v
        for v in (str(x).lower() for x in get_args(model.model_fields["op"].annotation))
        if v.startswith(prefix)
    )


def _canon(model: type) -> dict[str, str]:
    """``lower-case -> declared casing`` map for *model*'s ``op`` values."""
    return {
        str(v).lower(): str(v) for v in get_args(model.model_fields["op"].annotation)
    }


# ── Predicate / function name sets (for dispatch) ──────────────────────────
SPATIAL_PREDICATES = _ops(SpatialPredicate, "s_")
TEMPORAL_PREDICATES = _ops(TemporalPredicate, "t_")
ARRAY_PREDICATES = _ops(ArrayPredicate, "a_")
TEXT_OP_PREDICATES = _ops(TextOpPredicate)
CHARACTER_FUNCTIONS = frozenset().union(
    _ops(CaseiExpression),
    _ops(AccentiExpression),
    _ops(LowerUpperCaseExpression),
    _ops(ConcatenateExpression),
    _ops(SubstituteExpression),
    _ops(FormatExpression),
)
GEOM_MANIPULATION_UNARY = _ops(GeometryManipulationUnary, "s_")
GEOM_MANIPULATION_BINARY = _ops(GeometryManipulationBinary, "s_")
GEOM_BUFFER = _ops(GeometryBuffer, "s_")
SPATIAL_RELATE = next(iter(_ops(SpatialRelatePredicate)))  # "s_relate"

# ── Canonicalisation maps (lower-case input -> CQL2-JSON casing) ───────────
SPATIAL_CANON = _canon(SpatialPredicate)
TEMPORAL_CANON = _canon(TemporalPredicate)
ARRAY_CANON = _canon(ArrayPredicate)
TEXT_OP_CANON = _canon(TextOpPredicate)
LOWER_UPPER_CANON = _canon(LowerUpperCaseExpression)
GEOM_UNARY_CANON = _canon(GeometryManipulationUnary)
GEOM_BINARY_CANON = _canon(GeometryManipulationBinary)

# ── OGC primitives that are not an ``op`` enum ────────────────────────────
# WKT geometry type names <-> GeoJSON ``type``, from GeometryLiteral.geom_type.
WKT_TO_GEOJSON = {
    g.lower(): g for g in get_args(GeometryLiteral.model_fields["geom_type"].annotation)
}
WKT_TYPES = frozenset(WKT_TO_GEOJSON)
# Temporal-literal constructors, from TemporalLiteral.temporal_type.
TEMPORAL_LITERAL_NAMES = frozenset(
    str(v).lower()
    for v in get_args(TemporalLiteral.model_fields["temporal_type"].annotation)
)
# BBOX(...) is a CQL2-Text function keyword (OGC 21-065r2 §A) mapping to
# BboxLiteral, which has no ``op`` field.
BBOX = "bbox"

# ── Everything ``_dispatch_call_ctx`` should treat as a known CQL2 call ────
KNOWN_CQL2_CALLS = frozenset().union(
    SPATIAL_PREDICATES,
    {SPATIAL_RELATE},
    TEMPORAL_PREDICATES,
    ARRAY_PREDICATES,
    TEXT_OP_PREDICATES,
    CHARACTER_FUNCTIONS,
    GEOM_MANIPULATION_UNARY,
    GEOM_MANIPULATION_BINARY,
    GEOM_BUFFER,
    WKT_TYPES,
    TEMPORAL_LITERAL_NAMES,
    {BBOX},
)

# ── Grammar operator token -> internal BinaryOperator ─────────────────────
# Keyed by the generated ``arithmeticOperator*`` context accessor name, so
# the mapping follows the grammar's token *identifiers* rather than their
# literal text (``IDIV`` stays ``IDIV`` even if its spelling changes).
ARITH_MUL_BY_TOKEN = {
    "MUL": BinaryOperator.MULTIPLY,
    "DIV": BinaryOperator.DIVIDE,
    "IDIV": BinaryOperator.INTEGER_DIVIDE,
    "MOD": BinaryOperator.MODULO,
}
ARITH_ADD_BY_TOKEN = {
    "PLUS": BinaryOperator.ADD,
    "MINUS": BinaryOperator.SUBTRACT,
}
