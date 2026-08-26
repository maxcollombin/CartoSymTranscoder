"""
Command-line interface for CartoSym Transcoder.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Optional
from antlr4 import FileStream, CommonTokenStream
from cartosym_transcoder.grammar.generated.CartoSymCSSLexer import CartoSymCSSLexer
from cartosym_transcoder.grammar.generated.CartoSymCSSGrammar import CartoSymCSSGrammar
from jsonschema import validate as jsonschema_validate, ValidationError

from . import __version__
from .parser import CartoSymParser
from .converter import Converter


# Subcommands that are dispatched explicitly (not the default conversion path)
_SUBCOMMANDS = frozenset({'parse', 'validate'})


def main() -> int:
    """Main CLI entry point."""
    # Pre-detect whether a named subcommand is being used so that argparse
    # doesn't confuse a file path for a subcommand name (or vice-versa).
    positionals = [a for a in sys.argv[1:] if not a.startswith('-')]
    is_subcommand = bool(positionals) and positionals[0] in _SUBCOMMANDS

    parser = _create_subcommand_parser() if is_subcommand else _create_convert_parser()
    args = parser.parse_args()

    try:
        if is_subcommand:
            if args.command == 'parse':
                return parse_command(args)
            elif args.command == 'validate':
                return validate_command(args)
        else:
            if getattr(args, 'input_file', None) is None:
                parser.print_help()
                return 1
            return convert_command(args)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    return 0


def create_argument_parser() -> argparse.ArgumentParser:
    """Return the default (conversion) argument parser."""
    return _create_convert_parser()


def _create_convert_parser() -> argparse.ArgumentParser:
    """Parser for the default conversion mode: cartosym <input> -o <output>."""
    parser = argparse.ArgumentParser(
        prog='cartosym',
        description='CartoSym transcoder: convert between .cscss and .cs.json formats',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            'Examples:\n'
            '  cartosym input/example.cscss -o output/example.cs.json\n'
            '  cartosym output/example.cs.json -o output/example.cscss\n'
            '  cartosym input/example.cscss --print\n'
            '\n'
            'Other commands:\n'
            '  cartosym parse <input>     Parse a CSCSS file\n'
            '  cartosym validate <input>  Validate a .cscss or .cs.json file\n'
        ),
    )

    parser.add_argument(
        '--version',
        action='version',
        version=f'cartosym-transcoder {__version__}'
    )
    parser.add_argument(
        'input_file',
        nargs='?',
        type=Path,
        default=None,
        help='Input file to convert (.cscss or .cs.json)'
    )
    parser.add_argument(
        '-o', '--output',
        type=Path,
        help='Output file (if omitted, prints to console)'
    )
    parser.add_argument(
        '--validate',
        action='store_true',
        help='Validate the output after conversion'
    )
    parser.add_argument(
        '--print',
        action='store_true',
        help='Print the result to stdout'
    )
    parser.add_argument(
        '--force',
        action='store_true',
        help='Overwrite output file if it exists'
    )
    parser.add_argument(
        '--from-format',
        choices=['cscss', 'csjson', 'sld', 'maplibre'],
        help='Source format (auto-detected from file extension if omitted)'
    )
    parser.add_argument(
        '--to-format',
        choices=['cscss', 'csjson', 'sld', 'maplibre'],
        help='Target format (auto-detected from file extension if omitted)'
    )
    return parser


def _create_subcommand_parser() -> argparse.ArgumentParser:
    """Parser for named subcommands: cartosym parse|validate <input>."""
    parser = argparse.ArgumentParser(
        prog='cartosym',
        description='CartoSym transcoder',
    )
    parser.add_argument(
        '--version',
        action='version',
        version=f'cartosym-transcoder {__version__}'
    )

    subparsers = parser.add_subparsers(dest='command')

    # parse subcommand
    parse_parser = subparsers.add_parser('parse', help='Parse a CSCSS file and display info')
    parse_parser.add_argument(
        'input_file',
        type=Path,
        help='Input CartoSym CSS (.cscss) file to parse'
    )
    parse_parser.add_argument(
        '--log-level',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        default='INFO',
        help='Set the logging level'
    )

    # validate subcommand
    validate_parser = subparsers.add_parser('validate', help='Validate a .cscss or .cs.json file')
    validate_parser.add_argument(
        'input_file',
        type=Path,
        help='File to validate (.cscss or .cs.json)'
    )

    return parser


def parse_command(args) -> int:
    """Handle the parse command."""
    parser = CartoSymParser(log_level=args.log_level)
    
    try:
        stylesheet = parser.parse_file(args.input_file)
        print(f"Successfully parsed {args.input_file}")
        print(f"Found {len(stylesheet.metadata)} metadata entries")
        if stylesheet.styling_rules:
            print(f"Found {len(stylesheet.styling_rules.rules)} styling rules")
        return 0
    except FileNotFoundError:
        print(f"Error: File not found: {args.input_file}", file=sys.stderr)
        return 1


def detect_format(path: Path) -> Optional[str]:
    """Detect the format of a file from its extension."""
    name = path.name.lower()
    if name.endswith('.cscss'):
        return 'cscss'
    if name.endswith('.cs.json'):
        return 'csjson'
    if name.endswith('.sld') or name.endswith('.se'):
        return 'sld'
    if name.endswith('.maplibre.json'):
        return 'maplibre'
    return None


def convert_command(args) -> int:
    """Handle the convert command with auto format detection."""
    converter = Converter()
    from_format = args.from_format or detect_format(args.input_file)
    to_format = args.to_format or (detect_format(args.output) if args.output else None)
    if not from_format or not to_format:
        print(f"Conversion from {from_format} to {to_format} not supported yet", file=sys.stderr)
        return 1
    try:
        # Validate input before conversion
        input_path = args.input_file
        ext = input_path.suffix.lower()
        has_errors = False
        if from_format == 'cscss':
            from antlr4 import FileStream, CommonTokenStream
            from cartosym_transcoder.grammar.generated.CartoSymCSSLexer import CartoSymCSSLexer
            from cartosym_transcoder.grammar.generated.CartoSymCSSGrammar import CartoSymCSSGrammar
            input_stream = FileStream(str(input_path), encoding='utf-8')
            lexer = CartoSymCSSLexer(input_stream)
            tokens = CommonTokenStream(lexer)
            parser = CartoSymCSSGrammar(tokens)
            parser.removeErrorListeners()
            from antlr4.error.ErrorListener import ConsoleErrorListener
            parser.addErrorListener(ConsoleErrorListener())
            parser.styleSheet()
            if parser.getNumberOfSyntaxErrors() > 0:
                print(f"Error: Input CSCSS file contains syntax errors. Conversion aborted.", file=sys.stderr)
                has_errors = True
        elif from_format == 'csjson':
            try:
                with open(input_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                schema_path = Path(__file__).parent / 'schemas' / 'CartoSym-JSON.schema.json'
                with open(schema_path, 'r', encoding='utf-8') as sf:
                    schema = json.load(sf)
                from jsonschema import validate as jsonschema_validate, ValidationError
                jsonschema_validate(instance=data, schema=schema)
            except (json.JSONDecodeError, ValidationError) as ve:
                print(f"Error: Input CSJSON file is invalid: {ve}", file=sys.stderr)
                has_errors = True
            except Exception as e:
                print(f"Error: Could not validate CSJSON: {e}", file=sys.stderr)
                has_errors = True
        if has_errors:
            return 1
        # If no errors, proceed with conversion
        if from_format == 'cscss' and to_format == 'csjson':
            result = converter.cscss_to_csjson(args.input_file)
            if args.print:
                print(json.dumps(result, indent=2, ensure_ascii=False))
            if args.output:
                with open(args.output, 'w', encoding='utf-8') as f:
                    json.dump(result, f, indent=2, ensure_ascii=False)
        elif from_format == 'csjson' and to_format == 'cscss':
            result = converter.csjson_to_cscss(args.input_file)
            if args.print:
                print(result)
            if args.output:
                with open(args.output, 'w', encoding='utf-8') as f:
                    f.write(result)
        elif from_format == 'csjson' and to_format == 'csjson':
            style = converter.csjson_to_style(args.input_file)
            result = style.to_dict()
            if args.print:
                print(json.dumps(result, indent=2, ensure_ascii=False))
            if args.output:
                with open(args.output, 'w', encoding='utf-8') as f:
                    json.dump(result, f, indent=2, ensure_ascii=False)
        else:
            # Try codec-based routing for new/future formats
            from .codecs import get_codec
            src_codec = get_codec(from_format)
            dst_codec = get_codec(to_format)
            if src_codec and dst_codec and src_codec.reader and dst_codec.writer:
                try:
                    style = src_codec.read(args.input_file)
                    result = dst_codec.write(style)
                    if isinstance(result, dict):
                        output_str = json.dumps(result, indent=2, ensure_ascii=False)
                    else:
                        output_str = str(result)
                    if args.print:
                        print(output_str)
                    if args.output:
                        with open(args.output, 'w', encoding='utf-8') as f:
                            f.write(output_str)
                except NotImplementedError as nie:
                    print(f"Error: {nie}", file=sys.stderr)
                    return 1
            else:
                print(f"Conversion from {from_format} to {to_format} not supported yet", file=sys.stderr)
                return 1
        print(f"Successfully converted {args.input_file} to {args.output}")
        return 0
    except FileNotFoundError:
        print(f"Error: File not found: {args.input_file}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error during conversion: {e}", file=sys.stderr)
        return 1


def validate_command(args) -> int:
    """Validate a CSCSS or CSJSON file."""
    input_path = args.input_file
    ext = input_path.suffix.lower()
    try:
        if ext == '.cscss':
            input_stream = FileStream(str(input_path), encoding='utf-8')
            lexer = CartoSymCSSLexer(input_stream)
            tokens = CommonTokenStream(lexer)
            parser = CartoSymCSSGrammar(tokens)
            parser.removeErrorListeners()
            from antlr4.error.ErrorListener import ConsoleErrorListener
            parser.addErrorListener(ConsoleErrorListener())
            tree = parser.styleSheet()
            if parser.getNumberOfSyntaxErrors() == 0:
                print(f"Syntaxe CSCSS valide : {input_path}")
                return 0
            else:
                print(f"Erreurs de syntaxe CSCSS dans {input_path}", file=sys.stderr)
                return 1
        elif ext == '.json' and input_path.name.endswith('.cs.json'):
            with open(input_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            schema_path = Path(__file__).parent / 'schemas' / 'CartoSym-JSON.schema.json'
            with open(schema_path, 'r', encoding='utf-8') as sf:
                schema = json.load(sf)
            try:
                jsonschema_validate(instance=data, schema=schema)
                print(f"Syntaxe CSJSON valide : {input_path}")
                return 0
            except ValidationError as ve:
                print(f"Erreur de validation CSJSON : {ve.message}", file=sys.stderr)
                return 1
        else:
            print(f"Extension non reconnue pour la validation : {input_path}", file=sys.stderr)
            return 1
    except Exception as e:
        print(f"Erreur lors de la validation : {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
