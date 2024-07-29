import sys
from antlr4 import *
from CartoSymCSSLexer import CartoSymCSSLexer
from CartoSymCSSGrammar import CartoSymCSSGrammar
from CartoSymCSSGrammarListener import CartoSymCSSGrammarListener

# Initialize the listener
class CartoSymCSS2PythonConverter(CartoSymCSSGrammarListener):
    def __init__(self):
        self.stack = []

    def enterEveryRule(self, ctx:ParserRuleContext):
        self.stack.append([])

    def exitEveryRule(self, ctx:ParserRuleContext):
        node = self.stack.pop()
        node_text = ctx.getText()  # Get the text of the current node
        if not node:  # Only add the text if the node is empty
            node.append(node_text)
        if self.stack:
            self.stack[-1].append(node)
        else:
            self.result = node

    def getResult(self):
        return self.result

def parse_input(input_file):
    input_stream = FileStream(input_file, encoding='utf-8')
    lexer = CartoSymCSSLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = CartoSymCSSGrammar(stream)
    tree = parser.styleSheet()
    return tree

def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py path_to_input_file")
        sys.exit(1)
    
    input_file = sys.argv[1]
    tree = parse_input(input_file)
    
    # Walk the tree with the listener
    walker = ParseTreeWalker()
    listener = CartoSymCSS2PythonConverter()
    walker.walk(listener, tree)
    
    # Print the nested array structure
    print(listener.getResult())
    
if __name__ == '__main__':
    main()