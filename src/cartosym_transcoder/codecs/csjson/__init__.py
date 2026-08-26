"""
CartoSym-JSON codec — ``.cs.json`` reader and writer.
"""

from ..base import Codec
from .reader import CsjsonReader
from .writer import CsjsonWriter

codec = Codec(
    format_name="csjson",
    extensions=[".cs.json"],
    reader=CsjsonReader(),
    writer=CsjsonWriter(),
)

__all__ = ["codec", "CsjsonReader", "CsjsonWriter"]
