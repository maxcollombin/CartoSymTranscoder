"""
OGC SLD/SE codec — ``.sld`` reader and writer (stub).

Implementation tracked in ROADMAP §3.3.
"""

from ..base import Codec
from .reader import SldSeReader
from .writer import SldSeWriter

codec = Codec(
    format_name="sld",
    extensions=[".sld", ".se"],
    reader=SldSeReader(),
    writer=SldSeWriter(),
)

__all__ = ["codec", "SldSeReader", "SldSeWriter"]
