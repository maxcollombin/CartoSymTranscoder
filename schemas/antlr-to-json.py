import os
import json
from antlr4 import *
# from antlr4.tree.Trees import Trees
from CartoSymCSSLexer import CartoSymCSSLexer
from CartoSymCSSGrammar import CartoSymCSSGrammar
from CartoSymCSSGrammarListener import CartoSymCSSGrammarListener

# Note: Before running the script, make sure to generate the lexer and parser files using the following command:
# antlr4 -Dlanguage=Python3 CartoSymCSSLexer.g4
# antlr4 -Dlanguage=Python3 CartoSymCSSGrammar.g4

from CartoSymCSSGrammarListener import CartoSymCSSGrammarListener

class JsonListener(CartoSymCSSGrammarListener):
    def __init__(self):
        self.stack = []
        self.json = {}
        self.currentRule = None
    
    def enterMetadata(self, ctx):
        identifier = ctx.IDENTIFIER().getText()
        value = ctx.CHARACTER_LITERAL().getText().strip("'")

        if "metadata" not in self.json:
            self.json["metadata"] = {"title": "", "abstract": ""}

        if identifier == "title":
            self.json["metadata"]["title"] = value
        elif identifier == "abstract":
            self.json["metadata"]["abstract"] = value

    def enterStylingRule(self, ctx):
        self.currentRule = {"selector": [], "symbolizer": {}}
        if self.stack:
            self.stack[-1].setdefault("nestedRules", []).append(self.currentRule)
        self.stack.append(self.currentRule)

        if not self.stack or len(self.stack) == 1:
            if "stylingRules" not in self.json:
                self.json["stylingRules"] = []
            self.json["stylingRules"].append(self.currentRule)

    def exitStylingRule(self, ctx):
        self.stack.pop()
        if self.stack:
            self.currentRule = self.stack[-1]
        else:
            self.currentRule = None
        
    def enterSelector(self, ctx):
        if self.stack:
            # Handle spaces in the selector
            start = ctx.start.start
            stop = ctx.stop.stop
            selector_text = ctx.start.getInputStream().getText(start, stop)

            self.stack[-1]["selector"].append(selector_text)

    def enterPropertyAssignment(self, ctx):
        if self.stack:
            # Get the entire text of the property assignment
            start = ctx.start.start
            stop = ctx.stop.stop
            property_assignment_text = ctx.start.getInputStream().getText(start, stop)

            # Split the text into the property name and value
            property_name, property_value = property_assignment_text.split(':', 1)

            # Strip leading and trailing spaces from the property name and value
            property_name = property_name.strip()
            property_value = property_value.strip()

            self.stack[-1]["symbolizer"][property_name] = property_value

# Parse the input
input_filepath = "../examples/8-coverage-hillshading.cscss"
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

# Write the output to the output file

with open(output_filepath, 'w') as f:
    json.dump(json_listener.json, f, indent=4)
