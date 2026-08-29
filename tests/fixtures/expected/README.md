# Golden CS-JSON fixtures

One `<stem>.cs.json` per `examples/<stem>.cscss`, holding the expected output
of `Converter.cscss_to_csjson`.

Used by:

- `tests/test_roundtrip.py` — forward conversion must equal the golden;
  write-back (`golden → cscss → json`) must equal the forward result.
- `tests/test_csjson_strictness.py` — every golden validates against
  `CartoSym-JSON.schema.json`.

## Regenerating

After an **intentional** change to the CSCSS → CS-JSON output:

```bash
uv run python tests/fixtures/expected/regenerate.py
git diff tests/fixtures/expected/   # review every change before committing
```

An unreviewed regen would mask a regression — the whole point of these files
is that the diff is visible in code review.
