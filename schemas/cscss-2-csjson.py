import os
import re
import json
import selectors
from antlr4 import *
# from antlr4.tree.Trees import Trees
from CartoSymCSSLexer import CartoSymCSSLexer
from CartoSymCSSGrammar import CartoSymCSSGrammar
from CartoSymCSSGrammarListener import CartoSymCSSGrammarListener

# Note: Before running the script, make sure to generate the lexer and parser files using the following command:
# antlr4 -Dlanguage=Python3 CartoSymCSSLexer.g4
# antlr4 -Dlanguage=Python3 CartoSymCSSGrammar.g4
class JsonListener(CartoSymCSSGrammarListener):
    def __init__(self):
        self.stack = []
        self.json = {}  
        self.currentRule = None

    def enterMetadata(self, ctx):
        identifier = ctx.IDENTIFIER().getText()
        value = ctx.CHARACTER_LITERAL().getText().strip("'")

        # Initialize the metadata dictionary in the json dictionary
        if "metadata" not in self.json:
            self.json["metadata"] = {}

        # Assign the value to the corresponding identifier in the dictionary
        self.json["metadata"][identifier] = value

    def enterStylingRuleList(self, ctx):
        # Initialize the styling rule list in the dictionary
        self.json["stylingRules"] = []

    def enterStylingRule(self, ctx):
        # Create a new styling rule dictionary
        stylingRule = {"selector": []}
        # stylingRule = {"selectors": [], "properties": {}, "nestedRules": []}
        # Add the styling rule dictionary to the stylingRules list
        self.json["stylingRules"].append(stylingRule)
    
    def enterSelector(self, ctx):
    # Initialize the 'selector' dictionary
        self.json["stylingRules"][-1]["selector"] = {"op": "and", "args": []}
        if ctx.IDENTIFIER():
            identifier = ctx.IDENTIFIER().getText()
            identifier_dict = {"op": "=", "args": [{"sysId": "dataLayer.id"}, identifier]}
            self.json["stylingRules"][-1]["selector"]["args"].append(identifier_dict)
            print(self.json)
        elif ctx.expression():
            expression = ctx.expression().getText()
            # print(expression)
        #     expression_dict = {"op": "expression", "args": [expression]}
        #     self.json["stylingRules"][-1]["selector"]["args"].append(expression_dict)
        #     print(self.json)

# Parse the input
input_filepath = "../examples/1-core.cscss"
input_stream = FileStream(input_filepath)
lexer = CartoSymCSSLexer(input_stream)
token_stream = CommonTokenStream(lexer)
parser = CartoSymCSSGrammar(token_stream)
tree = parser.styleSheet()  # replace with the start rule

# Walk the tree
json_listener = JsonListener()
walker = ParseTreeWalker()
walker.walk(json_listener, tree)

# Get the filename without extension
base_filename = os.path.basename(input_filepath)
filename_without_extension = os.path.splitext(base_filename)[0]

# Create the output filename
output_filename = filename_without_extension + ".cs.json"

# Prepend the directory path to the output filename
output_filepath = os.path.join("../examples/", output_filename)

# Write the output to the file

with open(output_filepath, 'w') as f:
    print(json_listener.json)
    json.dump(json_listener.json, f, indent=4)
