"""
Enhanced AST to Pydantic converter with Phase A expression support.
"""

from typing import List, Optional, Dict, Union, Any
from .models.expressions import *
from .models.base import BaseCartoSymModel
from .models.styles import Style, Metadata, StylingRule
from .models.symbolizers import Symbolizer, Fill, Stroke, Marker
from .ast import (
    StyleSheet, StylingRuleList, StylingRule, Symbolizer,
    Fill, Stroke, Metadata as AstMetadata
)

# Import ANTLR generated classes - will be used when needed
# These are loaded dynamically by the main parser


class ExpressionParser:
    """Parser for converting ANTLR expression contexts to Pydantic expressions."""
    
    @staticmethod
    def parse_expression(ctx) -> Expression:
        """Convert ANTLR expression context to Pydantic Expression."""
        if not ctx:
            return None
        
        # Get the text representation for fallback parsing
        ctx_text = ctx.getText() if hasattr(ctx, 'getText') else str(ctx)
        
        # Handle different expression types based on context structure
        
        # Check for binary operations first (most common in conditions)
        # Use original text with proper spacing if available
        original_text = ctx_text
        if hasattr(ctx, 'start') and hasattr(ctx, 'stop') and hasattr(ctx.start, 'source'):
            try:
                # Try to get original text with spacing from token stream
                input_stream = ctx.start.source
                start_idx = ctx.start.start
                stop_idx = ctx.stop.stop
                original_text = input_stream.strdata[start_idx:stop_idx + 1]
            except:
                # Fallback to getText() if extraction fails
                pass
        
        # Check for logical operations with proper spacing
        if ' and ' in original_text or ' or ' in original_text:
            return ExpressionParser._parse_logical_expression(original_text)
        
        # Check for relational operations with proper spacing
        for op in ['>=', '<=', '!=', '=', '>', '<']:
            if f' {op} ' in original_text:
                return ExpressionParser._parse_relational_expression(original_text, op)
        
        # Handle member access (contains dots)
        if '.' in ctx_text and not ctx_text.startswith('"') and not ctx_text.startswith("'"):
            return ExpressionParser._parse_member_access_from_text(ctx_text)
        
        # Handle string literals
        if (ctx_text.startswith('"') and ctx_text.endswith('"')) or \
           (ctx_text.startswith("'") and ctx_text.endswith("'")):
            return StringExpression(value=ctx_text[1:-1])
        
        # Handle numbers
        if ctx_text.replace('.', '').replace('-', '').isdigit():
            try:
                value = int(ctx_text) if '.' not in ctx_text else float(ctx_text)
                return ConstantExpression(value=value)
            except ValueError:
                pass
        
        # Handle boolean constants
        if ctx_text.lower() in ['true', 'false']:
            return ConstantExpression(value=ctx_text.lower() == 'true')
        
        # Handle function calls (Text(...), DATE(...))
        if '(' in ctx_text and ')' in ctx_text:
            return ExpressionParser._parse_function_call_from_text(original_text)
        
        # Handle object literals {color: red; opacity: 0.5}
        if ctx_text.startswith('{') and ctx_text.endswith('}'):
            return ExpressionParser._parse_instance_from_text(original_text)
        
        # Default: treat as identifier
        return IdentifierExpression(name=ctx_text)
    
    @staticmethod
    def _parse_logical_expression(text: str) -> BinaryOperationExpression:
        """Parse logical expressions like 'a and b' or 'x or y'."""
        # Handle nested logical expressions with proper precedence
        # OR has lower precedence than AND, so we parse OR first
        
        # Find the main logical operator (rightmost OR for left-associativity)
        or_pos = -1
        paren_depth = 0
        for i in range(len(text) - 4, -1, -1):  # -4 for ' or '
            if text[i] == ')':
                paren_depth += 1
            elif text[i] == '(':
                paren_depth -= 1
            elif paren_depth == 0 and text[i:i+4] == ' or ':
                or_pos = i
                break
        
        if or_pos != -1:
            left_part = text[:or_pos].strip()
            right_part = text[or_pos+4:].strip()  # +4 for ' or '
            left_expr = ExpressionParser._parse_single_expression(left_part)
            right_expr = ExpressionParser._parse_single_expression(right_part)
            return BinaryOperationExpression(left=left_expr, operator=BinaryOperator.OR, right=right_expr)
        
        # If no OR, look for AND
        and_pos = -1
        paren_depth = 0
        for i in range(len(text) - 5, -1, -1):  # -5 for ' and '
            if text[i] == ')':
                paren_depth += 1
            elif text[i] == '(':
                paren_depth -= 1
            elif paren_depth == 0 and text[i:i+5] == ' and ':
                and_pos = i
                break
        
        if and_pos != -1:
            left_part = text[:and_pos].strip()
            right_part = text[and_pos+5:].strip()  # +5 for ' and '
            left_expr = ExpressionParser._parse_single_expression(left_part)
            right_expr = ExpressionParser._parse_single_expression(right_part)
            return BinaryOperationExpression(left=left_expr, operator=BinaryOperator.AND, right=right_expr)
        
        # No logical operators found, parse as single expression
        return ExpressionParser._parse_single_expression(text)
    
    @staticmethod  
    def _parse_relational_expression(text: str, operator_str: str) -> BinaryOperationExpression:
        """Parse relational expressions like 'a = b' or 'x < 5'."""
        # Find the operator position, respecting parentheses
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
        
        # Check for logical operations
        if ' and ' in text or ' or ' in text:
            return ExpressionParser._parse_logical_expression(text)
        
        # Check for relational operations  
        for op in ['>=', '<=', '!=', '=', '>', '<']:
            if f' {op} ' in text:
                return ExpressionParser._parse_relational_expression(text, op)
        
        # Handle string literals
        if (text.startswith('"') and text.endswith('"')) or \
           (text.startswith("'") and text.endswith("'")):
            return StringExpression(value=text[1:-1])
        
        # Handle function calls
        if '(' in text and text.endswith(')'):
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
        
        # Check for relational operations  
        for op in ['>=', '<=', '!=', '=', '>', '<']:
            if f' {op} ' in text:
                return ExpressionParser._parse_relational_expression(text, op)
        
        # Handle string literals
        if (text.startswith('"') and text.endswith('"')) or \
           (text.startswith("'") and text.endswith("'")):
            return StringExpression(value=text[1:-1])
        
        # Handle function calls
        if '(' in text and text.endswith(')'):
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
