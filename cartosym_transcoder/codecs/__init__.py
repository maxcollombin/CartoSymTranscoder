"""
Codec registry — automatic format detection and routing.

Each sub-package (``cscss``, ``csjson``, ``sld_se``, ``maplibre``) registers
its codec here so the CLI and public API can route conversions transparently.
"""

from pathlib import Path
from typing import Dict, Optional

from .base import Codec, CodecReader, CodecWriter

# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------
_REGISTRY: Dict[str, Codec] = {}


def register(codec: Codec) -> Codec:
    """Register a *codec* for each of its declared extensions."""
    for ext in codec.extensions:
        _REGISTRY[ext.lower()] = codec
    # Also register by format name (lower-cased) for --from/--to flags
    _REGISTRY[codec.format_name.lower()] = codec
    return codec


def get_codec(key: str) -> Optional[Codec]:
    """Look up a codec by extension (e.g. ``".cscss"``) or format name."""
    return _REGISTRY.get(key.lower())


def detect_codec(path: Path) -> Optional[Codec]:
    """Auto-detect the codec for *path* from its file extension.

    Handles compound extensions like ``.cs.json`` by trying the longest
    match first.
    """
    name = path.name.lower()
    # Try compound extensions first (e.g. ".cs.json")
    for ext, codec in sorted(_REGISTRY.items(), key=lambda kv: -len(kv[0])):
        if ext.startswith(".") and name.endswith(ext):
            return codec
    # Fallback: simple suffix
    return _REGISTRY.get(path.suffix.lower())


def list_codecs() -> list:
    """Return the list of unique registered codecs."""
    seen = set()
    codecs = []
    for codec in _REGISTRY.values():
        if id(codec) not in seen:
            seen.add(id(codec))
            codecs.append(codec)
    return codecs


# ---------------------------------------------------------------------------
# Auto-register built-in codecs on import
# ---------------------------------------------------------------------------
from .cscss import codec as _cscss_codec   # noqa: E402, F401
from .csjson import codec as _csjson_codec  # noqa: E402, F401

register(_cscss_codec)
register(_csjson_codec)

# SLD/SE and MapLibre are registered only if their modules are importable
# (they may raise NotImplementedError but the codec objects exist).
from .sld_se import codec as _sld_se_codec    # noqa: E402, F401
from .maplibre import codec as _maplibre_codec  # noqa: E402, F401

register(_sld_se_codec)
register(_maplibre_codec)

__all__ = [
    "Codec",
    "CodecReader",
    "CodecWriter",
    "register",
    "get_codec",
    "detect_codec",
    "list_codecs",
]
