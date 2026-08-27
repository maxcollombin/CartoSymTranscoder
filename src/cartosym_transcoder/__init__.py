"""
CartoSym Transcoder - Lossless transcoding between CartoSym CSS, CartoSym JSON, and other encodings.

This package provides tools for converting between CartoSym CSS, CartoSym JSON format, and other
cartographic symbology encodings like SLD (Styled Layer Descriptor) and MapLibre GL Style.
"""

__version__ = "0.1.0"
__author__ = "Maxime Collombin"
__email__ = "maxime.collombin@example.com"

# Codec registry (lazy — sub-codecs register on first import of .codecs)
from .codecs import detect_codec, get_codec, list_codecs  # noqa: F401
from .converter import Converter
from .parser import CartoSymParser

__all__ = [
    "CartoSymParser",
    "Converter",
    "get_codec",
    "detect_codec",
    "list_codecs",
]
