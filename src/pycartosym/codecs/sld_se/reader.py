"""Back-compat shim — moved to :mod:`pycartosym.codecs.sld.reader`.

``SldSeReader`` is the SE 1.1.0-bound
:class:`~pycartosym.codecs.sld.reader.SldReader` (its default dialect).
"""

from __future__ import annotations

from ..sld.reader import SldReader as SldSeReader

__all__ = ["SldSeReader"]
