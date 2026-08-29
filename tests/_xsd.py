"""XML-Schema validation of SLD/SE output against the vendored OGC schemas.

Helper for ``tests/test_sld_xsd.py`` — not a test module itself.

The schema graph (``tests/schemas/ogc-sld-se-1.1.0/``) is built once per
session. It is built with ``validation='lax'`` because GML 3.1.1 — pulled
in transitively by SE 1.1.0 — is not itself strictly XSD-1.0-valid (a
well-known upstream defect); lax build records those internal defects as
warnings instead of aborting, while still validating instance documents
correctly. See that directory's ``README.md``.
"""

from __future__ import annotations

import functools
from pathlib import Path

import xmlschema

_SCHEMA_ROOT = Path(__file__).parent / "schemas" / "ogc-sld-se-1.1.0"
_ENTRY_POINT = _SCHEMA_ROOT / "StyledLayerDescriptor.xsd"


@functools.lru_cache(maxsize=1)
def sld_se_schema() -> xmlschema.XMLSchema:
    """Return the (cached) OGC SLD 1.1.0 / SE 1.1.0 schema."""
    return xmlschema.XMLSchema(str(_ENTRY_POINT), validation="lax")


def sld_validation_errors(xml: str) -> list[str]:
    """Return a list of human-readable schema-validation errors for *xml*.

    Empty list means *xml* is a schema-valid SLD document.
    """
    errors: list[str] = []
    seen = set()
    for err in sld_se_schema().iter_errors(xml):
        line = f"{err.reason} | at {err.path}"
        if line not in seen:
            seen.add(line)
            errors.append(line)
    return errors


def assert_sld_valid(xml: str, *, label: str = "") -> None:
    """Assert that *xml* is a schema-valid SLD 1.1.0 / SE 1.1.0 document."""
    errors = sld_validation_errors(xml)
    if errors:
        prefix = f"{label}: " if label else ""
        raise AssertionError(
            prefix
            + f"{len(errors)} SLD/SE schema violation(s):\n  "
            + "\n  ".join(errors)
        )
