#!/usr/bin/env python3
"""Regenerate the committed golden CS-JSON fixtures from ``examples/*.cscss``.

Run after an intentional change to the CSCSS -> CS-JSON output, then review
the diff before committing::

    uv run python tests/fixtures/expected/regenerate.py
    git diff tests/fixtures/expected/

``tests/test_roundtrip.py`` and ``tests/test_csjson_strictness.py`` compare
the live converter output against these files, so an unreviewed change here
would mask a regression.
"""

from __future__ import annotations

import json
from pathlib import Path

from pycartosym.converter import Converter

ROOT = Path(__file__).resolve().parents[3]
EXAMPLES_DIR = ROOT / "examples"
EXPECTED_DIR = ROOT / "tests" / "fixtures" / "expected"


def main() -> None:
    converter = Converter()
    for cscss in sorted(EXAMPLES_DIR.glob("*.cscss")):
        data = converter.cscss_to_csjson(cscss)
        out = EXPECTED_DIR / f"{cscss.stem}.cs.json"
        out.write_text(
            json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        print(f"wrote {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
