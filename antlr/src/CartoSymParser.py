from __future__ import annotations

import logging
import argparse
import functools
from antlr4 import *
from CartoSymCSSLexer import CartoSymCSSLexer
from CartoSymCSSGrammar import CartoSymCSSGrammar
from CartoSymCSSGrammarListener import CartoSymCSSGrammarListener

from dataclasses import dataclass
from typing import Optional
from enum import Enum

#---------------------------------------------
# Import modules
#---------------------------------------------  
from CartoSym.highLevel.StyleSheet import StyleSheet
from CartoSym.highLevel.Metadata import Metadata
from CartoSym.highLevel.StylingRuleList import StylingRuleList
from CartoSym.highLevel.StylingRule import StylingRule
from CartoSym.highLevel.Selector import Selector
from CartoSym.expressions.Expression import Expression
from CartoSym.propertyAssignments.PropertyAssignment import PropertyAssignment
from CartoSym.propertyAssignments.PropertyAssignmentList import PropertyAssignmentList
from CartoSym.expressions.Visualization import Visualization

#---------------------------------------------
# Logging configuration
#---------------------------------------------

def configure_logging(log_level: str) -> logging.Logger:
    """Configure logging based on the provided log level."""
    logging.basicConfig(
        level=getattr(logging, log_level.upper(), "INFO"),
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    return logging.getLogger(__name__)

def log_step(logger, step_name: str):
    """Helper function to log initialization steps."""
    logger.debug(f"{step_name} initialized successfully")

#---------------------------------------------
# High level classes
#---------------------------------------------  
@dataclass
class Symbolizer:
    visibility: Optional[bool] = None
    opacity: Optional[float] = None
    zOrder: Optional[int] = None

class DataLayerType(Enum):
    map = 1
    vector = 2
    coverage = 3

@dataclass
class DataLayer:
    identifier: str
    type: DataLayerType

#---------------------------------------------
# CartoSymParser
#---------------------------------------------
class CartoSymParser(CartoSymCSSGrammarListener):
    def __init__(self):
        self.result = None

    def set_result(self, ctx, cls):
        self.result = cls(ctx)

    def enterStyleSheet(self, ctx):
        self.set_result(ctx, StyleSheet)

    def enterMetadata(self, ctx):
        self.set_result(ctx, Metadata)

    def enterStylingRuleList(self, ctx):
        self.set_result(ctx, StylingRuleList)

    def enterStylingRule(self, ctx):
        self.set_result(ctx, StylingRule)

    def enterSelector(self, ctx):
        self.set_result(ctx, Selector)

    def enterExpression(self, ctx):
        self.set_result(ctx, Expression)

    def enterVisualization(self, ctx):
        self.set_result(ctx, Visualization)

    def enterPropertyAssignment(self, ctx):
        property_assignment = PropertyAssignment(ctx)
        self.result = property_assignment.lhValue or property_assignment.expression

    def enterPropertyAssignmentList(self, ctx):
        self.set_result(ctx, PropertyAssignmentList)

#---------------------------------------------
# Parse the input file
#---------------------------------------------
def parse_input(input_file: str, logger: logging.Logger):
    logger.info(f"Parsing file: {input_file}")
    
    try:
        input_stream = FileStream(input_file, encoding='utf-8')
        lexer = CartoSymCSSLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = CartoSymCSSGrammar(stream)
        
        tree = parser.styleSheet()
        
        if logger.isEnabledFor(logging.DEBUG):
            pass
            # logger.debug(f"Parse tree: {tree.toStringTree(recog=parser)}")
            # logger.debug(f"Root rule: {type(tree).__name__}")
            # logger.debug(f"Top-level rules: {[child.__class__.__name__ for child in tree.children]}")

        walker = ParseTreeWalker()
        cartoSymParser = CartoSymParser()
        walker.walk(cartoSymParser, tree)

        return cartoSymParser.result

    except Exception as e:
        logger.error(f"Error during parsing: {e}")
        raise

#---------------------------------------------
# Argument parsing and dynamic decorator application
#---------------------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse a CartoSym CSS file.")
    parser.add_argument("input_file", help="Path to the input file.")
    parser.add_argument("--log-level", default="INFO", help="Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).")
    args = parser.parse_args()

    # Configure logging based on the provided log level
    logger = configure_logging(args.log_level)

    # Parse the input file
    result = parse_input(args.input_file, logger)
    # print(result)
