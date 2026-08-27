"""
SLD/SE writer — serialise Style models to OGC Styled Layer Descriptor /
Symbology Encoding XML.

Scope: vector symbolizers (Point/Line/Polygon/Text) plus basic Part-1
raster/coverage styling. GeoServer vendor extensions and advanced/Part-4
raster are out of scope — see ``docs/sld_se_mapping_issues.md`` for the
exact boundary. Out-of-scope content raises :exc:`NotImplementedError`
naming the unsupported field rather than being silently dropped, per this
project's lossless-transcoding requirement.
"""

from collections import OrderedDict
from typing import List, Optional, Tuple

from lxml import etree

from ...models.styles import Style, StylingRule
from ..base import CodecWriter
from ._filter import extract_feature_type_name, selector_to_filter_xml
from ._symbolizer import symbolizer_to_elements
from ._xml_helpers import NSMAP, se_el, sld_el


class SldSeWriter(CodecWriter):
    """Write a Style model as SLD/SE XML."""

    def write(self, style: Style) -> str:
        root = self._build_sld(style)
        return etree.tostring(
            root, pretty_print=True, xml_declaration=True, encoding="UTF-8"
        ).decode("utf-8")

    def _build_sld(self, style: Style) -> etree._Element:
        root = etree.Element(f"{{{NSMAP[None]}}}StyledLayerDescriptor", nsmap=NSMAP)
        root.set("version", "1.1.0")
        named_layer = sld_el("NamedLayer", parent=root)
        # SLD 1.1.0 requires se:Name as the first child of NamedLayer
        # (minOccurs=1). CartoSym has no layer-name concept, so this is
        # synthesised from the style title (write-only; the reader ignores
        # it) — see docs/sld_se_mapping_issues.md.
        title = getattr(style.metadata, "title", None) if style.metadata else None
        se_el("Name", parent=named_layer, text=title or "CartoSym Style")
        named_layer.append(self._build_user_style(style))
        return root

    def _build_user_style(self, style: Style) -> etree._Element:
        user_style = sld_el("UserStyle")

        metadata = style.metadata
        if metadata is not None:
            for field in ("authors", "keywords", "geo_data_classes"):
                if getattr(metadata, field, None):
                    raise NotImplementedError(
                        f"Style.metadata.{field} has no SLD/SE mapping in "
                        "this codec (see mapping-issues issue #9)"
                    )
            if metadata.title or metadata.abstract:
                description = se_el("Description", parent=user_style)
                if metadata.title:
                    se_el("Title", parent=description, text=metadata.title)
                if metadata.abstract:
                    se_el("Abstract", parent=description, text=metadata.abstract)
        if style.variables:
            raise NotImplementedError(
                "Style.$variables has no SLD/SE mapping in this codec (see "
                "mapping-issues issue #9)"
            )
        if style.include:
            raise NotImplementedError(
                "Style.$include has no SLD/SE mapping in this codec (see "
                "mapping-issues issue #9)"
            )

        groups = self._group_rules_by_feature_type(style.styling_rules)
        for feature_type_name, rules in groups.items():
            user_style.append(self._build_feature_type_style(feature_type_name, rules))
        return user_style

    def _group_rules_by_feature_type(
        self, rules: List[StylingRule]
    ) -> "OrderedDict[Optional[str], List[Tuple[StylingRule, Optional[dict]]]]":
        """Group top-level rules by their ``dataLayer.id`` conjunct.

        Rules with no ``dataLayer.id`` conjunct are grouped under the key
        ``None`` and go into a ``se:FeatureTypeStyle`` with no
        ``se:FeatureTypeName`` child. Also strips (without re-emitting)
        any ``dataLayer.type``/``dataLayer.featuresGeometryDimensions``
        conjuncts found alongside it — see
        ``_filter.py::extract_feature_type_name`` and mapping-issues
        issue #31.
        """
        groups: (
            "OrderedDict[Optional[str], List[Tuple[StylingRule, Optional[dict]]]]"
        ) = OrderedDict()
        for rule in rules:
            selector = rule.selector
            if selector is not None and not isinstance(selector, dict):
                raise NotImplementedError(
                    f"StylingRule.selector of type {type(selector).__name__} "
                    "(bare string/list selector, not a CQL2-JSON dict) has "
                    "no SLD/SE mapping in this codec"
                )
            feature_type_name, remaining = extract_feature_type_name(selector)
            groups.setdefault(feature_type_name, []).append((rule, remaining))
        return groups

    def _build_feature_type_style(
        self,
        feature_type_name: Optional[str],
        rules_and_selectors: List[Tuple[StylingRule, Optional[dict]]],
    ) -> etree._Element:
        fts = se_el("FeatureTypeStyle")
        if feature_type_name is not None:
            se_el("FeatureTypeName", parent=fts, text=str(feature_type_name))
        for rule, remaining_selector in rules_and_selectors:
            fts.append(self._build_rule(rule, remaining_selector))
            for else_rule in self._flatten_nested_rules(rule):
                fts.append(else_rule)
        return fts

    def _flatten_nested_rules(self, rule: StylingRule) -> List[etree._Element]:
        """Flatten ``StylingRule.nested_rules`` into sibling ``se:Rule``
        elements carrying ``se:ElseFilter`` (mapping-issues issue #1).

        This treats CartoSym's ``nestedRules`` uniformly as OGC's
        else-rule sibling semantics — it does not implement CartoSym's
        cascading filter-AND / property-inheritance semantics for nested
        rules, which is a separate, larger piece of scope left for a
        follow-up pass (see mapping-issues issue #1's implementation note).
        """
        out = []
        for nested in rule.nested_rules or []:
            out.append(self._build_rule(nested, None, is_else=True))
            out.extend(self._flatten_nested_rules(nested))
        return out

    def _build_rule(
        self,
        rule: StylingRule,
        remaining_selector: Optional[dict],
        is_else: bool = False,
    ) -> etree._Element:
        rule_el = se_el("Rule")
        name = rule.styling_rule_name or rule.name
        if name:
            se_el("Name", parent=rule_el, text=name)

        if is_else:
            se_el("ElseFilter", parent=rule_el)
        else:
            filt = selector_to_filter_xml(remaining_selector)
            if filt is not None:
                rule_el.append(filt)

        if rule.symbolizer is not None:
            for sym_el in symbolizer_to_elements(rule.symbolizer):
                rule_el.append(sym_el)

        return rule_el
