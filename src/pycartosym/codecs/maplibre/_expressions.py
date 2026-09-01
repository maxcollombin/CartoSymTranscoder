"""MapLibre value-expression arrays <-> CartoSym value expressions.

Scope: the six MapLibre operators this pass targets — ``get``, ``case``,
``match``, ``interpolate``, ``step``, ``coalesce`` — mapped onto the typed
models in :mod:`pycartosym.models.value_expressions`. Every other
MapLibre expression operator (comparisons, ``all``/``any``/``!``, ``zoom``,
the arithmetic/string operators, ``interpolate-hcl``/``-lab``, ``let``/
``var``, ...) raises :exc:`NotImplementedError` naming the operator — a
deliberate scope boundary, not an oversight.

Legacy MapLibre "zoom functions" (``{"stops": [...]}``) are a separate,
unrelated value shape and stay out of scope here too (rejected in
``_layers.py`` before this module ever sees them).
"""

from __future__ import annotations

from typing import Any

from ...models.value_expressions import (
    CaseExpression,
    CoalesceExpression,
    InterpolateExpression,
    MatchExpression,
    PropertyRef,
    StepExpression,
)

# A MapLibre value that is already a plain JSON scalar, not an expression.
_SCALAR = (str, int, float, bool, type(None))

_INTERPOLATION_TYPES = frozenset({"linear", "exponential", "cubic-bezier"})


def maplibre_expr_to_value(value: Any, prop: str) -> Any:
    """Convert one MapLibre paint/layout value to its CartoSym equivalent.

    A literal (number / string / bool / ``None``) passes through unchanged.
    A MapLibre expression array becomes the matching dict shape
    (``{"property": ...}`` for ``get``, ``{"op": ..., "args": [...]}`` for
    the other five in-scope operators) for the Pydantic ``Style`` model to
    validate into a typed :mod:`.value_expressions` model downstream.

    Raises:
        NotImplementedError: *value* is a MapLibre expression using an
            operator this codec does not map.
    """
    if isinstance(value, _SCALAR):
        return value
    if not isinstance(value, list) or not value:
        raise NotImplementedError(
            f"{prop}: {value!r} is not a supported MapLibre value or expression"
        )

    op, args = value[0], value[1:]

    if op == "literal":
        if len(args) != 1:
            raise NotImplementedError(f"{prop}: malformed ['literal', ...] expression")
        return args[0]
    if op == "get":
        if len(args) != 1 or not isinstance(args[0], str):
            raise NotImplementedError(
                f"{prop}: only single-argument ['get', 'property'] maps in this codec"
            )
        return {"property": args[0]}
    if op == "case":
        if len(args) < 3 or len(args) % 2 == 0:
            raise NotImplementedError(
                f"{prop}: malformed ['case', ...] expression (need "
                "cond, out, ..., fallback)"
            )
        return {"op": "case", "args": [maplibre_expr_to_value(a, prop) for a in args]}
    if op == "match":
        return _match_to_value(args, prop)
    if op == "step":
        if len(args) < 2 or len(args) % 2 != 0:
            raise NotImplementedError(
                f"{prop}: malformed ['step', ...] expression (need "
                "input, output0, stop1, output1, ...)"
            )
        return {"op": "step", "args": [maplibre_expr_to_value(a, prop) for a in args]}
    if op == "interpolate":
        return _interpolate_to_value(args, prop)
    if op == "coalesce":
        if not args:
            raise NotImplementedError(f"{prop}: malformed ['coalesce', ...] expression")
        return {
            "op": "coalesce",
            "args": [maplibre_expr_to_value(a, prop) for a in args],
        }
    raise NotImplementedError(
        f"{prop}: MapLibre expression operator {op!r} is not mapped by this codec"
    )


def _match_label(label: Any, prop: str) -> Any:
    """Return a ``match`` label: a literal, or a literal array of literals."""
    if isinstance(label, list):
        if not all(isinstance(item, _SCALAR) for item in label):
            raise NotImplementedError(
                f"{prop}: ['match', ...] label group {label!r} must be literal values"
            )
        return label
    if isinstance(label, _SCALAR):
        return label
    raise NotImplementedError(
        f"{prop}: ['match', ...] label {label!r} must be a literal"
    )


