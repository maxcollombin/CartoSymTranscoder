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
./setup.sh
source CartoSym/bin/activate
```

## Usage

```bash
# Convert CSCSS → CS-JSON
cartosym input/example.cscss -o output/example.cs.json

# Convert CS-JSON → CSCSS
cartosym output/example.cs.json -o output/example.cscss

# Explicit format selection
cartosym --from-format cscss --to-format csjson input/example.cscss -o output/example.cs.json

# Print the result to the console instead of writing a file
cartosym input/example.cscss --print

# Convert and validate the output against the JSON schema
cartosym input/example.cscss -o output/example.cs.json --validate

# Overwrite an existing output file
cartosym input/example.cscss -o output/example.cs.json --force

# Parse a CSCSS file (display structure info)
cartosym parse input/example.cscss

# Validate a file
cartosym validate input/example.cs.json

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
./setup.sh
source CartoSym/bin/activate
pip install -e ".[dev]"
pytest tests/
```

## License

See [LICENSE](LICENSE).
