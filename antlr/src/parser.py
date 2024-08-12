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

# Expression
from parser_classes.expressions.Expression import Expression

# Selector class
from parser_classes.Selector import Selector    
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
# IdentifierExpression
@dataclass
class IdentifierExpression(Expression):
    name = str()
# IdOrConstant
from parser_classes.expressions.IdOrConstant import IdOrConstant
# ExpConstant
from parser_classes.expressions.ExpConstant import ExpConstant

# ExpString
from parser_classes.expressions.ExpString import ExpString

# ExpCall
from parser_classes.expressions.ExpCall import ExpCall

# ExpArray
from parser_classes.expressions.ExpArray import ExpArray

# PropertyAssignmentInferred
@dataclass
class PropertyAssignmentInferred:
    propertyAssignment = str
    expression = Expression

# PropertyAssignment
@dataclass
class PropertyAssignment:
    expression = Expression

# PropertyAssignmentList)
@dataclass
class PropertyAssignmentList:
    propertyAssignment = List[PropertyAssignment]

# ExpInstance
from parser_classes.expressions.ExpInstance import ExpInstance

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
# ExpCall
# Arguments
from parser_classes.expressions.Arguments import Arguments
# ArrayElements
from parser_classes.expressions.ArrayElements import ArrayElements
#---------------------------------------------
# Operators
#---------------------------------------------
from parser_classes.operators.ArithmeticOperatorExp import ArithmeticOperatorExp
from parser_classes.operators.ArithmeticOperatorMul import ArithmeticOperatorMul
from parser_classes.operators.ArithmeticOperatorAdd import ArithmeticOperatorAdd
from parser_classes.operators.BinaryLogicalOperator import BinaryLogicalOperator
from parser_classes.operators.RelationalOperator import RelationalOperator
from parser_classes.operators.BetweenOperator import BetweenOperator
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
        selector = Selector(ctx)
        self.result = selector.identifier or selector.expression
        self.exitSelector(ctx)
    #---------------------------------------------
    # Expressions
    #---------------------------------------------
    # Expression
    def enterExpression(self, ctx):
        expression = Expression(ctx)
        self.result = expression.expression or expression.identifier or expression.idOrConstant or expression.expString or expression.expCall or expression.expArray or expression.expInstance or expression.expConstant or expression.arithmeticOperatorExp or expression.arithmeticOperatorMul or expression.arithmeticOperatorAdd or expression.binaryLogicalOperator or expression.relationalOperator or expression.betweenOperator or expression.unaryLogicalOperator or expression.unaryArithmeticOperator or expression.tuple_
        self.result = self.exitExpression(ctx)            
    # IdOrConstant
    def enterIdOrConstant(self, ctx):
        idOrConstant = IdOrConstant(ctx)
        self.result = idOrConstant.identifier or idOrConstant.expConstant
        self.result = self.exitIdOrConstant(ctx)
    # ExpConstant
    def enterExpConstant(self, ctx):
        expConstant = ExpConstant(ctx)
        self.result = expConstant.numericLiteral or expConstant.hexLiteral or expConstant.unit
        self.result = self.exitExpConstant(ctx) 
    # ExpString
    def enterExpString(self, ctx):
        expString = ExpString(ctx)
        self.result = expString.characterLiteral
        self.result = self.exitExpString(ctx) 
    # ExpCall
    def enterExpCall(self, ctx):
        expCall = ExpCall(ctx)
        self.result = expCall.identifier or expCall.arguments
        self.result = self.exitExpCall(ctx)
    # Arguments
    def enterArguments(self, ctx):
        arguments = Arguments(ctx)
        self.result = arguments.arguments or arguments.expression
        self.result = self.exitArguments(ctx)
    # ExpArray
    def enterExpArray(self, ctx):
        expArray = ExpArray()
        self.result = expArray.arrayElements
        self.result = self.exitExpArray(ctx)
    # ArrayElements
    def enterArrayElements(self, ctx):
        arrayElements = ArrayElements(ctx)
        self.result = arrayElements.arrayElements or arrayElements.expression
        self.result = self.exitArrayElements(ctx)
    # ExpInstance
    def enterExpInstance(self, ctx):
        expInstance = ExpInstance(ctx)
        self.result = expInstance.identifier or expInstance.propertyAssignmentInferredList
        self.result = self.exitExpInstance(ctx)
    #---------------------------------------------
    # Operators
    #---------------------------------------------
    # ArithmeticOperatorExp
    def enterArithmeticOperatorExp(self, ctx):
        arithmeticOperatorExp = ArithmeticOperatorExp(ctx)
        self.result = arithmeticOperatorExp.pow
        self.result = self.exitArithmeticOperatorExp(ctx)
    # ArithmeticOperatorMul
    def enterArithmeticOperatorMul(self, ctx):
        arithmeticOperatorMul = ArithmeticOperatorMul(ctx)
        self.result = arithmeticOperatorMul.mul or arithmeticOperatorMul.div or arithmeticOperatorMul.mod
        self.result = self.exitArithmeticOperatorMul(ctx)
    # ArithmeticOperatorAdd
    def enterArithmeticOperatorAdd(self, ctx):
        arithmeticOperatorAdd = ArithmeticOperatorAdd(ctx)
        self.result = arithmeticOperatorAdd.minus or arithmeticOperatorAdd.plus
        self.result = self.exitArithmeticOperatorAdd(ctx)
    # BinaryLogicalOperator
    def enterBinaryLogicalOperator(self, ctx):
        binaryLogicalOperator = BinaryLogicalOperator(ctx)
        self.result = binaryLogicalOperator.and_ or binaryLogicalOperator.or_
        self.result = self.exitBinaryLogicalOperator(ctx)
    # RelationalOperator
    def enterRelationalOperator(self, ctx):
        relationalOperator = RelationalOperator(ctx)
        self.result = relationalOperator.eq or relationalOperator.lt or relationalOperator.lteq or relationalOperator.gt or relationalOperator.gteq or relationalOperator.in_ or relationalOperator.not_ or relationalOperator.is_ or relationalOperator.like or relationalOperator.not_like
        self.result = self.exitRelationalOperator(ctx) 
    # BetweenOperator
    def enterBetweenOperator(self, ctx):
        betweenOperator = BetweenOperator(ctx)
        self.result = betweenOperator.operator or betweenOperator.not_
        self.result = self.exitBetweenOperator(ctx)
    #---------------------------------------------
    # PropertyAssignments
    #---------------------------------------------
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
            # print(ctx.propertyAssignment().getText())
            self.enterPropertyAssignment(ctx.propertyAssignment())
        self.result = self.exitPropertyAssignmentList(ctx)
#---------------------------------------------
# Parse the input file
#---------------------------------------------
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
#---------------------------------------------
# Argument parsing
#---------------------------------------------
if __name__ == "__main__":
    input_file = sys.argv[1]
    result = parse_input(input_file)
    # print(result)
