"""
Expression model — re-exports from :mod:`cartosym_transcoder.models.expressions`.

This module exists so that consumers can import from the
``cartosym_transcoder.expressions`` package following the target directory
structure documented in the ROADMAP, while the canonical definitions remain
in ``models/expressions.py``.
"""

# Re-export everything from the canonical location
from ..models.expressions import *  # noqa: F401,F403
from ..models.expressions import (  # Explicitly re-export the main classes for IDE auto-complete
    ArrayExpression,
    BaseExpression,
    BinaryOperationExpression,
    BinaryOperator,
    ConditionalExpression,
    ConstantExpression,
    Expression,
    ExpressionType,
    FunctionCallExpression,
    IdentifierExpression,
    InstanceExpression,
    MemberAccessExpression,
    PropertyAssignment,
    Selector,
    StringExpression,
    StylingRuleExpression,
    UnaryOperationExpression,
    UnaryOperator,
)
