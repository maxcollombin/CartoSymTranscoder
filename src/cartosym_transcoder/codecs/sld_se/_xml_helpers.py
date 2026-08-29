"""
XML namespace constants and small ``lxml`` element-building helpers shared
by :mod:`_filter`, :mod:`_symbolizer`, :mod:`reader`, and :mod:`writer`.
"""

from typing import Optional, cast

from lxml import etree

SLD_NS = "http://www.opengis.net/sld"
SE_NS = "http://www.opengis.net/se"
OGC_NS = "http://www.opengis.net/ogc"
GML_NS = "http://www.opengis.net/gml"
XLINK_NS = "http://www.w3.org/1999/xlink"

NSMAP = {
    None: SLD_NS,
    "se": SE_NS,
    "ogc": OGC_NS,
    "gml": GML_NS,
    "xlink": XLINK_NS,
}

SE = f"{{{SE_NS}}}"
OGC = f"{{{OGC_NS}}}"
GML = f"{{{GML_NS}}}"
SLD = f"{{{SLD_NS}}}"
XLINK = f"{{{XLINK_NS}}}"


def se_el(
    tag: str,
    parent: Optional[etree._Element] = None,
    text: Optional[str] = None,
) -> etree._Element:
    """Create a ``se:<tag>`` element, optionally appended to *parent*."""
    el = (
        etree.SubElement(parent, f"{SE}{tag}")
        if parent is not None
        else etree.Element(f"{SE}{tag}", nsmap=NSMAP)
    )
    if text is not None:
        el.text = text
    return el


def sld_el(
    tag: str,
    parent: Optional[etree._Element] = None,
    text: Optional[str] = None,
) -> etree._Element:
    """Create an unprefixed ``sld:<tag>`` element, optionally appended to *parent*."""
    el = (
        etree.SubElement(parent, f"{SLD}{tag}")
        if parent is not None
        else etree.Element(f"{SLD}{tag}", nsmap=NSMAP)
    )
    if text is not None:
        el.text = text
    return el


def ogc_el(
    tag: str,
    parent: Optional[etree._Element] = None,
    text: Optional[str] = None,
) -> etree._Element:
    """Create an ``ogc:<tag>`` element, optionally appended to *parent*."""
    el = (
        etree.SubElement(parent, f"{OGC}{tag}")
        if parent is not None
        else etree.Element(f"{OGC}{tag}", nsmap=NSMAP)
    )
    if text is not None:
        el.text = text
    return el


def svg_param(parent: etree._Element, name: str, value: str) -> etree._Element:
    """Append an ``se:SvgParameter name="...">value</se:SvgParameter>`` child.

    Always ``se:SvgParameter`` — never the SLD 1.0.0 ``CssParameter``
    (see ``docs/sld_se_mapping_issues.md`` issue #2).
    """
    el = se_el("SvgParameter", parent, text=value)
    el.set("name", name)
    return el


def local_name(elem: etree._Element) -> str:
    """Return the local (unprefixed) tag name of *elem*."""
    return str(etree.QName(elem).localname)


def find_se(elem: etree._Element, tag: str):
    """Find the first direct-or-descendant ``se:<tag>`` child of *elem*."""
    return elem.find(f".//{SE}{tag}")


def find_se_direct(elem: etree._Element, tag: str):
    """Find the first direct ``se:<tag>`` child of *elem*."""
    return elem.find(f"{SE}{tag}")


def findall_se(elem: etree._Element, tag: str):
    """Find all direct ``se:<tag>`` children of *elem*."""
    return elem.findall(f"{SE}{tag}")


def get_svg_param(elem: etree._Element, name: str) -> Optional[str]:
    """Return the text of the ``se:SvgParameter[@name=...]`` child, if present."""
    for param in findall_se(elem, "SvgParameter"):
        if param.get("name") == name:
            return cast(Optional[str], param.text)
    return None
