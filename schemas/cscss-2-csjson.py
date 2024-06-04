# Note: Before running the script, make sure to generate the lexer and parser files using the following command:
# antlr4 -Dlanguage=Python3 CartoSymCSSLexer.g4
# antlr4 -Dlanguage=Python3 CartoSymCSSGrammar.g4

import os
import json
from antlr4 import *
from CartoSymCSSLexer import CartoSymCSSLexer
from CartoSymCSSGrammar import CartoSymCSSGrammar
from CartoSymCSSGrammarListener import CartoSymCSSGrammarListener
from pathlib import Path

class Metadata:
    def __init__(self):
        self.data = {}

    def add(self, identifier, value):
        self.data[identifier] = value

    def to_json(self):
        return self.data
    
class Selector:
    def __init__(self):
        self.data = {"op": "and", "args": []}

    def add_identifier(self, identifier):
        identifier_dict = {"op": "=", "args": [{"sysId": "dataLayer.id"}, identifier]}
        self.data["args"].append(identifier_dict)

    def add_expression(self, expression):
        expression_dict = {"op": "expression", "args": [expression]}
        self.data["args"].append(expression_dict)

    def to_json(self):
        return self.data
class StylingRule:
    def __init__(self):
        self.data = {"selector": Selector()}

    def to_json(self):
        return {"selector": self.data["selector"].to_json()}
class JsonListener(CartoSymCSSGrammarListener):
    def __init__(self):
        self.json = {"metadata": Metadata(), "stylingRules": []}
        self.currentRule = None

    def enterMetadata(self, ctx):
        identifier = ctx.IDENTIFIER().getText()
        value = ctx.CHARACTER_LITERAL().getText().strip("'")
        self.json["metadata"].add(identifier, value)

    def enterStylingRule(self, ctx):
        self.json["stylingRules"].append(StylingRule())

    def enterSelector(self, ctx):
        if ctx.IDENTIFIER():
            identifier = ctx.IDENTIFIER().getText()
            self.json["stylingRules"][-1].data["selector"].add_identifier(identifier)
        elif ctx.expression():
            expression = ctx.expression().getText()
            self.json["stylingRules"][-1].data["selector"].add_expression(expression)

# Parse the input
input_filename = "../examples/1-core.cscss"
input_filename = os.path.basename(input_filename)  # Get the base name to avoid path traversal
input_filepath = Path("../examples") / input_filename  # Use pathlib to safely join paths
input_stream = FileStream(str(input_filepath))  # Convert Path object to string

lexer = CartoSymCSSLexer(input_stream)
token_stream = CommonTokenStream(lexer)
parser = CartoSymCSSGrammar(token_stream)
tree = parser.styleSheet()  # replace with the start rule

# Walk the tree
json_listener = JsonListener()
walker = ParseTreeWalker()
walker.walk(json_listener, tree)

# Get the filename without extension
base_filename = os.path.basename(str(input_filepath))
filename_without_extension = os.path.splitext(base_filename)[0]

# Create the output filename
output_filename = filename_without_extension + ".cs.json"

# Prepend the directory path to the output filename
output_filepath = Path("../examples") / output_filename  # Use pathlib to safely join paths

# Write the output to the file
with open(output_filepath, 'w') as f:
    json.dump(
        {
            "metadata": json_listener.json["metadata"].to_json(),
            "stylingRules": [rule.to_json() for rule in json_listener.json["stylingRules"]],
        },
        f,
        indent=4,
    )