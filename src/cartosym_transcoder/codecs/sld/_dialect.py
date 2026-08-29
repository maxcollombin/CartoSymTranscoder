"""SLD dialect object — everything that differs between SLD 1.0.0 and SE 1.1.0.

The two OGC dialects share their whole document model (``UserStyle >
FeatureTypeStyle > Rule > Symbolizer``, the symbolizer semantics, the
Filter Encoding grammar, scalar formatting, cascade flattening). Only the
XML surface differs:

* the namespace that wraps ``Rule`` / ``*Symbolizer`` / ``Stroke`` / ``Fill`` /
  ``Graphic`` / ... — ``se:`` (SE 1.1.0) vs. the unprefixed SLD namespace
  (SLD 1.0.0);
* the styling-parameter element — ``se:SvgParameter`` vs. ``CssParameter``;
* the raster colour-map form — ``se:Categorize`` vs. ``<ColorMapEntry>``;
* whether style ``Title``/``Abstract`` sit inside a ``se:Description``
  wrapper (SE 1.1.0) or directly under ``UserStyle`` (SLD 1.0.0);
* whether a raster group maps to ``se:CoverageStyle`` (SE 1.1.0 only) or
  stays a plain ``FeatureTypeStyle`` (SLD 1.0.0 has no ``CoverageStyle``);
* the root ``version`` attribute and the namespace map.

A :class:`SldDialect` captures those points of variation plus the
``lxml`` element factories bound to them, so :mod:`._symbolizer`,
:mod:`.reader` and :mod:`.writer` stay dialect-agnostic. It carries no
mutable state — the two module-level instances are frozen constants.

The Filter Encoding layer (:mod:`._filter`) needs no dialect: FE 1.0 and
FE 1.1 share the ``http://www.opengis.net/ogc`` namespace and are
identical for every operator this codec emits.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, cast

from lxml import etree

from ._xml_helpers import NSMAP, OGC_NS, SE_NS, SLD_NS, XLINK_NS, element_text

# SE 1.1.0 shares the module-level NSMAP (also used for detached ogc:Filter
# roots). SLD 1.0.0 needs no ``se`` prefix.
_SE_NSMAP = NSMAP
_SLD10_NSMAP = {
    None: SLD_NS,
    "ogc": OGC_NS,
    "xlink": XLINK_NS,
}


@dataclass(frozen=True)
class SldDialect:
    """One OGC styling dialect: SLD 1.0.0 or SLD 1.1.0 / SE 1.1.0.

    Attributes:
        version: Value of the root ``version`` attribute (``"1.0.0"`` / ``"1.1.0"``).
        symbology_ns: Namespace URI wrapping ``Rule`` / ``*Symbolizer`` /
            ``Stroke`` / ``Fill`` / ``Graphic`` / ``Font`` / placement / ...
            and the ``ElseFilter`` marker. ``SE_NS`` for 1.1.0, ``SLD_NS``
            for 1.0.0.
        param_tag: Local name of the styling-parameter element —
            ``"SvgParameter"`` (SE 1.1.0) or ``"CssParameter"`` (SLD 1.0.0).
            It lives in ``symbology_ns`` in both dialects.
        raster_colormap: Which raster colour-map encoding this dialect uses
            — ``"categorize"`` (``se:ColorMap/se:Categorize``, SE 1.1.0) or
            ``"entry"`` (``ColorMap/ColorMapEntry``, SLD 1.0.0).
        description_element: ``True`` if style ``Title``/``Abstract`` are
            wrapped in a ``se:Description`` element (SE 1.1.0); ``False`` if
            they are direct ``UserStyle`` children (SLD 1.0.0).
        coverage_style: ``True`` if a raster group maps to
            ``se:CoverageStyle`` / ``se:CoverageName`` (SE 1.1.0); ``False``
            if raster stays in a plain ``FeatureTypeStyle`` (SLD 1.0.0 has
            no ``CoverageStyle``).
        nsmap: Namespace map for the document root element.
    """

    version: str
    symbology_ns: str
    param_tag: str
    raster_colormap: Literal["categorize", "entry"]
    description_element: bool
    coverage_style: bool
    nsmap: dict[str | None, str]

    # -- element factories -------------------------------------------------

    def el(
        self,
        tag: str,
        parent: etree._Element | None = None,
        text: str | None = None,
    ) -> etree._Element:
        """Create a symbology element (``se:<tag>`` or SLD ``<tag>``)."""
        qname = f"{{{self.symbology_ns}}}{tag}"
        el = (
            etree.SubElement(parent, qname)
            if parent is not None
            else etree.Element(qname, nsmap=self.nsmap)
        )
        if text is not None:
            el.text = text
        return el

    def wrap(
        self,
        tag: str,
        parent: etree._Element | None = None,
        text: str | None = None,
    ) -> etree._Element:
        """Create an SLD wrapper element, always in the SLD namespace.

        Wrapper elements (``StyledLayerDescriptor``, ``NamedLayer``,
        ``UserStyle``) stay in the SLD namespace in both dialects.
        """
        qname = f"{{{SLD_NS}}}{tag}"
        el = (
            etree.SubElement(parent, qname)
            if parent is not None
            else etree.Element(qname, nsmap=self.nsmap)
        )
        if text is not None:
            el.text = text
        return el

    def param(self, parent: etree._Element, name: str, value: str) -> etree._Element:
        """Append a styling-parameter child (``SvgParameter`` / ``CssParameter``)."""
        el = self.el(self.param_tag, parent, text=value)
        el.set("name", name)
        return el

    # -- readers ---------------------------------------------------------

    def find(self, elem: etree._Element, tag: str) -> etree._Element | None:
        """Return the first direct symbology-namespace ``<tag>`` child of *elem*."""
        return elem.find(f"{{{self.symbology_ns}}}{tag}")

    def findall(self, elem: etree._Element, tag: str) -> list[etree._Element]:
        """Return all direct symbology-namespace ``<tag>`` children of *elem*."""
        return cast(
            "list[etree._Element]", elem.findall(f"{{{self.symbology_ns}}}{tag}")
        )

    def finddeep(self, elem: etree._Element, tag: str) -> etree._Element | None:
        """Return the first descendant symbology-namespace ``<tag>`` of *elem*."""
        return elem.find(f".//{{{self.symbology_ns}}}{tag}")

    def get_param(self, elem: etree._Element, name: str) -> str | None:
        """Return the value of the ``<SvgParameter name=...>`` child, if present.

        Unwraps a ``<ogc:Literal>``-wrapped constant (a common GeoServer
        SLD 1.0.0 spelling).
        """
        for param in self.findall(elem, self.param_tag):
            if param.get("name") == name:
                return element_text(param)
        return None


SE_1_1_0 = SldDialect(
    version="1.1.0",
    symbology_ns=SE_NS,
    param_tag="SvgParameter",
    raster_colormap="categorize",
    description_element=True,
    coverage_style=True,
    nsmap=_SE_NSMAP,
)

SLD_1_0_0 = SldDialect(
    version="1.0.0",
    symbology_ns=SLD_NS,
    param_tag="CssParameter",
    raster_colormap="entry",
    description_element=False,
    coverage_style=False,
    nsmap=_SLD10_NSMAP,
)

__all__ = ["SldDialect", "SE_1_1_0", "SLD_1_0_0"]
