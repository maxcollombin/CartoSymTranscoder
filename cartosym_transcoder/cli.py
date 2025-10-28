"""
Command-line interface for CartoSym Transcoder.
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

from . import __version__
from .parser import CartoSymParser
from .converter import Converter


def main() -> int:
    """Main CLI entry point."""
    parser = create_argument_parser()
    args = parser.parse_args()
    
    try:
        if args.command == 'parse':
            return parse_command(args)
        elif args.command == 'convert':
            return convert_command(args)
        else:
            parser.print_help()
            return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def create_argument_parser() -> argparse.ArgumentParser:
    """Create the command-line argument parser."""
    parser = argparse.ArgumentParser(
        prog='cartosym-parse',
        description='CartoSym CSS parser and converter',
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version=f'cartosym-transcoder {__version__}'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Parse command
    parse_parser = subparsers.add_parser('parse', help='Parse a CartoSym CSS file')
    parse_parser.add_argument(
        'input_file',
        type=Path,
        help='Input CartoSym CSS (CSCSS) file to parse'
    )
    parse_parser.add_argument(
        '--log-level',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        default='INFO',
        help='Set the logging level'
    )
    
    # Convert command
    convert_parser = subparsers.add_parser('convert', help='Convert between formats')
    convert_parser.add_argument(
        'input_file',
        type=Path,
        help='Input file to convert'
    )
    convert_parser.add_argument(
        '-o', '--output',
        type=Path,
        help='Output file (if omitted, prints to console)'
    )
    convert_parser.add_argument(
        '--validate',
        action='store_true',
        help='Validate the output after conversion'
    )
    convert_parser.add_argument(
        '--print',
        action='store_true',
        help='Print the result to stdout instead of writing to a file'
    )
    convert_parser.add_argument(
        '--force',
        action='store_true',
        help='Overwrite output file if it exists'
    )
    # Optional: allow explicit format override
    convert_parser.add_argument(
        '--from-format',
        choices=['cscss', 'csjson'],
        help='Source format (auto-detected if omitted)'
    )
    convert_parser.add_argument(
        '--to-format',
        choices=['cscss', 'csjson'],
        help='Target format (auto-detected if omitted)'
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
    ext = path.suffix.lower()
    if ext == '.cscss':
        return 'cscss'
    if ext == '.json' and path.name.endswith('.cs.json'):
        return 'csjson'
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
        if from_format == 'cscss' and to_format == 'csjson':
            result = converter.cscss_to_csjson(args.input_file)
            import json
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
            import json
            if args.print:
                print(json.dumps(result, indent=2, ensure_ascii=False))
            if args.output:
                with open(args.output, 'w', encoding='utf-8') as f:
                    json.dump(result, f, indent=2, ensure_ascii=False)
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


if __name__ == '__main__':
    sys.exit(main())
