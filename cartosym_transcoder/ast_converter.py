"""
AST to Pydantic converter for CartoSym CSS.

This module converts ANTLR-generated AST nodes to Pydantic models.
"""

import re as _re
from typing import Dict, Any, List, Optional, Union
from .ast import StyleSheet as AstStyleSheet, StylingRule as AstStylingRule, Metadata as AstMetadata
from .models import (
    Style, StylingRule, Metadata, 
    Symbolizer, Fill, Stroke, Marker, Label, BaseCartoSymModel
)


def _strip_inline_comment(s: str) -> str:
    """Strip a ``//`` line comment from *s*, but only outside single/double-quoted
    string literals so that URLs like ``'http://...'`` are preserved intact."""
    result = []
    i = 0
    while i < len(s):
        ch = s[i]
        if ch in ("'", '"'):
            quote = ch
            result.append(ch)
            i += 1
            while i < len(s) and s[i] != quote:
                result.append(s[i])
                i += 1
            if i < len(s):
                result.append(s[i])
                i += 1
        elif ch == '/' and i + 1 < len(s) and s[i + 1] == '/':
            break
        else:
            result.append(ch)
            i += 1
    return ''.join(result).rstrip()


def _parse_resource_string(inner: str) -> dict:
    """Parse ``uri: 'val'; path: 'val'; ...`` (content inside ``{}``) into a
    resource dict, stripping surrounding quotes from each value."""
    result = {}
    for part in inner.split(';'):
        part = part.strip()
        if not part:
            continue
        if ':' in part:
            key, _, value = part.partition(':')
            key = key.strip()
            value = value.strip().strip("'\"")
            if key:
                result[key] = value
    return result


def _parse_hotspot_string(s: str) -> list:
    """Convert ``'N unit N unit'`` (e.g. ``'50 pc 50 pc'``) to a unitPoint
    array ``[{unit: N}, {unit: N}]`` as expected by the CS.JSON schema."""
    parts = s.strip().split()
    if len(parts) == 4:
        try:
            x_val = float(parts[0]) if '.' in parts[0] else int(parts[0])
            x_unit = parts[1]
            y_val = float(parts[2]) if '.' in parts[2] else int(parts[2])
            y_unit = parts[3]
            return [{x_unit: x_val}, {y_unit: y_val}]
        except (ValueError, IndexError):
            pass
    elif len(parts) == 2:
        try:
            return [int(parts[0]), int(parts[1])]
        except ValueError:
            pass
    return s  # keep as-is if unparseable


def _parse_nested_props(props_str: str) -> dict:
    """Brace-aware CSS property parser (mirrors parser._parse_element_props)."""
    props = {}
    parts = []
    current = ""
    depth = 0
    for char in props_str:
        if char == '{':
            depth += 1
            current += char
        elif char == '}':
            if depth > 0:
                depth -= 1
                current += char
            else:
                break
        elif char in (';', ',') and depth == 0:
            if current.strip():
                parts.append(current.strip())
            current = ""
        else:
            current += char
    if current.strip():
        parts.append(current.strip())
    for part in parts:
        if '//' in part:
            part = _strip_inline_comment(part)
        if not part:
            continue
        if ':' in part:
            colon_idx = part.index(':')
            key = part[:colon_idx].strip()
            value = part[colon_idx + 1:].strip()
            if key:
                props[key] = value
    return props


def _parse_color_value(v: str):
    """Convert a color string to schema-valid form: hex #rrggbb or #rgb → [r,g,b]; web names kept as-is."""
    if isinstance(v, str) and v.startswith('#') and len(v) in (4, 7):
        hex_str = v[1:]
        if len(hex_str) == 3:
            hex_str = ''.join(c * 2 for c in hex_str)
        try:
            return [int(hex_str[0:2], 16), int(hex_str[2:4], 16), int(hex_str[4:6], 16)]
        except ValueError:
            pass
    return v


