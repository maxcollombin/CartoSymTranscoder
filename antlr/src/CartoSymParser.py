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
# Import modules
#---------------------------------------------  
# HighLevel
from CartoSym.highLevel.StyleSheet import StyleSheet
from CartoSym.highLevel.Metadata import Metadata
from CartoSym.highLevel.StylingRuleList import StylingRuleList
from CartoSym.highLevel.StylingRule import StylingRule
from CartoSym.highLevel.Selector import Selector
# Expressions
from CartoSym.expressions.Expression import Expression
from CartoSym.expressions.IdentifierExpression import IdentifierExpression
from CartoSym.expressions.SystemIdentifierExpression import SystemIdentifierExpression
from CartoSym.expressions.IdOrConstant import IdOrConstant
from CartoSym.expressions.ExpConstant import ExpConstant
from CartoSym.expressions.ExpString import ExpString
from CartoSym.expressions.ExpCall import ExpCall
from CartoSym.expressions.ExpArray import ExpArray
from CartoSym.expressions.ExpInstance import ExpInstance
from CartoSym.expressions.Arguments import Arguments
from CartoSym.expressions.ArrayElements import ArrayElements
# Operators
from CartoSym.operators.ArithmeticOperatorExp import ArithmeticOperatorExp
from CartoSym.operators.ArithmeticOperatorMul import ArithmeticOperatorMul
from CartoSym.operators.ArithmeticOperatorAdd import ArithmeticOperatorAdd
from CartoSym.operators.BinaryLogicalOperator import BinaryLogicalOperator
from CartoSym.operators.RelationalOperator import RelationalOperator
from CartoSym.operators.BetweenOperator import BetweenOperator
# PropertyAssignments
from CartoSym.propertyAssignments.PropertyAssignment import PropertyAssignment
from CartoSym.propertyAssignments.PropertyAssignmentList import PropertyAssignmentList
from CartoSym.propertyAssignments.PropertyAssignmentInferred import PropertyAssignmentInferred
from CartoSym.propertyAssignments.PropertyAssignmentInferredList import PropertyAssignmentInferredList
#---------------------------------------------
# High level classes
#---------------------------------------------  
# Expression

# Symbolizer class
@dataclass
class Symbolizer:
    visibility = Optional[bool]
    opacity = Optional[float]
    zOrder = Optional[int]
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
#---------------------------------------------
# CartoSymParser
#---------------------------------------------
class CartoSymParser(CartoSymCSSGrammarListener):
    #---------------------------------------------
    # High level
    #---------------------------------------------
    # StyleSheet
    def enterStyleSheet(self, ctx):
        styleSheet = StyleSheet(ctx)
        self.result = styleSheet.metadata or styleSheet.stylingRuleList
        self.result = self.exitStyleSheet(ctx)
    # Metadata
    def enterMetadata(self, ctx):
        metadata = Metadata(ctx)
        self.result = metadata.name or metadata.title or metadata.description or metadata.authors or metadata.keywords or metadata.geoDataClasses
        self.result = self.exitMetadata(ctx)
    # StylingRuleList
    def enterStylingRuleList(self, ctx):
        stylingRuleList = StylingRuleList(ctx)
        self.result = stylingRuleList.stylingRule or stylingRuleList.stylingRuleList
        self.result = self.exitStylingRuleList(ctx)    
    # StylingRule
    def enterStylingRule(self, ctx):
        stylingRule = StylingRule(ctx)
        self.result = stylingRule.selector or stylingRule.symbolizer or stylingRule.nestedRules
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
        expArray = ExpArray(ctx)
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
    # Operators clas methods
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
        propertyAssignmentInferredList = PropertyAssignmentInferredList(ctx)
        self.result = propertyAssignmentInferredList.propertyAssignmentInferred or propertyAssignmentInferredList.propertyAssignmentInferredList
        print(propertyAssignmentInferredList.propertyAssignmentInferred)
        self.result = self.exitPropertyAssignmentInferredList(ctx)
    # PropertyAssignmentInferred
    def enterPropertyAssignmentInferred(self, ctx):
        propertyAssignmentInferred = PropertyAssignmentInferred(ctx)
        self.result = propertyAssignmentInferred.propertyAssignment or propertyAssignmentInferred.expression
        self.result = self.exitPropertyAssignmentInferred(ctx)
    # PropertyAssignment
    def enterPropertyAssignment(self, ctx):
        propertyAssignment = PropertyAssignment(ctx)
        self.result = propertyAssignment.lhValue or propertyAssignment.expression
        self.exitPropertyAssignment(ctx)
    # PropertyAssignmentList
    def enterPropertyAssignmentList(self, ctx):
        propertyAssignmentList = PropertyAssignmentList(ctx)
        self.result = propertyAssignmentList.propertyAssignment or propertyAssignmentList.propertyAssignmentList
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
