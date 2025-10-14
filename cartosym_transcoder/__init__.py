"""
CartoSym Transcoder - Lossless transcoding between CartoSym CSS, CartoSym JSON, and other encodings.

This package provides tools for converting between CartoSym CSS, CartoSym JSON format, and other
cartographic symbology encodings like SLD (Styled Layer Descriptor).
"""

__version__ = "0.1.0"
__author__ = "Maxime Collombin"
__email__ = "maxime.collombin@example.com"

from .parser import CartoSymParser
from .converter import Converter

__all__ = ["CartoSymParser", "Converter"]
