from __future__ import annotations

import inspect

from antlr4 import *
from CartoSymCSSLexer import CartoSymCSSLexer
from CartoSymCSSGrammar import CartoSymCSSGrammar
from CartoSymCSSGrammarListener import CartoSymCSSGrammarListener
import sys

from dataclasses import dataclass, field
from typing import List, Optional
from abc import ABC, abstractmethod
from enum import Enum

#---------------------------------------------
# High level classes
#---------------------------------------------  
# Metadata
@dataclass
class Metadata:
    name: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    authors: List[str] = field(default_factory=list)
    keywords: List[str] = field(default_factory=list)
    geoDataClasses: List[str] = field(default_factory=list)

# Expression class
@dataclass
class Expression(ABC):
    identifier: str = None

# Selector class
@dataclass
class Selector:
    _identifier: Optional[str] = None
    _expression: Optional[Expression] = None
    _selectors: List['Selector'] = field(default_factory=list, init=False)

    @property
    def identifier(self):
        return self._identifier

    @identifier.setter
    def identifier(self, value):
        self._identifier = value

    @property
    def expression(self):
        return self._expression

    @expression.setter
    def expression(self, value):
        self._expression = value

    @property
    def selectors(self):
        return self._selectors
    


# Symbolizer class
@dataclass
class Symbolizer:
    visibility = Optional[bool]
    opacity = Optional[float]
    zOrder = Optional[int]

# StylingRule class
@dataclass
class StylingRule:
    name: Optional[str] = None
    selector: Optional[Expression] = None
    symbolizer: Optional[Symbolizer] = None
    nestedRules: StylingRuleList = None

# StylingRuleList
@dataclass
class StylingRuleList:
    stylingRules: Optional[List[StylingRule]] = None

# StyleSheet
@dataclass
class StyleSheet:
    metadata = Metadata()
    stylingRuleList = StylingRuleList()

# IdentifierExpressionExpression
@dataclass
class IdentifierExpression(Expression):
    name = str()

# IdOrConstant
@dataclass
class IdOrConstant:
    identifier : str = None


# ExpConstant class (not in the conceptual model)
@dataclass
class ExpConstant:
    numeric_literal = str = None
    hex_literal = str = None
    unit = Optional[str]

# ExpString class (not in the conceptual model)
@dataclass
class ExpString:
    character_literal = str = None

# ExpCall class (not in the conceptual model)
@dataclass
class ExpCall:
    identifier = str
    arguments = List[Expression]

# ExpArray class (not in the conceptual model)
@dataclass
class ExpArray:
    arrayElements = Optional[List[Expression]]

# PropertyAssignmentInferred class (not in the conceptual model)
@dataclass
class PropertyAssignmentInferred:
    propertyAssignment = str
    expression = Expression

# PropertyAssignment class (not in the conceptual model)
@dataclass
class PropertyAssignment:
    expression = Expression

# PropertyAssignmentList class (not in the conceptual model)
@dataclass
class PropertyAssignmentList:
    propertyAssignment = List[PropertyAssignment]

# ExpInstance class (not in the conceptual model)
@dataclass
class ExpInstance:
    identifier = str
    propertyAssignmentInferredList = List[PropertyAssignmentInferred]

# TimeOfDay class
@dataclass
class TimeOfDay:
    hour = int
    minutes = int
    seconds = int

# Month class
class Month(Enum):
    january = 1
    february = 2
    march = 3
    april = 4
    may = 5
    june = 6
    july = 7
    august = 8
    september = 9
    october = 10
    november = 11
    december = 12

# Date class
@dataclass
class Date:
    year = int
    month = Month
    day = int

# TimeInstant class
@dataclass
class TimeInstant:
    date = Date()
    timeOfDay = TimeOfDay()

# TimeInterval class
@dataclass
class TimeInterval:
    start = TimeInstant()
    end = TimeInstant()

# DataLayerType class
class DataLayerType(Enum):
    map = 1
    vector = 2
    coverage = 3

# DataLayer class
@dataclass
class DataLayer:
    identifier = str
    type = DataLayerType

# Visualization class
@dataclass
class Visualization:
    scale_denominator = float
    date_time = TimeInstant()
    date = Date()
    time_of_day = TimeOfDay()
    time_interval = TimeInterval()
    pass_ = int

# SystemIdentifierExpression class
@dataclass
class SystemIdentifierExpression(IdentifierExpression, Visualization, DataLayer):
    visualization = Visualization()
    data_layer = DataLayer()

