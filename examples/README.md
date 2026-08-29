# Example styles

Hand-written sample styles used throughout the docs and the test suite.

| File(s) | Format | Notes |
|---|---|---|
| `*.cscss` | CartoSym-CSS | `0-basic` … `12-include`, roughly increasing in complexity (basic vector → coverage/raster → `@include`) |
| `*.cs.json` | CS-JSON | a few canonical JSON encodings, incl. `example-functional.cs.json` |
| `sld/*.sld` | SLD/SE 1.1.0 | hand-written fixtures exercising the `sld_se` codec (feature-by-feature; not a third-party corpus — those live under `tests/fixtures/`) |

## Run them

```bash
# CartoSym-CSS → CS-JSON
uv run cartosym examples/3-vector-line.cscss -o output/3-vector-line.cs.json --force

# …and back
uv run cartosym output/3-vector-line.cs.json -o output/3-vector-line.cscss --force

# CartoSym-CSS → SLD/SE
uv run cartosym examples/2-vector-polygon.cscss --to-format sld -o output/2-vector-polygon.sld --force

# validate
uv run cartosym validate examples/example-functional.cs.json
```

The expected CS-JSON for every `*.cscss` here is committed as a golden under
`tests/fixtures/expected/` — regenerate with
`uv run python tests/fixtures/expected/regenerate.py` after an intentional
output change, then review the diff.
