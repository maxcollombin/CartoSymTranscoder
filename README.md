# CartoSym Transcoder

A Python package for lossless transcoding between [CartoSym CSS](https://github.com/opengeospatial/styles-and-symbology) (`.cscss`) and CS-JSON (`.cs.json`).

## Installation

### From PyPI (Coming Soon)

```bash
pip install cartosym-transcoder
```

### From Source

```bash
git clone https://github.com/maxcollombin/CartoSymTranscoder.git
cd CartoSymTranscoder
uv sync
```

The generated ANTLR lexer/parser are already committed under
`src/cartosym_transcoder/grammar/generated/`, so no separate grammar build
step is needed. Prefix commands with `uv run`, or activate the
project's `.venv` with `source .venv/bin/activate`.

## Usage

```bash
# Convert CSCSS → CS-JSON
cartosym examples/0-basic.cscss -o output/0-basic.cs.json

# Convert CS-JSON → CSCSS
cartosym output/0-basic.cs.json -o output/0-basic.cscss

# Explicit format selection
cartosym --from-format cscss --to-format csjson examples/0-basic.cscss -o output/0-basic.cs.json

# Print the result to the console instead of writing a file
cartosym examples/0-basic.cscss --print

# Convert and validate the output against the JSON schema
cartosym examples/0-basic.cscss -o output/0-basic.cs.json --validate

# Overwrite an existing output file
cartosym examples/0-basic.cscss -o output/0-basic.cs.json --force

# Parse a CSCSS file (display structure info)
cartosym parse examples/0-basic.cscss

# Validate a file
cartosym validate examples/example-functional.cs.json

# Help & version
cartosym --help
cartosym --version
```

## Supported Formats

| Format | Extension | Read | Write |
| --- | --- | --- | --- |
| CartoSym-CSS | `.cscss` | ✅ | ✅ |
| CS-JSON | `.cs.json` | ✅ | ✅ |
| SLD/SE | `.sld` | 🚧 | 🚧 |
| MapLibre Style | `.json` | 🚧 | 🚧 |

## Development

```bash
uv sync --all-extras
uv run pytest
```

## License

See [LICENSE](LICENSE).
