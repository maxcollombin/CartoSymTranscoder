"""Back-compat shim — moved to :mod:`cartosym_transcoder.codecs.sld.writer`.

``SldSeWriter`` is the SE 1.1.0-bound
:class:`~cartosym_transcoder.codecs.sld.writer.SldWriter` (its default dialect).
"""

from __future__ import annotations

from ..sld.writer import SldWriter as SldSeWriter

__all__ = ["SldSeWriter"]