#---------------------------------------------
# Expressions
#---------------------------------------------
# IdOrConstant
# ExpConstant
# ExpString
# ExpCall
# Arguments
# ExpArray
# ArrayElements
# ExpInstance
#---------------------------------------------
# Operators
#---------------------------------------------
# ArithmeticOperatorExp
# ArithmeticOperatorMul
# ArithmeticOperatorAdd
# ArithmeticOperatorExp class
# BinaryLogicalOperator
class BinaryLogicalOperator:
    pass
# RelationalOperator
@dataclass
class RelationalOperator:
    ctx: object
    @property
    def operator(self):
        if self.ctx.EQ() is not None:
            return self.ctx.EQ().getText()
        if self.ctx.LT() is not None:
            return self.ctx.LT().getText()
        if self.ctx.LTEQ() is not None:
            return self.ctx.LTEQ().getText()
        if self.ctx.GT() is not None:
            return self.ctx.GT().getText()
        if self.ctx.GTEQ() is not None:
            return self.ctx.GTEQ().getText()
        if self.ctx.IN() is not None:
            return self.ctx.IN().getText()
        if self.ctx.NOT() is not None and self.ctx.IN() is not None:
            return self.ctx.NOT().getText(), self.ctx.IN().getText()
        if self.ctx.IS() is not None:
            return self.ctx.IS().getText()
        if self.ctx.IS() is not None and self.ctx.NOT() is not None:
            return self.ctx.IS().getText(), self.ctx.NOT().getText()
        if self.ctx.LIKE() is not None:
            return self.ctx.LIKE().getText()
        if self.ctx.NOT() is not None and self.ctx.LIKE() is not None:
            return self.ctx.NOT().getText(), self.ctx.LIKE().getText()
        return None
    
# BetweenOperator
@dataclass
class BetweenOperator:
    ctx: object
    @property
    def operator(self):
        if self.ctx.BETWEEN() is not None:
            return self.ctx.BETWEEN().getText()
        if self.ctx.NOT() is not None and self.ctx.BETWEEN() is not None:
            return self.ctx.NOT().getText(), self.ctx.BETWEEN().getText()
        return None
#---------------------------------------------
# PropertyAssignment
#---------------------------------------------
# PropertyAssignmentInferredList
@dataclass
class PropertyAssignmentInferredList:
    pass

# PropertyAssignmentInferred
# PropertyAssignment
# PropertyAssignmentList

