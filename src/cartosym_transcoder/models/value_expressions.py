"""Property-driven value expressions for symbolizer properties.

MapLibre GL styles let paint/layout properties be driven by data through
expression arrays (``["get", "prop"]``, ``["case", ...]``, ``["match", ...]``,
``["interpolate", ...]``, ``["step", ...]``, ``["coalesce", ...]``). The
CartoSym-JSON schema has no native construct for most of these MapLibre
operators — only a generic function-call container
(``{"op": ..., "args": [...]}``) and a property reference
(``{"property": "..."}``, schema def ``propertyRef``).

This module gives each of those MapLibre operators its own typed Pydantic
model layered over that generic container — the same pattern already used
in :mod:`cartosym_transcoder.cql2.model` for e.g. ``ArithmeticExpression``
or ``BitwiseLogical`` (a fixed ``Literal`` ``op`` over a generic op/args
shape). ``PropertyRef`` maps 1:1 onto the schema's own ``propertyRef``; the
other five have no CartoSym-JSON equivalent and serialise as an ordinary
``functionCall`` — an honest, lossless pass-through, not an invented
mapping.

Deliberately **not** placed in :mod:`cartosym_transcoder.cql2.model`: that
module is scoped to CQL2 (OGC 21-065r2), a standalone standard, and
``case``/``match``/``step``/``interpolate``/``coalesce`` are MapLibre Style
Spec vocabulary, not CQL2 vocabulary.
"""

from __future__ import annotations

from typing import Literal

from pydantic import Field, field_validator

from .base import BaseCartoSymModel


class PropertyRef(BaseCartoSymModel):
    """Property reference: ``{"property": "name"}`` (MapLibre ``["get", "name"]``).

    Maps 1:1 onto the CartoSym-JSON schema's ``propertyRef`` definition.
    """

    property: str


class CaseExpression(BaseCartoSymModel):
    """MapLibre ``["case", cond1, out1, cond2, out2, ..., fallback]``."""

    op: Literal["case"] = "case"
    args: list[ValueExpressionArg] = Field(
        min_length=3, description="cond1, out1, cond2, out2, ..., fallback"
    )

    @field_validator("args")
    @classmethod
    def _odd_length(cls, v: list) -> list:
        if len(v) % 2 == 0:
            raise ValueError(
                "case: args must have an odd length "
                "(cond, out, ..., fallback pairs plus a trailing fallback)"
            )
        return v


class MatchExpression(BaseCartoSymModel):
    """MapLibre ``["match", input, label1, out1, label2, out2, ..., fallback]``.

    A ``label`` may itself be a list of literals (several input values
    sharing one output) — MapLibre's own shorthand, kept as a plain
    ``list`` here rather than a nested expression.
    """

    op: Literal["match"] = "match"
    args: list[ValueExpressionArg | list[str | int | float | bool]] = Field(
        min_length=4, description="input, label, out, ..., fallback"
    )

    @field_validator("args")
    @classmethod
    def _pair_shape(cls, v: list) -> list:
        if (len(v) - 2) % 2 != 0:
            raise ValueError("match: args must be [input, label, out, ..., fallback]")
        return v


class StepExpression(BaseCartoSymModel):
    """MapLibre ``["step", input, output0, stop1, output1, ...]``."""

    op: Literal["step"] = "step"
    args: list[ValueExpressionArg] = Field(
        min_length=2, description="input, output0, stop1, output1, ..."
    )

    @field_validator("args")
    @classmethod
    def _even_length(cls, v: list) -> list:
        if len(v) % 2 != 0:
            raise ValueError(
                "step: args must have an even length "
                "(input, output0, then stop/output pairs)"
            )
        return v


class InterpolateExpression(BaseCartoSymModel):
    """MapLibre ``["interpolate", [interpolation, ...], input, stop1, output1, ...]``.

    The interpolation-type sub-array is unpacked into ``interpolation`` /
    ``base`` / ``control_points``; ``args`` keeps the remaining
    ``input, stop1, output1, ...`` sequence.
    """

    op: Literal["interpolate"] = "interpolate"
    interpolation: Literal["linear", "exponential", "cubic-bezier"] = "linear"
    base: float | None = Field(None, description="Exponential interpolation base")
    control_points: list[float] | None = Field(
        None, alias="controlPoints", description="Cubic-bezier control points"
    )
    args: list[ValueExpressionArg] = Field(
        min_length=3, description="input, stop1, output1, ..."
    )

    @field_validator("args")
    @classmethod
    def _odd_length(cls, v: list) -> list:
        if len(v) % 2 == 0:
            raise ValueError(
                "interpolate: args must have an odd length "
                "(input, then stop/output pairs)"
            )
        return v


class CoalesceExpression(BaseCartoSymModel):
    """MapLibre ``["coalesce", e1, e2, ...]`` — first non-null value."""

    op: Literal["coalesce"] = "coalesce"
    args: list[ValueExpressionArg] = Field(min_length=1)


ValueExpression = (
    PropertyRef
    | CaseExpression
    | MatchExpression
    | StepExpression
    | InterpolateExpression
    | CoalesceExpression
)
"""Any of the typed MapLibre-derived value expressions."""

ValueExpressionArg = ValueExpression | bool | int | float | str | None
"""An expression argument: a nested expression, or a JSON literal."""

for _cls in (
    CaseExpression,
    MatchExpression,
    StepExpression,
    InterpolateExpression,
    CoalesceExpression,
):
    _cls.model_rebuild()
del _cls
