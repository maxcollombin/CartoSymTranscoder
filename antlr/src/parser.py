import sys
from antlr4 import *
from CartoSymCSSLexer import CartoSymCSSLexer
from CartoSymCSSGrammar import CartoSymCSSGrammar
from CartoSymCSSGrammarListener import CartoSymCSSGrammarListener

class CartoSymParser(CartoSymCSSGrammarListener):
    def __init__(self):
        self.result = {
            'title': '',
            'abstract': '',
            'description': '',
            'rules': []
        }
        self.rule_stack = []  # Initialize rule_stack to handle nested rules

    def enterMetadata(self, ctx):
        identifier = ctx.IDENTIFIER().getText()
        character_literal = ctx.CHARACTER_LITERAL().getText().strip('"')
        
        if identifier == 'title':
            self.result['title'] = character_literal
        elif identifier == 'abstract':
            self.result['abstract'] = character_literal
        elif identifier == 'description':
            self.result['description'] = character_literal
        else:
            self.result[identifier] = character_literal

    def enterStylingRule(self, ctx):
        # Extract selectors and create a new rule for each selector
        selectors = []
        for selector in ctx.selector():
            selectors.append(selector.getText())

        rule = {
            'selectors': selectors,
            'properties': {}
        }
  
        # Extract property assignments
        if ctx.propertyAssignmentList():
            self.enterPropertyAssignments(ctx.propertyAssignmentList(), rule['properties'])

        # Handle nested rules
        if self.rule_stack:
            parent_rule = self.rule_stack[-1]
            parent_rule['properties'].update(rule['properties'])
        else:
            self.result['rules'].append(rule)

        self.rule_stack.append(rule)
    
    def enterSelector(self, ctx):
        if ctx.IDENTIFIER():
            self.rule_stack[-1]['selectors'].append(ctx.IDENTIFIER().getText())


    def enterExpression(self, ctx):
        
        if ctx.DOT():

            # System Identifiers
            system_identifier = ctx.expression(0).getText()

            # Visualization System Identifiers
            if system_identifier == 'viz' or system_identifier == 'visualization':

                # scaleDenominator
                if ctx.IDENTIFIER().getText() == 'sd':
                    if ctx.parentCtx.expression(1).binaryLogicalOperator():
                        # MaxScaleDenominator
                        if ctx.parentCtx.relationalOperator().getText() == '<':
                            value = ctx.parentCtx.expression(1).expression(0).getText()
                            self.result['max_scale_denominator'] = value
                        # MinScaleDenominator
                        elif ctx.parentCtx.relationalOperator().getText() == '>':
                            value = ctx.parentCtx.expression(1).expression(0).getText()
                            self.result['min_scale_denominator'] = value

                # date
                if ctx.IDENTIFIER().getText() == 'date':
                    value =  ctx.parentCtx.parentCtx.parentCtx.expression(1).expCall().arguments().getText()
                    self.result['date'] = value

            # Layer System Identifiers
            if system_identifier == 'dataLayer':
                
                # Data Layer Types
                if ctx.IDENTIFIER().getText() == 'type':
                    if ctx.parentCtx.relationalOperator():
                        value =  ctx.parentCtx.expression(1).getText()
                        self.result['data_layer_type'] = value

    def enterPropertyAssignments(self, ctx, properties):
        if ctx.propertyAssignment():
            property_assignments = ctx.propertyAssignment()
            if not isinstance(property_assignments, list):
                property_assignments = [property_assignments]
            for property_assignment in property_assignments:
                key = property_assignment.lhValue().getText()
                value = property_assignment.expression().getText()
                properties[key] = value

        if ctx.propertyAssignmentList():
            # Recursively handle nested propertyAssignmentList
            sub_lists = ctx.propertyAssignmentList()
            if not isinstance(sub_lists, list):
                sub_lists = [sub_lists]
            for sub_ctx in sub_lists:
                self.enterPropertyAssignments(sub_ctx, properties)

    def exitStylingRule(self, ctx):
        self.rule_stack.pop()
        print(self.result)

    def getResult(self):
        return self.result

def parse_input(input_file):
    input_stream = FileStream(input_file, encoding='utf-8')
    lexer = CartoSymCSSLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = CartoSymCSSGrammar(stream)
    tree = parser.styleSheet()
    
    converter = CartoSymParser()
    walker = ParseTreeWalker()
    walker.walk(converter, tree)
    
    return converter.getResult()

if __name__ == "__main__":
    input_file = sys.argv[1]
    result = parse_input(input_file)