#---------------------------------------------
# CartoSymParser
#---------------------------------------------
class CartoSymParser(CartoSymCSSGrammarListener):
    def __init__(self):
        self.styleSheet = StyleSheet()
        self.metadata = Metadata()
        self.stylingRuleList = StylingRuleList()
        self.stylingRule = StylingRule([], None, None)
        self.selectors = []
        self.result = None
        self.expression = {}

    # StyleSheet
    def enterStyleSheet(self, ctx):
        for metadata in ctx.metadata():
            self.enterMetadata(metadata)
        self.enterStylingRuleList(ctx.stylingRuleList())
        self.result = self.styleSheet

    # Metadata
    def enterMetadata(self, ctx):
        identifier = ctx.IDENTIFIER().getText()
        character_literal = ctx.CHARACTER_LITERAL().getText()
        if hasattr(self.metadata, identifier):
            setattr(self.metadata, identifier, character_literal)
        self.result = self.metadata
        self.result = self.exitMetadata(ctx)

    # StylingRuleList
    def enterStylingRuleList(self, ctx):
        if ctx.stylingRuleList() is not None:
            self.enterStylingRuleList(ctx.stylingRuleList())
        self.enterStylingRule(ctx.stylingRule())
        self.result = self.exitStylingRuleList(ctx)

    # StylingRule
    def enterStylingRule(self, ctx):
        for selector in ctx.selector():
            self.enterSelector(selector)
        if ctx.propertyAssignmentList() is not None:
            self.enterPropertyAssignmentList(ctx.propertyAssignmentList())
        if ctx.stylingRuleList() is not None:
            self.enterStylingRuleList(ctx.stylingRuleList())
        self.result = self.exitStylingRule(ctx)

    # Selector
    def enterSelector(self, ctx):
        identifier = ctx.IDENTIFIER().getText() if ctx.IDENTIFIER() else None
        expression = self.enterExpression(ctx.expression()) if ctx.expression() else None
        selector = Selector(identifier, expression)
        self.selectors.append(selector)
        self.exitSelector(ctx)
        print(self.selectors)

    # Expression
    def enterExpression(self, ctx):
        identifier = None
        for expression in ctx.expression():
            self.enterExpression(expression)
        if ctx.idOrConstant() is not None:
            self.enterIdOrConstant(ctx.idOrConstant())
        if ctx.IDENTIFIER() is not None:
            identifier = ctx.IDENTIFIER().getText()
        if ctx.expString() is not None:
            self.enterExpString(ctx.expString())
        if ctx.expCall() is not None:
            self.enterExpCall(ctx.expCall())
        if ctx.expArray() is not None:
            self.enterExpArray(ctx.expArray())
        if ctx.expInstance() is not None:
            self.enterExpInstance(ctx.expInstance())
        if ctx.expConstant() is not None:
            self.enterExpConstant(ctx.expConstant())
        if ctx.arithmeticOperatorExp() is not None:
            self.enterArithmeticOperatorExp(ctx.arithmeticOperatorExp())
        if ctx.arithmeticOperatorMul() is not None:
            self.enterArithmeticOperatorMul(ctx.arithmeticOperatorMul())
        if ctx.arithmeticOperatorAdd() is not None:
            self.enterArithmeticOperatorAdd(ctx.arithmeticOperatorAdd())
        if ctx.binaryLogicalOperator() is not None:
            self.enterBinaryLogicalOperator(ctx.binaryLogicalOperator())
        if ctx.relationalOperator() is not None:
            self.enterRelationalOperator(ctx.relationalOperator())
        if ctx.betweenOperator() is not None:
            self.enterBetweenOperator(ctx.betweenOperator())
        if ctx.unaryLogicalOperator() is not None:
            self.enterUnaryLogicalOperator(ctx.unaryLogicalOperator())
        if ctx.unaryArithmeticOperator() is not None:
            self.enterUnaryArithmeticOperator(ctx.unaryArithmeticOperator())
        if ctx.tuple_() is not None:
            self.enterTuple(ctx.tuple_())
        if identifier and hasattr(self.expression, identifier):
            setattr(self.expression, identifier, None)
        self.result = self.exitExpression(ctx)
        
    # Specific Expression methods
    
    # IdOrConstant
    def enterIdOrConstant(self, ctx):
        identifier = None
        if ctx.IDENTIFIER() is not None:
            identifier = ctx.IDENTIFIER().getText()
        if ctx.expConstant() is not None:
            self.enterExpConstant(ctx.expConstant())
        if identifier and hasattr(self.expression, identifier):
            setattr(self.expression, identifier, None)
        self.result = self.exitIdOrConstant(ctx)
    
    # ExpConstant
    def enterExpConstant(self, ctx):
        hex_literal = None
        unit = None
        numeric_literal = None
        if ctx.NUMERIC_LITERAL() is not None:
            numeric_literal = ctx.NUMERIC_LITERAL().getText()
        if ctx.HEX_LITERAL() is not None:
            hex_literal = ctx.HEX_LITERAL().getText()
        if ctx.UNIT() is not None:
            unit = ctx.UNIT().getText()
        if numeric_literal and hasattr(self.expression, numeric_literal):
            setattr(self.expression, numeric_literal, None)
        if hex_literal and hasattr(self.expression, hex_literal):
            setattr(self.expression, hex_literal, None)
        if unit and hasattr(self.expression, unit):
            setattr(self.expression, unit, None)
        self.result = self.exitExpConstant(ctx)
 
    # ExpString
    def enterExpString(self, ctx):
        if ctx.CHARACTER_LITERAL() is not None:
            character_literal = ctx.CHARACTER_LITERAL().getText()
        if character_literal and hasattr(self.expression, character_literal):
            setattr(self.expression, character_literal, None)
        self.result = self.exitExpString(ctx)
 
    # ExpCall
    def enterExpCall(self, ctx):
        if ctx.IDENTIFIER() is not None:
            identifier = ctx.IDENTIFIER().getText()
        if ctx.arguments() is not None:
            self.enterArguments(ctx.arguments())
        if identifier and hasattr(self.expression, identifier):
            setattr(self.expression, identifier, None)
        self.result = self.exitExpCall(ctx)

    # Arguments
    def enterArguments(self, ctx):
        for expression in ctx.expression():
            self.enterExpression(expression)
        self.result = self.exitArguments(ctx)

    # ExpArray
    def enterExpArray(self, ctx):
        if ctx.arrayElements() is not None:
            self.enterArrayElements(ctx.arrayElements())
        self.result = self.exitExpArray(ctx)

    # ArrayElements
    def enterArrayElements(self, ctx):
        expression = ctx.expression()
        if isinstance(expression, list):
            for expression in ctx.expression():
                self.enterExpression(expression)
        else:
            self.enterExpression(expression)
        self.result = self.exitArrayElements(ctx)

    # ExpInstance
    def enterExpInstance(self, ctx):
        identifier = None
        if ctx.IDENTIFIER() is not None:
            identifier = ctx.IDENTIFIER().getText()
        if ctx.propertyAssignmentInferredList() is not None:
            self.enterPropertyAssignmentInferredList(ctx.propertyAssignmentInferredList())
        if identifier and hasattr(self.expression, identifier):
            setattr(self.expression, identifier, None)
        self.result = self.exitExpInstance(ctx)
        
    # Operators
    # ArithmeticOperatorExp
    def enterArithmeticOperatorExp(self, ctx):
        if ctx.POW() is not None:
            self.result = ctx.POW().getText()
        self.result = self.exitArithmeticOperatorExp(ctx)
    def enterArithmeticOperatorMul(self, ctx):
        if ctx.MUL is not None:
            self.result = ctx.MUL().getText()
        if ctx.DIV is not None:
            self.result = ctx.DIV().getText()
        if ctx.IDIV is not None:
            self.result = ctx.IDIV().getText()
        if ctx.MOD is not None:
            self.result = ctx.MOD().getText()
        self.result = self.exitArithmeticOperatorMul(ctx)
    def enterArithmeticOperatorAdd(self, ctx):
        if ctx.MINUS() is not None:
            self.result = ctx.MINUS().getText()
        if ctx.PLUS() is not None:
            self.result = ctx.PLUS().getText()
        self.result = self.exitArithmeticOperatorAdd(ctx)
    def enterBinaryLogicalOperator(self, ctx):
        if ctx.AND() is not None:
            self.result = ctx.AND().getText()
        if ctx.OR() is not None:
            self.result = ctx.OR().getText()
        self.result = self.exitBinaryLogicalOperator(ctx)
    
    # RelationalOperator
    def enterRelationalOperator(self, ctx):
        relationalOperator = RelationalOperator(ctx)
        self.result = relationalOperator.operator
        self.result = self.exitRelationalOperator(ctx)
    
    # BetweenOperator
    def enterBetweenOperator(self, ctx):
        self.betweenOperator.enterBetweenOperator(ctx)
        self.result = self.betweenOperator.result
        self.betweenOperator.exitBetweenOperator(ctx)
        
    # PropertyAssignment methods
    def enterPropertyAssignmentInferredList(self, ctx):
        if ctx.propertyAssignmentInferred() is not None:
            self.enterPropertyAssignmentInferred(ctx.propertyAssignmentInferred())
        if ctx.propertyAssignmentInferredList() is not None:
            self.enterPropertyAssignmentInferredList(ctx.propertyAssignmentInferredList())
        self.result = self.exitPropertyAssignmentInferredList(ctx)

    def enterPropertyAssignmentInferred(self, ctx):
        if ctx.propertyAssignment() is not None:
            self.enterPropertyAssignment(ctx.propertyAssignment())
        if ctx.expression() is not None:
            self.enterExpression(ctx.expression())
        self.result = self.exitPropertyAssignmentInferred(ctx)

    def enterPropertyAssignment(self, ctx):
        if ctx.expression() is not None:
            self.enterExpression(ctx.expression())
        self.result = self.exitPropertyAssignment(ctx)    

    def enterPropertyAssignmentList(self, ctx):
        if ctx.propertyAssignment() is not None:
            self.enterPropertyAssignment(ctx.propertyAssignment())
        self.result = self.exitPropertyAssignmentList(ctx)

# Parse the input file
def parse_input(input_file):
    input_stream = FileStream(input_file, encoding='utf-8')
    lexer = CartoSymCSSLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = CartoSymCSSGrammar(stream)
    tree = parser.styleSheet()

    walker = ParseTreeWalker()
    cartoSymParser = CartoSymParser()
    walker.walk(cartoSymParser, tree)

    result = cartoSymParser.result
    return result

if __name__ == "__main__":
    input_file = sys.argv[1]
    result = parse_input(input_file)
    # print(result)
