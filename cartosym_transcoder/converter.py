"""
Converter module for transforming between different formats.

This module provides conversion capabilities between CartoSym CSS and other formats,
using Pydantic models for robust validation and serialization.
"""

from typing import Union, Dict, Any
from pathlib import Path
import os
import json
from .models import Style
from .parser import CartoSymParser


class Converter:
    """Main converter class for format transformations using Pydantic models."""
    
    def __init__(self):
        self.parser = CartoSymParser()
    
    def _resolve_path(self, path: Union[str, Path]) -> Path:
        """
        Résout le chemin relatif par rapport à la racine du projet (là où se trouve pyproject.toml).
        """
        p = Path(path)
        if p.is_absolute() or p.exists():
            return p
        # Cherche la racine du projet
        root = Path(__file__).resolve().parent.parent.parent
        pyproject = root / "pyproject.toml"
        if pyproject.exists():
            abs_path = root / p
            return abs_path
        return p

    def cscss_to_csjson(self, cscss_input: Union[str, Path, Style]) -> Dict[str, Any]:
        """
        Convert CartoSym CSS (CSCSS) to CartoSym JSON (CSJSON) format.
        
        Args:
            cscss_input: CSCSS string, file path, or Style model
            
        Returns:
            Dictionary representation suitable for CSJSON serialization
        """
        if isinstance(cscss_input, Style):
            # Already a Style model
            style = cscss_input
        elif isinstance(cscss_input, (str, Path)):
            # Check if it's a path first (shorter strings, no newlines)
            if isinstance(cscss_input, Path):
                resolved = self._resolve_path(cscss_input)
                style = self.parser.parse_file_to_pydantic(resolved)
            elif isinstance(cscss_input, str) and len(cscss_input) < 500 and '\n' not in cscss_input and Path(cscss_input).exists():
                resolved = self._resolve_path(cscss_input)
                style = self.parser.parse_file_to_pydantic(resolved)
            else:
                # Parse from string using ANTLR parser
                style = self.parser.parse_string_to_pydantic(cscss_input)
        else:
            raise ValueError("Invalid input type - expected str, Path, or Style model")
        
        result = style.to_dict()
        # Fix invalid selectors that are just property references
        self._fix_invalid_selectors(result)
        # Fix unit value serialization for JSON schema compliance
        self._fix_unit_values(result)
        # Fix system identifier expressions that contain operators
        self._fix_sysid_expressions(result)
        return result
    
    def _fix_invalid_selectors(self, data):
        """Fix invalid selectors in the data structure."""
        if isinstance(data, dict):
            if 'selector' in data:
                selector = data['selector']
                if isinstance(selector, dict) and 'property' in selector and len(selector) == 1:
                    # Invalid standalone property selector - this is likely a parsing error
                    # where a member access like 'viz.timeInterval.start.date' was incorrectly split
                    prop_name = selector['property']
                    # Remove the invalid selector entirely
                    del data['selector']
                elif isinstance(selector, dict) and 'property' in selector:
                    # If it's a property reference that's part of a larger expression, ensure it has the right structure
                    # Property references in selectors should be propertyRef objects
                    if 'op' not in selector and 'args' not in selector:
                        # This is a bare property reference, which is invalid in selector context
                        del data['selector']
            # Recursively fix nested structures
            for value in data.values():
                if isinstance(value, (dict, list)):
                    self._fix_invalid_selectors(value)
        elif isinstance(data, list):
            for item in data:
                self._fix_invalid_selectors(item)
    
    def csjson_to_style(self, csjson_input: Union[str, Dict[str, Any], Path]) -> Style:
        """
        Convert CSJSON to CartoSym Style model.
        
        Args:
            csjson_input: CSJSON string, dictionary, or file path
            
        Returns:
            Validated Style model
        """
        if isinstance(csjson_input, Style):
            return csjson_input
        elif isinstance(csjson_input, Path) or (isinstance(csjson_input, str) and Path(csjson_input).exists()):
            file_path = self._resolve_path(csjson_input)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return Style.from_json(content)
        elif isinstance(csjson_input, str):
            # Parse JSON string
            return Style.from_json(csjson_input)
        elif isinstance(csjson_input, dict):
            # Parse dictionary
            return Style.from_dict(csjson_input)
        else:
            raise ValueError("Invalid input type - expected str, dict, Path, or Style model")
    
    def csjson_to_cscss(self, csjson_input: Union[str, Dict[str, Any], Path]) -> str:
        """
        Convert CSJSON to CartoSym CSS (CSCSS) format.
        
        Args:
            csjson_input: CSJSON string, dictionary, or file path
            
        Returns:
            CSCSS string representation
        """
        # First convert to Style model for validation
        style = self.csjson_to_style(csjson_input)
        
        # Then convert Style to CSS
        return self.style_to_cscss(style)
    
    def style_to_cscss(self, style: Style) -> str:
        """
        Convert Style model to CSCSS string with pretty-print indentation.
        """
        lines = []
        # Add metadata as CSCSS directives
        if style.metadata:
            if getattr(style.metadata, 'title', None):
                lines.append(f".title '{style.metadata.title}'")
            if getattr(style.metadata, 'abstract', None):
                lines.append(f".abstract '{style.metadata.abstract}'")
            if getattr(style.metadata, 'description', None):
                lines.append(f".description '{style.metadata.description}'")
            if getattr(style.metadata, 'authors', None):
                for author in style.metadata.authors:
                    lines.append(f'.author "{author}"')
            if getattr(style.metadata, 'keywords', None):
                kw = style.metadata.keywords
                kw_str = ', '.join(kw) if isinstance(kw, list) else kw
                lines.append(f".keywords '{kw_str}'")
            if getattr(style.metadata, 'geoDataClasses', None):
                gc = style.metadata.geoDataClasses
                gc_str = ', '.join(gc) if isinstance(gc, list) else gc
                lines.append(f".geoDataClasses '{gc_str}'")
            lines.append("")  # Empty line after metadata

        # Add only top-level rules; nested rules are emitted only within their parent
        for rule in style.styling_rules:
            lines.extend(self._rule_to_css(rule, emit_nested=True, indent=0))
            lines.append("")  # Empty line between rules

        return '\n'.join(lines).strip()
    
    def _rule_to_css(self, rule, emit_nested=True, indent=0) -> list:
        """Convert StylingRule model to CSS lines with pretty-print indentation."""
        lines = []
        pad = '    ' * indent
        # Add rule comment if present
        if rule.comment:
            lines.append(f"{pad}/* {rule.comment} */")
        # Add selector
        if rule.selector:
            selector_str = self._selector_to_cscss(rule.selector)
            lines.append(f"{pad}{selector_str}")
        # Add symbolizer
        lines.append(f"{pad}{{")
        if rule.symbolizer:
            for l in self._symbolizer_to_css(rule.symbolizer, indent=indent+1):
                lines.append(f"{pad}    {l.lstrip()}")
        # Emit nested rules only within this block
        if emit_nested and getattr(rule, 'nested_rules', None):
            for nested_rule in rule.nested_rules:
                lines.extend(self._rule_to_css(nested_rule, emit_nested=True, indent=indent+1))
        lines.append(f"{pad}}}")
        return lines

    def _selector_to_cscss(self, selector) -> str:
        """
        Convert a selector (dict, list, or str) to a CSCSS selector string.
        Handles:
        - Landuse
        - Landuse[other filter]
        - [complex filter]
        """
        # Simple string selector
        if isinstance(selector, str):
            return selector
        # List of selectors (rare, but possible)
        if isinstance(selector, list):
            if len(selector) == 1 and isinstance(selector[0], dict):
                return self._selector_to_cscss(selector[0])
            return " ".join(self._selector_to_cscss(s) for s in selector)
        # Dict selector (expression)
        if isinstance(selector, dict):
            # Special case: Landuse[filter] form
            if selector.get('op') == 'and' and isinstance(selector.get('args'), list):
                args = selector['args']
                id_arg = None
                other_args = []
                for arg in args:
                    if (
                        isinstance(arg, dict)
                        and arg.get('op') == '='
                        and isinstance(arg.get('args'), list)
                        and len(arg['args']) == 2
                        and isinstance(arg['args'][0], dict)
                        and arg['args'][0].get('sysId') == 'dataLayer.id'
                    ):
                        landuse_val = arg['args'][1]
                        if isinstance(landuse_val, dict) and 'property' in landuse_val:
                            landuse_val = landuse_val['property']
                        id_arg = landuse_val
                    else:
                        other_args.append(arg)
                if id_arg is not None:
                    if other_args:
                        filter_str = self._format_selector_expr(other_args[0]) if len(other_args) == 1 else self._format_selector_expr({'op': 'and', 'args': other_args})
                        return f"{id_arg}[{filter_str}]"
                    else:
                        return str(id_arg)
            # Otherwise, always reconstruct as a filter expression
            return f"[{self._format_selector_expr(selector)}]"
        # Fallback
        return str(selector)

    def _format_selector_expr(self, expr, _quote_bare_strings: bool = True) -> str:
        """
        Recursively format a selector expression dict as a CSCSS filter string.

        _quote_bare_strings: when True (default) plain string values are
        single-quoted.  Set to False when the right-hand side of a sysId
        comparison is an unquoted identifier/enum (e.g. ``dataLayer.type = vector``).
        """
        if not isinstance(expr, dict):
            s = str(expr)
            if not _quote_bare_strings:
                return s  # unquoted identifier/constant
            # Quote bare strings that are not numbers / booleans — they came from
            # CHARACTER_LITERALs like 'parking' and must be re-quoted on write-back.
            try:
                float(s)
                return s  # numeric literal – no quotes
            except ValueError:
                pass
            if s.lower() in ('true', 'false', 'null'):
                return s
            # Plain string value → single-quote it
            return f"'{s}'"
        # Handle bare property reference (e.g., {"property": "viz.date"})
        if 'property' in expr and len(expr) == 1:
            return expr['property']
        # Function call formatting
        if 'function' in expr and 'args' in expr:
            func_name = expr['function']
            args = expr['args']
            def format_arg(a):
                if isinstance(a, str):
                    if (a.startswith("'") and a.endswith("'")) or (a.startswith('"') and a.endswith('"')):
                        return a
                    try:
                        float(a)
                        return a
                    except Exception:
                        return f"'{a}'"
                return self._format_selector_expr(a)
            args_str = ", ".join(format_arg(a) for a in args)
            return f"{func_name}({args_str})"
        op = expr.get('op')
        args = expr.get('args', [])
        if op and isinstance(args, list):
            # Format n-ary ops (like 'and', 'or')
            if op in ('and', 'or'):
                def needs_parens(arg):
                    return isinstance(arg, dict) and arg.get('op') in ('and', 'or') and arg.get('op') != op
                joined = f" {op} ".join(
                    f"({self._format_selector_expr(a)})" if needs_parens(a) else self._format_selector_expr(a)
                    for a in args
                )
                return joined
            # Format binary comparison ops
            if len(args) == 2:
                left_arg, right_arg = args[0], args[1]
                left = self._format_selector_expr(left_arg)
                # If left side is a sysId, right side is an identifier/enum — don't quote
                right_quote = not (isinstance(left_arg, dict) and 'sysId' in left_arg)
                right = self._format_selector_expr(right_arg, _quote_bare_strings=right_quote)
                return f"{left} {op} {right}"
        # Handle sysId
        if 'sysId' in expr:
            return expr['sysId']
        if 'property' in expr:
            return expr['property']
        return str(expr)
    
    def _symbolizer_to_css(self, symbolizer, indent=1) -> list:
        """Convert Symbolizer model to CSS property lines."""
        lines = []
        # Core symbolizer properties
        if getattr(symbolizer, 'visibility', None) is not None:
            lines.append(f"  visibility: {str(symbolizer.visibility).lower()};")
        if getattr(symbolizer, 'opacity', None) is not None:
            lines.append(f"  opacity: {symbolizer.opacity};")
        # Support both z_order and zOrder
        zorder_val = getattr(symbolizer, 'zOrder', None)
        if zorder_val is None:
            zorder_val = getattr(symbolizer, 'z_order', None)
        if zorder_val is not None:
            lines.append(f"  zOrder: {zorder_val};")
        # Vector symbolizers
        if getattr(symbolizer, 'fill', None):
            lines.extend(self._fill_to_css(symbolizer.fill))
        if getattr(symbolizer, 'stroke', None):
            lines.extend(self._stroke_to_css(symbolizer.stroke))
        if getattr(symbolizer, 'marker', None):
            lines.extend(self._marker_to_css(symbolizer.marker))
        if getattr(symbolizer, 'label', None):
            lines.extend(self._label_to_css(symbolizer.label))
        # Coverage / raster symbolizer properties
        # Use explicit None-check (not `or`) to correctly handle 0 / 0.0 / False
        sc = getattr(symbolizer, 'single_channel', None)
        if sc is None:
            sc = getattr(symbolizer, 'singleChannel', None)
        if sc is not None:
            lines.append(f"  singleChannel: {self._channel_expr_to_css(sc)};")
        cc = getattr(symbolizer, 'color_channels', None)
        if cc is None:
            cc = getattr(symbolizer, 'colorChannels', None)
        if cc is not None:
            lines.append(f"  colorChannels: {self._channels_to_css(cc)};")
        ac = getattr(symbolizer, 'alpha_channel', None)
        if ac is None:
            ac = getattr(symbolizer, 'alphaChannel', None)
        if ac is not None:
            lines.append(f"  alphaChannel: {self._channel_expr_to_css(ac)};")
        cm = getattr(symbolizer, 'color_map', None)
        if cm is None:
            cm = getattr(symbolizer, 'colorMap', None)
        if cm is not None:
            lines.append(f"  colorMap: {self._color_map_to_css(cm)};")
        om = getattr(symbolizer, 'opacity_map', None)
        if om is None:
            om = getattr(symbolizer, 'opacityMap', None)
        if om is not None:
            lines.append(f"  opacityMap: {self._opacity_map_to_css(om)};")
        hs = getattr(symbolizer, 'hill_shading', None)
        if hs is None:
            hs = getattr(symbolizer, 'hillShading', None)
        if hs is not None:
            lines.extend(self._hill_shading_to_css(hs, sym_indent=indent))
        return lines

    def _channel_expr_to_css(self, expr) -> str:
        """Format a channel expression (property-ref, arithmetic expr, or string) to CSCSS."""
        if isinstance(expr, dict):
            if 'property' in expr:
                return expr['property']
            if 'op' in expr:
                return self._arith_expr_to_css(expr)
        return str(expr)

    def _arith_expr_to_css(self, expr) -> str:
        """Recursively convert an arithmetic expression dict back to CSCSS string."""
        if isinstance(expr, dict):
            if 'property' in expr:
                return expr['property']
            if 'op' in expr and 'args' in expr:
                op = expr['op']
                args = [self._arith_expr_to_css(a) for a in expr['args']]
                if op in ('*', '/', '+', '-'):
                    left, right = args[0], args[1]
                    # Wrap sub-expressions in parens when needed to preserve precedence
                    return f"({left} {op} {right})"
                return ' '.join([op] + args)
        if isinstance(expr, (int, float)):
            return str(expr)
        return str(expr)

    def _channels_to_css(self, channels) -> str:
        """Format colorChannels (list of property-refs or single expr) to CSCSS."""
        if isinstance(channels, list):
            return ' '.join(self._channel_expr_to_css(c) for c in channels)
        return self._channel_expr_to_css(channels)

    def _color_entry_to_css(self, entry) -> str:
        """Format one colorMap entry [threshold, color] to CSCSS."""
        if isinstance(entry, (list, tuple)) and len(entry) >= 2:
            threshold = entry[0]
            color = entry[1]
            if isinstance(color, (list, tuple)) and len(color) == 3:
                color_str = '{} {} {}'.format(int(color[0]), int(color[1]), int(color[2]))
            elif isinstance(color, dict) and 'r' in color:
                color_str = '{} {} {}'.format(int(color['r']), int(color['g']), int(color['b']))
            else:
                color_str = self._format_color(color)
            return f"{threshold} {color_str}"
        return str(entry)

    def _color_map_to_css(self, color_map) -> str:
        """Format colorMap to CSCSS array syntax: [v1 r g b, v2 name, ...]."""
        if isinstance(color_map, list):
            entries = ', '.join(self._color_entry_to_css(e) for e in color_map)
            return f"[{entries}]"
        return str(color_map)

    def _opacity_map_to_css(self, opacity_map) -> str:
        """Format opacityMap to CSCSS array syntax: [v1 op1, v2 op2, ...]."""
        if isinstance(opacity_map, list):
            entries = []
            for e in opacity_map:
                if isinstance(e, (list, tuple)) and len(e) >= 2:
                    entries.append(f"{e[0]} {e[1]}")
                else:
                    entries.append(str(e))
            return '[' + ', '.join(entries) + ']'
        return str(opacity_map)

    def _hill_shading_to_css(self, hill_shading, sym_indent=1) -> list:
        """Format hillShading object to CSCSS property lines."""
        if not isinstance(hill_shading, dict):
            return []
        parts = []
        factor = hill_shading.get('factor')
        if factor is not None:
            parts.append(f"factor: {factor}")
        sun = hill_shading.get('sun')
        if sun and isinstance(sun, dict):
            sun_parts = '; '.join(f"{k}: {v}" for k, v in sun.items())
            parts.append(f"sun: {{{sun_parts}}}")
        cm = hill_shading.get('colorMap')
        if cm is not None:
            parts.append(f"colorMap: {self._color_map_to_css(cm)}")
        om = hill_shading.get('opacityMap')
        if om is not None:
            parts.append(f"opacityMap: {self._opacity_map_to_css(om)}")
        if not parts:
            return []
        # Multi-line block. The returned string has no leading whitespace on the
        # first line (caller does lstrip + re-indent). Continuation lines carry
        # absolute indentation: sym_indent levels for the closing }, and
        # sym_indent+1 levels for the inner properties.
        inner_pad = '    ' * (sym_indent + 1)
        close_pad = '    ' * sym_indent
        sep = ';\n' + inner_pad
        inner = sep.join(parts)
        return [f"hillShading: {{\n{inner_pad}{inner};\n{close_pad}}};"]


    def _marker_to_css(self, marker) -> list:
        """Convert Marker model to CSS lines.

        Two forms:
        * Normal list → ``marker: { elements: [ Type { ... }, ... ] };``
        * Indexed override → ``marker.elements[N]: Type { ... };``
        """
        lines = []
        elements = getattr(marker, 'elements', None)
        if not elements:
            return lines

        # ── Indexed override: marker.elements[N]: Type { ... } ────────────────
        if isinstance(elements, dict) and 'index' in elements and 'value' in elements:
            idx = elements['index']
            el = elements['value']
            lines.append(f"  marker.elements[{idx}]:")
            lines.append(f"     {self._graphic_element_to_css_block(el, indent=15)};")
            return lines

        # ── Normal list: marker: { elements: [ ... ] } ───────────────────────
        element_strs = []
        for el in (elements if isinstance(elements, list) else [elements]):
            element_strs.append(self._graphic_element_to_css_block(el, indent=15))
        elements_block = '[\n                ' + ',\n                '.join(element_strs) + '\n             ]'
        lines.append(f"  marker: {{elements: {elements_block}}};")
        return lines

    def _label_to_css(self, label) -> list:
        """Convert Label model to CSS lines."""
        lines = []
        elements = getattr(label, 'elements', None)
        if not elements:
            return lines
        element_strs = []
        for el in (elements if isinstance(elements, list) else [elements]):
            element_strs.append(self._graphic_element_to_css_block(el, indent=15))
        elements_block = '[\n                ' + ',\n                '.join(element_strs) + '\n             ]'
        lines.append(f"  label: {{elements: {elements_block}}};")
        return lines

    def _graphic_element_to_css_block(self, el, indent: int = 0) -> str:
        """Render a single graphic element as a CSS block, e.g. ``Dot { ... }``."""
        def _get(o, k):
            return o.get(k) if isinstance(o, dict) else getattr(o, k, None)

        el_type = _get(el, 'type') or 'Graphic'
        pad = ' ' * indent
        inner_pad = ' ' * (indent + 3)

        prop_lines = []

        # position
        pos = _get(el, 'position')
        if pos is not None:
            if hasattr(pos, 'x') and hasattr(pos, 'y'):
                prop_lines.append(f"position: {pos.x} {pos.y}")
            elif isinstance(pos, dict) and 'x' in pos and 'y' in pos:
                prop_lines.append(f"position: {pos['x']} {pos['y']}")

        # size
        size = _get(el, 'size')
        if size is not None:
            if isinstance(size, dict) and len(size) == 1:
                unit, val = next(iter(size.items()))
                prop_lines.append(f"size: {val} {unit}")
            else:
                prop_lines.append(f"size: {size}")

        # color
        color = _get(el, 'color')
        if color is not None:
            prop_lines.append(f"color: {self._format_color(color)}")

        # text — property ref → bare identifier; plain string → quoted
        text = _get(el, 'text')
        if text is not None:
            if isinstance(text, dict) and 'property' in text:
                prop_lines.append(f"text: {text['property']}")
            elif isinstance(text, str):
                prop_lines.append(f"text: '{text}'")
            else:
                prop_lines.append(f"text: {text}")

        # alignment
        alignment = _get(el, 'alignment')
        if alignment is not None:
            if isinstance(alignment, list) and len(alignment) == 2:
                prop_lines.append(f"alignment: {alignment[0]} {alignment[1]}")
            else:
                prop_lines.append(f"alignment: {alignment}")

        # font
        font = _get(el, 'font')
        if font is not None:
            if isinstance(font, dict):
                fp = []
                for k, v in font.items():
                    if k == 'face' and isinstance(v, str):
                        fv = f"'{v}'"
                    elif k == 'color':
                        fv = self._format_color(v)
                    elif k == 'outline' and isinstance(v, dict):
                        # Serialize outline as CSCSS inline object: {key: val; ...}
                        out_parts = []
                        for ok, ov in v.items():
                            if ok == 'color':
                                ovf = self._format_color(ov)
                            elif isinstance(ov, bool):
                                ovf = str(ov).lower()
                            else:
                                ovf = ov
                            out_parts.append(f"{ok}: {ovf}")
                        fv = '{' + '; '.join(out_parts) + '}'
                    elif isinstance(v, bool):
                        fv = str(v).lower()
                    else:
                        fv = v
                    fp.append(f"{k}: {fv}")
                font_inner = (';\n' + inner_pad + '   ').join(fp)
                prop_lines.append(f"font: {{\n{inner_pad}   {font_inner};\n{inner_pad}}}")
            else:
                prop_lines.append(f"font: {font}")

        # image resource (Image type)
        image = _get(el, 'image')
        if image is not None:
            res_parts = []
            for k in ('uri', 'path', 'id', 'type', 'ext'):
                v = _get(image, k)
                if v is not None:
                    res_parts.append(f"{k}: '{v}'")
            if res_parts:
                prop_lines.append(f"image: {{{'; '.join(res_parts)}}}")

        # hotSpot — list of {unit: val} → "val unit val unit ..."
        hot_spot = _get(el, 'hotSpot') or _get(el, 'hot_spot')
        if hot_spot is not None:
            if isinstance(hot_spot, list):
                parts = []
                for item in hot_spot:
                    if isinstance(item, dict) and len(item) == 1:
                        unit, val = next(iter(item.items()))
                        parts.append(f"{val} {unit}")
                    elif hasattr(item, 'value') and hasattr(item, 'unit'):
                        parts.append(f"{item.value} {item.unit}")
                    else:
                        parts.append(str(item))
                prop_lines.append(f"hotSpot: {' '.join(parts)}")
            else:
                prop_lines.append(f"hotSpot: {hot_spot}")

        # tint / blackTint / alphaThreshold
        tint = _get(el, 'tint')
        if tint is not None:
            prop_lines.append(f"tint: {tint}")

        black_tint = _get(el, 'blackTint') or _get(el, 'black_tint')
        if black_tint is not None:
            prop_lines.append(f"blackTint: {black_tint}")

        alpha_threshold = _get(el, 'alphaThreshold') or _get(el, 'alpha_threshold')
        if alpha_threshold is not None:
            prop_lines.append(f"alphaThreshold: {alpha_threshold}")

        # opacity (only when non-default for elements other than font)
        opacity = _get(el, 'opacity')
        if opacity is not None and 'font' not in [p.split(':')[0].strip() for p in prop_lines]:
            prop_lines.append(f"opacity: {opacity}")

        body = (';\n' + inner_pad).join(prop_lines)
        if prop_lines:
            body += ';'
        return f"{el_type} {{\n{inner_pad}{body}\n{pad}}}"
    
    def _format_color(self, color) -> str:
        """Format a color value for CSCSS output.
        - [r, g, b] integer array → '#rrggbb' hex
        - {r, g, b} object → '#rrggbb' hex
        - named color string → as-is
        """
        if isinstance(color, list) and len(color) == 3:
            try:
                return '#{:02x}{:02x}{:02x}'.format(int(color[0]), int(color[1]), int(color[2]))
            except (TypeError, ValueError):
                pass
        if isinstance(color, dict) and all(k in color for k in ('r', 'g', 'b')):
            try:
                return '#{:02x}{:02x}{:02x}'.format(int(color['r']), int(color['g']), int(color['b']))
            except (TypeError, ValueError):
                pass
        return str(color)

    def _format_unit_value(self, uv) -> str:
        """Format a UnitValue (or {unit: val} dict) as CSCSS syntax, e.g. '2.0 px'."""
        if hasattr(uv, 'value') and hasattr(uv, 'unit'):
            unit_str = uv.unit.value if hasattr(uv.unit, 'value') else str(uv.unit)
            return f"{uv.value} {unit_str}"
        if isinstance(uv, dict) and len(uv) == 1:
            unit, val = next(iter(uv.items()))
            return f"{val} {unit}"
        return str(uv)

    def _fill_to_css(self, fill) -> list:
        """Convert Fill model to CSS lines."""
        lines = []
        color = getattr(fill, 'color', None)
        opacity = getattr(fill, 'opacity', None)

        if color is not None and opacity is not None:
            # Full compound fill block
            lines.append(f"  fill: {{color: {self._format_color(color)}; opacity: {opacity}}};")
        elif color is not None:
            # Single sub-property: use dot-notation alter (preserves cascade semantics)
            lines.append(f"  fill.color: {self._format_color(color)};")
        elif opacity is not None:
            lines.append(f"  fill.opacity: {opacity};")

        # TODO: Add pattern support
        return lines
    
    def _stroke_to_css(self, stroke) -> list:
        """Convert Stroke model to CSS lines."""
        color = getattr(stroke, 'color', None)
        width = getattr(stroke, 'width', None)
        opacity = getattr(stroke, 'opacity', None)

        set_props = sum(1 for v in (color, width, opacity) if v is not None)

        # Single sub-property: use dot-notation alter (preserves cascade semantics)
        if set_props == 1:
            if color is not None:
                return [f"  stroke.color: {self._format_color(color)};"]
            if width is not None:
                return [f"  stroke.width: {self._format_unit_value(width)};"]
            if opacity is not None:
                return [f"  stroke.opacity: {opacity};"]

        # Multiple sub-properties: full compound block
        if set_props > 1:
            parts = []
            if color is not None:
                parts.append(f"color: {self._format_color(color)}")
            if width is not None:
                parts.append(f"width: {self._format_unit_value(width)}")
            if opacity is not None:
                parts.append(f"opacity: {opacity}")
            return [f"  stroke: {{{'; '.join(parts)}}};"]

        return []
    
    def _fix_unit_values(self, data):
        """Fix unit value serialization to match JSON schema format."""
        if isinstance(data, dict):
            # Check if this looks like a unit value with value/unit structure
            if 'value' in data and 'unit' in data and len(data) == 2:
                # This is a unit value that should be converted to {unit: value} format
                value = data['value']
                unit = data['unit']
                # Replace the dict contents with the correct format
                data.clear()
                data[unit] = value
                return
            
            # Check for string values that should be unit values
            # Common properties that should have unit values
            unit_properties = ['width', 'height', 'size', 'radius', 'distance', 'spacing']
            for key, value in list(data.items()):
                if key in unit_properties and isinstance(value, str):
                    # Try to parse "value unit" format like "8.0 m"
                    converted = self._parse_unit_string(value)
                    if converted is not None:
                        data[key] = converted
                elif isinstance(value, (dict, list)):
                    self._fix_unit_values(value)
        elif isinstance(data, list):
            for item in data:
                self._fix_unit_values(item)
    
    def _parse_unit_string(self, value_str: str):
        """Parse a string like '8.0 m' or '5 px' into {unit: value} format."""
        if not isinstance(value_str, str):
            return None
        
        parts = value_str.strip().split()
        if len(parts) == 2:
            try:
                # Parse the numeric value
                num_value = float(parts[0]) if '.' in parts[0] else int(parts[0])
                unit = parts[1]
                # Valid units according to JSON schema
                valid_units = ['px', 'mm', 'cm', 'in', 'pt', 'em', 'pc', 'm', 'ft']
                if unit in valid_units:
                    return {unit: num_value}
            except ValueError:
                pass
        return None
    
    def _fix_sysid_expressions(self, data):
        """Fix system identifier expressions that contain comparison operators."""
        if isinstance(data, dict):
            if 'selector' in data:
                selector = data['selector']
                if isinstance(selector, dict) and 'sysId' in selector:
                    sysid = selector['sysId']
                    if isinstance(sysid, str):
                        # Check if the sysId contains comparison operators
                        for op in ['>=', '<=', '!=', '=', '>', '<']:
                            if op in sysid:
                                # Split the expression
                                parts = sysid.split(op, 1)
                                if len(parts) == 2:
                                    left_part = parts[0].strip()
                                    right_part = parts[1].strip()
                                    
                                    # Convert right part to appropriate type
                                    try:
                                        if '.' in right_part:
                                            right_value = float(right_part)
                                        else:
                                            right_value = int(right_part)
                                    except ValueError:
                                        right_value = right_part.strip('\'"')
                                    
                                    # Replace the selector with a proper comparison
                                    data['selector'] = {
                                        "op": op,
                                        "args": [{"sysId": left_part}, right_value]
                                    }
                                    break
            # Recursively fix nested structures
            for value in data.values():
                if isinstance(value, (dict, list)):
                    self._fix_sysid_expressions(value)
        elif isinstance(data, list):
            for item in data:
                self._fix_sysid_expressions(item)