def _match_to_value(args: list[Any], prop: str) -> dict[str, Any]:
    if len(args) < 3:
        raise NotImplementedError(f"{prop}: malformed ['match', ...] expression")
    body, fallback = args[1:-1], args[-1]
    if len(body) % 2 != 0:
        raise NotImplementedError(f"{prop}: malformed ['match', ...] expression")
    out: list[Any] = [maplibre_expr_to_value(args[0], prop)]
    for i in range(0, len(body), 2):
        out.append(_match_label(body[i], prop))
        out.append(maplibre_expr_to_value(body[i + 1], prop))
    out.append(maplibre_expr_to_value(fallback, prop))
    return {"op": "match", "args": out}


def _interpolate_to_value(args: list[Any], prop: str) -> dict[str, Any]:
    if len(args) < 3:
        raise NotImplementedError(f"{prop}: malformed ['interpolate', ...] expression")
    interp_spec, input_expr, *rest = args
    if not isinstance(interp_spec, list) or not interp_spec:
        raise NotImplementedError(
            f"{prop}: ['interpolate', ...] needs an interpolation-type array"
        )
    interp_type = interp_spec[0]
    if interp_type not in _INTERPOLATION_TYPES:
        raise NotImplementedError(
            f"{prop}: interpolation type {interp_type!r} is not mapped by this codec"
        )

    out: dict[str, Any] = {
        "op": "interpolate",
        "interpolation": interp_type,
        "args": [maplibre_expr_to_value(input_expr, prop)]
        + [maplibre_expr_to_value(a, prop) for a in rest],
    }
    if interp_type == "exponential":
        if len(interp_spec) != 2 or not isinstance(interp_spec[1], (int, float)):
            raise NotImplementedError(
                f"{prop}: ['exponential', base] needs a numeric base"
            )
        out["base"] = interp_spec[1]
    elif interp_type == "cubic-bezier":
        if len(interp_spec) != 5 or not all(
            isinstance(v, (int, float)) for v in interp_spec[1:]
        ):
            raise NotImplementedError(
                f"{prop}: ['cubic-bezier', x1, y1, x2, y2] needs 4 numeric "
                "control points"
            )
        out["controlPoints"] = list(interp_spec[1:])
    return out


def value_to_maplibre_expr(value: Any, prop: str) -> Any:
    """Inverse of :func:`maplibre_expr_to_value`.

    Raises:
        NotImplementedError: *value* is not a literal or one of the
            typed :mod:`.value_expressions` models this codec maps.
    """
    if isinstance(value, PropertyRef):
        return ["get", value.property]
    if isinstance(value, CaseExpression):
        return ["case", *(value_to_maplibre_expr(a, prop) for a in value.args)]
    if isinstance(value, MatchExpression):
        return _match_to_expr(value, prop)
    if isinstance(value, StepExpression):
        return ["step", *(value_to_maplibre_expr(a, prop) for a in value.args)]
    if isinstance(value, InterpolateExpression):
        return _interpolate_to_expr(value, prop)
    if isinstance(value, CoalesceExpression):
        return ["coalesce", *(value_to_maplibre_expr(a, prop) for a in value.args)]
    if isinstance(value, _SCALAR):
        return value
    raise NotImplementedError(
        f"{prop}: {value!r} has no MapLibre expression mapping in this codec"
    )


def _match_to_expr(value: MatchExpression, prop: str) -> list[Any]:
    args = value.args
    out: list[Any] = ["match", value_to_maplibre_expr(args[0], prop)]
    body, fallback = args[1:-1], args[-1]
    for i in range(0, len(body), 2):
        out.append(body[i])  # label(s): already a plain literal / literal list
        out.append(value_to_maplibre_expr(body[i + 1], prop))
    out.append(value_to_maplibre_expr(fallback, prop))
    return out


def _interpolate_to_expr(value: InterpolateExpression, prop: str) -> list[Any]:
    if value.interpolation == "exponential":
        base = value.base if value.base is not None else 1
        interp_spec: list[Any] = ["exponential", base]
    elif value.interpolation == "cubic-bezier":
        if not value.control_points or len(value.control_points) != 4:
            raise NotImplementedError(
                f"{prop}: cubic-bezier interpolation needs 4 control points"
            )
        interp_spec = ["cubic-bezier", *value.control_points]
    else:
        interp_spec = ["linear"]
    return [
        "interpolate",
        interp_spec,
        *(value_to_maplibre_expr(a, prop) for a in value.args),
    ]
