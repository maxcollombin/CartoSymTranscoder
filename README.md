# pycartosym

[![CI](https://github.com/maxcollombin/pycartosym/actions/workflows/ci.yml/badge.svg)](https://github.com/maxcollombin/pycartosym/actions/workflows/ci.yml)

A Python package for lossless transcoding between [CartoSym CSS](https://github.com/opengeospatial/styles-and-symbology) (`.cscss`) and other encodings of the OGC Style & Symbology conceptual model (CS-JSON, SLD/SE), plus MapLibre Style as a practical interoperability target.

## Supported Formats

| Format | Extension | Standard | Read | Write |
| --- | --- | --- | --- | --- |
| CartoSym-CSS | `.cscss` | OGC Style & Symbology | yes | yes |
| CS-JSON | `.cs.json` | OGC Style & Symbology | yes | yes |
| SLD/SE (1.1.0, 1.0.0) | `.sld` | OGC | yes | yes |
| SLD 1.0.0 with GeoServer `<VendorOption>` pass-through | `.sld` | GeoServer vendor extension, not OGC | yes | yes |
| MapLibre Style | `.json` | MapLibre/Mapbox de facto spec, not OGC | yes | yes |

Each codec is covered for the constructs the target format actually
expresses (a symbolizer or property with no equivalent on the other side
raises rather than silently dropping data).

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
# Format auto-detected from the file extensions where that's unambiguous
cartosym <input-file> -o <output-file>

# Explicit target format (needed for the SLD dialects and MapLibre,
# since a plain .sld/.json extension can't disambiguate those)
cartosym --to-format <sld|sld:1.0.0|sld:geoserver|maplibre|cscss|csjson> <input-file> -o <output-file>

# Display structure info for a CSCSS file, without converting it
cartosym parse <input-file>

# Validate a .cscss or .cs.json file against the grammar/JSON schema
cartosym validate <input-file>

# Full option and format reference
cartosym --help
```

Real input files to try these against live under [`examples/`](examples/)
(`examples/sld/` for SLD/SE).

## Development

```bash
uv sync --all-extras
uv run pytest
```

## License

See [LICENSE](LICENSE).
