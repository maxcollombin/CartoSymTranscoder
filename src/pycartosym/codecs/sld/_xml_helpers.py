"""XML namespace constants and the dialect-invariant ``lxml`` helpers.

Everything that differs between SLD 1.0.0 and SE 1.1.0 (the symbology
namespace, ``SvgParameter`` vs. ``CssParameter``, ...) lives on
:class:`._dialect.SldDialect`. What stays here is common to both dialects:
the namespace URIs, the Clark-notation prefixes, ``local_name``, and the
Filter Encoding element factory (FE 1.0 and FE 1.1 share a namespace).
"""

from __future__ import annotations

from typing import cast

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

# Namespace map for the SE 1.1.0 document root (also SldDialect.nsmap for
# SE_1_1_0). Kept as a named constant so both uses stay in sync.
NSMAP = {
    None: SLD_NS,
    "se": SE_NS,
    "ogc": OGC_NS,
    "gml": GML_NS,
    "xlink": XLINK_NS,
}

# Namespace map declared on a detached ``ogc:Filter`` / ``ogc:BBOX`` root
# before it is appended into the document tree. Only the prefixes a Filter
# Encoding fragment can actually use — lxml drops whichever are already in
# scope at the insertion point, so the serialised output is unchanged, and
# an SLD 1.0.0 document (whose root has no ``se`` prefix) stays clean.
_FILTER_NSMAP = {"ogc": OGC_NS, "gml": GML_NS, "xlink": XLINK_NS}


def ogc_el(
    tag: str,
    parent: etree._Element | None = None,
    text: str | None = None,
) -> etree._Element:
    """Create an ``ogc:<tag>`` Filter Encoding element, optionally under *parent*."""
    el = (
        etree.SubElement(parent, f"{OGC}{tag}")
        if parent is not None
        else etree.Element(f"{OGC}{tag}", nsmap=_FILTER_NSMAP)
    )
    if text is not None:
        el.text = text
    return el


def local_name(elem: etree._Element) -> str:
    """Return the local (unprefixed) tag name of *elem*."""
    return str(etree.QName(elem).localname)


def element_text(elem: etree._Element | None) -> str | None:
    """Return *elem*'s value, unwrapping a single wrapping ``<ogc:Literal>``.

    SLD lets a parameter or scalar element hold either bare text
    (``<Size>6</Size>``) or an expression; GeoServer very often writes the
    constant case as ``<Size><ogc:Literal>6</ogc:Literal></Size>`` /
    ``<CssParameter name="fill"><ogc:Literal>#abc</ogc:Literal></CssParameter>``.
    Both spell the same constant, so they read back identically.
    """
    if elem is None:
        return None
    if elem.text is not None and elem.text.strip():
        return cast("str", elem.text)
    literal = elem.find(f"{OGC}Literal")
    if literal is not None and literal.text is not None:
        return cast("str", literal.text)
    return cast("str | None", elem.text)
