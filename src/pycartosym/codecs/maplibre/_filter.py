"""MapLibre GL layer ``filter`` ↔ CartoSym selector (CQL2-JSON dict).

MapLibre filters come in two spellings — the *legacy* form
(``["==", "key", value]``) and the *expression* form
(``["==", ["get", "key"], value]``) — plus the combinators ``all`` /
``any`` / ``none``. Both spellings map to the same CQL2-JSON selector
dict that ``StylingRule.selector`` carries
(``{"op": "=", "args": [{"property": "key"}, value]}``).

Special MapLibre keys (``$type``, ``$id``, ``geometry-type``) and
data-driven operands have no CQL2 equivalent and raise
:exc:`NotImplementedError`. A ``sysId dataLayer.id = <name>`` equality
conjunct — the implicit self-reference a CartoSym-CSS ``RuleName[...]``
rule always carries (its parser-generated ``sysId`` twin of the rule's
own name, unrelated to any real per-feature filtering) — is dropped
rather than raised on: this codec has no data-source concept (see
:mod:`.writer`'s module docstring) for a real ``dataLayer.id`` to bind
to, and the value is redundant with the MapLibre layer's own ``id``
regardless (see :func:`strip_datalayer_id`). Any other ``sysId``, or a
``dataLayer.id`` compared with anything but ``=``, still raises — real
information this codec has no target for.
"""

from __future__ import annotations

from typing import Any

from ._zoom import zoom_filter_conjunct

# MapLibre comparison op -> CQL2 op
_CMP: dict[str, str] = {
    "==": "=",
    "!=": "<>",
    "<": "<",
    "<=": "<=",
    ">": ">",
    ">=": ">=",
}
_CMP_INV = {v: k for k, v in _CMP.items()}

_SPECIAL_KEYS = {"$type", "$id"}


# ── MapLibre filter → selector ────────────────────────────────────────────


def _operand_to_property(operand: Any) -> dict[str, str]:
    """A filter operand that names a feature property → ``{"property": name}``."""
    if isinstance(operand, str):
        if operand in _SPECIAL_KEYS:
            raise NotImplementedError(
                f"MapLibre filter key {operand!r} has no CartoSym selector mapping"
            )
        return {"property": operand}
    if (
        isinstance(operand, list)
        and len(operand) == 2
        and operand[0] == "get"
        and isinstance(operand[1], str)
    ):
        return {"property": operand[1]}
    raise NotImplementedError(
        f"MapLibre filter operand {operand!r} is not a plain property reference"
    )


def _literal(operand: Any) -> Any:
    if isinstance(operand, list):
        if len(operand) == 2 and operand[0] == "literal":
            return operand[1]
        raise NotImplementedError(
            f"MapLibre filter value {operand!r} is data-driven — not mapped"
        )
    return operand


def filter_to_selector(mb_filter: list[Any]) -> dict[str, Any]:
    """Convert a MapLibre layer ``filter`` to a CartoSym selector dict."""
    if not isinstance(mb_filter, list) or not mb_filter:
        raise NotImplementedError(f"unrecognised MapLibre filter {mb_filter!r}")

    op = mb_filter[0]
    args = mb_filter[1:]

    if op in ("all", "any"):
        return {
            "op": "and" if op == "all" else "or",
            "args": [filter_to_selector(f) for f in args],
        }
    if op == "none":
        return {
            "op": "not",
            "args": [{"op": "or", "args": [filter_to_selector(f) for f in args]}],
        }
    if op == "!":
        (inner,) = args
        return {"op": "not", "args": [filter_to_selector(inner)]}

    if op in _CMP:
        prop, value = args
        return {
            "op": _CMP[op],
            "args": [_operand_to_property(prop), _literal(value)],
        }

    if op in ("in", "!in"):
        prop, *rest = args
        # legacy: ["in", "k", v1, v2, …] — each remaining arg is a value.
        # expression: ["in", ["get","k"], ["literal", [...]]] — one list arg.
        if len(rest) == 1 and isinstance(rest[0], list):
            values = list(_literal(rest[0]))
        else:
            values = list(rest)
        pred = {"op": "in", "args": [_operand_to_property(prop), values]}
        return {"op": "not", "args": [pred]} if op == "!in" else pred

    if op in ("has", "!has"):
        (prop,) = args
        is_null = {"op": "isNull", "args": [_operand_to_property(prop)]}
        return is_null if op == "!has" else {"op": "not", "args": [is_null]}

    raise NotImplementedError(f"MapLibre filter operator {op!r} is not supported")


