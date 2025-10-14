"""
AST to Pydantic converter for CartoSym CSS.

This module converts ANTLR-generated AST nodes to Pydantic models.
"""

from typing import Dict, Any, List, Optional, Union
from .ast import StyleSheet as AstStyleSheet, StylingRule as AstStylingRule, Metadata as AstMetadata
from .models import (
    Style, StylingRule, Metadata, 
    Symbolizer, Fill, Stroke, Marker, Label, BaseCartoSymModel
)


class AstToPydanticConverter:
    """Converts ANTLR AST nodes to Pydantic models."""
    
    def convert_stylesheet(self, ast_stylesheet: AstStyleSheet) -> Style:
        """Convert AST StyleSheet to Pydantic Style model."""
        try:
            # Convert metadata
            metadata = None
            if ast_stylesheet.metadata:
                metadata_dict = {}
                for meta in ast_stylesheet.metadata:
                    if hasattr(meta, 'key') and hasattr(meta, 'value'):
                        metadata_dict[meta.key] = meta.value
                
                if metadata_dict:
                    metadata = Metadata(**metadata_dict)
            
            # Convert styling rules
            styling_rules = []
            if ast_stylesheet.styling_rules and hasattr(ast_stylesheet.styling_rules, 'rules'):
                for ast_rule in ast_stylesheet.styling_rules.rules:
                    pydantic_rule = self._convert_styling_rule(ast_rule)
                    if pydantic_rule:
                        styling_rules.append(pydantic_rule)
            
            return Style(
                metadata=metadata,
                styling_rules=styling_rules
            )
            
        except Exception as e:
            raise ValueError(f"Failed to convert AST stylesheet: {e}") from e
    
    def _format_selector_expression(self, expression) -> str:
        """Format a selector expression into a readable string."""
        try:
            # Handle IdentifierExpression
            if hasattr(expression, 'name') and hasattr(expression, 'type'):
                if str(expression.type) == "ExpressionType.IDENTIFIER":
                    return expression.name
            
            # Handle MemberAccessExpression
            if hasattr(expression, 'object') and hasattr(expression, 'member'):
                obj_str = self._format_selector_expression(expression.object)
                return f"{obj_str}.{expression.member}"
            
            # Handle BinaryOperationExpression
            if hasattr(expression, 'left') and hasattr(expression, 'right') and hasattr(expression, 'operator'):
                left_str = self._format_selector_expression(expression.left)
                right_str = self._format_selector_expression(expression.right)
                
                # Map operator enum to string
                op_str = str(expression.operator)
                if 'AND' in op_str:
                    op_str = ' and '
                elif 'OR' in op_str:
                    op_str = ' or '
                elif 'EQ' in op_str or 'EQUAL' in op_str:
                    op_str = ' = '
                elif 'LT' in op_str and 'LESS_THAN' in op_str:
                    op_str = ' < '
                elif 'GT' in op_str and 'GREATER_THAN' in op_str:
                    op_str = ' > '
                elif 'LTE' in op_str or 'LESS_EQUAL' in op_str:
                    op_str = ' <= '
                elif 'GTE' in op_str or 'GREATER_EQUAL' in op_str:
                    op_str = ' >= '
                elif 'NEQ' in op_str or 'NOT_EQUAL' in op_str:
                    op_str = ' != '
                else:
                    # Extract operator from string representation and add spaces
                    if '.' in op_str:
                        op_name = op_str.split('.')[-1].lower()
                        if op_name in ['and', 'or', 'not']:
                            op_str = f" {op_name} "
                        elif op_name in ['equal', 'eq']:
                            op_str = ' = '
                        elif op_name in ['less_than', 'lt']:
                            op_str = ' < '
                        elif op_name in ['greater_than', 'gt']:
                            op_str = ' > '
                        elif op_name in ['less_equal', 'lte']:
                            op_str = ' <= '
                        elif op_name in ['greater_equal', 'gte']:
                            op_str = ' >= '
                        elif op_name in ['not_equal', 'neq']:
                            op_str = ' != '
                        else:
                            op_str = f" {op_name} "
                    else:
                        op_str = f" {op_str} "
                
                return f"{left_str}{op_str}{right_str}"
            
            # Handle LiteralExpression/ConstantExpression
            if hasattr(expression, 'value'):
                if isinstance(expression.value, str):
                    # Handle string literals with quotes if needed
                    if expression.value.startswith("'") or expression.value.startswith('"'):
                        return expression.value
                    return f"'{expression.value}'"
                return str(expression.value)
            
            # Handle FunctionCallExpression
            if hasattr(expression, 'function_name') and hasattr(expression, 'arguments'):
                args_str = ", ".join(self._format_selector_expression(arg) for arg in expression.arguments)
                return f"{expression.function_name}({args_str})"
            
            # Handle simple name attribute
            if hasattr(expression, 'name'):
                return expression.name
                
            # Fallback to string representation
            return str(expression)
            
        except Exception as e:
            # If anything goes wrong, return the string representation
            return str(expression)

    def _post_process_selector(self, selector) -> Dict[str, Any]:
        """Post-process selector to fix parsing issues and ensure proper JSON structure."""
        if isinstance(selector, dict):
            if "op" in selector and "args" in selector:
                # Post-process arguments recursively
                processed_args = []
                for arg in selector["args"]:
                    processed_args.append(self._post_process_selector(arg))
                selector["args"] = processed_args
                return selector
            elif "sysId" in selector:
                sysid = selector["sysId"]
                # Check if sysId contains an embedded expression
                for op in ['>=', '<=', '!=', '=', '>', '<']:
                    if op in sysid and not (sysid.startswith('"') or sysid.startswith("'")):
                        parts = sysid.split(op, 1)
                        if len(parts) == 2:
                            left_part = parts[0].strip()
                            right_part = parts[1].strip()
                            
                            # Convert right part
                            if right_part.isdigit():
                                right_arg = int(right_part)
                            elif right_part.replace('.', '').isdigit():
                                right_arg = float(right_part)
                            else:
                                right_arg = right_part.strip('\'"')
                            
                            return {
                                "op": op,
                                "args": [{"sysId": left_part}, right_arg]
                            }
            return selector
        elif isinstance(selector, str):
            # Handle string selectors that should be expressions
            return self._convert_string_to_json_selector(selector)
        else:
            return selector
    
    def _convert_string_to_json_selector(self, selector_str: str) -> Dict[str, Any]:
        """Convert string selector to proper JSON structure."""
        # Handle expressions embedded in strings
        for op in ['>=', '<=', '!=', '=', '>', '<']:
            if op in selector_str and not (selector_str.startswith('"') or selector_str.startswith("'")):
                parts = selector_str.split(op, 1)
                if len(parts) == 2:
                    left_part = parts[0].strip()
                    right_part = parts[1].strip().strip('\'"')
                    
                    # Determine if left part is system property or regular property
                    if '.' in left_part and any(left_part.startswith(prefix) for prefix in ['viz', 'vis', 'dataLayer']):
                        left_arg = {"sysId": left_part.replace('viz.', 'vis.')}
                    elif left_part in ['validDate', 'FunctionCode', 'FunctionTitle']:
                        left_arg = {"property": left_part}
                    else:
                        left_arg = left_part
                    
                    # Convert right part
                    if right_part.isdigit():
                        right_arg = int(right_part)
                    elif right_part.replace('.', '').isdigit():
                        right_arg = float(right_part)
                    else:
                        right_arg = right_part
                    
                    return {
                        "op": op,
                        "args": [left_arg, right_arg]
                    }
        
        # If no operator found, treat as property
        return {"property": selector_str}

    def _convert_expression_to_json_selector(self, expression) -> Dict[str, Any]:
        """
        Convert ANTLR expression to CS.JSON selector format.
        Enhanced version based on AST analysis from debug_antlr.py output.
        """
        if not expression:
            return {}
        
        try:
            # Handle ANTLR context objects (from grammar)
            if hasattr(expression, 'getRuleIndex'):
                from .grammar.generated.CartoSymCSSGrammar import CartoSymCSSGrammar
                rule_name = CartoSymCSSGrammar.ruleNames[expression.getRuleIndex()]
                return self._convert_antlr_expression(expression, rule_name)
            
            # Handle BinaryOperationExpression (AST objects)
            if hasattr(expression, 'left') and hasattr(expression, 'right') and hasattr(expression, 'operator'):
                left_arg = self._convert_expression_to_json_selector(expression.left)
                right_arg = self._convert_expression_to_json_selector(expression.right)
                
                # Map operator enum to string
                op_str = str(expression.operator)
                if 'AND' in op_str:
                    op = 'and'
                elif 'OR' in op_str:
                    op = 'or'
                elif 'EQ' in op_str or 'EQUAL' in op_str:
                    op = '='
                elif 'LT' in op_str and 'LESS_THAN' in op_str:
                    op = '<'
                elif 'GT' in op_str and 'GREATER_THAN' in op_str:
                    op = '>'
                elif 'LTE' in op_str or 'LESS_EQUAL' in op_str:
                    op = '<='
                elif 'GTE' in op_str or 'GREATER_EQUAL' in op_str:
                    op = '>='
                elif 'NEQ' in op_str or 'NOT_EQUAL' in op_str:
                    op = '!='
                else:
                    # Extract operator from string representation
                    if '.' in op_str:
                        op_name = op_str.split('.')[-1].lower()
                        op = op_name
                    else:
                        op = str(expression.operator)
                
                return {
                    "op": op,
                    "args": [left_arg, right_arg]
                }
            
            # Handle MemberAccessExpression (system properties)
            if hasattr(expression, 'object') and hasattr(expression, 'member'):
                obj_name = expression.object.name if hasattr(expression.object, 'name') else str(expression.object)
                member_name = expression.member
                
                # Map system properties
                property_mapping = {
                    'viz.sd': 'vis.id',
                    'viz.timeInterval': 'vis.timeInterval',
                    'dataLayer.type': 'dataLayer.type',
                    'dataLayer.id': 'dataLayer.id',
                    'dataLayer.featuresGeometryDimensions': 'dataLayer.featuresGeometryDimensions'
                }
                
                full_property = f"{obj_name}.{member_name}"
                mapped_property = property_mapping.get(full_property, full_property)
                
                if obj_name in ['viz', 'vis', 'dataLayer']:
                    return {"sysId": mapped_property}
                else:
                    return {"property": member_name}
            
            # Handle IdentifierExpression (simple properties)
            if hasattr(expression, 'name'):
                return self._convert_identifier(expression.name)
            
            # Handle LiteralExpression/ConstantExpression
            if hasattr(expression, 'value'):
                return self._convert_literal_value(expression.value)
            
            # Handle string representation (fallback)
            if isinstance(expression, str):
                return self._convert_identifier(expression)
            
            # Final fallback - convert to string
            return str(expression)
            
        except Exception as e:
            # Return as string if conversion fails
            return str(expression)
    
    def _convert_antlr_expression(self, expr_ctx, rule_name: str) -> Dict[str, Any]:
        """
        Convert ANTLR expression context based on the actual AST structure.
        Based on detailed AST analysis showing binary expressions as:
        expression -> expression + operator + expression
        """
        if rule_name == 'expression':
            if hasattr(expr_ctx, 'getChildCount'):
                child_count = expr_ctx.getChildCount()
                
                # Binary expression pattern: expression + operator + expression (count = 3)
                if child_count == 3:
                    left_child = expr_ctx.getChild(0)
                    op_child = expr_ctx.getChild(1)  
                    right_child = expr_ctx.getChild(2)
                    
                    # Check if middle child is an operator
                    if hasattr(op_child, 'getRuleIndex'):
                        from .grammar.generated.CartoSymCSSGrammar import CartoSymCSSGrammar
                        op_rule = CartoSymCSSGrammar.ruleNames[op_child.getRuleIndex()]
                        
                        if op_rule in ['relationalOperator', 'binaryLogicalOperator']:
                            # This is a binary operation
                            left_arg = self._convert_antlr_expression(left_child, 'expression')
                            operator = op_child.getText()
                            right_arg = self._convert_antlr_expression(right_child, 'expression')
                            
                            return {
                                "op": operator,
                                "args": [left_arg, right_arg]
                            }
                    
                    # Property access pattern: expression + '.' + terminal
                    elif (hasattr(left_child, 'getRuleIndex') and
                          not hasattr(op_child, 'getRuleIndex') and op_child.getText() == '.' and
                          not hasattr(right_child, 'getRuleIndex')):
                        
                        # Build property path: obj.member
                        left_part = self._convert_antlr_expression(left_child, 'expression')
                        right_part = right_child.getText()
                        
                        if isinstance(left_part, str):
                            full_path = f"{left_part}.{right_part}"
                        elif isinstance(left_part, dict) and "sysId" in left_part:
                            full_path = f"{left_part['sysId']}.{right_part}"
                        elif isinstance(left_part, dict) and "property" in left_part:
                            full_path = f"{left_part['property']}.{right_part}"
                        else:
                            full_path = f"{left_part}.{right_part}"
                        
                        return self._convert_identifier(full_path)
                
                # Single child expression
                elif child_count == 1:
                    child = expr_ctx.getChild(0)
                    if hasattr(child, 'getRuleIndex'):
                        from .grammar.generated.CartoSymCSSGrammar import CartoSymCSSGrammar
                        child_rule = CartoSymCSSGrammar.ruleNames[child.getRuleIndex()]
                        return self._convert_antlr_expression(child, child_rule)
                    else:
                        # Terminal
                        return self._convert_identifier(child.getText())
        
        elif rule_name == 'idOrConstant':
            # Check for expConstant child (numeric literal)
            if hasattr(expr_ctx, 'getChildCount') and expr_ctx.getChildCount() == 1:
                child = expr_ctx.getChild(0)
                if hasattr(child, 'getRuleIndex'):
                    from .grammar.generated.CartoSymCSSGrammar import CartoSymCSSGrammar
                    child_rule = CartoSymCSSGrammar.ruleNames[child.getRuleIndex()]
                    if child_rule == 'expConstant':
                        return self._convert_literal_value(child.getText())
            
            # Otherwise treat as identifier
            return self._convert_identifier(expr_ctx.getText())
        
        elif rule_name == 'expString':
            # String literal - remove quotes
            text = expr_ctx.getText()
            if (text.startswith("'") and text.endswith("'")) or (text.startswith('"') and text.endswith('"')):
                return text[1:-1]
            return text
        
        # Default: get text and convert as identifier
        return self._convert_identifier(expr_ctx.getText())
    
    def _convert_identifier(self, name: str) -> Union[Dict[str, Any], str, int, float]:
        """Convert identifier to appropriate JSON selector part with proper system property mapping."""
        # Handle embedded operators first
        for op in ['>=', '<=', '!=', '=', '>', '<']:
            if f'{op}' in name and not (name.startswith('"') or name.startswith("'")):
                parts = name.split(op, 1)
                if len(parts) == 2:
                    left_part = parts[0].strip()
                    right_part = parts[1].strip()
                    
                    # Convert left part (property)
                    if '.' in left_part:
                        if any(left_part.startswith(prefix) for prefix in ['viz', 'vis', 'dataLayer']):
                            # Map system properties correctly
                            mapped_prop = self._map_system_property(left_part)
                            left_arg = {"sysId": mapped_prop}
                        else:
                            left_arg = {"property": left_part}
                    else:
                        if left_part in ['validDate', 'FunctionCode', 'FunctionTitle']:
                            left_arg = {"property": left_part}
                        elif any(left_part.startswith(prefix) for prefix in ['viz', 'vis', 'dataLayer']):
                            mapped_prop = self._map_system_property(left_part)
                            left_arg = {"sysId": mapped_prop}
                        else:
                            left_arg = left_part
                    
                    # Convert right part (value)
                    right_arg = self._convert_literal_value(right_part)
                    
                    return {
                        "op": op,
                        "args": [left_arg, right_arg]
                    }
        
        # No operator - determine property type
        if '.' in name:
            if any(name.startswith(prefix) for prefix in ['viz', 'vis', 'dataLayer']):
                mapped_prop = self._map_system_property(name)
                return {"sysId": mapped_prop}
            else:
                return {"property": name}
        else:
            if name in ['validDate', 'FunctionCode', 'FunctionTitle']:
                return {"property": name}
            elif any(name.startswith(prefix) for prefix in ['viz', 'vis', 'dataLayer']):
                mapped_prop = self._map_system_property(name)
                return {"sysId": mapped_prop}
            else:
                return self._convert_literal_value(name)
    
    def _map_system_property(self, prop: str) -> str:
        """Map CSCSS system properties to CS.JSON format."""
        # Normalize viz to vis first
        prop = prop.replace('viz.', 'vis.')
        
        # System property mappings based on CS.JSON reference
        system_mappings = {
            'vis.sd': 'vis.id',  # Scale denominator -> vis id
            'vis.timeInterval.start.date': 'vis.timeInterval.start.date',
            'vis.timeInterval.end.date': 'vis.timeInterval.end.date',
            'dataLayer.type': 'dataLayer.type',
            'dataLayer.id': 'dataLayer.id', 
            'dataLayer.featuresGeometryDimensions': 'dataLayer.featuresGeometryDimensions'
        }
        
        return system_mappings.get(prop, prop)
    
    def _convert_literal_value(self, value: Union[str, int, float]) -> Union[str, int, float, list]:
        """Convert literal value to appropriate JSON type with proper CS.JSON formatting."""
        if isinstance(value, (int, float)):
            return value
            
        if not isinstance(value, str):
            value = str(value)
            
        # Handle quoted strings
        if (value.startswith("'") and value.endswith("'")) or (value.startswith('"') and value.endswith('"')):
            return value[1:-1]  # Remove quotes
        
        # Handle hex colors - convert to RGB array for CS.JSON compliance
        if value.startswith('#') and len(value) == 7:
            try:
                hex_color = value[1:]
                r = int(hex_color[0:2], 16)
                g = int(hex_color[2:4], 16) 
                b = int(hex_color[4:6], 16)
                return [r, g, b]
            except ValueError:
                return value  # Keep as string if not valid hex
        
        # Handle numbers with units (e.g., "2.0px") -> UnitValue format for CS.JSON
        if value.endswith(('px', 'em', '%', 'pt', 'pc')):
            units = ['px', 'em', 'pt', 'pc', '%']
            for unit in units:
                if value.endswith(unit):
                    number_part = value[:-len(unit)]
                    try:
                        if '.' in number_part:
                            # Return as CS.JSON UnitValue format for Pydantic compatibility
                            from .models.types import UnitValue, UnitType
                            return UnitValue(value=float(number_part), unit=getattr(UnitType, unit.upper(), unit))
                        else:
                            # Return as CS.JSON UnitValue format for Pydantic compatibility
                            from .models.types import UnitValue, UnitType
                            return UnitValue(value=int(number_part), unit=getattr(UnitType, unit.upper(), unit))
                    except (ValueError, ImportError):
                        # Fallback to string if UnitValue creation fails
                        return value
        
        # Handle pure numbers
        if value.isdigit():
            return int(value)
        
        try:
            if '.' in value:
                return float(value)
        except ValueError:
            pass
        
        # Handle boolean values
        if value.lower() == 'true':
            return True
        elif value.lower() == 'false':
            return False
        
        # Keep known color names as strings (CS.JSON supports named colors)
        color_names = ['red', 'green', 'blue', 'yellow', 'black', 'white', 'gray', 'grey', 
                      'darkGray', 'lightGray', 'darkGreen', 'lightGreen', 'darkBlue', 'lightBlue',
                      'darkRed', 'lightRed', 'orange', 'purple', 'brown', 'pink', 'cyan', 'magenta']
        if value in color_names:
            return value
        
        # Keep known identifiers as strings
        return value

    def _convert_styling_rule(self, ast_rule: AstStylingRule) -> Optional[StylingRule]:
        """Convert AST StylingRule to Pydantic StylingRule."""
        try:
            # Extract rule name and selector
            selector = None
            rule_name = None
            
            # Check if we have selectors (plural) from parser
            if hasattr(ast_rule, 'selectors') and ast_rule.selectors:
                # If we have multiple selectors, create an AND operation
                if len(ast_rule.selectors) > 1:
                    # Multiple selectors - combine with AND
                    selector_args = []
                    for sel in ast_rule.selectors:
                        if hasattr(sel, 'name') and sel.name:
                            # Simple name selector like "Landuse" -> system property
                            selector_args.append({"op": "=", "args": [{"sysId": "dataLayer.id"}, sel.name]})
                            if not rule_name:
                                rule_name = sel.name
                        elif hasattr(sel, 'conditions') and sel.conditions:
                            # Conditional selector - convert to JSON structure
                            for condition in sel.conditions:
                                json_condition = self._convert_expression_to_json_selector(condition)
                                if isinstance(json_condition, dict):
                                    selector_args.append(json_condition)
                        elif hasattr(sel, 'expression') and sel.expression:
                            json_expr = self._convert_expression_to_json_selector(sel.expression)
                            if isinstance(json_expr, dict):
                                selector_args.append(json_expr)
                    
                    if len(selector_args) > 1:
                        selector = {"op": "and", "args": selector_args}
                    elif len(selector_args) == 1:
                        selector = selector_args[0]
                    else:
                        selector = None
                    
                    # Post-process selector
                    if selector:
                        selector = self._post_process_selector(selector)
                        
                else:
                    # Single selector
                    sel = ast_rule.selectors[0]
                    if hasattr(sel, 'name') and sel.name:
                        # Simple name selector
                        rule_name = sel.name
                        selector = {"op": "=", "args": [{"sysId": "dataLayer.id"}, sel.name]}
                    elif hasattr(sel, 'conditions') and sel.conditions:
                        # Complex conditional selector
                        if len(sel.conditions) > 1:
                            # Multiple conditions - combine with AND
                            condition_args = []
                            for condition in sel.conditions:
                                json_condition = self._convert_expression_to_json_selector(condition)
                                if isinstance(json_condition, dict):
                                    condition_args.append(json_condition)
                            if condition_args:
                                selector = {"op": "and", "args": condition_args}
                        else:
                            # Single condition
                            selector = self._convert_expression_to_json_selector(sel.conditions[0])
                    else:
                        selector = None
            
            # Fallback to simple name-based selector
            elif hasattr(ast_rule, 'name') and ast_rule.name:
                rule_name = ast_rule.name
                selector = [rule_name]
            elif hasattr(ast_rule, 'selector') and ast_rule.selector:
                # TODO: Parse complex selectors when available
                selector = ["Unknown"]
            
            # Convert symbolizer
            symbolizer = None
            if hasattr(ast_rule, 'symbolizer') and ast_rule.symbolizer:
                symbolizer = self._convert_symbolizer(ast_rule.symbolizer)
            
            # Convert nested rules (Phase B Coverage Support)
            nested_rules = None
            if hasattr(ast_rule, 'nested_rules') and ast_rule.nested_rules:
                nested_rules = []
                for nested_ast_rule in ast_rule.nested_rules:
                    nested_pydantic_rule = self._convert_styling_rule(nested_ast_rule)
                    if nested_pydantic_rule:
                        nested_rules.append(nested_pydantic_rule)
            
            return StylingRule(
                name=rule_name,
                selector=selector,
                symbolizer=symbolizer,
                nested_rules=nested_rules
            )
            
        except Exception as e:
            print(f"Warning: Failed to convert styling rule: {e}")
            return None
    
    def _convert_symbolizer(self, ast_symbolizer) -> Optional[Symbolizer]:
        """Convert AST Symbolizer to Pydantic Symbolizer."""
        try:
            symbolizer_data = {}
            
            # Basic properties
            if hasattr(ast_symbolizer, 'visibility') and ast_symbolizer.visibility is not None:
                symbolizer_data['visibility'] = ast_symbolizer.visibility
            
            if hasattr(ast_symbolizer, 'opacity') and ast_symbolizer.opacity is not None:
                symbolizer_data['opacity'] = ast_symbolizer.opacity
            
            if hasattr(ast_symbolizer, 'z_order') and ast_symbolizer.z_order is not None:
                symbolizer_data['z_order'] = ast_symbolizer.z_order
            
            # Complex properties
            if hasattr(ast_symbolizer, 'fill') and ast_symbolizer.fill:
                fill = self._convert_fill(ast_symbolizer.fill)
                if fill:
                    symbolizer_data['fill'] = fill
            
            if hasattr(ast_symbolizer, 'stroke') and ast_symbolizer.stroke:
                stroke = self._convert_stroke(ast_symbolizer.stroke)
                if stroke:
                    symbolizer_data['stroke'] = stroke
            
            if hasattr(ast_symbolizer, 'marker') and ast_symbolizer.marker:
                marker = self._convert_marker(ast_symbolizer.marker)
                if marker:
                    symbolizer_data['marker'] = marker
            
            if hasattr(ast_symbolizer, 'label') and ast_symbolizer.label:
                label = self._convert_label(ast_symbolizer.label)
                if label:
                    symbolizer_data['label'] = label
            
            # Coverage/Raster properties - Phase B Priority 1
            if hasattr(ast_symbolizer, 'single_channel') and ast_symbolizer.single_channel is not None:
                symbolizer_data['single_channel'] = ast_symbolizer.single_channel
            elif hasattr(ast_symbolizer, 'singleChannel') and ast_symbolizer.singleChannel is not None:
                symbolizer_data['single_channel'] = ast_symbolizer.singleChannel
            
            if hasattr(ast_symbolizer, 'color_channels') and ast_symbolizer.color_channels is not None:
                symbolizer_data['color_channels'] = ast_symbolizer.color_channels
            elif hasattr(ast_symbolizer, 'colorChannels') and ast_symbolizer.colorChannels is not None:
                symbolizer_data['color_channels'] = ast_symbolizer.colorChannels
            
            if hasattr(ast_symbolizer, 'alpha_channel') and ast_symbolizer.alpha_channel is not None:
                symbolizer_data['alpha_channel'] = ast_symbolizer.alpha_channel
            elif hasattr(ast_symbolizer, 'alphaChannel') and ast_symbolizer.alphaChannel is not None:
                symbolizer_data['alpha_channel'] = ast_symbolizer.alphaChannel
            
            if hasattr(ast_symbolizer, 'color_map') and ast_symbolizer.color_map is not None:
                symbolizer_data['color_map'] = self._convert_color_map(ast_symbolizer.color_map)
            elif hasattr(ast_symbolizer, 'colorMap') and ast_symbolizer.colorMap is not None:
                symbolizer_data['color_map'] = self._convert_color_map(ast_symbolizer.colorMap)
            
            if hasattr(ast_symbolizer, 'opacity_map') and ast_symbolizer.opacity_map is not None:
                symbolizer_data['opacity_map'] = self._convert_opacity_map(ast_symbolizer.opacity_map)
            elif hasattr(ast_symbolizer, 'opacityMap') and ast_symbolizer.opacityMap is not None:
                symbolizer_data['opacity_map'] = self._convert_opacity_map(ast_symbolizer.opacityMap)
            
            if hasattr(ast_symbolizer, 'hill_shading') and ast_symbolizer.hill_shading is not None:
                symbolizer_data['hill_shading'] = self._convert_hill_shading(ast_symbolizer.hill_shading)
            elif hasattr(ast_symbolizer, 'hillShading') and ast_symbolizer.hillShading is not None:
                symbolizer_data['hill_shading'] = self._convert_hill_shading(ast_symbolizer.hillShading)
            
            return Symbolizer(**symbolizer_data) if symbolizer_data else None
            
        except Exception as e:
            print(f"Warning: Failed to convert symbolizer: {e}")
            return None
    
    def _convert_fill(self, ast_fill) -> Optional[Fill]:
        """Convert AST Fill to Pydantic Fill with proper value conversion."""
        try:
            fill_data = {}
            
            if hasattr(ast_fill, 'color') and ast_fill.color is not None:
                # Use _convert_literal_value for proper hex/color conversion
                fill_data['color'] = self._convert_literal_value(str(ast_fill.color))
            
            if hasattr(ast_fill, 'opacity') and ast_fill.opacity is not None:
                fill_data['opacity'] = float(ast_fill.opacity)
            
            return Fill(**fill_data) if fill_data else None
            
        except Exception as e:
            print(f"Warning: Failed to convert fill: {e}")
            return None
    
    def _convert_stroke(self, ast_stroke) -> Optional[Stroke]:
        """Convert AST Stroke to Pydantic Stroke with proper value conversion."""
        try:
            stroke_data = {}
            
            if hasattr(ast_stroke, 'color') and ast_stroke.color is not None:
                # Use _convert_literal_value for proper hex/color conversion
                stroke_data['color'] = self._convert_literal_value(str(ast_stroke.color))
            
            if hasattr(ast_stroke, 'width') and ast_stroke.width is not None:
                # Use _convert_literal_value for proper unit conversion
                width_value = str(ast_stroke.width)
                stroke_data['width'] = self._convert_literal_value(width_value)
            
            if hasattr(ast_stroke, 'opacity') and ast_stroke.opacity is not None:
                stroke_data['opacity'] = float(ast_stroke.opacity)
            
            return Stroke(**stroke_data) if stroke_data else None
            
        except Exception as e:
            print(f"Warning: Failed to convert stroke: {e}")
            return None
    
    def _convert_marker(self, ast_marker) -> Optional[Marker]:
        """Convert AST Marker to Pydantic Marker."""
        try:
            # TODO: Implement when marker properties are defined
            return Marker()
        except Exception as e:
            print(f"Warning: Failed to convert marker: {e}")
            return None
    
    def _convert_label(self, ast_label) -> Optional[Label]:
        """Convert AST Label to Pydantic Label."""
        try:
            # TODO: Implement when label properties are defined  
            return Label()
        except Exception as e:
            print(f"Warning: Failed to convert label: {e}")
            return None
    
    def _convert_color_map(self, ast_color_map) -> Optional[Dict[str, Any]]:
        """Convert AST ColorMap to dictionary (temporary implementation)."""
        try:
            if isinstance(ast_color_map, (list, tuple)):
                # Handle array format: [0 96 136 73, 900 226 219 167, ...]
                return {"raw_array": list(ast_color_map)}
            elif isinstance(ast_color_map, dict):
                return dict(ast_color_map)
            else:
                # Handle string or other formats
                return {"raw_value": str(ast_color_map)}
        except Exception as e:
            print(f"Warning: Failed to convert color map: {e}")
            return {"raw_value": str(ast_color_map)}
    
    def _convert_opacity_map(self, ast_opacity_map) -> Optional[Dict[str, Any]]:
        """Convert AST OpacityMap to dictionary (temporary implementation)."""
        try:
            if isinstance(ast_opacity_map, (list, tuple)):
                return {"raw_array": list(ast_opacity_map)}
            elif isinstance(ast_opacity_map, dict):
                return dict(ast_opacity_map)
            else:
                return {"raw_value": str(ast_opacity_map)}
        except Exception as e:
            print(f"Warning: Failed to convert opacity map: {e}")
            return {"raw_value": str(ast_opacity_map)}
    
    def _convert_hill_shading(self, ast_hill_shading) -> Optional[Dict[str, Any]]:
        """Convert AST HillShading to dictionary (temporary implementation)."""
        try:
            if isinstance(ast_hill_shading, dict):
                # Handle object format: {factor: 56; sun: {azimuth: 45.0; elevation: 60.0}}
                result = {}
                for key, value in ast_hill_shading.items():
                    if key == "sun" and isinstance(value, dict):
                        result["sun"] = dict(value)
                    else:
                        result[key] = value
                return result
            else:
                return {"raw_value": str(ast_hill_shading)}
        except Exception as e:
            print(f"Warning: Failed to convert hill shading: {e}")
            return {"raw_value": str(ast_hill_shading)}


def convert_ast_to_pydantic(ast_stylesheet: AstStyleSheet) -> Style:
    """
    Convenience function to convert AST StyleSheet to Pydantic Style.
    
    Args:
        ast_stylesheet: ANTLR-generated AST stylesheet
        
    Returns:
        Pydantic Style model
        
    Raises:
        ValueError: If conversion fails
    """
    converter = AstToPydanticConverter()
    return converter.convert_stylesheet(ast_stylesheet)
