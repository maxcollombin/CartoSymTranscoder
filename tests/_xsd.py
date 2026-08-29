"""XML-Schema validation of SLD output against the vendored OGC schemas.

Helper for ``tests/test_sld_xsd.py`` (SLD 1.1.0 / SE 1.1.0) and
``tests/test_sld10_corpus.py`` (SLD 1.0.0) — not a test module itself.

Each schema graph (``tests/schemas/ogc-sld-se-1.1.0/`` and
``tests/schemas/ogc-sld-1.0.0/``) is built once per session, with
``validation='lax'`` because the transitively-imported GML (3.1.1 / 2.1.2)
is not itself strictly XSD-1.0-valid (a well-known upstream defect); a lax
build records those internal defects as warnings instead of aborting, while
still validating instance documents correctly. See each directory's
``README.md``.
"""

from __future__ import annotations

import functools
from pathlib import Path

import xmlschema

_SCHEMAS = Path(__file__).parent / "schemas"
_SE_ENTRY = _SCHEMAS / "ogc-sld-se-1.1.0" / "StyledLayerDescriptor.xsd"
_SLD10_ENTRY = _SCHEMAS / "ogc-sld-1.0.0" / "StyledLayerDescriptor.xsd"


@functools.lru_cache(maxsize=1)
def sld_se_schema() -> xmlschema.XMLSchema:
    """Return the (cached) OGC SLD 1.1.0 / SE 1.1.0 schema."""
    return xmlschema.XMLSchema(str(_SE_ENTRY), validation="lax")


@functools.lru_cache(maxsize=1)
def sld10_schema() -> xmlschema.XMLSchema:
    """Return the (cached) OGC SLD 1.0.0 schema."""
    return xmlschema.XMLSchema(str(_SLD10_ENTRY), validation="lax")


def _errors(schema: xmlschema.XMLSchema, xml: str) -> list[str]:
    errors: list[str] = []
    seen = set()
    for err in schema.iter_errors(xml):
        line = f"{err.reason} | at {err.path}"
        if line not in seen:
            seen.add(line)
            errors.append(line)
    return errors


def sld_validation_errors(xml: str) -> list[str]:
    """Return a list of human-readable SLD 1.1.0 / SE 1.1.0 schema errors for *xml*.

    Empty list means *xml* is a schema-valid SLD document.
    """
    return _errors(sld_se_schema(), xml)


def assert_sld_valid(xml: str, *, label: str = "") -> None:
    """Assert that *xml* is a schema-valid SLD 1.1.0 / SE 1.1.0 document."""
    _assert_valid(sld_validation_errors(xml), "SLD/SE", label)


def assert_sld10_valid(xml: str, *, label: str = "") -> None:
    """Assert that *xml* is a schema-valid SLD 1.0.0 document."""
    _assert_valid(_errors(sld10_schema(), xml), "SLD 1.0.0", label)


def _assert_valid(errors: list[str], kind: str, label: str) -> None:
    if errors:
        prefix = f"{label}: " if label else ""
        raise AssertionError(
            prefix
            + f"{len(errors)} {kind} schema violation(s):\n  "
            + "\n  ".join(errors)
        )
