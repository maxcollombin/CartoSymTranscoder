"""
CartoSym-CSS codec — ``.cscss`` reader and writer.
"""

from ..base import Codec
from .reader import CscssReader
from .writer import CscssWriter

codec = Codec(
    format_name="cscss",
    extensions=[".cscss"],
    reader=CscssReader(),
    writer=CscssWriter(),
)

__all__ = ["codec", "CscssReader", "CscssWriter"]
