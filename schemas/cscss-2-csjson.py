import os
import re
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

        # Initialize the dictionary
        if "metadata" not in self.json:
            self.json["metadata"] = {}

        # Assign the value to the corresponding identifier in the dictionary
        self.json["metadata"][identifier] = value

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

            # Parse the selector into an operation and its arguments
            operation, args = self.parse_selector(selector_text)

        self.stack[-1]["selector"] = {"op": operation, "args": args}
        # self.stack[-1]["selector"].append(selector_text)
        # self.stack[-1]["selector"].append({"op": "=", "args": [ { "sysId": "dataLayer.id" }, selector_text ]})

    def parse_selector(self, selector_text):
        # Split the selector_text on 'and' to get the individual conditions
        conditions = re.split(r'\s+and\s+', selector_text)
    
        # Initialize the args list
        args = []
    
        # Process each condition
        for condition in conditions:
            # Split the condition with the operators '<', '>', and '='
            parts = re.split(r'(<|>|=)', condition)
    
            # Check if the parts list has the expected number of elements
            if len(parts) >= 3:
                # The operation is the comparison operator
                operation = parts[1]
    
                # The arguments are the values on either side of the comparison operator
                left_arg = parts[0].strip()
                right_arg = parts[2].strip()
    
                # Remove unwanted characters from the arguments
                left_arg = left_arg.replace("[", "").replace("]", "")
                right_arg = right_arg.replace("[", "").replace("]", "")

                if "dataLayer" in left_arg or "viz" in left_arg or "feature" in left_arg:
                    args.append({"op": operation, "args": [{"sysId": left_arg.strip()}, right_arg]})
                else:
                    args.append({"op": operation, "args": [{"property": left_arg.strip()}, right_arg]})
        
        # The operation for the entire selector is 'and'
        # operation = "and"
        operation = "and" if len(args) > 1 else args[0]["op"] if args else ""
        # operation = "and" if len(args) > 1 else "=" if len(args) == 1 else ""

        return operation, args

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
    json.dump(json_listener.json, f, indent=4)
