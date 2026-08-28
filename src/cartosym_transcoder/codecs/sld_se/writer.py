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

import logging
from collections import OrderedDict
from typing import List, Optional, Tuple, Union

from lxml import etree

from ...models.styles import Style, StylingRule
from ..base import CodecWriter
from ._filter import (
    extract_feature_type_name,
    extract_scale_denominators,
    selector_to_filter_xml,
)
from ._symbolizer import has_raster_fields, symbolizer_to_elements
from ._xml_helpers import NSMAP, se_el, sld_el

logger = logging.getLogger(__name__)


def _scale_text(value: Union[int, float]) -> str:
    """Render a scale denominator, dropping a redundant ``.0`` on whole numbers."""
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value)


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
        emitted = 0
        for feature_type_name, rules in groups.items():
            fts = self._build_feature_type_style(feature_type_name, rules)
            if fts is not None:
                user_style.append(fts)
                emitted += 1
        if emitted == 0:
            raise NotImplementedError(
                "Style has no SLD/SE-renderable content — every styling rule "
                "is symbolizer-less (visibility / opacity / zOrder only). SE "
                "1.1.0 forbids a se:Rule without a symbolizer (see "
                "mapping-issues issue #36)"
            )
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
    ) -> Optional[etree._Element]:
        # A group styling a coverage (any rule carries raster fields) maps
        # to se:CoverageStyle/se:CoverageName; a feature group maps to
        # se:FeatureTypeStyle/se:FeatureTypeName. se:CoverageName only
        # exists on se:CoverageStyleType (SE 1.1.0).
        is_coverage = any(
            self._rule_has_raster(rule) for rule, _ in rules_and_selectors
        )
        if is_coverage:
            fts = se_el("CoverageStyle")
            if feature_type_name is not None:
                se_el("CoverageName", parent=fts, text=str(feature_type_name))
        else:
            fts = se_el("FeatureTypeStyle")
            if feature_type_name is not None:
                se_el("FeatureTypeName", parent=fts, text=str(feature_type_name))
        n_rules = 0
        for rule, remaining_selector in rules_and_selectors:
            rule_el = self._build_rule(rule, remaining_selector)
            if rule_el is not None:
                fts.append(rule_el)
                n_rules += 1
            for else_rule in self._flatten_nested_rules(rule):
                fts.append(else_rule)
                n_rules += 1
        if n_rules == 0:
            # Every rule in this group was symbolizer-less and faithfully
            # dropped — se:FeatureTypeStyle/se:CoverageStyle both require
            # >=1 se:Rule, so emit nothing for this group.
            return None
        return fts

    def _rule_has_raster(self, rule: StylingRule) -> bool:
        """True if *rule* or any of its nested rules carries raster fields."""
        if rule.symbolizer is not None and has_raster_fields(rule.symbolizer):
            return True
        return any(self._rule_has_raster(n) for n in rule.nested_rules or [])

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
            nested_el = self._build_rule(nested, None, is_else=True)
            if nested_el is not None:
                out.append(nested_el)
            out.extend(self._flatten_nested_rules(nested))
        return out

    def _build_rule(
        self,
        rule: StylingRule,
        remaining_selector: Optional[dict],
        is_else: bool = False,
    ) -> Optional[etree._Element]:
        sym_elements = (
            symbolizer_to_elements(rule.symbolizer)
            if rule.symbolizer is not None
            else []
        )
        if not sym_elements:
            # SE 1.1.0 forbids a se:Rule without a se:Symbolizer. A
            # symbolizer-less CartoSym rule (visibility / opacity / zOrder
            # only, or a cascade base case) is dropped; whatever intent it
            # carried is warned about, not silently lost, and the whole
            # style raises upstream if nothing renders at all.
            sym = rule.symbolizer
            carried = [
                f
                for f in ("visibility", "opacity", "z_order")
                if sym is not None and getattr(sym, f, None) is not None
            ]
            if carried and not is_else:
                logger.warning(
                    "SLD/SE writer: dropping symbolizer-less rule %r "
                    "(carried %s) — not representable in SE 1.1.0",
                    rule.styling_rule_name or rule.name or "<unnamed>",
                    ", ".join(carried),
                )
            return None

        rule_el = se_el("Rule")
        name = rule.styling_rule_name or rule.name
        if name:
            se_el("Name", parent=rule_el, text=name)

        if is_else:
            se_el("ElseFilter", parent=rule_el)
        else:
            min_sd, max_sd, filter_selector = extract_scale_denominators(
                remaining_selector
            )
            filt = selector_to_filter_xml(filter_selector)
            if filt is not None:
                rule_el.append(filt)
            # SE 1.1.0 RuleType order: (Filter|ElseFilter)?, then
            # MinScaleDenominator?, MaxScaleDenominator?, then Symbolizer*.
            if min_sd is not None:
                se_el("MinScaleDenominator", parent=rule_el, text=_scale_text(min_sd))
            if max_sd is not None:
                se_el("MaxScaleDenominator", parent=rule_el, text=_scale_text(max_sd))

        for sym_el in sym_elements:
            rule_el.append(sym_el)

        return rule_el
