"""
SLD/SE reader — parse OGC Styled Layer Descriptor / Symbology Encoding XML
into Style models.

Scope: vector symbolizers plus basic Part-1 raster/coverage styling. See
``writer.py``'s module docstring and ``docs/sld_se_mapping_issues.md`` for
the exact scope boundary. Out-of-scope SLD/SE constructs (e.g. advanced
raster, graphic fills, external graphics) raise :exc:`NotImplementedError`
rather than being silently skipped, per this project's lossless-transcoding
requirement.
"""

from pathlib import Path
from typing import List, Optional, Tuple, Union

from lxml import etree

from ...models.styles import Style
from ..base import CodecReader
from ._filter import filter_xml_to_selector, merge_feature_type_name
from ._symbolizer import elements_to_symbolizer
from ._xml_helpers import OGC, SLD, find_se_direct, findall_se, local_name


class SldSeReader(CodecReader):
    """Read ``.sld`` / ``.se`` XML files (or raw XML strings) into a Style model."""

    def read(self, source: Union[str, Path]) -> Style:
        """Parse *source* and return a validated Style.

        Parameters
        ----------
        source : str | Path
            A filesystem path to a ``.sld``/``.se`` file, or the raw XML text.
        """
        if isinstance(source, Path):
            xml_bytes = source.read_bytes()
        elif (
            isinstance(source, str)
            and len(source) < 500
            and "\n" not in source
            and Path(source).exists()
        ):
            xml_bytes = Path(source).read_bytes()
        elif isinstance(source, str):
            xml_bytes = source.encode("utf-8")
        else:
            xml_bytes = source

        root = etree.fromstring(xml_bytes)
        return self._parse_sld(root)

    def _parse_sld(self, root: etree._Element) -> Style:
        named_layer = root.find(f"{SLD}NamedLayer")
        if named_layer is None:
            raise NotImplementedError(
                "SLD document without sld:NamedLayer is not supported"
            )
        user_style = named_layer.find(f"{SLD}UserStyle")
        if user_style is None:
            raise NotImplementedError(
                "sld:NamedLayer without sld:UserStyle is not supported"
            )
        return self._parse_user_style(user_style)

    def _parse_user_style(self, user_style: etree._Element) -> Style:
        metadata: dict = {}
        description = find_se_direct(user_style, "Description")
        if description is not None:
            title_el = find_se_direct(description, "Title")
            abstract_el = find_se_direct(description, "Abstract")
            if title_el is not None and title_el.text:
                metadata["title"] = title_el.text
            if abstract_el is not None and abstract_el.text:
                metadata["abstract"] = abstract_el.text

        styling_rules: List[dict] = []
        for fts_el in [
            child
            for child in user_style
            if isinstance(child.tag, str)
            and local_name(child) in ("FeatureTypeStyle", "CoverageStyle")
        ]:
            styling_rules.extend(self._parse_feature_type_style(fts_el))

        style_dict: dict = {"stylingRules": styling_rules}
        if metadata:
            style_dict["metadata"] = metadata
        style: Style = Style.from_dict(style_dict)
        return style

    def _parse_feature_type_style(self, fts_el: etree._Element) -> List[dict]:
        ftn_el = find_se_direct(fts_el, "FeatureTypeName")
        if ftn_el is None:
            ftn_el = find_se_direct(fts_el, "CoverageName")
        feature_type_name = ftn_el.text if ftn_el is not None else None

        rule_dicts: List[dict] = []
        # Stack of the dict each subsequent ElseFilter rule should attach
        # to as a `nestedRules` entry — the writer flattens `nested_rules`
        # chains into consecutive siblings, so we reverse that here.
        attach_to: Optional[dict] = None

        for rule_el in findall_se(fts_el, "Rule"):
            rule_dict, is_else = self._parse_rule(rule_el)
            if is_else:
                if attach_to is None:
                    raise NotImplementedError(
                        "se:Rule/se:ElseFilter with no preceding rule in "
                        "the same se:FeatureTypeStyle is not supported"
                    )
                attach_to.setdefault("nestedRules", []).append(rule_dict)
                attach_to = rule_dict
            else:
                if feature_type_name is not None:
                    rule_dict["selector"] = merge_feature_type_name(
                        feature_type_name, rule_dict.get("selector")
                    )
                rule_dicts.append(rule_dict)
                attach_to = rule_dict

        return rule_dicts

    def _parse_rule(self, rule_el: etree._Element) -> Tuple[dict, bool]:
        rule_dict: dict = {}

        name_el = find_se_direct(rule_el, "Name")
        if name_el is not None and name_el.text:
            rule_dict["stylingRuleName"] = name_el.text

        if find_se_direct(rule_el, "MinScaleDenominator") is not None or (
            find_se_direct(rule_el, "MaxScaleDenominator") is not None
        ):
            raise NotImplementedError(
                "se:Rule MinScaleDenominator/MaxScaleDenominator has no "
                "CartoSym mapping in this codec's scope"
            )

        is_else = find_se_direct(rule_el, "ElseFilter") is not None

        if not is_else:
            filter_el = rule_el.find(f"{OGC}Filter")
            if filter_el is not None:
                rule_dict["selector"] = filter_xml_to_selector(filter_el)

        sym_children = [c for c in rule_el if local_name(c).endswith("Symbolizer")]
        if sym_children:
            rule_dict["symbolizer"] = elements_to_symbolizer(sym_children)

        return rule_dict, is_else