def _normalize_graphic_element(el: dict) -> None:
    """Normalize a raw graphic-element dict in-place so it validates against
    the CartoSym JSON schema.

    Handles:
    * ``opacity`` / ``bold`` / ``italic`` strings → proper Python types
    * ``alignment: "left middle"`` → ``["left", "middle"]`` array
    * ``font: "{ face: 'Arial'; size: 12; ... }"`` string → proper dict
    """
    if not isinstance(el, dict):
        return

    # Convert opacity string to float for any element type
    if 'opacity' in el and isinstance(el['opacity'], str):
        try:
            el['opacity'] = float(el['opacity'])
        except ValueError:
            pass

    el_type = el.get('type', '')

    if el_type == 'Text':
        # text: NAME (unquoted identifier) → {"property": "NAME"} property reference
        # text: 'literal' (quoted)         → strip quotes, keep as plain string
        if 'text' in el and isinstance(el['text'], str):
            t = el['text'].strip()
            if (t.startswith("'") and t.endswith("'")) or (t.startswith('"') and t.endswith('"')):
                el['text'] = t[1:-1]  # strip quotes → literal string
            else:
                # bare identifier → property reference
                el['text'] = {'property': t}

        # alignment: "left middle"  OR  { left, middle }  → ["left", "middle"]
        if 'alignment' in el and isinstance(el['alignment'], str):
            a = el['alignment'].strip()
            if a.startswith('{') and a.endswith('}'):
                # { left, middle } block syntax
                parts = [p.strip() for p in a[1:-1].split(',') if p.strip()]
            else:
                parts = a.split()
            if len(parts) == 2:
                el['alignment'] = parts

        # font: "{ face: 'Arial'; ... }" → proper dict
        if 'font' in el and isinstance(el['font'], str):
            font_str = el['font'].strip()
            # Strip outer braces if present
            if font_str.startswith('{') and font_str.endswith('}'):
                font_inner = font_str[1:-1]
            else:
                font_inner = font_str
            font_raw = _parse_nested_props(font_inner)
            font_dict: dict = {}
            for k, v in font_raw.items():
                v = v.strip().strip("'\"")
                if k == 'size':
                    try:
                        font_dict['size'] = int(v)
                    except ValueError:
                        try:
                            font_dict['size'] = float(v)
                        except ValueError:
                            font_dict['size'] = v
                elif k in ('bold', 'italic', 'underline'):
                    font_dict[k] = (v.lower() == 'true')
                elif k == 'opacity':
                    try:
                        font_dict[k] = float(v)
                    except ValueError:
                        font_dict[k] = v
                elif k == 'color':
                    font_dict['color'] = _parse_color_value(v)
                elif k == 'outline' and isinstance(v, str) and v.startswith('{') and v.endswith('}'):
                    # outline: { size: 3, opacity: 0.75, color: white } → proper dict
                    outline_raw = _parse_nested_props(v[1:-1])
                    outline_dict = {}
                    for ok, ov in outline_raw.items():
                        ov = ov.strip().strip("'\"")
                        if ok == 'size':
                            try:
                                outline_dict['size'] = int(ov)
                            except ValueError:
                                try:
                                    outline_dict['size'] = float(ov)
                                except ValueError:
                                    outline_dict['size'] = ov
                        elif ok == 'opacity':
                            try:
                                outline_dict['opacity'] = float(ov)
                            except ValueError:
                                outline_dict['opacity'] = ov
                        elif ok == 'color':
                            outline_dict['color'] = _parse_color_value(ov)
                        else:
                            outline_dict[ok] = ov
                    font_dict['outline'] = outline_dict
                else:
                    font_dict[k] = v
            el['font'] = font_dict

    elif el_type == 'Image':
        # Convert image resource string "{uri: '...'; path: '...'; ...}" to a
        # proper resource dict as required by the schema.
        if 'image' in el and isinstance(el['image'], str):
            img_str = el['image'].strip()
            if img_str.startswith('{') and img_str.endswith('}'):
                resource = _parse_resource_string(img_str[1:-1])
                if resource:
                    el['image'] = resource
        # Convert hotSpot string "N unit N unit" → [{unit: N}, {unit: N}]
        if 'hotSpot' in el and isinstance(el['hotSpot'], str):
            el['hotSpot'] = _parse_hotspot_string(el['hotSpot'])
        # Convert alphaThreshold string → float
        if 'alphaThreshold' in el and isinstance(el['alphaThreshold'], str):
            try:
                el['alphaThreshold'] = float(el['alphaThreshold'])
            except ValueError:
                pass