def strip_datalayer_id(selector: Any) -> Any:
    """Drop a ``sysId dataLayer.id = <literal>`` conjunct from *selector*.

    Walks the same ``and``-conjunction shape :func:`._zoom.extract_zoom_range`
    does, removing any ``dataLayer.id = <name>`` equality leaf wherever it
    appears (either operand order) and re-collapsing what remains — a
    single surviving conjunct is unwrapped, none leaves ``None``. See the
    module docstring for why this one sysId is dropped rather than raised
    on.
    """
    if not isinstance(selector, dict):
        return selector
    op = selector.get("op")
    if op == "and":
        kept = [
            stripped
            for a in selector.get("args", [])
            if (stripped := strip_datalayer_id(a)) is not None
        ]
        if not kept:
            return None
        if len(kept) == 1:
            return kept[0]
        return {"op": "and", "args": kept}
    if op == "=":
        args = selector.get("args", [])
        if len(args) == 2 and any(
            isinstance(a, dict) and a.get("sysId") == "dataLayer.id" for a in args
        ):
            return None
    return selector


# ── selector → MapLibre filter ───────────────────────────────────────────


def _property_name(arg: Any) -> str:
    if isinstance(arg, dict):
        name = arg.get("property")
        if isinstance(name, str):
            return name
    raise NotImplementedError(
        f"selector operand {arg!r} → MapLibre filter needs a plain property "
        "(sysId / expression operands are not mapped)"
    )


def selector_to_filter(selector: Any) -> list[Any]:
    """Convert a CartoSym selector dict to a MapLibre (expression-form) filter."""
    if not isinstance(selector, dict) or "op" not in selector:
        raise NotImplementedError(
            f"selector {selector!r} → MapLibre filter is not supported"
        )

    # A viz.sd comparison with no minzoom/maxzoom shape (extract_zoom_range
    # already pulled out the two that do) still has an exact MapLibre
    # equivalent via the ["zoom"] filter expression — see
    # ``_zoom.zoom_filter_conjunct``. Checked ahead of the generic
    # property-comparison dispatch below since viz.sd is a sysId, not a
    # feature property.
    zoom_conjunct = zoom_filter_conjunct(selector)
    if zoom_conjunct is not None:
        return zoom_conjunct

    op = selector["op"]
    args = selector.get("args", [])

    if op == "and":
        return ["all", *[selector_to_filter(a) for a in args]]
    if op == "or":
        return ["any", *[selector_to_filter(a) for a in args]]
    if op == "not":
        (inner,) = args
        if isinstance(inner, dict) and inner.get("op") == "isNull":
            # ¬(k is null)  ==  "feature has k"
            return ["has", _property_name(inner["args"][0])]
        if isinstance(inner, dict) and inner.get("op") == "in":
            prop, values = inner["args"]
            return ["!in", ["get", _property_name(prop)], ["literal", list(values)]]
        return ["!", selector_to_filter(inner)]

    if op in _CMP_INV:
        left, right = args
        return [_CMP_INV[op], ["get", _property_name(left)], right]

    if op == "in":
        prop, values = args
        return ["in", ["get", _property_name(prop)], ["literal", list(values)]]
    if op == "isNull":
        return ["!", ["has", _property_name(args[0])]]

    raise NotImplementedError(
        f"selector operator {op!r} → MapLibre filter is not supported"
    )
