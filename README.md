# CartoSymTranscoder

This repository contains the code elements required for lossless transcoding between the `*.cscss` and other encodings associated with the [OGC Style & Symbology Conceptual Model standard](https://github.com/opengeospatial/styles-and-symbology) into various other encodings.

Development is currently limited to `*.cscss` and [SLD](https://www.ogc.org/standard/sld/).

## Usage

To parse a `.cscss` file, use the following command:

```bash
python3 antlr/scr/CartoSymParser.py input/<input_file> [--log-level <level>]
```

### Log Levels

The `--log-level` option allows you to specify the verbosity of the logging output. The available log levels are:

- `DEBUG`: Provides detailed debugging information.
- `INFO`: Displays general information about the process.
- `WARNING`: Shows warnings that do not stop the execution.
- `ERROR`: Reports errors that may affect the process.
- `CRITICAL`: Logs critical issues that require immediate attention.

For example, to parse a file with `INFO` level logging:

```bash
python3 antlr/scr/CartoSymParser.py input/example.cscss --log-level INFO
```