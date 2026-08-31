"""Back-compat shim — the SLD/SE codec moved to :mod:`pycartosym.codecs.sld`.

Kept so ``from pycartosym.codecs.sld_se ...`` imports (and the
vendored-corpus test that exercises the SE 1.1.0 dialect) keep working.
New code should import from :mod:`pycartosym.codecs.sld`.
"""

from __future__ import annotations

from ..sld import codec
from .reader import SldSeReader
from .writer import SldSeWriter

__all__ = ["codec", "SldSeReader", "SldSeWriter"]
