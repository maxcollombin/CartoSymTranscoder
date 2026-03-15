"""
Enhanced AST to Pydantic converter with Phase A expression support.

Extended with CQL2 parsing for spatial, temporal, array predicates,
BETWEEN / IN / LIKE / IS NULL operators, and WKT / temporal literals.
"""

import re
from typing import List, Optional, Dict, Union, Any
from .models.expressions import *
from .models.base import BaseCartoSymModel
from .models.styles import Style, Metadata, StylingRule
from .models.symbolizers import Symbolizer, Fill, Stroke, Marker
from .ast import (
    StyleSheet, StylingRuleList, StylingRule, Symbolizer,
    Fill, Stroke, Metadata as AstMetadata
)

# ---------------------------------------------------------------------------
# CQL2 function-name sets (case-insensitive matching)
# ---------------------------------------------------------------------------
_SPATIAL_PREDICATES = {
    's_intersects', 's_contains', 's_within', 's_touches',
    's_crosses', 's_disjoint', 's_overlaps', 's_equals',
}
_SPATIAL_RELATE = 's_relate'
_TEMPORAL_PREDICATES = {
    't_before', 't_after', 't_meets', 't_metby',
    't_overlaps', 't_overlappedby', 't_begins', 't_begunby',
    't_during', 't_contains', 't_ends', 't_endedby',
    't_equals', 't_intersects', 't_disjoint',
}
_ARRAY_PREDICATES = {
    'a_equals', 'a_contains', 'a_containedby', 'a_overlaps',
}
_WKT_TYPES = {
    'point', 'linestring', 'polygon',
    'multipoint', 'multilinestring', 'multipolygon',
    'geometrycollection',
}
_WKT_TO_GEOJSON = {
    'point': 'Point', 'linestring': 'LineString', 'polygon': 'Polygon',
    'multipoint': 'MultiPoint', 'multilinestring': 'MultiLineString',
    'multipolygon': 'MultiPolygon', 'geometrycollection': 'GeometryCollection',
}

# Import ANTLR generated classes - will be used when needed
# These are loaded dynamically by the main parser


