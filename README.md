# CartoSym Transcoder

A Python package for lossless transcoding between CartoSym CSS (`.cscss`) and other encodings associated with the [OGC Style & Symbology Conceptual Model standard](https://github.com/opengeospatial/styles-and-symbology).

## Installation

### From Source

```bash
git clone --recursive https://github.com/maxcollombin/CartoSymTranscoder.git
cd CartoSymTranscoder
./setup.sh
```

### From PyPI (Coming Soon)

```bash
pip install cartosym-transcoder
```

## Usage

### Command Line

```bash
# Parse a file
cartosym-parse parse input/0-basic.cscss

# Convert between formats
cartosym-parse convert input/example.cscss -o output/example.json
# Convert and display the result in the console
cartosym-parse convert input/example.cscss --print
# Convert and validate the result
cartosym-parse convert input/example.cscss -o output/example.json --validate
# Display help
cartosym-parse --help
# Display version
cartosym-parse --version
```

### Python API

```python
from cartosym_transcoder import CartoSymParser, Converter

parser = CartoSymParser()
stylesheet = parser.parse_file("input/example.cscss")

converter = Converter()
json_data = converter.css_to_json(stylesheet)
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