"""
CartoSym CSS Parser module.

This module provides the main parsing functionality for CartoSym CSS files.
"""

from __future__ import annotations

import logging
import argparse
import functools
from pathlib import Path
from typing import Optional, Union
from antlr4 import *

from .grammar.generated import (
    CartoSymCSSLexer,
    CartoSymCSSGrammar,
    CartoSymCSSGrammarListener
)
from .ast import StyleSheet, Metadata, StylingRule, StylingRuleList, Symbolizer, PropertyAssignment as AstPropertyAssignment, Fill, Stroke
from .ast_converter import convert_ast_to_pydantic
from .models import Style
from .expression_parser import ExpressionParser
from .models.expressions import *


class CartoSymParser:
    """Main parser class for CartoSym CSS files."""
    
    def __init__(self, log_level: str = "INFO"):
        """Initialize the parser with the specified log level."""
        self.logger = self._configure_logging(log_level)
        
    def _configure_logging(self, log_level: str) -> logging.Logger:
        """Configure logging based on the provided log level."""
        logging.basicConfig(
            level=getattr(logging, log_level.upper(), "INFO"),
            format="%(asctime)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        return logging.getLogger(__name__)
    
    def parse_file(self, file_path: Union[str, Path]) -> StyleSheet:
        """Parse a CartoSym CSS file and return an AST."""
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
            
        self.logger.info(f"Parsing file: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            
        return self.parse_string(content)
    
    def parse_file_to_pydantic(self, file_path: Union[str, Path]) -> Style:
        """Parse a CartoSym CSS file and return a Pydantic Style model."""
        ast_stylesheet = self.parse_file(file_path)
        return convert_ast_to_pydantic(ast_stylesheet)
    
    def parse_string_to_pydantic(self, content: str) -> Style:
        """Parse a CartoSym CSS string and return a Pydantic Style model."""
        ast_stylesheet = self.parse_string(content)
        return convert_ast_to_pydantic(ast_stylesheet)
    
    def parse_string(self, content: str) -> StyleSheet:
        """Parse a CartoSym CSS string and return an AST."""
        # Create input stream
        input_stream = InputStream(content)
        
        # Create lexer
        lexer = CartoSymCSSLexer(input_stream)
        
        # Create token stream
        stream = CommonTokenStream(lexer)
        
        # Create parser
        parser = CartoSymCSSGrammar(stream)
        
        # Parse the input
        tree = parser.styleSheet()
        
        # Create listener and walk the tree
        listener = CartoSymStyleSheetListener()
        walker = ParseTreeWalker()
        walker.walk(listener, tree)
        
        return listener.stylesheet


class CartoSymStyleSheetListener(CartoSymCSSGrammarListener):
    """Enhanced listener to build AST from parse tree with expression support."""
    
    def __init__(self):
        self.stylesheet = None
        self.current_rule = None
        self.current_assignments = []
        self.rule_stack = []  # Stack for nested rules
        self.current_selectors = []  # Current selectors being processed
        
    def enterStyleSheet(self, ctx):
        """Called when entering a stylesheet rule."""
        self.stylesheet = StyleSheet()
        
    def enterMetadata(self, ctx):
        """Called when entering metadata."""
        if ctx.IDENTIFIER() and ctx.CHARACTER_LITERAL():
            key = ctx.IDENTIFIER().getText()
            # Remove quotes from character literal
            value = ctx.CHARACTER_LITERAL().getText().strip('"\'')
            metadata = Metadata(key=key, value=value)
            if not self.stylesheet.metadata:
                self.stylesheet.metadata = []
            self.stylesheet.metadata.append(metadata)
    
    def enterStylingRule(self, ctx):
        """Called when entering a styling rule."""
        # Push current rule to stack if we have one (for nesting)
        if self.current_rule:
            self.rule_stack.append({
                'rule': self.current_rule,
                'assignments': self.current_assignments.copy(),
                'selectors': self.current_selectors.copy()
            })
        
        # Create new styling rule
        self.current_rule = StylingRule()
        self.current_assignments = []
        self.current_selectors = []
        
    def exitStylingRule(self, ctx):
        """Called when exiting a styling rule."""
        # Create symbolizer from collected assignments
        if self.current_assignments:
            symbolizer = Symbolizer()
            
            for assignment in self.current_assignments:
                self._handle_property_assignment_enhanced(
                    assignment.property_name, 
                    assignment.value, 
                    symbolizer
                )
            
            self.current_rule.symbolizer = symbolizer
        
        # Set selectors
        if self.current_selectors:
            self.current_rule.selectors = self.current_selectors
            # For backward compatibility, set name from first simple selector
            for selector in self.current_selectors:
                if hasattr(selector, 'name') and selector.name:
                    self.current_rule.name = selector.name
                    break
        
        # Handle nesting: if we're in a nested rule, add to parent
        if self.rule_stack:
            parent_state = self.rule_stack.pop()
            parent_rule = parent_state['rule']
            
            # Add current rule as nested rule to parent
            if not hasattr(parent_rule, 'nested_rules'):
                parent_rule.nested_rules = []
            parent_rule.nested_rules.append(self.current_rule)
            
            # Restore parent state
            self.current_rule = parent_rule
            self.current_assignments = parent_state['assignments']
            self.current_selectors = parent_state['selectors']
        else:
            # Top-level rule: add to stylesheet
            if not self.stylesheet.styling_rules:
                self.stylesheet.styling_rules = StylingRuleList(rules=[])
            
            self.stylesheet.styling_rules.rules.append(self.current_rule)
            self.current_rule = None
            self.current_assignments = []
            self.current_selectors = []
    
    def enterSelector(self, ctx):
        """Called when entering a selector."""
        # Create a new selector
        selector = Selector()
        
        # Handle simple name selector
        if ctx.IDENTIFIER():
            selector.name = ctx.IDENTIFIER().getText()
        
        # Handle conditional selector [expression] 
        # This can be either in the same context or separate
        conditions_found = False
        
        # Check if this selector context has an expression (for [expr] selectors)
        if hasattr(ctx, 'LSBR') and ctx.LSBR() and hasattr(ctx, 'expression') and ctx.expression():
            try:
                # Parse the expression inside []
                expr = ExpressionParser.parse_expression(ctx.expression())
                selector.conditions = [expr]
                conditions_found = True
            except Exception as e:
                # Fallback: treat as simple text
                expr_text = ctx.expression().getText() if ctx.expression() else ""
                selector.conditions = [IdentifierExpression(name=expr_text)]
                conditions_found = True
        
        # If no conditions found and we have an identifier, it's a simple selector
        if not conditions_found and selector.name:
            # This is a simple selector like "Landuse"
            pass
        
        self.current_selectors.append(selector)
    
    def enterPropertyAssignment(self, ctx):
        """Called when entering a property assignment."""        
        if ctx.lhValue() and ctx.expression():
            # Get property name from lhValue - handle dot notation like fill.color
            prop_name = ctx.lhValue().getText()
            
            # Parse the expression for the value
            try:
                expr = ExpressionParser.parse_expression(ctx.expression())
                # For now, convert expression back to string for compatibility
                # Later we can store the full expression
                prop_value = self._expression_to_string(expr)
            except Exception as e:
                # Fallback to simple text extraction
                prop_value = ctx.expression().getText()
                # Handle special case where value might be an object like {color: red; opacity: 0.5}
                if prop_value.startswith('{') and prop_value.endswith('}'):
                    # Keep as-is for object parsing
                    pass
            
            if prop_name and prop_value:
                assignment = AstPropertyAssignment(property_name=prop_name, value=prop_value)
                self.current_assignments.append(assignment)
    
    def _expression_to_string(self, expr: Expression) -> str:
        """Convert expression back to string representation for compatibility."""
        if isinstance(expr, IdentifierExpression):
            return expr.name
        elif isinstance(expr, ConstantExpression):
            result = str(expr.value)
            if expr.unit:
                result += f" {expr.unit}"
            return result
        elif isinstance(expr, StringExpression):
            return f'"{expr.value}"'
        elif isinstance(expr, MemberAccessExpression):
            obj_str = self._expression_to_string(expr.object)
            return f"{obj_str}.{expr.member}"
        elif isinstance(expr, BinaryOperationExpression):
            left_str = self._expression_to_string(expr.left)
            right_str = self._expression_to_string(expr.right)
            return f"{left_str} {expr.operator.value} {right_str}"
        elif isinstance(expr, InstanceExpression):
            # Handle instance expressions like {color: red; opacity: 0.5}
            if expr.class_name:
                return f"{expr.class_name}(...)"  # Simplified
            else:
                props = []
                for prop in expr.properties:
                    prop_val = self._expression_to_string(prop.value)
                    props.append(f"{prop.property}: {prop_val}")
                return "{" + "; ".join(props) + "}"
        else:
            # Fallback
            return str(expr)
    
    def _handle_property_assignment_enhanced(self, prop_name: str, prop_value: str, symbolizer):
        """Enhanced property assignment handler with expression support."""
        # Handle dot notation properties like fill.color, stroke.width
        if '.' in prop_name:
            parts = prop_name.split('.')
            if len(parts) == 2:
                obj_name, attr_name = parts
                
                if obj_name.lower() == 'fill':
                    if not symbolizer.fill:
                        symbolizer.fill = Fill()
                    if attr_name.lower() == 'color':
                        symbolizer.fill.color = prop_value
                    elif attr_name.lower() == 'opacity':
                        try:
                            symbolizer.fill.opacity = float(prop_value)
                        except ValueError:
                            pass
                            
                elif obj_name.lower() == 'stroke':
                    if not symbolizer.stroke:
                        symbolizer.stroke = Stroke()
                    if attr_name.lower() == 'color':
                        symbolizer.stroke.color = prop_value
                    elif attr_name.lower() == 'width':
                        symbolizer.stroke.width = prop_value
                    elif attr_name.lower() == 'opacity':
                        try:
                            symbolizer.stroke.opacity = float(prop_value)
                        except ValueError:
                            pass
        else:
            # Handle direct properties
            prop_name_lower = prop_name.lower()
            
            # Handle special property value parsing for complex objects
            if prop_value.startswith('{') and prop_value.endswith('}'):
                # This is an object literal like {color: gray; opacity: 0.5}
                self._handle_object_property(prop_name_lower, prop_value, symbolizer)
            else:
                # Simple property
                if prop_name_lower == 'visibility':
                    if prop_value.lower() == 'false':
                        symbolizer.visibility = False
                    elif prop_value.lower() == 'true':
                        symbolizer.visibility = True
                elif prop_name_lower == 'opacity':
                    try:
                        symbolizer.opacity = float(prop_value)
                    except ValueError:
                        pass
                elif prop_name_lower == 'zorder':
                    try:
                        symbolizer.z_order = int(prop_value)
                    except ValueError:
                        pass
                elif prop_name_lower == 'fill':
                    # Simple fill color
                    if not symbolizer.fill:
                        symbolizer.fill = Fill()
                    symbolizer.fill.color = prop_value
                elif prop_name_lower == 'stroke':
                    # Simple stroke color
                    if not symbolizer.stroke:
                        symbolizer.stroke = Stroke()
                    symbolizer.stroke.color = prop_value
                
                # Coverage/Raster properties (Phase B Priority 1)
                elif prop_name_lower in ['singlechannel', 'single_channel']:
                    symbolizer.single_channel = prop_value
                elif prop_name_lower in ['colorchannels', 'color_channels']:
                    symbolizer.color_channels = prop_value
                elif prop_name_lower in ['alphachannel', 'alpha_channel']:
                    symbolizer.alpha_channel = prop_value
                elif prop_name_lower in ['colormap', 'color_map']:
                    # Parse color map array: [0 96 136 73, 900 226 219 167, ...]
                    symbolizer.color_map = self._parse_color_map(prop_value)
                elif prop_name_lower in ['opacitymap', 'opacity_map']:
                    symbolizer.opacity_map = self._parse_opacity_map(prop_value)
                elif prop_name_lower in ['hillshading', 'hill_shading']:
                    # This will be handled as an object property below
                    pass
    
    def _handle_object_property(self, prop_name: str, prop_value: str, symbolizer):
        """Handle object properties like fill: {color: gray; opacity: 0.5}."""
        # Remove braces and trim
        content = prop_value.strip('{}').strip()
        
        # Parse individual properties
        properties = {}
        if content:
            # Split by semicolon, but be careful with nested structures
            parts = []
            current_part = ""
            brace_count = 0
            
            for char in content:
                if char == '{':
                    brace_count += 1
                elif char == '}':
                    brace_count -= 1
                elif char == ';' and brace_count == 0:
                    if current_part.strip():
                        parts.append(current_part.strip())
                    current_part = ""
                    continue
                current_part += char
            
            # Add the last part
            if current_part.strip():
                parts.append(current_part.strip())
            
            # Parse each part as key: value
            for part in parts:
                if ':' in part:
                    key, value = part.split(':', 1)
                    properties[key.strip()] = value.strip()
        
        # Apply properties to symbolizer
        if prop_name == 'fill':
            if not symbolizer.fill:
                symbolizer.fill = Fill()
            if 'color' in properties:
                symbolizer.fill.color = properties['color']
            if 'opacity' in properties:
                try:
                    symbolizer.fill.opacity = float(properties['opacity'])
                except ValueError:
                    pass
        
        elif prop_name == 'stroke':
            if not symbolizer.stroke:
                symbolizer.stroke = Stroke()
            if 'color' in properties:
                symbolizer.stroke.color = properties['color']
            if 'width' in properties:
                symbolizer.stroke.width = properties['width']
            if 'opacity' in properties:
                try:
                    symbolizer.stroke.opacity = float(properties['opacity'])
                except ValueError:
                    pass
        
        elif prop_name == 'marker':
            # Handle marker objects - for now, just store as text
            # Later we can implement full marker support
            if not hasattr(symbolizer, 'marker_text'):
                symbolizer.marker_text = prop_value
        
        # Coverage/Raster object properties (Phase B Priority 1)
        elif prop_name in ['hillshading', 'hill_shading']:
            # Handle hillShading: {factor: 56; sun: {azimuth: 45.0; elevation: 60.0}}
            symbolizer.hill_shading = self._parse_hill_shading_object(properties)
    
    def _parse_color_map(self, prop_value: str):
        """Parse color map from string format."""
        try:
            # Handle array format: [0 96 136 73, 900 226 219 167, ...]
            if prop_value.startswith('[') and prop_value.endswith(']'):
                content = prop_value.strip('[]').strip()
                if content:
                    # Split by commas first
                    segments = [seg.strip() for seg in content.split(',')]
                    parsed_segments = []
                    for seg in segments:
                        # Each segment is "value r g b"
                        parts = seg.strip().split()
                        if len(parts) >= 4:
                            try:
                                value = float(parts[0])
                                r, g, b = int(parts[1]), int(parts[2]), int(parts[3])
                                parsed_segments.append({'value': value, 'r': r, 'g': g, 'b': b})
                            except (ValueError, IndexError):
                                parsed_segments.append({'raw': seg})
                        else:
                            parsed_segments.append({'raw': seg})
                    return parsed_segments
            return {'raw_value': prop_value}
        except Exception:
            return {'raw_value': prop_value}
    
    def _parse_opacity_map(self, prop_value: str):
        """Parse opacity map from string format."""
        # Similar logic to color map but for opacity values
        return {'raw_value': prop_value}
    
    def _parse_hill_shading_object(self, properties: dict):
        """Parse hill shading object from properties."""
        result = {}
        for key, value in properties.items():
            if key == 'sun':
                # Handle nested sun object: {azimuth: 45.0; elevation: 60.0}
                if value.startswith('{') and value.endswith('}'):
                    sun_content = value.strip('{}').strip()
                    sun_props = {}
                    if sun_content:
                        for part in sun_content.split(';'):
                            if ':' in part:
                                k, v = part.split(':', 1)
                                try:
                                    sun_props[k.strip()] = float(v.strip())
                                except ValueError:
                                    sun_props[k.strip()] = v.strip()
                    result['sun'] = sun_props
                else:
                    result['sun'] = value
            else:
                # Handle other properties like factor
                try:
                    result[key] = float(value) if '.' in value else int(value)
                except ValueError:
                    result[key] = value
        return result
