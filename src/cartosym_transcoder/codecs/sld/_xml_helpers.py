"""XML namespace constants and the dialect-invariant ``lxml`` helpers.

Everything that differs between SLD 1.0.0 and SE 1.1.0 (the symbology
namespace, ``SvgParameter`` vs. ``CssParameter``, ...) lives on
:class:`._dialect.SldDialect`. What stays here is common to both dialects:
the namespace URIs, the Clark-notation prefixes, ``local_name``, and the
Filter Encoding element factory (FE 1.0 and FE 1.1 share a namespace).
"""

from __future__ import annotations

from lxml import etree

SLD_NS = "http://www.opengis.net/sld"
SE_NS = "http://www.opengis.net/se"
OGC_NS = "http://www.opengis.net/ogc"
GML_NS = "http://www.opengis.net/gml"
XLINK_NS = "http://www.w3.org/1999/xlink"

SE = f"{{{SE_NS}}}"
OGC = f"{{{OGC_NS}}}"
GML = f"{{{GML_NS}}}"
SLD = f"{{{SLD_NS}}}"
XLINK = f"{{{XLINK_NS}}}"

# Full namespace map declared on a detached ``ogc:Filter`` / ``ogc:BBOX``
# root before it is appended into the document tree. lxml drops the
# declarations already in scope at the insertion point, so this keeps the
# serialised output identical to declaring the prefixes only on the
# document root.
NSMAP = {
    None: SLD_NS,
    "se": SE_NS,
    "ogc": OGC_NS,
    "gml": GML_NS,
    "xlink": XLINK_NS,
}


def ogc_el(
    tag: str,
    parent: etree._Element | None = None,
    text: str | None = None,
) -> etree._Element:
    """Create an ``ogc:<tag>`` Filter Encoding element, optionally under *parent*."""
    el = (
        etree.SubElement(parent, f"{OGC}{tag}")
        if parent is not None
        else etree.Element(f"{OGC}{tag}", nsmap=NSMAP)
    )
    if text is not None:
        el.text = text
    return el


def local_name(elem: etree._Element) -> str:
    """Return the local (unprefixed) tag name of *elem*."""
    return str(etree.QName(elem).localname)
