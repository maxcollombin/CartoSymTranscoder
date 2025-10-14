"""
Converter module for transforming between different formats.

This module provides conversion capabilities between CartoSym CSS and other formats,
using Pydantic models for robust validation and serialization.
"""

from typing import Union, Dict, Any
from pathlib import Path
import os
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
        
        return style.to_dict()
    
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
        Convert Style model to CSCSS string.
        
        Args:
            style: Validated Style model
            
        Returns:
            CSCSS string representation
        """
        lines = []
        
        # Add metadata as CSS comments and directives
        if style.metadata:
            lines.append("/* CartoSym CSS Generated from JSON */")
            if style.metadata.title:
                lines.append(f'.title "{style.metadata.title}";')
            if style.metadata.description:
                lines.append(f'.description "{style.metadata.description}";')
            if style.metadata.authors:
                for author in style.metadata.authors:
                    lines.append(f'.author "{author}";')
            lines.append("")  # Empty line after metadata
        
        # Add styling rules
        for rule in style.styling_rules:
            lines.extend(self._rule_to_css(rule))
            lines.append("")  # Empty line between rules
        
        return '\n'.join(lines).strip()
    
    def _rule_to_css(self, rule) -> list:
        """Convert StylingRule model to CSS lines."""
        lines = []
        
        # Add rule comment if present
        if rule.comment:
            lines.append(f"/* {rule.comment} */")
        
        # Add selector (simplified for now)
        if rule.selector:
            if isinstance(rule.selector, list):
                # Simple array selector like ["Landuse"]
                selector_str = " ".join(rule.selector)
            elif isinstance(rule.selector, str):
                selector_str = rule.selector
            else:
                # Complex expression - simplified representation
                selector_str = str(rule.selector)
            lines.append(f"[{selector_str}]")
        
        # Add symbolizer
        lines.append("{")
        if rule.symbolizer:
            lines.extend(self._symbolizer_to_css(rule.symbolizer))
        lines.append("}")
        
        # Add nested rules if any
        for nested_rule in (rule.nested_rules or []):
            lines.extend(self._rule_to_css(nested_rule))
        
        return lines
    
    def _symbolizer_to_css(self, symbolizer) -> list:
        """Convert Symbolizer model to CSS property lines."""
        lines = []
        
        # Core symbolizer properties
        if symbolizer.visibility is not None:
            lines.append(f"  visibility: {str(symbolizer.visibility).lower()};")
        
        if symbolizer.opacity is not None:
            lines.append(f"  opacity: {symbolizer.opacity};")
        
        if symbolizer.z_order is not None:
            lines.append(f"  z-order: {symbolizer.z_order};")
        
        # Vector symbolizers
        if symbolizer.fill:
            lines.extend(self._fill_to_css(symbolizer.fill))
        
        if symbolizer.stroke:
            lines.extend(self._stroke_to_css(symbolizer.stroke))
        
        # TODO: Add marker, label, raster properties
        
        return lines
    
    def _fill_to_css(self, fill) -> list:
        """Convert Fill model to CSS lines."""
        lines = []
        
        if fill.color:
            lines.append(f"  fill: {fill.color};")
        
        if fill.opacity is not None:
            lines.append(f"  fill-opacity: {fill.opacity};")
        
        # TODO: Add pattern support
        
        return lines
    
    def _stroke_to_css(self, stroke) -> list:
        """Convert Stroke model to CSS lines.""" 
        lines = []
        
        if stroke.color:
            lines.append(f"  stroke: {stroke.color};")
        
        if stroke.width:
            lines.append(f"  stroke-width: {stroke.width};")
        
        if stroke.opacity is not None:
            lines.append(f"  stroke-opacity: {stroke.opacity};")
        
        # TODO: Add dash pattern, casing support
        
        return lines
