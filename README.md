# CartoSym Transcoder

A Python package for lossless transcoding between CartoSym CSS (`.cscss`) and other encodings associated with the [OGC Style & Symbology Conceptual Model standard](https://github.com/opengeospatial/styles-and-symbology).

## Installation

### From Source

```bash
git clone --recursive https://github.com/maxcollombin/CartoSymTranscoder.git
cd CartoSymTranscoder
./setup.sh
source CartoSym/bin/activate
```

### From PyPI (Coming Soon)

```bash
pip install cartosym-transcoder
```

## Usage

### Command Line

```bash
# Convert a CSCSS file to CS-JSON
cartosym input/example.cscss -o output/example.cs.json

# Convert a CS-JSON file back to CSCSS
cartosym output/example.cs.json -o output/example.cscss

# Convert and display the result in the console
cartosym input/example.cscss --print

# Convert and validate the result against the schema
cartosym input/example.cscss -o output/example.cs.json --validate

# Parse a CSCSS file (display structure info only)
cartosym parse input/example.cscss

# Validate a file
cartosym validate input/example.cs.json

# Display help
cartosym --help

# Display version
cartosym --version
```

## Development

```bash
# Setup
./setup.sh

# Install development dependencies
source CartoSym/bin/activate
pip install -e ".[dev]"

# Run tests
pytest tests/

# Clean up
./clean.sh
```

## Project Structure

- `cartosym_transcoder/` - Main Python package
- `grammar/` - Git submodule with ANTLR grammar files  
- `input/` - Sample files
- `tests/` - Unit tests