"""
MapLibre / MapBox GL Style codec — ``.maplibre.json`` reader and writer (stub).

Implementation tracked in ROADMAP §3.4.
"""

from ..base import Codec
from .reader import MaplibreReader
from .writer import MaplibreWriter

codec = Codec(
    format_name="maplibre",
    extensions=[".maplibre.json"],
    reader=MaplibreReader(),
    writer=MaplibreWriter(),
)

__all__ = ["codec", "MaplibreReader", "MaplibreWriter"]
