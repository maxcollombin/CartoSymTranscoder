# pycartosym

[![CI](https://github.com/maxcollombin/pycartosym/actions/workflows/ci.yml/badge.svg)](https://github.com/maxcollombin/pycartosym/actions/workflows/ci.yml)

A Python package for lossless transcoding between [CartoSym CSS](https://github.com/opengeospatial/styles-and-symbology) (`.cscss`) and other encodings associated with the OGC Style & Symbology conceptual model — CS-JSON, SLD/SE, and MapLibre Style.

## Supported Formats

| Format | Extension | Read | Write |
| --- | --- | --- | --- |
| CartoSym-CSS | `.cscss` | ✅ | ✅ |
| CS-JSON | `.cs.json` | ✅ | ✅ |
| SLD/SE (1.1.0, 1.0.0, GeoServer vendor extension) | `.sld` | ✅ | ✅ |
| MapLibre Style | `.json` | ✅ | ✅ |

SLD/SE and MapLibre are covered for the constructs each format actually
expresses — a symbolizer or property with no equivalent on the other side
raises rather than silently dropping data.

## Installation

### From PyPI (Coming Soon)

```bash
pip install pycartosym
```

### From Source

```bash
git clone https://github.com/maxcollombin/pycartosym.git
cd pycartosym
uv sync --all-extras
```

The generated ANTLR lexer/parser are already committed under
`src/pycartosym/grammar/generated/`, so no separate grammar build
step is needed. Prefix commands with `uv run`, or activate the
project's `.venv` with `source .venv/bin/activate`.

## Usage

```bash
# Convert CSCSS → CS-JSON (format auto-detected from the file extensions)
cartosym examples/0-basic.cscss -o output/0-basic.cs.json

# Convert CS-JSON → CSCSS
cartosym output/0-basic.cs.json -o output/0-basic.cscss

# Convert SLD/SE → CS-JSON (the .sld extension auto-detects)
cartosym examples/sld/1-polygon-fill-stroke.sld -o output/1-polygon.cs.json

# CS-JSON → SLD 1.0.0 / the GeoServer <VendorOption> dialect / MapLibre —
# name the target explicitly, since a plain .sld/.json extension can't
# disambiguate the SLD dialect (or MapLibre from CS-JSON)
cartosym --to-format sld:1.0.0 output/1-polygon.cs.json -o output/1-polygon-10.sld
cartosym --to-format sld:geoserver output/1-polygon.cs.json -o output/1-polygon-gs.sld
cartosym --to-format maplibre your-style.cs.json -o your-style.maplibre.json

# Print the result to the console instead of writing a file
cartosym examples/0-basic.cscss --print

# Convert and validate the output against the JSON schema
cartosym examples/0-basic.cscss -o output/0-basic.cs.json --validate

# Overwrite an existing output file
cartosym examples/0-basic.cscss -o output/0-basic.cs.json --force

# Parse a CSCSS file (display structure info)
cartosym parse examples/0-basic.cscss

# Validate a file
cartosym validate examples/0-basic.cs.json

# Help & version
cartosym --help
cartosym --version
```

More worked examples live under [`examples/`](examples/) (`examples/sld/`
for SLD/SE), including the full round-trip a given `.cscss` file goes
through in the test suite. Each codec only covers the constructs it maps
today — a `NotImplementedError` naming the unsupported construct means a
real, documented gap, not a silent data drop; see the format's codec
module for current coverage.

## Development

```bash
uv sync --all-extras
uv run pytest
```

## License

See [LICENSE](LICENSE).
