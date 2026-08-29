"""Regression guard for the ANTLR-tree expression parser (ROADMAP §4.2 / Phase A1).

``ExpressionParser`` historically re-parsed selector *text* by hand instead of
walking the ``ExpressionContext`` parse tree the grammar already built. This
module locks the observable contract of that refactor:

1. **Golden snapshot** — every ``selector`` dict emitted for the real
   ``examples/*.cscss`` corpus (keys ``file:*``) *plus* a set of synthetic selector
   snippets (keys ``expr:*``) is snapshotted in
   ``tests/fixtures/expression_selectors_golden.json``. The ``file:*`` entries
   are the hard no-regression contract; the ``expr:*`` entries are allowed to
   *improve* (the pre-refactor parser mangles several of them). Regenerate with
   ``CARTOSYM_UPDATE_GOLDEN=1 uv run pytest -k golden_selector`` and review the
   diff.
2. **Structural assertions** — targeted checks on the constructs the tree walk
   is meant to get right.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

from cartosym_transcoder.converter import Converter

ROOT = Path(__file__).resolve().parent.parent
EXAMPLES_DIR = ROOT / "examples"
GOLDEN = (
    Path(__file__).resolve().parent / "fixtures" / "expression_selectors_golden.json"
)

# Synthetic selector expressions exercising every branch of the expression
# grammar. Each is spliced into a minimal bare ``[expr] { ... }`` rule.
SYNTHETIC_SELECTORS = [
    "a = 1",
    "a = 1 and b = 2",
    "a = 1 and b = 2 and c = 3",
    "a = 1 or b = 2 or c = 3",
    "a = 1 and (b = 2 or c = 3)",
    "(a = 1) or (b = 2)",
    "not (a = 1)",
    "not a = 1",
    "name = 'a and b'",
    "name = 'x or y' or other = 1",
    "a.b.c = 1",
    "dataLayer.type = vector",
    "viz.sd < 200000",
    "viz.sd >= 1000 and viz.sd < 5000",
    "x between 1 and 10",
    "x not between 1 and 10",
    "kind in ('a', 'b', 'c')",
    "kind not in ('a', 'b')",
    "label like 'A%'",
    "label not like '%z'",
    "descr is null",
    "descr is not null",
    "active = true",
    "flag = false",
    "ref = null",
    "area = width * height + margin",
    "rank = (a + b) * c",
    "S_INTERSECTS(geom, BBOX(0, 0, 10, 10))",
    "T_BEFORE(validFrom, DATE('2020-01-01'))",
    "CONTAINS(name, 'ville')",
    "casei(name) like casei('paris')",
]


def _collect_selectors(node, out):
    """Recursively pull every ``selector`` value out of a CS-JSON structure."""
    if isinstance(node, dict):
        if "selector" in node:
            out.append(node["selector"])
        for value in node.values():
            _collect_selectors(value, out)
    elif isinstance(node, list):
        for item in node:
            _collect_selectors(item, out)


def _one_selector(conv: Converter, expr: str):
    cscss = f"[{expr}]\n{{\n   visibility: true;\n}}\n"
    result = conv.cscss_to_csjson(cscss)
    found: list = []
    _collect_selectors(result, found)
    assert len(found) == 1, f"expected exactly one selector for {expr!r}, got {found!r}"
    return found[0]


def _snapshot() -> dict:
    conv = Converter()
    snap: dict = {}

    for cscss in sorted(EXAMPLES_DIR.glob("*.cscss")):
        try:
            result = conv.cscss_to_csjson(cscss)
            found: list = []
            _collect_selectors(result, found)
            snap[f"file:{cscss.name}"] = found
        except Exception as exc:  # noqa: BLE001 - recorded, not raised
            snap[f"file:{cscss.name}"] = {"error": f"{type(exc).__name__}: {exc}"}

    for expr in SYNTHETIC_SELECTORS:
        try:
            snap[f"expr:{expr}"] = _one_selector(conv, expr)
        except Exception as exc:  # noqa: BLE001 - recorded, not raised
            snap[f"expr:{expr}"] = {"error": f"{type(exc).__name__}: {exc}"}

    return snap


def test_golden_selector_snapshot():
    """``file:*`` selector serialization is byte-stable against the golden.

    ``expr:*`` drift is reported as a non-fatal warning-style assertion list so
    intentional improvements are visible without blocking.
    """
    current = _snapshot()

    if os.environ.get("CARTOSYM_UPDATE_GOLDEN") == "1" or not GOLDEN.exists():
        GOLDEN.parent.mkdir(parents=True, exist_ok=True)
        GOLDEN.write_text(json.dumps(current, indent=2, sort_keys=True) + "\n")
        if os.environ.get("CARTOSYM_UPDATE_GOLDEN") != "1":
            pytest.fail(f"golden snapshot created at {GOLDEN} — inspect it and re-run")
        return

    expected = json.loads(GOLDEN.read_text())

    file_keys = sorted(k for k in expected if k.startswith("file:"))
    for key in file_keys:
        assert current.get(key) == expected[key], f"REGRESSION: {key!r} changed"

    expr_drift = [
        k for k in expected if k.startswith("expr:") and current.get(k) != expected[k]
    ]
    if expr_drift:
        # Not a hard failure: synthetic-snippet output is expected to improve.
        print("\nexpr:* snapshot drift (review & regenerate golden if intended):")
        for k in expr_drift:
            print(
                f"  {k}\n    was: {json.dumps(expected[k])}\n    now: "
                f"{json.dumps(current.get(k))}"
            )


# ---------------------------------------------------------------------------
# Structural assertions
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def convert_selector():
    conv = Converter()
    return lambda expr: _one_selector(conv, expr)


def test_and_chain_is_left_associative(convert_selector):
    sel = convert_selector("a = 1 and b = 2 and c = 3")
    assert sel["op"] == "and"
    assert sel["args"][0]["op"] == "and"  # ((a and b) and c)
    assert sel["args"][1]["args"][0] == {"property": "c"}


def test_quoted_operator_not_split(convert_selector):
    sel = convert_selector("name = 'a and b'")
    assert sel["op"] == "="
    assert sel["args"][1] == "a and b"


def test_between_predicate(convert_selector):
    sel = convert_selector("x between 1 and 10")
    assert sel["op"] == "between"
    assert sel["args"][0] == {"property": "x"}
    assert sel["args"][1:] == [1, 10]


def test_not_between_predicate(convert_selector):
    sel = convert_selector("x not between 1 and 10")
    assert sel["op"] == "not"
    assert sel["args"][0]["op"] == "between"


def test_in_list_predicate(convert_selector):
    sel = convert_selector("kind in ('a', 'b', 'c')")
    assert sel["op"] == "in"
    assert sel["args"][0] == {"property": "kind"}
    assert sel["args"][1] == ["a", "b", "c"]


def test_not_in_list_predicate(convert_selector):
    sel = convert_selector("kind not in ('a', 'b')")
    assert sel["op"] == "not"
    assert sel["args"][0]["op"] == "in"
    assert sel["args"][0]["args"][1] == ["a", "b"]


def test_like_predicate_keeps_string_pattern(convert_selector):
    sel = convert_selector("label like 'A%'")
    assert sel["op"] == "like"
    assert sel["args"][1] == "A%"


def test_is_null_predicate(convert_selector):
    sel = convert_selector("descr is null")
    assert sel["op"] == "isNull"
    assert sel["args"][0] == {"property": "descr"}


def test_is_not_null_predicate(convert_selector):
    sel = convert_selector("descr is not null")
    assert sel["op"] == "not"
    assert sel["args"][0]["op"] == "isNull"


def test_boolean_and_null_literals(convert_selector):
    assert convert_selector("active = true")["args"][1] is True
    assert convert_selector("flag = false")["args"][1] is False
    assert convert_selector("ref = null")["args"][1] is None


def test_member_access_chain(convert_selector):
    sel = convert_selector("a.b.c = 1")
    assert sel["op"] == "="
    assert sel["args"][0] == {"property": "a.b.c"}


def test_parenthesised_groups(convert_selector):
    sel = convert_selector("(a = 1) or (b = 2)")
    assert sel["op"] == "or"
    assert sel["args"][0]["op"] == "="
    assert sel["args"][1]["op"] == "="


def test_arithmetic_precedence(convert_selector):
    sel = convert_selector("area = width * height + margin")
    assert sel["op"] == "="
    rhs = sel["args"][1]
    assert rhs["op"] == "+"  # (width * height) + margin
    assert rhs["args"][0]["op"] == "*"


def test_parenthesised_arithmetic(convert_selector):
    sel = convert_selector("rank = (a + b) * c")
    rhs = sel["args"][1]
    assert rhs["op"] == "*"
    assert rhs["args"][0]["op"] == "+"