class ExpressionParser:
    """Parser for converting ANTLR expression contexts to Pydantic expressions."""
    
    @staticmethod
    def parse_expression(ctx) -> Expression:
        """Convert ANTLR expression context to Pydantic Expression."""
        if not ctx:
            return None

        # Always use the original text with spaces for parsing
        original_text = None
        if hasattr(ctx, 'start') and hasattr(ctx, 'stop') and hasattr(ctx.start, 'source'):
            try:
                input_stream = ctx.start.source
                start_idx = ctx.start.start
                stop_idx = ctx.stop.stop
                original_text = input_stream.strdata[start_idx:stop_idx + 1]
            except Exception:
                pass
        if not original_text:
            original_text = ctx.getText() if hasattr(ctx, 'getText') else str(ctx)

        # Check for logical operations with proper spacing (case-insensitive)
        text_lower = original_text.lower()
        if ' and ' in text_lower or ' or ' in text_lower:
            # But not if ' and ' only appears inside a BETWEEN expression
            if not ExpressionParser._only_between_and(original_text):
                return ExpressionParser._parse_logical_expression(original_text)

        # --- CQL2 postfix operators (before relational so they take priority) ---
        cql2 = ExpressionParser._try_parse_cql2_operator(original_text)
        if cql2 is not None:
            return cql2

        # Check for relational operations with proper spacing
        for op in ['>=', '<=', '!=', '=', '>', '<']:
            if f' {op} ' in original_text:
                return ExpressionParser._parse_relational_expression(original_text, op)

        # Handle member access (contains dots)
        if '.' in original_text and not original_text.startswith('"') and not original_text.startswith("'"):
            return ExpressionParser._parse_member_access_from_text(original_text)

        # Handle string literals
        if (original_text.startswith('"') and original_text.endswith('"')) or \
            (original_text.startswith("'") and original_text.endswith("'")):
            return StringExpression(value=original_text[1:-1])

        # Handle numbers
        if original_text.replace('.', '').replace('-', '').isdigit():
            try:
                value = int(original_text) if '.' not in original_text else float(original_text)
                return ConstantExpression(value=value)
            except ValueError:
                pass

        # Handle boolean constants
        if original_text.lower() in ['true', 'false']:
            return ConstantExpression(value=original_text.lower() == 'true')

        # Handle function calls — dispatch CQL2 predicates / literals first
        if '(' in original_text and ')' in original_text:
            cql2_func = ExpressionParser._try_parse_cql2_function(original_text)
            if cql2_func is not None:
                return cql2_func
            return ExpressionParser._parse_function_call_from_text(original_text)

        # Handle object literals {color: red; opacity: 0.5}
        if original_text.startswith('{') and original_text.endswith('}'):
            return ExpressionParser._parse_instance_from_text(original_text)

        # Default: treat as identifier
        return IdentifierExpression(name=original_text)
    
    @staticmethod
    def _parse_logical_expression(text: str) -> BinaryOperationExpression:
        """Parse logical expressions like 'a and b' or 'x or y'."""
        # Always split at the top-level logical operator (lowest precedence), respecting parentheses
        text_lower = text.lower()
        paren_depth = 0
        # Find top-level ' or '
        for i in range(len(text)):
            if text[i] == '(': paren_depth += 1
            elif text[i] == ')': paren_depth -= 1
            elif paren_depth == 0 and text_lower[i:i+4] == ' or ':
                left = text[:i].strip()
                right = text[i+4:].strip()
                return BinaryOperationExpression(
                    left=ExpressionParser.parse_expression(left),
                    operator=BinaryOperator.OR,
                    right=ExpressionParser.parse_expression(right)
                )
        # Find top-level ' and '
        paren_depth = 0
        for i in range(len(text)):
            if text[i] == '(': paren_depth += 1
            elif text[i] == ')': paren_depth -= 1
            elif paren_depth == 0 and text_lower[i:i+5] == ' and ':
                left = text[:i].strip()
                right = text[i+5:].strip()
                return BinaryOperationExpression(
                    left=ExpressionParser.parse_expression(left),
                    operator=BinaryOperator.AND,
                    right=ExpressionParser.parse_expression(right)
                )
        # No logical op at top level, parse as relational or single
        return ExpressionParser._parse_single_expression(text)
    
    @staticmethod  
    def _parse_relational_expression(text: str, operator_str: str) -> BinaryOperationExpression:
        """Parse relational expressions like 'a = b' or 'x < 5'."""
        # Always check for logical operators at the same level first
        text_lower = text.lower()
        paren_depth = 0
        for i in range(len(text) - 4, -1, -1):  # -4 for ' or '
            if text[i] == ')':
                paren_depth += 1
            elif text[i] == '(': 
                paren_depth -= 1
            elif paren_depth == 0 and text_lower[i:i+4] == ' or ':
                left = text[:i].strip()
                right = text[i+4:].strip()
                return ExpressionParser._parse_logical_expression(text)
        paren_depth = 0
        for i in range(len(text) - 5, -1, -1):  # -5 for ' and '
            if text[i] == ')':
                paren_depth += 1
            elif text[i] == '(': 
                paren_depth -= 1
            elif paren_depth == 0 and text_lower[i:i+5] == ' and ':
                left = text[:i].strip()
                right = text[i+5:].strip()
                return ExpressionParser._parse_logical_expression(text)

        # No logical op at this level, parse as relational
        op_pos = -1
        paren_depth = 0
        op_pattern = f' {operator_str} '
        for i in range(len(text) - len(op_pattern) + 1):
            if text[i] == '(': 
                paren_depth += 1
            elif text[i] == ')':
                paren_depth -= 1
            elif paren_depth == 0 and text[i:i+len(op_pattern)] == op_pattern:
                op_pos = i
                break
        if op_pos != -1:
            left_part = text[:op_pos].strip()
            right_part = text[op_pos+len(op_pattern):].strip()
            left_expr = ExpressionParser._parse_single_expression(left_part)
            right_expr = ExpressionParser._parse_single_expression(right_part)
            operator = ExpressionParser._map_relational_operator(operator_str)
            return BinaryOperationExpression(left=left_expr, operator=operator, right=right_expr)
        # Fallback: try without spaces for cases like 'a=b'
        if operator_str in text:
            parts = text.split(operator_str, 1)
            if len(parts) == 2:
                left_expr = ExpressionParser._parse_single_expression(parts[0].strip())
                right_expr = ExpressionParser._parse_single_expression(parts[1].strip())
                operator = ExpressionParser._map_relational_operator(operator_str)
                return BinaryOperationExpression(left=left_expr, operator=operator, right=right_expr)
        return IdentifierExpression(name=text)
    
    @staticmethod
    def _parse_member_access_from_text(text: str) -> MemberAccessExpression:
        """Parse member access from text like 'dataLayer.type'."""
        parts = text.split('.')
        if len(parts) == 2:
            return MemberAccessExpression(
                object=IdentifierExpression(name=parts[0]),
                member=parts[1]
            )
        elif len(parts) > 2:
            # Chain of member accesses: a.b.c.d
            base = IdentifierExpression(name=parts[0])
            for i in range(1, len(parts) - 1):
                base = MemberAccessExpression(object=base, member=parts[i])
            return MemberAccessExpression(object=base, member=parts[-1])
        
        return IdentifierExpression(name=text)
    
    @staticmethod
    def _parse_function_call_from_text(text: str) -> FunctionCallExpression:
        """Parse function calls like 'Text(...)' from text."""
        if '(' not in text:
            return IdentifierExpression(name=text)
        
        func_name = text.split('(')[0].strip()
        args_part = text[text.find('(')+1:text.rfind(')')]
        
        # Simple argument parsing - can be enhanced
        arguments = []
        if args_part.strip():
            # For now, treat each comma-separated part as a separate argument
            for arg in args_part.split(','):
                arg = arg.strip()
                arguments.append(ExpressionParser._parse_single_expression(arg))
        
        return FunctionCallExpression(function_name=func_name, arguments=arguments)
    
    @staticmethod
    def _parse_instance_from_text(text: str) -> InstanceExpression:
        """Parse object instances like '{color: gray; opacity: 0.5}' from text."""
        # Remove braces
        content = text.strip('{}').strip()
        
        properties = []
        if content:
            # Split by semicolon for properties
            for prop_def in content.split(';'):
                prop_def = prop_def.strip()
                if ':' in prop_def:
                    key, value = prop_def.split(':', 1)
                    key = key.strip()
                    value = value.strip()
                    prop_expr = ExpressionParser._parse_single_expression(value)
                    properties.append(PropertyAssignment(property=key, value=prop_expr))
        
        return InstanceExpression(class_name=None, properties=properties)
    
    @staticmethod
    def _parse_expression_text(text: str) -> Expression:
        """Helper to parse expression from text string."""
        text = text.strip()
        
        # Handle parentheses - remove outer parentheses if they wrap the entire expression
        if text.startswith('(') and text.endswith(')'):
            # Check if these parentheses actually wrap the whole expression
            paren_depth = 0
            for i, char in enumerate(text):
                if char == '(':
                    paren_depth += 1
                elif char == ')':
                    paren_depth -= 1
                    if paren_depth == 0 and i < len(text) - 1:
                        # Parentheses don't wrap the whole expression
                        break
            else:
                # Parentheses wrap the whole expression, remove them
                text = text[1:-1].strip()
        
        # Check for logical operations (case-insensitive)
        text_lower = text.lower()
        if ' and ' in text_lower or ' or ' in text_lower:
            # But not if ' and ' only appears inside a BETWEEN expression
            if not ExpressionParser._only_between_and(text):
                return ExpressionParser._parse_logical_expression(text)

        # --- CQL2 postfix operators (BETWEEN, IN, LIKE, IS NULL) ---
        cql2 = ExpressionParser._try_parse_cql2_operator(text)
        if cql2 is not None:
            return cql2

        # Check for relational operations  
        for op in ['>=', '<=', '!=', '=', '>', '<']:
            if f' {op} ' in text:
                return ExpressionParser._parse_relational_expression(text, op)
        
        # Handle string literals
        if (text.startswith('"') and text.endswith('"')) or \
           (text.startswith("'") and text.endswith("'")):
            return StringExpression(value=text[1:-1])
        
        # Handle function calls — CQL2 predicates / literals first
        if '(' in text and text.endswith(')'):
            cql2_func = ExpressionParser._try_parse_cql2_function(text)
            if cql2_func is not None:
                return cql2_func
            return ExpressionParser._parse_function_call_from_text(text)
        
        # Handle numbers
        try:
            if '.' in text:
                return ConstantExpression(value=float(text))
            else:
                return ConstantExpression(value=int(text))
        except ValueError:
            pass
        
        # Handle boolean
        if text.lower() in ['true', 'false']:
            return ConstantExpression(value=text.lower() == 'true')
        
        # Handle member access
        if '.' in text:
            return ExpressionParser._parse_member_access_from_text(text)
        
        # Default: identifier
        return IdentifierExpression(name=text)
    
    @staticmethod
    def _parse_member_access(ctx) -> MemberAccessExpression:
        """Parse member access like 'object.member'."""
        # This is complex - we need to handle chains like a.b.c.d
        parts = ctx.getText().split('.')
        if len(parts) == 2:
            obj_name, member = parts
            return MemberAccessExpression(
                object=IdentifierExpression(name=obj_name),
                member=member
            )
        elif len(parts) > 2:
            # Chain of member accesses: a.b.c becomes (a.b).c
            base = IdentifierExpression(name=parts[0])
            for i in range(1, len(parts) - 1):
                base = MemberAccessExpression(object=base, member=parts[i])
            return MemberAccessExpression(object=base, member=parts[-1])
        else:
            return IdentifierExpression(name=parts[0])
    
    @staticmethod
    def _parse_constant(ctx) -> ConstantExpression:
        """Parse constant value."""
        text = ctx.getText()
        unit = None
        
        # Check for unit
        if hasattr(ctx, 'UNIT') and ctx.UNIT():
            unit = ctx.UNIT().getText()
            # Remove unit from text
            text = text.replace(unit, '').strip()
        
        # Parse value
        try:
            if '.' in text:
                value = float(text)
            else:
                value = int(text)
        except ValueError:
            value = text
            
        return ConstantExpression(value=value, unit=unit)
    
    @staticmethod
    def _parse_string(ctx) -> StringExpression:
        """Parse string literal."""
        text = ctx.getText()
        # Remove quotes
        if text.startswith('"') and text.endswith('"'):
            text = text[1:-1]
        elif text.startswith("'") and text.endswith("'"):
            text = text[1:-1]
        return StringExpression(value=text)
    
    @staticmethod
    def _parse_function_call(ctx) -> FunctionCallExpression:
        """Parse function call like Text(...)."""
        function_name = ""
        arguments = []
        
        if hasattr(ctx, 'IDENTIFIER') and ctx.IDENTIFIER():
            function_name = ctx.IDENTIFIER().getText()
        
        if hasattr(ctx, 'arguments') and ctx.arguments():
            # Parse arguments
            args_ctx = ctx.arguments()
            if hasattr(args_ctx, 'expression'):
                if isinstance(args_ctx.expression(), list):
                    for expr_ctx in args_ctx.expression():
                        arguments.append(ExpressionParser.parse_expression(expr_ctx))
                else:
                    arguments.append(ExpressionParser.parse_expression(args_ctx.expression()))
        
        return FunctionCallExpression(function_name=function_name, arguments=arguments)
    
    @staticmethod
    def _parse_instance(ctx) -> InstanceExpression:
        """Parse instance creation like {color: red; opacity: 0.5}."""
        class_name = None
        properties = []
        
        # Check if it has a class name (like Text {...} vs just {...})
        if hasattr(ctx, 'IDENTIFIER') and ctx.IDENTIFIER():
            class_name = ctx.IDENTIFIER().getText()
        
        # Parse property assignments
        if hasattr(ctx, 'propertyAssignmentInferredList') and ctx.propertyAssignmentInferredList():
            prop_list = ctx.propertyAssignmentInferredList()
            properties = ExpressionParser._parse_property_assignments(prop_list)
        
        return InstanceExpression(class_name=class_name, properties=properties)
    
    @staticmethod
    def _parse_array(ctx) -> ArrayExpression:
        """Parse array literal like [a, b, c]."""
        elements = []
        
        if hasattr(ctx, 'arrayElements') and ctx.arrayElements():
            elements_ctx = ctx.arrayElements()
            if hasattr(elements_ctx, 'expression'):
                if isinstance(elements_ctx.expression(), list):
                    for expr_ctx in elements_ctx.expression():
                        elements.append(ExpressionParser.parse_expression(expr_ctx))
                else:
                    elements.append(ExpressionParser.parse_expression(elements_ctx.expression()))
        
        return ArrayExpression(elements=elements)
    
    @staticmethod
    def _parse_binary_operation(ctx) -> BinaryOperationExpression:
        """Parse binary operation like 'a + b' or 'x = y'."""
        # Get expressions
        expressions = []
        if hasattr(ctx, 'expression') and ctx.expression():
            if isinstance(ctx.expression(), list):
                expressions = [ExpressionParser.parse_expression(e) for e in ctx.expression()]
            else:
                expressions = [ExpressionParser.parse_expression(ctx.expression())]
        
        if len(expressions) < 2:
            # Not enough expressions for binary operation
            return expressions[0] if expressions else ConstantExpression(value="<error>")
        
        # Determine operator
        operator = BinaryOperator.EQUAL  # Default
        
        if hasattr(ctx, 'relationalOperator') and ctx.relationalOperator():
            op_text = ctx.relationalOperator().getText()
            operator = ExpressionParser._map_relational_operator(op_text)
        elif hasattr(ctx, 'binaryLogicalOperator') and ctx.binaryLogicalOperator():
            op_text = ctx.binaryLogicalOperator().getText()
            operator = BinaryOperator.AND if op_text.lower() == 'and' else BinaryOperator.OR
        elif hasattr(ctx, 'arithmeticOperatorAdd') and ctx.arithmeticOperatorAdd():
            op_text = ctx.arithmeticOperatorAdd().getText()
            operator = BinaryOperator.ADD if op_text == '+' else BinaryOperator.SUBTRACT
        # Add more operator mappings as needed
        
        return BinaryOperationExpression(
            left=expressions[0],
            operator=operator,
            right=expressions[1]
        )
    
    @staticmethod
    def _parse_unary_operation(ctx) -> UnaryOperationExpression:
        """Parse unary operation like 'not x'."""
        operand = None
        operator = UnaryOperator.NOT  # Default
        
        if hasattr(ctx, 'expression') and ctx.expression():
            operand = ExpressionParser.parse_expression(ctx.expression())
        
        if hasattr(ctx, 'unaryLogicalOperator') and ctx.unaryLogicalOperator():
            op_text = ctx.unaryLogicalOperator().getText().lower()
            operator = UnaryOperator.NOT
        
        return UnaryOperationExpression(operator=operator, operand=operand)
    
    @staticmethod
    def _parse_conditional(ctx) -> ConditionalExpression:
        """Parse ternary conditional like 'condition ? true_value : false_value'."""
        expressions = []
        if hasattr(ctx, 'expression') and ctx.expression():
            if isinstance(ctx.expression(), list):
                expressions = [ExpressionParser.parse_expression(e) for e in ctx.expression()]
        
        if len(expressions) >= 3:
            return ConditionalExpression(
                condition=expressions[0],
                true_value=expressions[1],
                false_value=expressions[2]
            )
        
        return ConstantExpression(value="<conditional_error>")
    
    @staticmethod
    def _parse_property_assignments(ctx) -> List[PropertyAssignment]:
        """Parse property assignments within an instance."""
        assignments = []
        # This is a simplified version - would need more complex parsing
        # for the real implementation
        return assignments
    
    @staticmethod
    def _map_relational_operator(op_text: str) -> BinaryOperator:
        """Map operator text to BinaryOperator enum."""
        mapping = {
            '=': BinaryOperator.EQUAL,
            '!=': BinaryOperator.NOT_EQUAL,
            '<': BinaryOperator.LESS_THAN,
            '<=': BinaryOperator.LESS_EQUAL,
            '>': BinaryOperator.GREATER_THAN,
            '>=': BinaryOperator.GREATER_EQUAL,
            'in': BinaryOperator.IN,
            'not in': BinaryOperator.NOT_IN,
            'is': BinaryOperator.IS,
            'is not': BinaryOperator.IS_NOT,
            'like': BinaryOperator.LIKE,
            'not like': BinaryOperator.NOT_LIKE,
        }
        return mapping.get(op_text.lower(), BinaryOperator.EQUAL)
    
    @staticmethod
    def _parse_single_expression(text: str) -> Expression:
        """Parse a single expression without logical operators."""
        text = text.strip()

        # Handle parentheses - remove outer parentheses if they wrap the entire expression
        if text.startswith('(') and text.endswith(')'):
            # Check if these parentheses actually wrap the whole expression
            paren_depth = 0
            for i, char in enumerate(text):
                if char == '(': 
                    paren_depth += 1
                elif char == ')':
                    paren_depth -= 1
                    if paren_depth == 0 and i < len(text) - 1:
                        # Parentheses don't wrap the whole expression
                        break
            else:
                # Parentheses wrap the whole expression, remove them
                text = text[1:-1].strip()

        # --- CQL2 postfix operators ---
        cql2 = ExpressionParser._try_parse_cql2_operator(text)
        if cql2 is not None:
            return cql2

        # Check for relational operations  
        for op in ['>=', '<=', '!=', '=', '>', '<']:
            if f' {op} ' in text:
                result = ExpressionParser._parse_relational_expression(text, op)
                return result

        # Handle string literals
        if (text.startswith('"') and text.endswith('"')) or \
           (text.startswith("'") and text.endswith("'")):
            result = StringExpression(value=text[1:-1])
            return result

        # Handle function calls — CQL2 functions first
        if '(' in text and text.endswith(')'):
            cql2_func = ExpressionParser._try_parse_cql2_function(text)
            if cql2_func is not None:
                return cql2_func
            result = ExpressionParser._parse_function_call_from_text(text)
            return result

        # Handle numbers
        try:
            if '.' in text:
                result = ConstantExpression(value=float(text))
            else:
                result = ConstantExpression(value=int(text))
            return result
        except ValueError:
            pass

        # Handle boolean
        if text.lower() in ['true', 'false']:
            result = ConstantExpression(value=text.lower() == 'true')
            return result

        # Handle member access
        if '.' in text:
            result = ExpressionParser._parse_member_access_from_text(text)
            return result

        # Default: identifier
        result = IdentifierExpression(name=text)
        return result

    # =================================================================
    # CQL2 operator parsing helpers
    # =================================================================

    @staticmethod
    def _only_between_and(text: str) -> bool:
        """Return True if the only ' and ' in *text* is part of a BETWEEN."""
        tl = text.lower()
        m = re.search(r'\bbetween\b', tl)
        if not m:
            return False
        # Find the ' and ' after 'between'
        and_pos = tl.find(' and ', m.end())
        if and_pos == -1:
            return False
        # Check there's no other ' and ' or ' or ' outside the between
        rest = tl[and_pos + 5:]
        return ' and ' not in rest and ' or ' not in rest

    @staticmethod
    def _try_parse_cql2_operator(text: str) -> Optional[Expression]:
        """Try to parse CQL2 postfix operators: BETWEEN, IN, LIKE, IS NULL.

        Returns the parsed Expression or None if no CQL2 operator was found.
        """
        tl = text.lower().strip()

        # --- IS NULL / IS NOT NULL (must precede other checks) ---
        m = re.match(r'^(.+?)\s+is\s+not\s+null\s*$', tl)
        if m:
            operand = ExpressionParser._parse_single_expression(text[:m.end(1)])
            return NotExpression(args=[IsNullPredicate(args=[operand])])
        m = re.match(r'^(.+?)\s+is\s+null\s*$', tl)
        if m:
            operand = ExpressionParser._parse_single_expression(text[:m.end(1)])
            return IsNullPredicate(args=[operand])

        # --- NOT BETWEEN x AND y ---
        m = re.match(r'^(.+?)\s+not\s+between\s+(.+?)\s+and\s+(.+)$', tl)
        if m:
            val = ExpressionParser._parse_single_expression(
                text[:m.end(1)])
            lo = ExpressionParser._parse_single_expression(
                text[m.start(2):m.end(2)])
            hi = ExpressionParser._parse_single_expression(
                text[m.start(3):])
            return NotExpression(
                args=[IsBetweenPredicate(args=[val, lo, hi])],
            )

        # --- BETWEEN x AND y ---
        m = re.match(r'^(.+?)\s+between\s+(.+?)\s+and\s+(.+)$', tl)
        if m:
            val = ExpressionParser._parse_single_expression(
                text[:m.end(1)])
            lo = ExpressionParser._parse_single_expression(
                text[m.start(2):m.end(2)])
            hi = ExpressionParser._parse_single_expression(
                text[m.start(3):])
            return IsBetweenPredicate(args=[val, lo, hi])

        # --- NOT IN (...) ---
        m = re.match(r'^(.+?)\s+not\s+in\s*\((.*)\)\s*$', tl)
        if m:
            val = ExpressionParser._parse_single_expression(
                text[:m.end(1)])
            items = ExpressionParser._split_args(
                text[m.start(2):m.end(2)])
            list_exprs = [ExpressionParser._parse_single_expression(i) for i in items]
            return NotExpression(
                args=[IsInListPredicate(args=[val, list_exprs])],
            )

        # --- IN (...) ---
        m = re.match(r'^(.+?)\s+in\s*\((.*)\)\s*$', tl)
        if m:
            val = ExpressionParser._parse_single_expression(
                text[:m.end(1)])
            items = ExpressionParser._split_args(
                text[m.start(2):m.end(2)])
            list_exprs = [ExpressionParser._parse_single_expression(i) for i in items]
            return IsInListPredicate(args=[val, list_exprs])

        # --- NOT LIKE 'pattern' ---
        m = re.match(r'^(.+?)\s+not\s+like\s+(.+)$', tl)
        if m:
            val = ExpressionParser._parse_single_expression(
                text[:m.end(1)])
            pat = ExpressionParser._parse_single_expression(
                text[m.start(2):])
            return NotExpression(
                args=[IsLikePredicate(op='like', args=[val, pat])],
            )

        # --- LIKE 'pattern' ---
        m = re.match(r'^(.+?)\s+like\s+(.+)$', tl)
        if m:
            val = ExpressionParser._parse_single_expression(
                text[:m.end(1)])
            pat = ExpressionParser._parse_single_expression(
                text[m.start(2):])
            return IsLikePredicate(op='like', args=[val, pat])

        # --- ILIKE 'pattern' ---
        m = re.match(r'^(.+?)\s+ilike\s+(.+)$', tl)
        if m:
            val = ExpressionParser._parse_single_expression(
                text[:m.end(1)])
            pat = ExpressionParser._parse_single_expression(
                text[m.start(2):])
            return IsLikePredicate(op='ilike', args=[val, pat])

        return None

    @staticmethod
    def _try_parse_cql2_function(text: str) -> Optional[Expression]:
        """Try to parse CQL2 function-style expressions.

        Handles: spatial predicates, temporal predicates, array predicates,
        WKT geometry literals, BBOX, DATE, TIMESTAMP, INTERVAL.

        Returns the parsed Expression or None if not a CQL2 function.
        """
        paren_pos = text.index('(')
        func_name = text[:paren_pos].strip()
        func_lower = func_name.lower()

        # Extract the arguments substring (inside outermost parens)
        args_str = text[paren_pos + 1:text.rfind(')')]

        # ── Spatial predicates: S_INTERSECTS(a, b) ──
        if func_lower in _SPATIAL_PREDICATES:
            args = ExpressionParser._split_args(args_str)
            parsed_args = [ExpressionParser._parse_single_expression(a) for a in args]
            return SpatialPredicate(op=func_lower, args=parsed_args)

        # ── S_RELATE(a, b, pattern) ──
        if func_lower == _SPATIAL_RELATE:
            args = ExpressionParser._split_args(args_str)
            if len(args) >= 3:
                parsed_a = ExpressionParser._parse_single_expression(args[0])
                parsed_b = ExpressionParser._parse_single_expression(args[1])
                pattern = args[2].strip().strip("'").strip('"')
                return SpatialRelatePredicate(
                    args=[parsed_a, parsed_b], pattern=pattern,
                )

        # ── Temporal predicates: T_BEFORE(a, b) ──
        if func_lower in _TEMPORAL_PREDICATES:
            args = ExpressionParser._split_args(args_str)
            parsed_args = [ExpressionParser._parse_single_expression(a) for a in args]
            return TemporalPredicate(op=func_lower, args=parsed_args)

        # ── Array predicates: A_CONTAINS(a, b) ──
        if func_lower in _ARRAY_PREDICATES:
            args = ExpressionParser._split_args(args_str)
            parsed_args = [ExpressionParser._parse_single_expression(a) for a in args]
            return ArrayPredicate(op=func_lower, args=parsed_args)

        # ── DATE('...') ──
        if func_lower == 'date':
            value = args_str.strip().strip("'").strip('"')
            return TemporalLiteral(temporal_type='date', value=value)

        # ── TIMESTAMP('...') ──
        if func_lower == 'timestamp':
            value = args_str.strip().strip("'").strip('"')
            return TemporalLiteral(temporal_type='timestamp', value=value)

        # ── INTERVAL('start', 'end') ──
        if func_lower == 'interval':
            parts = ExpressionParser._split_args(args_str)
            interval = [p.strip().strip("'").strip('"') for p in parts]
            return TemporalLiteral(temporal_type='interval', interval=interval)

        # ── BBOX(x1, y1, x2, y2[, x3, y3]) ──
        if func_lower == 'bbox':
            parts = ExpressionParser._split_args(args_str)
            bbox_vals = [float(p.strip()) for p in parts]
            return BboxLiteral(bbox=bbox_vals)

        # ── WKT geometry literals: POINT(x y), POLYGON((...)), etc. ──
        if func_lower in _WKT_TYPES:
            geom_type = _WKT_TO_GEOJSON[func_lower]
            coords = ExpressionParser._parse_wkt_coordinates(func_lower, args_str)
            if geom_type == 'GeometryCollection':
                # GeometryCollection contains sub-geometries
                return GeometryLiteral(geom_type=geom_type, geometries=coords)
            return GeometryLiteral(geom_type=geom_type, coordinates=coords)

        return None

    # =================================================================
    # WKT coordinate parsing
    # =================================================================

    @staticmethod
    def _parse_wkt_coordinates(geom_lower: str, args_str: str):
        """Parse WKT coordinate content into GeoJSON-style coordinate arrays."""
        args_str = args_str.strip()

        if geom_lower == 'point':
            # POINT(x y) or POINT(x y z)
            nums = args_str.split()
            return [float(n) for n in nums]

        if geom_lower == 'linestring':
            # LINESTRING(x1 y1, x2 y2, ...)
            return ExpressionParser._parse_coord_list(args_str)

        if geom_lower == 'polygon':
            # POLYGON((x1 y1, x2 y2, ...), (hole x1 y1, ...))
            return ExpressionParser._parse_ring_list(args_str)

        if geom_lower == 'multipoint':
            # MULTIPOINT((x1 y1), (x2 y2)) or MULTIPOINT(x1 y1, x2 y2)
            if '(' in args_str:
                rings = ExpressionParser._extract_parens_groups(args_str)
                return [ExpressionParser._parse_coord_list(r)[0] for r in rings]
            return ExpressionParser._parse_coord_list(args_str)

        if geom_lower == 'multilinestring':
            # MULTILINESTRING((x1 y1, x2 y2), (x3 y3, x4 y4))
            rings = ExpressionParser._extract_parens_groups(args_str)
            return [ExpressionParser._parse_coord_list(r) for r in rings]

        if geom_lower == 'multipolygon':
            # MULTIPOLYGON(((x1 y1, ...)), ((x1 y1, ...)))
            # Each element is a polygon (list of rings)
            outer = ExpressionParser._extract_parens_groups(args_str)
            return [ExpressionParser._parse_ring_list(o) for o in outer]

        if geom_lower == 'geometrycollection':
            # GEOMETRYCOLLECTION(POINT(...), LINESTRING(...))
            # Return list of GeometryLiteral sub-geometries
            sub_geoms = []
            # Use a simple state machine to split top-level sub-geometries
            depth = 0
            current = []
            for ch in args_str:
                if ch == '(':
                    depth += 1
                    current.append(ch)
                elif ch == ')':
                    depth -= 1
                    current.append(ch)
                elif ch == ',' and depth == 0:
                    sub_text = ''.join(current).strip()
                    if sub_text:
                        parsed = ExpressionParser._try_parse_cql2_function(sub_text + ')'[0:0] if False else sub_text)
                        # Re-parse as full expression — it's a WKT sub-geometry
                        parsed = ExpressionParser._try_parse_cql2_function(sub_text)
                        if parsed and isinstance(parsed, GeometryLiteral):
                            sub_geoms.append(parsed)
                    current = []
                else:
                    current.append(ch)
            last = ''.join(current).strip()
            if last:
                parsed = ExpressionParser._try_parse_cql2_function(last)
                if parsed and isinstance(parsed, GeometryLiteral):
                    sub_geoms.append(parsed)
            return sub_geoms

        return []

    @staticmethod
    def _parse_coord_list(text: str) -> list:
        """Parse 'x1 y1, x2 y2, ...' into [[x1,y1], [x2,y2], ...]."""
        coords = []
        for pair in text.split(','):
            nums = pair.strip().split()
            if nums:
                coords.append([float(n) for n in nums])
        return coords

    @staticmethod
    def _parse_ring_list(text: str) -> list:
        """Parse '(x1 y1, x2 y2), (x3 y3, ...)' into rings."""
        groups = ExpressionParser._extract_parens_groups(text)
        return [ExpressionParser._parse_coord_list(g) for g in groups]

    @staticmethod
    def _extract_parens_groups(text: str) -> list:
        """Extract content of each top-level (...) group."""
        groups = []
        depth = 0
        current = []
        for ch in text:
            if ch == '(':
                if depth > 0:
                    current.append(ch)
                depth += 1
            elif ch == ')':
                depth -= 1
                if depth == 0:
                    groups.append(''.join(current))
                    current = []
                elif depth > 0:
                    current.append(ch)
            elif depth > 0:
                current.append(ch)
        return groups

    @staticmethod
    def _split_args(text: str) -> list:
        """Split comma-separated arguments respecting parentheses and quotes."""
        args = []
        depth = 0
        in_single = False
        in_double = False
        current = []
        for ch in text:
            if ch == "'" and not in_double:
                in_single = not in_single
                current.append(ch)
            elif ch == '"' and not in_single:
                in_double = not in_double
                current.append(ch)
            elif not in_single and not in_double:
                if ch == '(':
                    depth += 1
                    current.append(ch)
                elif ch == ')':
                    depth -= 1
                    current.append(ch)
                elif ch == ',' and depth == 0:
                    args.append(''.join(current).strip())
                    current = []
                else:
                    current.append(ch)
            else:
                current.append(ch)
        last = ''.join(current).strip()
        if last:
            args.append(last)
        return args