class AstToPydanticConverter:
    """Converts ANTLR AST nodes to Pydantic models."""
    
    def convert_stylesheet(self, ast_stylesheet: AstStyleSheet) -> Style:
        """Convert AST StyleSheet to Pydantic Style model, preserving nested rules only as children."""
        try:
            # Convert metadata
            metadata = None
            if ast_stylesheet.metadata:
                metadata_dict = {}
                _list_fields = {'keywords', 'authors', 'geoDataClasses'}
                _multiline_fields = {'abstract', 'description', 'title'}
                for meta in ast_stylesheet.metadata:
                    if not (hasattr(meta, 'key') and hasattr(meta, 'value')):
                        continue
                    key, value = meta.key, meta.value
                    if key in _list_fields:
                        if isinstance(value, str):
                            items = [v.strip() for v in value.split(',') if v.strip()]
                        elif isinstance(value, list):
                            items = value
                        else:
                            items = [str(value)]
                        existing = metadata_dict.get(key, [])
                        metadata_dict[key] = existing + items
                    elif key in _multiline_fields and key in metadata_dict:
                        metadata_dict[key] = metadata_dict[key] + '\n' + value
                    else:
                        metadata_dict[key] = value
                if metadata_dict:
                    metadata = Metadata(**metadata_dict)

            # Convert variables (if present)
            variables = None
            if hasattr(ast_stylesheet, 'variables') and ast_stylesheet.variables:
                from .models.styles import Variable
                variables = [Variable(name=v.name, value=v.value, type=getattr(v, 'type', None)) for v in ast_stylesheet.variables]

            # Convert only top-level styling rules (do not flatten nested rules)
            styling_rules = []
            if ast_stylesheet.styling_rules and hasattr(ast_stylesheet.styling_rules, 'rules'):
                for ast_rule in ast_stylesheet.styling_rules.rules:
                    pydantic_rule = self._convert_styling_rule(ast_rule)
                    if pydantic_rule:
                        styling_rules.append(pydantic_rule)

            return Style(
                metadata=metadata,
                styling_rules=styling_rules,
                variables=variables
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
                op = selector.get("op", "")
                is_comparison = op in ['=', '<', '<=', '>', '>=', '!=']
                for i, arg in enumerate(selector["args"]):
                    # Convert string arguments to property references in comparisons
                    if isinstance(arg, str):
                        # In a comparison, right-hand arguments (index > 0) are VALUE literals
                        # (they came from CHARACTER_LITERALs like 'parking') – keep as plain strings.
                        if is_comparison and i > 0:
                            processed_args.append(arg)
                        # Check if it's a simple identifier that should be a property
                        # Don't convert if it contains quotes, spaces, dots, or is purely numeric
                        elif arg and not any(c in arg for c in ['"', "'", ' ', '.']) and not arg.replace('-', '').replace('_', '').isdigit():
                            # Simple identifier on left side - convert to property reference
                            processed_args.append({"property": arg})
                        else:
                            # Keep as-is (string literal or numeric string)
                            processed_args.append(arg)
                    else:
                        # Recursively process non-string arguments
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
            elif "property" in selector:
                prop = selector["property"]
                # Check if property contains an embedded expression
                for op in ['>=', '<=', '!=', '=', '>', '<']:
                    if op in prop and not (prop.startswith('"') or prop.startswith("'")):
                        parts = prop.split(op, 1)
                        if len(parts) == 2:
                            left_part = parts[0].strip()
                            right_part = parts[1].strip()
                            
                            # Determine if left part is system property or regular property
                            if '.' in left_part and any(left_part.startswith(prefix) for prefix in ['viz', 'dataLayer', 'feature']):
                                left_arg = {"sysId": left_part}
                            # Special case: certain properties are known system identifiers
                            elif left_part in ['featuresGeometryDimensions', 'featuresGeometry', 'geometryDimensions']:
                                left_arg = {"sysId": f"dataLayer.{left_part}"}
                            else:
                                left_arg = {"property": left_part}
                            
                            # Convert right part
                            if right_part.isdigit():
                                right_arg = int(right_part)
                            elif right_part.replace('.', '').replace('-', '').isdigit():
                                right_arg = float(right_part)
                            else:
                                right_arg = right_part.strip('\'"')
                            
                            return {
                                "op": op,
                                "args": [left_arg, right_arg]
                            }
            return selector
        elif isinstance(selector, str):
            # Handle string selectors that should be expressions
            return self._convert_string_to_json_selector(selector)
        elif isinstance(selector, dict) and "property" in selector and len(selector) == 1:
            # Invalid standalone property selector - convert to a valid boolean expression
            prop_name = selector["property"]
            # Convert standalone property to boolean check (property IS NOT NULL)
            return {
                "op": "!=",
                "args": [{"property": prop_name}, None]
            }
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
                    if '.' in left_part and any(left_part.startswith(prefix) for prefix in ['viz', 'dataLayer']):
                        left_arg = {"sysId": left_part}
                    elif left_part in ['validDate', 'FunctionCode', 'FunctionTitle']:
                        left_arg = {"property": left_part}
                    else:
                        left_arg = left_part
                    # Convert right part (handle sysId for dot notation)
                    if right_part.isdigit():
                        right_arg = int(right_part)
                    elif right_part.replace('.', '').isdigit():
                        right_arg = float(right_part)
                    elif '.' in right_part and any(right_part.startswith(prefix) for prefix in ['viz', 'dataLayer']):
                        right_arg = {"sysId": right_part}
                    elif right_part in ['validDate', 'FunctionCode', 'FunctionTitle']:
                        right_arg = {"property": right_part}
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
        
        # Handle MemberAccessExpression (system properties, recursive for deep access)
        if hasattr(expression, 'object') and hasattr(expression, 'member'):
            def get_full_property(expr):
                if hasattr(expr, 'object') and hasattr(expr, 'member'):
                    return get_full_property(expr.object) + '.' + str(expr.member)
                elif hasattr(expr, 'name'):
                    return str(expr.name)
                else:
                    return str(expr)
            full_property = get_full_property(expression)
            # Top-level prefix check for sysId
            top_level = full_property.split('.', 1)[0]
            if top_level in ['viz', 'vis', 'dataLayer']:
                return {"sysId": full_property}
            else:
                return {"property": full_property}
        
        # Handle FunctionCallExpression
        if hasattr(expression, 'function_name') and hasattr(expression, 'arguments'):
            func_name = expression.function_name
            # DATE('...') → { "date": "..." } (OGC scalar-data-types)
            if func_name.upper() == 'DATE' and len(expression.arguments) == 1:
                arg = expression.arguments[0]
                date_val = arg.value if hasattr(arg, 'value') else str(arg)
                # Strip surrounding quotes if present
                if isinstance(date_val, str):
                    date_val = date_val.strip("'\"")
                return {"date": date_val}
            # Other function calls use "op" (not "function")
            return {
                "op": func_name,
                "args": [self._convert_expression_to_json_selector(arg) for arg in expression.arguments]
            }

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
        """Retourne la propriété système telle quelle (mapping identique)."""
        return prop
    
    def _convert_literal_value(self, value: Union[str, int, float]) -> Union[str, int, float, list]:
        """Convert literal value to appropriate JSON type with proper CS.JSON formatting."""
        if isinstance(value, (int, float)):
            return value
            
        if not isinstance(value, str):
            value = str(value)
            
        # Handle quoted strings
        if (value.startswith("'") and value.endswith("'")) or (value.startswith('"') and value.endswith('"')):
            return value[1:-1]  # Remove quotes
        
        # Handle hex colors - convert to [r, g, b] array (CS.JSON color schema only accepts
        # arrays, {r,g,b} objects, or web color names – not hex strings)
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
        """Convert AST StylingRule to Pydantic StylingRule, including nested selectors and stylingRuleName."""
        try:
            selector = None
            rule_name = None
            styling_rule_name = None
            # Support explicit stylingRuleName if present
            if hasattr(ast_rule, 'styling_rule_name') and ast_rule.styling_rule_name:
                styling_rule_name = ast_rule.styling_rule_name
            # Always process selectors for any rule (top-level or nested)
            if hasattr(ast_rule, 'selectors') and ast_rule.selectors:
                if len(ast_rule.selectors) > 1:
                    selector_args = []
                    for sel in ast_rule.selectors:
                        if hasattr(sel, 'name') and sel.name:
                            selector_args.append({"op": "=", "args": [{"sysId": "dataLayer.id"}, sel.name]})
                            if not rule_name:
                                rule_name = sel.name
                        elif hasattr(sel, 'conditions') and sel.conditions:
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
                    if selector:
                        selector = self._post_process_selector(selector)
                else:
                    sel = ast_rule.selectors[0]
                    if hasattr(sel, 'name') and sel.name:
                        rule_name = sel.name
                        selector = {"op": "=", "args": [{"sysId": "dataLayer.id"}, sel.name]}
                    elif hasattr(sel, 'conditions') and sel.conditions:
                        if len(sel.conditions) > 1:
                            condition_args = []
                            for condition in sel.conditions:
                                json_condition = self._convert_expression_to_json_selector(condition)
                                if isinstance(json_condition, dict):
                                    condition_args.append(json_condition)
                            if condition_args:
                                selector = {"op": "and", "args": condition_args}
                        else:
                            selector = self._convert_expression_to_json_selector(sel.conditions[0])
                    else:
                        selector = None
                    if selector:
                        selector = self._post_process_selector(selector)
            elif hasattr(ast_rule, 'name') and ast_rule.name:
                rule_name = ast_rule.name
                selector = [rule_name]
            elif hasattr(ast_rule, 'selector') and ast_rule.selector:
                selector = ["Unknown"]

            # Convert symbolizer
            symbolizer = None
            if hasattr(ast_rule, 'symbolizer') and ast_rule.symbolizer:
                symbolizer = self._convert_symbolizer(ast_rule.symbolizer)

            # Convert nested rules (ensure selectors are processed for each)
            nested_rules = None
            if hasattr(ast_rule, 'nested_rules') and ast_rule.nested_rules:
                nested_rules = []
                for nested_ast_rule in ast_rule.nested_rules:
                    nested_pydantic_rule = self._convert_styling_rule(nested_ast_rule)
                    if nested_pydantic_rule:
                        nested_rules.append(nested_pydantic_rule)

            return StylingRule(
                name=rule_name,
                styling_rule_name=styling_rule_name,
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
                symbolizer_data['zOrder'] = ast_symbolizer.z_order
            
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
                symbolizer_data['single_channel'] = self._convert_channel_value(ast_symbolizer.single_channel)
            elif hasattr(ast_symbolizer, 'singleChannel') and ast_symbolizer.singleChannel is not None:
                symbolizer_data['single_channel'] = self._convert_channel_value(ast_symbolizer.singleChannel)
            
            if hasattr(ast_symbolizer, 'color_channels') and ast_symbolizer.color_channels is not None:
                symbolizer_data['color_channels'] = self._convert_channel_value(ast_symbolizer.color_channels)
            elif hasattr(ast_symbolizer, 'colorChannels') and ast_symbolizer.colorChannels is not None:
                symbolizer_data['color_channels'] = self._convert_channel_value(ast_symbolizer.colorChannels)
            
            if hasattr(ast_symbolizer, 'alpha_channel') and ast_symbolizer.alpha_channel is not None:
                symbolizer_data['alpha_channel'] = self._convert_channel_value(ast_symbolizer.alpha_channel)
            elif hasattr(ast_symbolizer, 'alphaChannel') and ast_symbolizer.alphaChannel is not None:
                symbolizer_data['alpha_channel'] = self._convert_channel_value(ast_symbolizer.alphaChannel)
            
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
        """Convert AST Marker to Pydantic Marker, including position and opacity if present, and preserving all element properties."""
        try:
            from .models.symbolizers import Marker as PydanticMarker
            marker_data = {}
            # Position and opacity at marker level
            if hasattr(ast_marker, 'position') and ast_marker.position is not None:
                marker_data['position'] = ast_marker.position
            if hasattr(ast_marker, 'opacity') and ast_marker.opacity is not None:
                marker_data['opacity'] = ast_marker.opacity
            # Elements — either a list of graphics or an indexed override {index, value}
            if hasattr(ast_marker, 'elements') and ast_marker.elements is not None:
                elements = ast_marker.elements
                if isinstance(elements, dict) and 'index' in elements and 'value' in elements:
                    # Indexed override: keep the {index, value} form
                    el_dict = dict(elements['value']) if hasattr(elements['value'], 'items') else elements['value']
                    if isinstance(el_dict, dict) and 'position' in el_dict:
                        pos = el_dict['position']
                        if isinstance(pos, str):
                            from .models.symbolizers import UnitPoint as ModelUnitPoint
                            el_dict['position'] = ModelUnitPoint.from_string(pos)
                        elif isinstance(pos, dict) and 'x' in pos and 'y' in pos:
                            el_dict['position'] = pos
                    _normalize_graphic_element(el_dict)
                    marker_data['elements'] = {'index': elements['index'], 'value': el_dict}
                else:
                    converted_elements = []
                    for el in (elements if isinstance(elements, list) else [elements]):
                        # Accept dicts (from marker.elements[N] patch) or objects
                        el_dict = dict(el) if hasattr(el, 'items') else el
                        # Ensure type is present (default to Dot if missing)
                        if isinstance(el_dict, dict) and 'type' not in el_dict:
                            el_dict['type'] = 'Dot'
                        # Convert position if present and as string or dict
                        if isinstance(el_dict, dict) and 'position' in el_dict:
                            pos = el_dict['position']
                            if isinstance(pos, str):
                                from .models.symbolizers import UnitPoint as ModelUnitPoint
                                el_dict['position'] = ModelUnitPoint.from_string(pos)
                            elif isinstance(pos, dict) and 'x' in pos and 'y' in pos:
                                el_dict['position'] = pos
                        _normalize_graphic_element(el_dict)
                        converted_elements.append(el_dict)
                    marker_data['elements'] = converted_elements
            # If no data was collected the marker would serialize to {}, which
            # fails schema validation.  Return None so the symbolizer omits it.
            if not marker_data:
                return None
            return PydanticMarker(**marker_data)
        except Exception as e:
            print(f"Warning: Failed to convert marker: {e}")
            return None
    
    def _convert_channel_value(self, value: Any) -> Any:
        """Convert a channel value to proper expression format.
        
        If value is a simple identifier string, convert to property reference.
        If value is multiple space-separated identifiers, convert to array of property references.
        If value contains arithmetic operators, parse it as a mathematical expression.
        Otherwise return as-is for numeric values or complex expressions.
        """
        if isinstance(value, str):
            # Check if it contains arithmetic operators - if so, parse as expression
            if any(op in value for op in ['+', '-', '*', '/', '(', ')']):
                try:
                    return self._parse_arithmetic_expression(value)
                except Exception as e:
                    print(f"Warning: Failed to parse arithmetic expression '{value}': {e}")
                    return value
            
            # Check if it contains multiple space-separated identifiers (like "B04 B03 B02")
            parts = value.split()
            if len(parts) > 1:
                # Multiple identifiers - check if they're all simple identifiers
                if all(p and not any(c in p for c in ['+', '-', '*', '/', '(', ')', '[', ']', '{', '}', ';', '.']) for p in parts):
                    # Convert to array of property references
                    return [{'property': p} for p in parts]
            # Single identifier - check if it's a simple identifier (no spaces, no operators)
            elif value and not any(c in value for c in [' ', '+', '-', '*', '/', '(', ')', '[', ']', '{', '}', ';']):
                # Check if it's a numeric literal
                try:
                    # Try to parse as number
                    if '.' in value:
                        return float(value)
                    else:
                        return int(value)
                except ValueError:
                    # Not a number - convert to property reference
                    return {"property": value}
            # Otherwise return as-is
            return value
        elif isinstance(value, (int, float)):
            # Numeric value - return as-is
            return value
        elif isinstance(value, dict):
            # Already an expression object
            return value
        else:
            return value
    
    def _parse_arithmetic_expression(self, expr: str) -> Dict[str, Any]:
        """Parse arithmetic expression string into JSON expression format.
        
        Handles basic arithmetic: +, -, *, / with parentheses.
        Example: "(B08 - B04)/(B08 + B04)" -> {"op": "/", "args": [...]}
        """
        expr = expr.strip()
        
        # Remove outer parentheses if they wrap the entire expression
        while expr.startswith('(') and expr.endswith(')'):
            # Check if these parentheses match
            depth = 0
            matches = True
            for i, c in enumerate(expr):
                if c == '(':
                    depth += 1
                elif c == ')':
                    depth -= 1
                if depth == 0 and i < len(expr) - 1:
                    matches = False
                    break
            if matches:
                expr = expr[1:-1].strip()
            else:
                break
        
        # Parse operators with precedence: / and * before + and -
        # Find the last + or - that's not inside parentheses (lowest precedence)
        depth = 0
        last_add_sub = -1
        for i in range(len(expr) - 1, -1, -1):
            if expr[i] == ')':
                depth += 1
            elif expr[i] == '(':
                depth -= 1
            elif depth == 0 and expr[i] in ['+', '-']:
                # Make sure it's not a unary operator at the start
                if i > 0:
                    last_add_sub = i
                    break
        
        if last_add_sub > 0:
            op = expr[last_add_sub]
            left = expr[:last_add_sub].strip()
            right = expr[last_add_sub + 1:].strip()
            return {
                "op": op,
                "args": [
                    self._parse_arithmetic_expression(left),
                    self._parse_arithmetic_expression(right)
                ]
            }
        
        # Find the last * or / that's not inside parentheses (higher precedence)
        depth = 0
        last_mul_div = -1
        for i in range(len(expr) - 1, -1, -1):
            if expr[i] == ')':
                depth += 1
            elif expr[i] == '(':
                depth -= 1
            elif depth == 0 and expr[i] in ['*', '/']:
                last_mul_div = i
                break
        
        if last_mul_div > 0:
            op = expr[last_mul_div]
            left = expr[:last_mul_div].strip()
            right = expr[last_mul_div + 1:].strip()
            return {
                "op": op,
                "args": [
                    self._parse_arithmetic_expression(left),
                    self._parse_arithmetic_expression(right)
                ]
            }
        
        # No operators found - must be a terminal (identifier or number)
        # Check if it's a number
        try:
            if '.' in expr:
                return float(expr)
            else:
                return int(expr)
        except ValueError:
            # It's an identifier - convert to property reference
            return {"property": expr}
    
    def _convert_label(self, ast_label) -> Optional[Label]:
        """Convert AST Label to Pydantic Label, preserving all element properties."""
        try:
            from .models.symbolizers import Label as PydanticLabel
            label_data = {}
            # Position and opacity at label level
            if hasattr(ast_label, 'position') and ast_label.position is not None:
                label_data['position'] = ast_label.position
            if hasattr(ast_label, 'opacity') and ast_label.opacity is not None:
                label_data['opacity'] = ast_label.opacity
            if hasattr(ast_label, 'placement') and ast_label.placement is not None:
                label_data['placement'] = ast_label.placement
            # Elements — list of graphics
            if hasattr(ast_label, 'elements') and ast_label.elements is not None:
                elements = ast_label.elements
                converted_elements = []
                for el in (elements if isinstance(elements, list) else [elements]):
                    el_dict = dict(el) if hasattr(el, 'items') else el
                    if isinstance(el_dict, dict) and 'type' not in el_dict:
                        el_dict['type'] = 'Dot'
                    if isinstance(el_dict, dict) and 'position' in el_dict:
                        pos = el_dict['position']
                        if isinstance(pos, str):
                            from .models.symbolizers import UnitPoint as ModelUnitPoint
                            el_dict['position'] = ModelUnitPoint.from_string(pos)
                        elif isinstance(pos, dict) and 'x' in pos and 'y' in pos:
                            el_dict['position'] = pos
                    _normalize_graphic_element(el_dict)
                    converted_elements.append(el_dict)
                label_data['elements'] = converted_elements
            if not label_data:
                return None
            return PydanticLabel(**label_data)
        except Exception as e:
            print(f"Warning: Failed to convert label: {e}")
            return None
    
    def _convert_color_map(self, ast_color_map) -> Optional[Any]:
        """Convert AST ColorMap to array format per JSON schema."""
        try:
            if isinstance(ast_color_map, (list, tuple)):
                # Return array directly per JSON schema
                return list(ast_color_map)
            elif isinstance(ast_color_map, dict):
                # Handle idOrFnExpression format
                return dict(ast_color_map)
            else:
                # Handle string or other formats - return as-is for validation to catch
                return str(ast_color_map)
        except Exception as e:
            print(f"Warning: Failed to convert color map: {e}")
            return None
    
    def _convert_opacity_map(self, ast_opacity_map) -> Optional[Any]:
        """Convert AST OpacityMap to array format per JSON schema."""
        try:
            if isinstance(ast_opacity_map, (list, tuple)):
                # Return array directly per JSON schema
                return list(ast_opacity_map)
            elif isinstance(ast_opacity_map, dict):
                # Handle idOrFnExpression format
                return dict(ast_opacity_map)
            else:
                # Handle string or other formats
                return str(ast_opacity_map)
        except Exception as e:
            print(f"Warning: Failed to convert opacity map: {e}")
            return None
    
    def _convert_hill_shading(self, ast_hill_shading) -> Optional[Dict[str, Any]]:
        """Convert AST HillShading to dictionary per JSON schema."""
        try:
            if isinstance(ast_hill_shading, dict):
                # Handle object format: {factor: 56; sun: {azimuth: 45.0; elevation: 60.0}; colorMap: [...]; opacityMap: [...]}
                result = {}
                for key, value in ast_hill_shading.items():
                    if key == "sun":
                        if isinstance(value, dict):
                            result["sun"] = dict(value)
                        elif isinstance(value, str) and value.startswith('{') and value.endswith('}'):
                            # Parse sun string like "{azimuth: 45.0; elevation: 60.0}" to object
                            sun_obj = {}
                            content = value.strip('{}').strip()
                            for part in content.split(';'):
                                if ':' in part:
                                    k, v = part.split(':', 1)
                                    try:
                                        sun_obj[k.strip()] = float(v.strip())
                                    except ValueError:
                                        sun_obj[k.strip()] = v.strip()
                            result["sun"] = sun_obj
                        else:
                            result["sun"] = value
                    elif key == "colorMap":
                        # colorMap inside hillShading uses 0-1 values for first element
                        result["colorMap"] = value if isinstance(value, (list, dict)) else str(value)
                    elif key == "opacityMap":
                        # opacityMap inside hillShading
                        result["opacityMap"] = value if isinstance(value, (list, dict)) else str(value)
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
