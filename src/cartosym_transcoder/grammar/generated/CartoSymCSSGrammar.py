# Generated from vendor/cartosymcss-grammar/CartoSymCSSGrammar.g4 by ANTLR 4.13.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,39,363,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        2,14,7,14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,7,19,2,20,
        7,20,2,21,7,21,2,22,7,22,2,23,7,23,2,24,7,24,2,25,7,25,2,26,7,26,
        2,27,7,27,2,28,7,28,2,29,7,29,2,30,7,30,1,0,5,0,64,8,0,10,0,12,0,
        67,9,0,1,0,5,0,70,8,0,10,0,12,0,73,9,0,1,0,3,0,76,8,0,1,1,1,1,1,
        1,1,2,1,2,1,2,1,2,1,2,1,3,1,3,1,3,1,3,1,4,1,4,1,4,1,4,1,5,1,5,1,
        5,1,5,1,5,5,5,99,8,5,10,5,12,5,102,9,5,1,6,5,6,105,8,6,10,6,12,6,
        108,9,6,1,6,1,6,3,6,112,8,6,1,6,1,6,1,6,3,6,117,8,6,1,6,3,6,120,
        8,6,1,6,1,6,1,7,1,7,1,7,1,7,1,7,3,7,129,8,7,1,8,1,8,3,8,133,8,8,
        1,9,1,9,1,9,1,9,1,9,1,9,5,9,141,8,9,10,9,12,9,144,9,9,1,10,1,10,
        1,10,1,10,1,10,1,10,1,10,1,10,1,10,1,10,1,10,1,10,1,10,1,10,1,10,
        1,10,1,10,1,10,3,10,164,8,10,1,10,1,10,1,10,1,10,1,10,1,10,1,10,
        1,10,1,10,1,10,1,10,1,10,1,10,1,10,1,10,1,10,1,10,1,10,1,10,1,10,
        1,10,1,10,1,10,1,10,1,10,1,10,1,10,1,10,1,10,1,10,1,10,1,10,1,10,
        1,10,1,10,1,10,1,10,1,10,1,10,1,10,5,10,206,8,10,10,10,12,10,209,
        9,10,1,11,1,11,3,11,213,8,11,1,11,3,11,216,8,11,1,12,1,12,1,13,3,
        13,221,8,13,1,13,1,13,3,13,225,8,13,1,13,3,13,228,8,13,1,13,1,13,
        1,13,1,13,3,13,234,8,13,1,13,3,13,237,8,13,1,13,3,13,240,8,13,1,
        14,1,14,1,14,1,14,1,14,1,14,1,14,1,14,1,14,1,14,1,14,5,14,253,8,
        14,10,14,12,14,256,9,14,1,15,1,15,1,15,1,15,1,16,1,16,1,16,1,16,
        1,16,1,16,5,16,268,8,16,10,16,12,16,271,9,16,1,17,1,17,3,17,275,
        8,17,1,18,1,18,1,18,1,18,1,18,1,18,1,18,1,18,1,18,5,18,286,8,18,
        10,18,12,18,289,9,18,1,19,1,19,3,19,293,8,19,1,19,1,19,1,19,3,19,
        298,8,19,1,19,3,19,301,8,19,1,20,1,20,1,20,1,20,1,20,1,20,5,20,309,
        8,20,10,20,12,20,312,9,20,1,21,1,21,1,21,1,21,1,21,1,22,1,22,1,22,
        1,22,1,22,1,22,5,22,325,8,22,10,22,12,22,328,9,22,1,23,1,23,1,24,
        1,24,1,25,1,25,1,26,1,26,1,27,1,27,1,28,1,28,1,29,1,29,1,29,1,29,
        1,29,1,29,1,29,1,29,1,29,1,29,1,29,1,29,1,29,1,29,3,29,356,8,29,
        1,30,1,30,1,30,3,30,361,8,30,1,30,0,8,10,18,20,28,32,36,40,44,31,
        0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,38,40,42,44,
        46,48,50,52,54,56,58,60,0,3,1,0,22,23,1,0,29,30,1,0,24,27,390,0,
        65,1,0,0,0,2,77,1,0,0,0,4,80,1,0,0,0,6,85,1,0,0,0,8,89,1,0,0,0,10,
        93,1,0,0,0,12,106,1,0,0,0,14,128,1,0,0,0,16,132,1,0,0,0,18,134,1,
        0,0,0,20,163,1,0,0,0,22,215,1,0,0,0,24,217,1,0,0,0,26,239,1,0,0,
        0,28,241,1,0,0,0,30,257,1,0,0,0,32,261,1,0,0,0,34,274,1,0,0,0,36,
        276,1,0,0,0,38,300,1,0,0,0,40,302,1,0,0,0,42,313,1,0,0,0,44,318,
        1,0,0,0,46,329,1,0,0,0,48,331,1,0,0,0,50,333,1,0,0,0,52,335,1,0,
        0,0,54,337,1,0,0,0,56,339,1,0,0,0,58,355,1,0,0,0,60,360,1,0,0,0,
        62,64,3,6,3,0,63,62,1,0,0,0,64,67,1,0,0,0,65,63,1,0,0,0,65,66,1,
        0,0,0,66,71,1,0,0,0,67,65,1,0,0,0,68,70,3,4,2,0,69,68,1,0,0,0,70,
        73,1,0,0,0,71,69,1,0,0,0,71,72,1,0,0,0,72,75,1,0,0,0,73,71,1,0,0,
        0,74,76,3,10,5,0,75,74,1,0,0,0,75,76,1,0,0,0,76,1,1,0,0,0,77,78,
        5,36,0,0,78,79,5,35,0,0,79,3,1,0,0,0,80,81,3,2,1,0,81,82,5,10,0,
        0,82,83,3,20,10,0,83,84,5,4,0,0,84,5,1,0,0,0,85,86,5,3,0,0,86,87,
        5,35,0,0,87,88,5,34,0,0,88,7,1,0,0,0,89,90,5,3,0,0,90,91,5,35,0,
        0,91,92,5,34,0,0,92,9,1,0,0,0,93,94,6,5,-1,0,94,95,3,12,6,0,95,100,
        1,0,0,0,96,97,10,1,0,0,97,99,3,12,6,0,98,96,1,0,0,0,99,102,1,0,0,
        0,100,98,1,0,0,0,100,101,1,0,0,0,101,11,1,0,0,0,102,100,1,0,0,0,
        103,105,3,14,7,0,104,103,1,0,0,0,105,108,1,0,0,0,106,104,1,0,0,0,
        106,107,1,0,0,0,107,109,1,0,0,0,108,106,1,0,0,0,109,111,5,1,0,0,
        110,112,3,8,4,0,111,110,1,0,0,0,111,112,1,0,0,0,112,116,1,0,0,0,
        113,114,3,32,16,0,114,115,5,4,0,0,115,117,1,0,0,0,116,113,1,0,0,
        0,116,117,1,0,0,0,117,119,1,0,0,0,118,120,3,10,5,0,119,118,1,0,0,
        0,119,120,1,0,0,0,120,121,1,0,0,0,121,122,5,2,0,0,122,13,1,0,0,0,
        123,129,5,35,0,0,124,125,5,5,0,0,125,126,3,20,10,0,126,127,5,6,0,
        0,127,129,1,0,0,0,128,123,1,0,0,0,128,124,1,0,0,0,129,15,1,0,0,0,
        130,133,5,35,0,0,131,133,3,22,11,0,132,130,1,0,0,0,132,131,1,0,0,
        0,133,17,1,0,0,0,134,135,6,9,-1,0,135,136,3,16,8,0,136,137,3,16,
        8,0,137,142,1,0,0,0,138,139,10,1,0,0,139,141,3,16,8,0,140,138,1,
        0,0,0,141,144,1,0,0,0,142,140,1,0,0,0,142,143,1,0,0,0,143,19,1,0,
        0,0,144,142,1,0,0,0,145,146,6,10,-1,0,146,164,3,16,8,0,147,164,3,
        24,12,0,148,164,3,42,21,0,149,164,3,38,19,0,150,164,3,26,13,0,151,
        152,5,7,0,0,152,153,3,20,10,0,153,154,5,8,0,0,154,164,1,0,0,0,155,
        156,3,48,24,0,156,157,3,20,10,4,157,164,1,0,0,0,158,159,3,50,25,
        0,159,160,3,20,10,3,160,164,1,0,0,0,161,164,3,18,9,0,162,164,3,2,
        1,0,163,145,1,0,0,0,163,147,1,0,0,0,163,148,1,0,0,0,163,149,1,0,
        0,0,163,150,1,0,0,0,163,151,1,0,0,0,163,155,1,0,0,0,163,158,1,0,
        0,0,163,161,1,0,0,0,163,162,1,0,0,0,164,207,1,0,0,0,165,166,10,11,
        0,0,166,167,3,52,26,0,167,168,3,20,10,12,168,206,1,0,0,0,169,170,
        10,10,0,0,170,171,3,54,27,0,171,172,3,20,10,11,172,206,1,0,0,0,173,
        174,10,9,0,0,174,175,3,56,28,0,175,176,3,20,10,10,176,206,1,0,0,
        0,177,178,10,8,0,0,178,179,3,46,23,0,179,180,3,20,10,9,180,206,1,
        0,0,0,181,182,10,7,0,0,182,183,3,58,29,0,183,184,3,20,10,8,184,206,
        1,0,0,0,185,186,10,6,0,0,186,187,3,60,30,0,187,188,3,20,10,0,188,
        189,5,22,0,0,189,190,3,20,10,7,190,206,1,0,0,0,191,192,10,5,0,0,
        192,193,5,20,0,0,193,194,3,20,10,0,194,195,5,21,0,0,195,196,3,20,
        10,6,196,206,1,0,0,0,197,198,10,18,0,0,198,199,5,3,0,0,199,206,5,
        35,0,0,200,201,10,12,0,0,201,202,5,5,0,0,202,203,3,22,11,0,203,204,
        5,6,0,0,204,206,1,0,0,0,205,165,1,0,0,0,205,169,1,0,0,0,205,173,
        1,0,0,0,205,177,1,0,0,0,205,181,1,0,0,0,205,185,1,0,0,0,205,191,
        1,0,0,0,205,197,1,0,0,0,205,200,1,0,0,0,206,209,1,0,0,0,207,205,
        1,0,0,0,207,208,1,0,0,0,208,21,1,0,0,0,209,207,1,0,0,0,210,212,5,
        33,0,0,211,213,5,31,0,0,212,211,1,0,0,0,212,213,1,0,0,0,213,216,
        1,0,0,0,214,216,5,32,0,0,215,210,1,0,0,0,215,214,1,0,0,0,216,23,
        1,0,0,0,217,218,5,34,0,0,218,25,1,0,0,0,219,221,5,35,0,0,220,219,
        1,0,0,0,220,221,1,0,0,0,221,222,1,0,0,0,222,224,5,1,0,0,223,225,
        3,36,18,0,224,223,1,0,0,0,224,225,1,0,0,0,225,227,1,0,0,0,226,228,
        5,4,0,0,227,226,1,0,0,0,227,228,1,0,0,0,228,229,1,0,0,0,229,240,
        5,2,0,0,230,231,5,35,0,0,231,233,5,7,0,0,232,234,3,36,18,0,233,232,
        1,0,0,0,233,234,1,0,0,0,234,236,1,0,0,0,235,237,5,4,0,0,236,235,
        1,0,0,0,236,237,1,0,0,0,237,238,1,0,0,0,238,240,5,8,0,0,239,220,
        1,0,0,0,239,230,1,0,0,0,240,27,1,0,0,0,241,242,6,14,-1,0,242,243,
        5,35,0,0,243,254,1,0,0,0,244,245,10,2,0,0,245,246,5,3,0,0,246,253,
        5,35,0,0,247,248,10,1,0,0,248,249,5,5,0,0,249,250,3,22,11,0,250,
        251,5,6,0,0,251,253,1,0,0,0,252,244,1,0,0,0,252,247,1,0,0,0,253,
        256,1,0,0,0,254,252,1,0,0,0,254,255,1,0,0,0,255,29,1,0,0,0,256,254,
        1,0,0,0,257,258,3,28,14,0,258,259,5,21,0,0,259,260,3,20,10,0,260,
        31,1,0,0,0,261,262,6,16,-1,0,262,263,3,30,15,0,263,269,1,0,0,0,264,
        265,10,1,0,0,265,266,5,4,0,0,266,268,3,30,15,0,267,264,1,0,0,0,268,
        271,1,0,0,0,269,267,1,0,0,0,269,270,1,0,0,0,270,33,1,0,0,0,271,269,
        1,0,0,0,272,275,3,30,15,0,273,275,3,20,10,0,274,272,1,0,0,0,274,
        273,1,0,0,0,275,35,1,0,0,0,276,277,6,18,-1,0,277,278,3,34,17,0,278,
        287,1,0,0,0,279,280,10,2,0,0,280,281,5,4,0,0,281,286,3,34,17,0,282,
        283,10,1,0,0,283,284,5,9,0,0,284,286,3,34,17,0,285,279,1,0,0,0,285,
        282,1,0,0,0,286,289,1,0,0,0,287,285,1,0,0,0,287,288,1,0,0,0,288,
        37,1,0,0,0,289,287,1,0,0,0,290,292,5,5,0,0,291,293,3,40,20,0,292,
        291,1,0,0,0,292,293,1,0,0,0,293,294,1,0,0,0,294,301,5,6,0,0,295,
        297,5,7,0,0,296,298,3,40,20,0,297,296,1,0,0,0,297,298,1,0,0,0,298,
        299,1,0,0,0,299,301,5,8,0,0,300,290,1,0,0,0,300,295,1,0,0,0,301,
        39,1,0,0,0,302,303,6,20,-1,0,303,304,3,20,10,0,304,310,1,0,0,0,305,
        306,10,1,0,0,306,307,5,9,0,0,307,309,3,20,10,0,308,305,1,0,0,0,309,
        312,1,0,0,0,310,308,1,0,0,0,310,311,1,0,0,0,311,41,1,0,0,0,312,310,
        1,0,0,0,313,314,5,35,0,0,314,315,5,7,0,0,315,316,3,44,22,0,316,317,
        5,8,0,0,317,43,1,0,0,0,318,319,6,22,-1,0,319,320,3,20,10,0,320,326,
        1,0,0,0,321,322,10,1,0,0,322,323,5,9,0,0,323,325,3,20,10,0,324,321,
        1,0,0,0,325,328,1,0,0,0,326,324,1,0,0,0,326,327,1,0,0,0,327,45,1,
        0,0,0,328,326,1,0,0,0,329,330,7,0,0,0,330,47,1,0,0,0,331,332,5,16,
        0,0,332,49,1,0,0,0,333,334,7,1,0,0,334,51,1,0,0,0,335,336,5,28,0,
        0,336,53,1,0,0,0,337,338,7,2,0,0,338,55,1,0,0,0,339,340,7,1,0,0,
        340,57,1,0,0,0,341,356,5,10,0,0,342,356,5,11,0,0,343,356,5,12,0,
        0,344,356,5,13,0,0,345,356,5,14,0,0,346,356,5,15,0,0,347,348,5,16,
        0,0,348,356,5,15,0,0,349,356,5,17,0,0,350,351,5,17,0,0,351,356,5,
        16,0,0,352,356,5,18,0,0,353,354,5,16,0,0,354,356,5,18,0,0,355,341,
        1,0,0,0,355,342,1,0,0,0,355,343,1,0,0,0,355,344,1,0,0,0,355,345,
        1,0,0,0,355,346,1,0,0,0,355,347,1,0,0,0,355,349,1,0,0,0,355,350,
        1,0,0,0,355,352,1,0,0,0,355,353,1,0,0,0,356,59,1,0,0,0,357,361,5,
        19,0,0,358,359,5,16,0,0,359,361,5,19,0,0,360,357,1,0,0,0,360,358,
        1,0,0,0,361,61,1,0,0,0,35,65,71,75,100,106,111,116,119,128,132,142,
        163,205,207,212,215,220,224,227,233,236,239,252,254,269,274,285,
        287,292,297,300,310,326,355,360
    ]

class CartoSymCSSGrammar ( Parser ):

    grammarFileName = "CartoSymCSSGrammar.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'{'", "'}'", "'.'", "';'", "'['", "']'", 
                     "'('", "')'", "','", "'='", "'<'", "'<='", "'>'", "'>='", 
                     "'in'", "'not'", "'is'", "'like'", "'between'", "'?'", 
                     "':'", "'and'", "'or'", "'*'", "'/'", "'div'", "'%'", 
                     "'^'", "'-'", "'+'", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "'@'" ]

    symbolicNames = [ "<INVALID>", "LCBR", "RCBR", "DOT", "SEMI", "LSBR", 
                      "RSBR", "LPAR", "RPAR", "COMMA", "EQ", "LT", "LTEQ", 
                      "GT", "GTEQ", "IN", "NOT", "IS", "LIKE", "BETWEEN", 
                      "QUESTION", "COLON", "AND", "OR", "MUL", "DIV", "IDIV", 
                      "MOD", "POW", "MINUS", "PLUS", "UNIT", "HEX_LITERAL", 
                      "NUMERIC_LITERAL", "CHARACTER_LITERAL", "IDENTIFIER", 
                      "AT_SIGN", "COMMENT", "LINE_COMMENT", "WS" ]

    RULE_styleSheet = 0
    RULE_variable = 1
    RULE_variableDef = 2
    RULE_metadata = 3
    RULE_stylingRuleName = 4
    RULE_stylingRuleList = 5
    RULE_stylingRule = 6
    RULE_selector = 7
    RULE_idOrConstant = 8
    RULE_tuple = 9
    RULE_expression = 10
    RULE_expConstant = 11
    RULE_expString = 12
    RULE_expInstance = 13
    RULE_lhValue = 14
    RULE_propertyAssignment = 15
    RULE_propertyAssignmentList = 16
    RULE_propertyAssignmentInferred = 17
    RULE_propertyAssignmentInferredList = 18
    RULE_expArray = 19
    RULE_arrayElements = 20
    RULE_expCall = 21
    RULE_arguments = 22
    RULE_binaryLogicalOperator = 23
    RULE_unaryLogicalOperator = 24
    RULE_unaryArithmeticOperator = 25
    RULE_arithmeticOperatorExp = 26
    RULE_arithmeticOperatorMul = 27
    RULE_arithmeticOperatorAdd = 28
    RULE_relationalOperator = 29
    RULE_betweenOperator = 30

    ruleNames =  [ "styleSheet", "variable", "variableDef", "metadata", 
                   "stylingRuleName", "stylingRuleList", "stylingRule", 
                   "selector", "idOrConstant", "tuple", "expression", "expConstant", 
                   "expString", "expInstance", "lhValue", "propertyAssignment", 
                   "propertyAssignmentList", "propertyAssignmentInferred", 
                   "propertyAssignmentInferredList", "expArray", "arrayElements", 
                   "expCall", "arguments", "binaryLogicalOperator", "unaryLogicalOperator", 
                   "unaryArithmeticOperator", "arithmeticOperatorExp", "arithmeticOperatorMul", 
                   "arithmeticOperatorAdd", "relationalOperator", "betweenOperator" ]

    EOF = Token.EOF
    LCBR=1
    RCBR=2
    DOT=3
    SEMI=4
    LSBR=5
    RSBR=6
    LPAR=7
    RPAR=8
    COMMA=9
    EQ=10
    LT=11
    LTEQ=12
    GT=13
    GTEQ=14
    IN=15
    NOT=16
    IS=17
    LIKE=18
    BETWEEN=19
    QUESTION=20
    COLON=21
    AND=22
    OR=23
    MUL=24
    DIV=25
    IDIV=26
    MOD=27
    POW=28
    MINUS=29
    PLUS=30
    UNIT=31
    HEX_LITERAL=32
    NUMERIC_LITERAL=33
    CHARACTER_LITERAL=34
    IDENTIFIER=35
    AT_SIGN=36
    COMMENT=37
    LINE_COMMENT=38
    WS=39

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class StyleSheetContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def metadata(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CartoSymCSSGrammar.MetadataContext)
            else:
                return self.getTypedRuleContext(CartoSymCSSGrammar.MetadataContext,i)


        def variableDef(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CartoSymCSSGrammar.VariableDefContext)
            else:
                return self.getTypedRuleContext(CartoSymCSSGrammar.VariableDefContext,i)


        def stylingRuleList(self):
            return self.getTypedRuleContext(CartoSymCSSGrammar.StylingRuleListContext,0)


        def getRuleIndex(self):
            return CartoSymCSSGrammar.RULE_styleSheet

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStyleSheet" ):
                listener.enterStyleSheet(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStyleSheet" ):
                listener.exitStyleSheet(self)




    def styleSheet(self):

        localctx = CartoSymCSSGrammar.StyleSheetContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_styleSheet)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 65
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==3:
                self.state = 62
                self.metadata()
                self.state = 67
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 71
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==36:
                self.state = 68
                self.variableDef()
                self.state = 73
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 75
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 34359738402) != 0):
                self.state = 74
                self.stylingRuleList(0)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class VariableContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def AT_SIGN(self):
            return self.getToken(CartoSymCSSGrammar.AT_SIGN, 0)

        def IDENTIFIER(self):
            return self.getToken(CartoSymCSSGrammar.IDENTIFIER, 0)

        def getRuleIndex(self):
            return CartoSymCSSGrammar.RULE_variable

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterVariable" ):
                listener.enterVariable(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitVariable" ):
                listener.exitVariable(self)




    def variable(self):

        localctx = CartoSymCSSGrammar.VariableContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_variable)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 77
            self.match(CartoSymCSSGrammar.AT_SIGN)
            self.state = 78
            self.match(CartoSymCSSGrammar.IDENTIFIER)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class VariableDefContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def variable(self):
            return self.getTypedRuleContext(CartoSymCSSGrammar.VariableContext,0)


        def EQ(self):
            return self.getToken(CartoSymCSSGrammar.EQ, 0)

        def expression(self):
            return self.getTypedRuleContext(CartoSymCSSGrammar.ExpressionContext,0)


        def SEMI(self):
            return self.getToken(CartoSymCSSGrammar.SEMI, 0)

        def getRuleIndex(self):
            return CartoSymCSSGrammar.RULE_variableDef

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterVariableDef" ):
                listener.enterVariableDef(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitVariableDef" ):
                listener.exitVariableDef(self)




    def variableDef(self):

        localctx = CartoSymCSSGrammar.VariableDefContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_variableDef)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 80
            self.variable()
            self.state = 81
            self.match(CartoSymCSSGrammar.EQ)
            self.state = 82
            self.expression(0)
            self.state = 83
            self.match(CartoSymCSSGrammar.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class MetadataContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def DOT(self):
            return self.getToken(CartoSymCSSGrammar.DOT, 0)

        def IDENTIFIER(self):
            return self.getToken(CartoSymCSSGrammar.IDENTIFIER, 0)

        def CHARACTER_LITERAL(self):
            return self.getToken(CartoSymCSSGrammar.CHARACTER_LITERAL, 0)

        def getRuleIndex(self):
            return CartoSymCSSGrammar.RULE_metadata

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMetadata" ):
                listener.enterMetadata(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMetadata" ):
                listener.exitMetadata(self)




    def metadata(self):

        localctx = CartoSymCSSGrammar.MetadataContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_metadata)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 85
            self.match(CartoSymCSSGrammar.DOT)
            self.state = 86
            self.match(CartoSymCSSGrammar.IDENTIFIER)
            self.state = 87
            self.match(CartoSymCSSGrammar.CHARACTER_LITERAL)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StylingRuleNameContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def DOT(self):
            return self.getToken(CartoSymCSSGrammar.DOT, 0)

        def IDENTIFIER(self):
            return self.getToken(CartoSymCSSGrammar.IDENTIFIER, 0)

        def CHARACTER_LITERAL(self):
            return self.getToken(CartoSymCSSGrammar.CHARACTER_LITERAL, 0)

        def getRuleIndex(self):
            return CartoSymCSSGrammar.RULE_stylingRuleName

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStylingRuleName" ):
                listener.enterStylingRuleName(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStylingRuleName" ):
                listener.exitStylingRuleName(self)




    def stylingRuleName(self):

        localctx = CartoSymCSSGrammar.StylingRuleNameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_stylingRuleName)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 89
            self.match(CartoSymCSSGrammar.DOT)
            self.state = 90
            self.match(CartoSymCSSGrammar.IDENTIFIER)
            self.state = 91
            self.match(CartoSymCSSGrammar.CHARACTER_LITERAL)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StylingRuleListContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def stylingRule(self):
            return self.getTypedRuleContext(CartoSymCSSGrammar.StylingRuleContext,0)


        def stylingRuleList(self):
            return self.getTypedRuleContext(CartoSymCSSGrammar.StylingRuleListContext,0)


        def getRuleIndex(self):
            return CartoSymCSSGrammar.RULE_stylingRuleList

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStylingRuleList" ):
                listener.enterStylingRuleList(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStylingRuleList" ):
                listener.exitStylingRuleList(self)



    def stylingRuleList(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = CartoSymCSSGrammar.StylingRuleListContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 10
        self.enterRecursionRule(localctx, 10, self.RULE_stylingRuleList, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 94
            self.stylingRule()
            self._ctx.stop = self._input.LT(-1)
            self.state = 100
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,3,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    localctx = CartoSymCSSGrammar.StylingRuleListContext(self, _parentctx, _parentState)
                    self.pushNewRecursionContext(localctx, _startState, self.RULE_stylingRuleList)
                    self.state = 96
                    if not self.precpred(self._ctx, 1):
                        from antlr4.error.Errors import FailedPredicateException
                        raise FailedPredicateException(self, "self.precpred(self._ctx, 1)")
                    self.state = 97
                    self.stylingRule() 
                self.state = 102
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,3,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class StylingRuleContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LCBR(self):
            return self.getToken(CartoSymCSSGrammar.LCBR, 0)

        def RCBR(self):
            return self.getToken(CartoSymCSSGrammar.RCBR, 0)

        def selector(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CartoSymCSSGrammar.SelectorContext)
            else:
                return self.getTypedRuleContext(CartoSymCSSGrammar.SelectorContext,i)


        def stylingRuleName(self):
            return self.getTypedRuleContext(CartoSymCSSGrammar.StylingRuleNameContext,0)


        def propertyAssignmentList(self):
            return self.getTypedRuleContext(CartoSymCSSGrammar.PropertyAssignmentListContext,0)


        def SEMI(self):
            return self.getToken(CartoSymCSSGrammar.SEMI, 0)

        def stylingRuleList(self):
            return self.getTypedRuleContext(CartoSymCSSGrammar.StylingRuleListContext,0)


        def getRuleIndex(self):
            return CartoSymCSSGrammar.RULE_stylingRule

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStylingRule" ):
                listener.enterStylingRule(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStylingRule" ):
                listener.exitStylingRule(self)




    def stylingRule(self):

        localctx = CartoSymCSSGrammar.StylingRuleContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_stylingRule)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 106
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==5 or _la==35:
                self.state = 103
                self.selector()
                self.state = 108
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 109
            self.match(CartoSymCSSGrammar.LCBR)
            self.state = 111
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==3:
                self.state = 110
                self.stylingRuleName()


            self.state = 116
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,6,self._ctx)
            if la_ == 1:
                self.state = 113
                self.propertyAssignmentList(0)
                self.state = 114
                self.match(CartoSymCSSGrammar.SEMI)


            self.state = 119
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 34359738402) != 0):
                self.state = 118
                self.stylingRuleList(0)


            self.state = 121
            self.match(CartoSymCSSGrammar.RCBR)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SelectorContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENTIFIER(self):
            return self.getToken(CartoSymCSSGrammar.IDENTIFIER, 0)

        def LSBR(self):
            return self.getToken(CartoSymCSSGrammar.LSBR, 0)

        def expression(self):
            return self.getTypedRuleContext(CartoSymCSSGrammar.ExpressionContext,0)


        def RSBR(self):
            return self.getToken(CartoSymCSSGrammar.RSBR, 0)

        def getRuleIndex(self):
            return CartoSymCSSGrammar.RULE_selector

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSelector" ):
                listener.enterSelector(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSelector" ):
                listener.exitSelector(self)




    def selector(self):

        localctx = CartoSymCSSGrammar.SelectorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_selector)
        try:
            self.state = 128
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [35]:
                self.enterOuterAlt(localctx, 1)
                self.state = 123
                self.match(CartoSymCSSGrammar.IDENTIFIER)
                pass
            elif token in [5]:
                self.enterOuterAlt(localctx, 2)
                self.state = 124
                self.match(CartoSymCSSGrammar.LSBR)
                self.state = 125
                self.expression(0)
                self.state = 126
                self.match(CartoSymCSSGrammar.RSBR)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class IdOrConstantContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENTIFIER(self):
            return self.getToken(CartoSymCSSGrammar.IDENTIFIER, 0)

        def expConstant(self):
            return self.getTypedRuleContext(CartoSymCSSGrammar.ExpConstantContext,0)


        def getRuleIndex(self):
            return CartoSymCSSGrammar.RULE_idOrConstant

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIdOrConstant" ):
                listener.enterIdOrConstant(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIdOrConstant" ):
                listener.exitIdOrConstant(self)




    def idOrConstant(self):

        localctx = CartoSymCSSGrammar.IdOrConstantContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_idOrConstant)
        try:
            self.state = 132
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [35]:
                self.enterOuterAlt(localctx, 1)
                self.state = 130
                self.match(CartoSymCSSGrammar.IDENTIFIER)
                pass
            elif token in [32, 33]:
                self.enterOuterAlt(localctx, 2)
                self.state = 131
                self.expConstant()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TupleContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def idOrConstant(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CartoSymCSSGrammar.IdOrConstantContext)
            else:
                return self.getTypedRuleContext(CartoSymCSSGrammar.IdOrConstantContext,i)


        def tuple_(self):
            return self.getTypedRuleContext(CartoSymCSSGrammar.TupleContext,0)


        def getRuleIndex(self):
            return CartoSymCSSGrammar.RULE_tuple

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTuple" ):
                listener.enterTuple(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTuple" ):
                listener.exitTuple(self)



    def tuple_(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = CartoSymCSSGrammar.TupleContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 18
        self.enterRecursionRule(localctx, 18, self.RULE_tuple, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 135
            self.idOrConstant()
            self.state = 136
            self.idOrConstant()
            self._ctx.stop = self._input.LT(-1)
            self.state = 142
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,10,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    localctx = CartoSymCSSGrammar.TupleContext(self, _parentctx, _parentState)
                    self.pushNewRecursionContext(localctx, _startState, self.RULE_tuple)
                    self.state = 138
                    if not self.precpred(self._ctx, 1):
                        from antlr4.error.Errors import FailedPredicateException
                        raise FailedPredicateException(self, "self.precpred(self._ctx, 1)")
                    self.state = 139
                    self.idOrConstant() 
                self.state = 144
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,10,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class ExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def idOrConstant(self):
            return self.getTypedRuleContext(CartoSymCSSGrammar.IdOrConstantContext,0)


        def expString(self):
            return self.getTypedRuleContext(CartoSymCSSGrammar.ExpStringContext,0)


        def expCall(self):
            return self.getTypedRuleContext(CartoSymCSSGrammar.ExpCallContext,0)


        def expArray(self):
            return self.getTypedRuleContext(CartoSymCSSGrammar.ExpArrayContext,0)


        def expInstance(self):
            return self.getTypedRuleContext(CartoSymCSSGrammar.ExpInstanceContext,0)


        def LPAR(self):
            return self.getToken(CartoSymCSSGrammar.LPAR, 0)

        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CartoSymCSSGrammar.ExpressionContext)
            else:
                return self.getTypedRuleContext(CartoSymCSSGrammar.ExpressionContext,i)


        def RPAR(self):
            return self.getToken(CartoSymCSSGrammar.RPAR, 0)

        def unaryLogicalOperator(self):
            return self.getTypedRuleContext(CartoSymCSSGrammar.UnaryLogicalOperatorContext,0)


        def unaryArithmeticOperator(self):
            return self.getTypedRuleContext(CartoSymCSSGrammar.UnaryArithmeticOperatorContext,0)


        def tuple_(self):
            return self.getTypedRuleContext(CartoSymCSSGrammar.TupleContext,0)


        def variable(self):
            return self.getTypedRuleContext(CartoSymCSSGrammar.VariableContext,0)


        def arithmeticOperatorExp(self):
            return self.getTypedRuleContext(CartoSymCSSGrammar.ArithmeticOperatorExpContext,0)


        def arithmeticOperatorMul(self):
            return self.getTypedRuleContext(CartoSymCSSGrammar.ArithmeticOperatorMulContext,0)


        def arithmeticOperatorAdd(self):
            return self.getTypedRuleContext(CartoSymCSSGrammar.ArithmeticOperatorAddContext,0)


        def binaryLogicalOperator(self):
            return self.getTypedRuleContext(CartoSymCSSGrammar.BinaryLogicalOperatorContext,0)


        def relationalOperator(self):
            return self.getTypedRuleContext(CartoSymCSSGrammar.RelationalOperatorContext,0)


        def betweenOperator(self):
            return self.getTypedRuleContext(CartoSymCSSGrammar.BetweenOperatorContext,0)


        def AND(self):
            return self.getToken(CartoSymCSSGrammar.AND, 0)

        def QUESTION(self):
            return self.getToken(CartoSymCSSGrammar.QUESTION, 0)

        def COLON(self):
            return self.getToken(CartoSymCSSGrammar.COLON, 0)

        def DOT(self):
            return self.getToken(CartoSymCSSGrammar.DOT, 0)

        def IDENTIFIER(self):
            return self.getToken(CartoSymCSSGrammar.IDENTIFIER, 0)

        def LSBR(self):
            return self.getToken(CartoSymCSSGrammar.LSBR, 0)

        def expConstant(self):
            return self.getTypedRuleContext(CartoSymCSSGrammar.ExpConstantContext,0)


        def RSBR(self):
            return self.getToken(CartoSymCSSGrammar.RSBR, 0)

        def getRuleIndex(self):
            return CartoSymCSSGrammar.RULE_expression

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExpression" ):
                listener.enterExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExpression" ):
                listener.exitExpression(self)



    def expression(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = CartoSymCSSGrammar.ExpressionContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 20
        self.enterRecursionRule(localctx, 20, self.RULE_expression, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 163
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,11,self._ctx)
            if la_ == 1:
                self.state = 146
                self.idOrConstant()
                pass

            elif la_ == 2:
                self.state = 147
                self.expString()
                pass

            elif la_ == 3:
                self.state = 148
                self.expCall()
                pass

            elif la_ == 4:
                self.state = 149
                self.expArray()
                pass

            elif la_ == 5:
                self.state = 150
                self.expInstance()
                pass

            elif la_ == 6:
                self.state = 151
                self.match(CartoSymCSSGrammar.LPAR)
                self.state = 152
                self.expression(0)
                self.state = 153
                self.match(CartoSymCSSGrammar.RPAR)
                pass

            elif la_ == 7:
                self.state = 155
                self.unaryLogicalOperator()
                self.state = 156
                self.expression(4)
                pass

            elif la_ == 8:
                self.state = 158
                self.unaryArithmeticOperator()
                self.state = 159
                self.expression(3)
                pass

            elif la_ == 9:
                self.state = 161
                self.tuple_(0)
                pass

            elif la_ == 10:
                self.state = 162
                self.variable()
                pass


            self._ctx.stop = self._input.LT(-1)
            self.state = 207
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,13,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 205
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,12,self._ctx)
                    if la_ == 1:
                        localctx = CartoSymCSSGrammar.ExpressionContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expression)
                        self.state = 165
                        if not self.precpred(self._ctx, 11):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 11)")
                        self.state = 166
                        self.arithmeticOperatorExp()
                        self.state = 167
                        self.expression(12)
                        pass

                    elif la_ == 2:
                        localctx = CartoSymCSSGrammar.ExpressionContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expression)
                        self.state = 169
                        if not self.precpred(self._ctx, 10):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 10)")
                        self.state = 170
                        self.arithmeticOperatorMul()
                        self.state = 171
                        self.expression(11)
                        pass

                    elif la_ == 3:
                        localctx = CartoSymCSSGrammar.ExpressionContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expression)
                        self.state = 173
                        if not self.precpred(self._ctx, 9):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 9)")
                        self.state = 174
                        self.arithmeticOperatorAdd()
                        self.state = 175
                        self.expression(10)
                        pass

                    elif la_ == 4:
                        localctx = CartoSymCSSGrammar.ExpressionContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expression)
                        self.state = 177
                        if not self.precpred(self._ctx, 8):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 8)")
                        self.state = 178
                        self.binaryLogicalOperator()
                        self.state = 179
                        self.expression(9)
                        pass

                    elif la_ == 5:
                        localctx = CartoSymCSSGrammar.ExpressionContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expression)
                        self.state = 181
                        if not self.precpred(self._ctx, 7):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 7)")
                        self.state = 182
                        self.relationalOperator()
                        self.state = 183
                        self.expression(8)
                        pass

                    elif la_ == 6:
                        localctx = CartoSymCSSGrammar.ExpressionContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expression)
                        self.state = 185
                        if not self.precpred(self._ctx, 6):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 6)")
                        self.state = 186
                        self.betweenOperator()
                        self.state = 187
                        self.expression(0)
                        self.state = 188
                        self.match(CartoSymCSSGrammar.AND)
                        self.state = 189
                        self.expression(7)
                        pass

                    elif la_ == 7:
                        localctx = CartoSymCSSGrammar.ExpressionContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expression)
                        self.state = 191
                        if not self.precpred(self._ctx, 5):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 5)")
                        self.state = 192
                        self.match(CartoSymCSSGrammar.QUESTION)
                        self.state = 193
                        self.expression(0)
                        self.state = 194
                        self.match(CartoSymCSSGrammar.COLON)
                        self.state = 195
                        self.expression(6)
                        pass

                    elif la_ == 8:
                        localctx = CartoSymCSSGrammar.ExpressionContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expression)
                        self.state = 197
                        if not self.precpred(self._ctx, 18):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 18)")
                        self.state = 198
                        self.match(CartoSymCSSGrammar.DOT)
                        self.state = 199
                        self.match(CartoSymCSSGrammar.IDENTIFIER)
                        pass

                    elif la_ == 9:
                        localctx = CartoSymCSSGrammar.ExpressionContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expression)
                        self.state = 200
                        if not self.precpred(self._ctx, 12):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 12)")
                        self.state = 201
                        self.match(CartoSymCSSGrammar.LSBR)
                        self.state = 202
                        self.expConstant()
                        self.state = 203
                        self.match(CartoSymCSSGrammar.RSBR)
                        pass

             
                self.state = 209
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,13,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class ExpConstantContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def NUMERIC_LITERAL(self):
            return self.getToken(CartoSymCSSGrammar.NUMERIC_LITERAL, 0)

        def UNIT(self):
            return self.getToken(CartoSymCSSGrammar.UNIT, 0)

        def HEX_LITERAL(self):
            return self.getToken(CartoSymCSSGrammar.HEX_LITERAL, 0)

        def getRuleIndex(self):
            return CartoSymCSSGrammar.RULE_expConstant

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExpConstant" ):
                listener.enterExpConstant(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExpConstant" ):
                listener.exitExpConstant(self)




    def expConstant(self):

        localctx = CartoSymCSSGrammar.ExpConstantContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_expConstant)
        try:
            self.state = 215
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [33]:
                self.enterOuterAlt(localctx, 1)
                self.state = 210
                self.match(CartoSymCSSGrammar.NUMERIC_LITERAL)
                self.state = 212
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,14,self._ctx)
                if la_ == 1:
                    self.state = 211
                    self.match(CartoSymCSSGrammar.UNIT)


                pass
            elif token in [32]:
                self.enterOuterAlt(localctx, 2)
                self.state = 214
                self.match(CartoSymCSSGrammar.HEX_LITERAL)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExpStringContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def CHARACTER_LITERAL(self):
            return self.getToken(CartoSymCSSGrammar.CHARACTER_LITERAL, 0)

        def getRuleIndex(self):
            return CartoSymCSSGrammar.RULE_expString

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExpString" ):
                listener.enterExpString(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExpString" ):
                listener.exitExpString(self)




    def expString(self):

        localctx = CartoSymCSSGrammar.ExpStringContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_expString)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 217
            self.match(CartoSymCSSGrammar.CHARACTER_LITERAL)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExpInstanceContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LCBR(self):
            return self.getToken(CartoSymCSSGrammar.LCBR, 0)

        def RCBR(self):
            return self.getToken(CartoSymCSSGrammar.RCBR, 0)

        def IDENTIFIER(self):
            return self.getToken(CartoSymCSSGrammar.IDENTIFIER, 0)

        def propertyAssignmentInferredList(self):
            return self.getTypedRuleContext(CartoSymCSSGrammar.PropertyAssignmentInferredListContext,0)


        def SEMI(self):
            return self.getToken(CartoSymCSSGrammar.SEMI, 0)

        def LPAR(self):
            return self.getToken(CartoSymCSSGrammar.LPAR, 0)

        def RPAR(self):
            return self.getToken(CartoSymCSSGrammar.RPAR, 0)

        def getRuleIndex(self):
            return CartoSymCSSGrammar.RULE_expInstance

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExpInstance" ):
                listener.enterExpInstance(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExpInstance" ):
                listener.exitExpInstance(self)




    def expInstance(self):

        localctx = CartoSymCSSGrammar.ExpInstanceContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_expInstance)
        self._la = 0 # Token type
        try:
            self.state = 239
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,21,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 220
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==35:
                    self.state = 219
                    self.match(CartoSymCSSGrammar.IDENTIFIER)


                self.state = 222
                self.match(CartoSymCSSGrammar.LCBR)
                self.state = 224
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 134754664610) != 0):
                    self.state = 223
                    self.propertyAssignmentInferredList(0)


                self.state = 227
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==4:
                    self.state = 226
                    self.match(CartoSymCSSGrammar.SEMI)


                self.state = 229
                self.match(CartoSymCSSGrammar.RCBR)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 230
                self.match(CartoSymCSSGrammar.IDENTIFIER)
                self.state = 231
                self.match(CartoSymCSSGrammar.LPAR)
                self.state = 233
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 134754664610) != 0):
                    self.state = 232
                    self.propertyAssignmentInferredList(0)


                self.state = 236
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==4:
                    self.state = 235
                    self.match(CartoSymCSSGrammar.SEMI)


                self.state = 238
                self.match(CartoSymCSSGrammar.RPAR)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class LhValueContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENTIFIER(self):
            return self.getToken(CartoSymCSSGrammar.IDENTIFIER, 0)

        def lhValue(self):
            return self.getTypedRuleContext(CartoSymCSSGrammar.LhValueContext,0)


        def DOT(self):
            return self.getToken(CartoSymCSSGrammar.DOT, 0)

        def LSBR(self):
            return self.getToken(CartoSymCSSGrammar.LSBR, 0)

        def expConstant(self):
            return self.getTypedRuleContext(CartoSymCSSGrammar.ExpConstantContext,0)


        def RSBR(self):
            return self.getToken(CartoSymCSSGrammar.RSBR, 0)

        def getRuleIndex(self):
            return CartoSymCSSGrammar.RULE_lhValue

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLhValue" ):
                listener.enterLhValue(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLhValue" ):
                listener.exitLhValue(self)



    def lhValue(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = CartoSymCSSGrammar.LhValueContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 28
        self.enterRecursionRule(localctx, 28, self.RULE_lhValue, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 242
            self.match(CartoSymCSSGrammar.IDENTIFIER)
            self._ctx.stop = self._input.LT(-1)
            self.state = 254
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,23,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 252
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,22,self._ctx)
                    if la_ == 1:
                        localctx = CartoSymCSSGrammar.LhValueContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_lhValue)
                        self.state = 244
                        if not self.precpred(self._ctx, 2):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 2)")
                        self.state = 245
                        self.match(CartoSymCSSGrammar.DOT)
                        self.state = 246
                        self.match(CartoSymCSSGrammar.IDENTIFIER)
                        pass

                    elif la_ == 2:
                        localctx = CartoSymCSSGrammar.LhValueContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_lhValue)
                        self.state = 247
                        if not self.precpred(self._ctx, 1):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 1)")
                        self.state = 248
                        self.match(CartoSymCSSGrammar.LSBR)
                        self.state = 249
                        self.expConstant()
                        self.state = 250
                        self.match(CartoSymCSSGrammar.RSBR)
                        pass

             
                self.state = 256
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,23,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class PropertyAssignmentContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def lhValue(self):
            return self.getTypedRuleContext(CartoSymCSSGrammar.LhValueContext,0)


        def COLON(self):
            return self.getToken(CartoSymCSSGrammar.COLON, 0)

        def expression(self):
            return self.getTypedRuleContext(CartoSymCSSGrammar.ExpressionContext,0)


        def getRuleIndex(self):
            return CartoSymCSSGrammar.RULE_propertyAssignment

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPropertyAssignment" ):
                listener.enterPropertyAssignment(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPropertyAssignment" ):
                listener.exitPropertyAssignment(self)




    def propertyAssignment(self):

        localctx = CartoSymCSSGrammar.PropertyAssignmentContext(self, self._ctx, self.state)
        self.enterRule(localctx, 30, self.RULE_propertyAssignment)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 257
            self.lhValue(0)
            self.state = 258
            self.match(CartoSymCSSGrammar.COLON)
            self.state = 259
            self.expression(0)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PropertyAssignmentListContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def propertyAssignment(self):
            return self.getTypedRuleContext(CartoSymCSSGrammar.PropertyAssignmentContext,0)


        def propertyAssignmentList(self):
            return self.getTypedRuleContext(CartoSymCSSGrammar.PropertyAssignmentListContext,0)


        def SEMI(self):
            return self.getToken(CartoSymCSSGrammar.SEMI, 0)

        def getRuleIndex(self):
            return CartoSymCSSGrammar.RULE_propertyAssignmentList

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPropertyAssignmentList" ):
                listener.enterPropertyAssignmentList(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPropertyAssignmentList" ):
                listener.exitPropertyAssignmentList(self)



    def propertyAssignmentList(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = CartoSymCSSGrammar.PropertyAssignmentListContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 32
        self.enterRecursionRule(localctx, 32, self.RULE_propertyAssignmentList, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 262
            self.propertyAssignment()
            self._ctx.stop = self._input.LT(-1)
            self.state = 269
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,24,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    localctx = CartoSymCSSGrammar.PropertyAssignmentListContext(self, _parentctx, _parentState)
                    self.pushNewRecursionContext(localctx, _startState, self.RULE_propertyAssignmentList)
                    self.state = 264
                    if not self.precpred(self._ctx, 1):
                        from antlr4.error.Errors import FailedPredicateException
                        raise FailedPredicateException(self, "self.precpred(self._ctx, 1)")
                    self.state = 265
                    self.match(CartoSymCSSGrammar.SEMI)
                    self.state = 266
                    self.propertyAssignment() 
                self.state = 271
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,24,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class PropertyAssignmentInferredContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def propertyAssignment(self):
            return self.getTypedRuleContext(CartoSymCSSGrammar.PropertyAssignmentContext,0)


        def expression(self):
            return self.getTypedRuleContext(CartoSymCSSGrammar.ExpressionContext,0)


        def getRuleIndex(self):
            return CartoSymCSSGrammar.RULE_propertyAssignmentInferred

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPropertyAssignmentInferred" ):
                listener.enterPropertyAssignmentInferred(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPropertyAssignmentInferred" ):
                listener.exitPropertyAssignmentInferred(self)




    def propertyAssignmentInferred(self):

        localctx = CartoSymCSSGrammar.PropertyAssignmentInferredContext(self, self._ctx, self.state)
        self.enterRule(localctx, 34, self.RULE_propertyAssignmentInferred)
        try:
            self.state = 274
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,25,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 272
                self.propertyAssignment()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 273
                self.expression(0)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PropertyAssignmentInferredListContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def propertyAssignmentInferred(self):
            return self.getTypedRuleContext(CartoSymCSSGrammar.PropertyAssignmentInferredContext,0)


        def propertyAssignmentInferredList(self):
            return self.getTypedRuleContext(CartoSymCSSGrammar.PropertyAssignmentInferredListContext,0)


        def SEMI(self):
            return self.getToken(CartoSymCSSGrammar.SEMI, 0)

        def COMMA(self):
            return self.getToken(CartoSymCSSGrammar.COMMA, 0)

        def getRuleIndex(self):
            return CartoSymCSSGrammar.RULE_propertyAssignmentInferredList

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPropertyAssignmentInferredList" ):
                listener.enterPropertyAssignmentInferredList(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPropertyAssignmentInferredList" ):
                listener.exitPropertyAssignmentInferredList(self)



    def propertyAssignmentInferredList(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = CartoSymCSSGrammar.PropertyAssignmentInferredListContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 36
        self.enterRecursionRule(localctx, 36, self.RULE_propertyAssignmentInferredList, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 277
            self.propertyAssignmentInferred()
            self._ctx.stop = self._input.LT(-1)
            self.state = 287
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,27,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 285
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,26,self._ctx)
                    if la_ == 1:
                        localctx = CartoSymCSSGrammar.PropertyAssignmentInferredListContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_propertyAssignmentInferredList)
                        self.state = 279
                        if not self.precpred(self._ctx, 2):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 2)")
                        self.state = 280
                        self.match(CartoSymCSSGrammar.SEMI)
                        self.state = 281
                        self.propertyAssignmentInferred()
                        pass

                    elif la_ == 2:
                        localctx = CartoSymCSSGrammar.PropertyAssignmentInferredListContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_propertyAssignmentInferredList)
                        self.state = 282
                        if not self.precpred(self._ctx, 1):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 1)")
                        self.state = 283
                        self.match(CartoSymCSSGrammar.COMMA)
                        self.state = 284
                        self.propertyAssignmentInferred()
                        pass

             
                self.state = 289
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,27,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class ExpArrayContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LSBR(self):
            return self.getToken(CartoSymCSSGrammar.LSBR, 0)

        def RSBR(self):
            return self.getToken(CartoSymCSSGrammar.RSBR, 0)

        def arrayElements(self):
            return self.getTypedRuleContext(CartoSymCSSGrammar.ArrayElementsContext,0)


        def LPAR(self):
            return self.getToken(CartoSymCSSGrammar.LPAR, 0)

        def RPAR(self):
            return self.getToken(CartoSymCSSGrammar.RPAR, 0)

        def getRuleIndex(self):
            return CartoSymCSSGrammar.RULE_expArray

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExpArray" ):
                listener.enterExpArray(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExpArray" ):
                listener.exitExpArray(self)




    def expArray(self):

        localctx = CartoSymCSSGrammar.ExpArrayContext(self, self._ctx, self.state)
        self.enterRule(localctx, 38, self.RULE_expArray)
        self._la = 0 # Token type
        try:
            self.state = 300
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [5]:
                self.enterOuterAlt(localctx, 1)
                self.state = 290
                self.match(CartoSymCSSGrammar.LSBR)
                self.state = 292
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 134754664610) != 0):
                    self.state = 291
                    self.arrayElements(0)


                self.state = 294
                self.match(CartoSymCSSGrammar.RSBR)
                pass
            elif token in [7]:
                self.enterOuterAlt(localctx, 2)
                self.state = 295
                self.match(CartoSymCSSGrammar.LPAR)
                self.state = 297
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 134754664610) != 0):
                    self.state = 296
                    self.arrayElements(0)


                self.state = 299
                self.match(CartoSymCSSGrammar.RPAR)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ArrayElementsContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expression(self):
            return self.getTypedRuleContext(CartoSymCSSGrammar.ExpressionContext,0)


        def arrayElements(self):
            return self.getTypedRuleContext(CartoSymCSSGrammar.ArrayElementsContext,0)


        def COMMA(self):
            return self.getToken(CartoSymCSSGrammar.COMMA, 0)

        def getRuleIndex(self):
            return CartoSymCSSGrammar.RULE_arrayElements

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterArrayElements" ):
                listener.enterArrayElements(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitArrayElements" ):
                listener.exitArrayElements(self)



    def arrayElements(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = CartoSymCSSGrammar.ArrayElementsContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 40
        self.enterRecursionRule(localctx, 40, self.RULE_arrayElements, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 303
            self.expression(0)
            self._ctx.stop = self._input.LT(-1)
            self.state = 310
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,31,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    localctx = CartoSymCSSGrammar.ArrayElementsContext(self, _parentctx, _parentState)
                    self.pushNewRecursionContext(localctx, _startState, self.RULE_arrayElements)
                    self.state = 305
                    if not self.precpred(self._ctx, 1):
                        from antlr4.error.Errors import FailedPredicateException
                        raise FailedPredicateException(self, "self.precpred(self._ctx, 1)")
                    self.state = 306
                    self.match(CartoSymCSSGrammar.COMMA)
                    self.state = 307
                    self.expression(0) 
                self.state = 312
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,31,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class ExpCallContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENTIFIER(self):
            return self.getToken(CartoSymCSSGrammar.IDENTIFIER, 0)

        def LPAR(self):
            return self.getToken(CartoSymCSSGrammar.LPAR, 0)

        def arguments(self):
            return self.getTypedRuleContext(CartoSymCSSGrammar.ArgumentsContext,0)


        def RPAR(self):
            return self.getToken(CartoSymCSSGrammar.RPAR, 0)

        def getRuleIndex(self):
            return CartoSymCSSGrammar.RULE_expCall

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExpCall" ):
                listener.enterExpCall(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExpCall" ):
                listener.exitExpCall(self)




    def expCall(self):

        localctx = CartoSymCSSGrammar.ExpCallContext(self, self._ctx, self.state)
        self.enterRule(localctx, 42, self.RULE_expCall)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 313
            self.match(CartoSymCSSGrammar.IDENTIFIER)
            self.state = 314
            self.match(CartoSymCSSGrammar.LPAR)
            self.state = 315
            self.arguments(0)
            self.state = 316
            self.match(CartoSymCSSGrammar.RPAR)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ArgumentsContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expression(self):
            return self.getTypedRuleContext(CartoSymCSSGrammar.ExpressionContext,0)


        def arguments(self):
            return self.getTypedRuleContext(CartoSymCSSGrammar.ArgumentsContext,0)


        def COMMA(self):
            return self.getToken(CartoSymCSSGrammar.COMMA, 0)

        def getRuleIndex(self):
            return CartoSymCSSGrammar.RULE_arguments

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterArguments" ):
                listener.enterArguments(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitArguments" ):
                listener.exitArguments(self)



    def arguments(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = CartoSymCSSGrammar.ArgumentsContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 44
        self.enterRecursionRule(localctx, 44, self.RULE_arguments, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 319
            self.expression(0)
            self._ctx.stop = self._input.LT(-1)
            self.state = 326
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,32,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    localctx = CartoSymCSSGrammar.ArgumentsContext(self, _parentctx, _parentState)
                    self.pushNewRecursionContext(localctx, _startState, self.RULE_arguments)
                    self.state = 321
                    if not self.precpred(self._ctx, 1):
                        from antlr4.error.Errors import FailedPredicateException
                        raise FailedPredicateException(self, "self.precpred(self._ctx, 1)")
                    self.state = 322
                    self.match(CartoSymCSSGrammar.COMMA)
                    self.state = 323
                    self.expression(0) 
                self.state = 328
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,32,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class BinaryLogicalOperatorContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def AND(self):
            return self.getToken(CartoSymCSSGrammar.AND, 0)

        def OR(self):
            return self.getToken(CartoSymCSSGrammar.OR, 0)

        def getRuleIndex(self):
            return CartoSymCSSGrammar.RULE_binaryLogicalOperator

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBinaryLogicalOperator" ):
                listener.enterBinaryLogicalOperator(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBinaryLogicalOperator" ):
                listener.exitBinaryLogicalOperator(self)




    def binaryLogicalOperator(self):

        localctx = CartoSymCSSGrammar.BinaryLogicalOperatorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 46, self.RULE_binaryLogicalOperator)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 329
            _la = self._input.LA(1)
            if not(_la==22 or _la==23):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class UnaryLogicalOperatorContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def NOT(self):
            return self.getToken(CartoSymCSSGrammar.NOT, 0)

        def getRuleIndex(self):
            return CartoSymCSSGrammar.RULE_unaryLogicalOperator

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterUnaryLogicalOperator" ):
                listener.enterUnaryLogicalOperator(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitUnaryLogicalOperator" ):
                listener.exitUnaryLogicalOperator(self)




    def unaryLogicalOperator(self):

        localctx = CartoSymCSSGrammar.UnaryLogicalOperatorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 48, self.RULE_unaryLogicalOperator)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 331
            self.match(CartoSymCSSGrammar.NOT)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class UnaryArithmeticOperatorContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def PLUS(self):
            return self.getToken(CartoSymCSSGrammar.PLUS, 0)

        def MINUS(self):
            return self.getToken(CartoSymCSSGrammar.MINUS, 0)

        def getRuleIndex(self):
            return CartoSymCSSGrammar.RULE_unaryArithmeticOperator

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterUnaryArithmeticOperator" ):
                listener.enterUnaryArithmeticOperator(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitUnaryArithmeticOperator" ):
                listener.exitUnaryArithmeticOperator(self)




    def unaryArithmeticOperator(self):

        localctx = CartoSymCSSGrammar.UnaryArithmeticOperatorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 50, self.RULE_unaryArithmeticOperator)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 333
            _la = self._input.LA(1)
            if not(_la==29 or _la==30):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ArithmeticOperatorExpContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def POW(self):
            return self.getToken(CartoSymCSSGrammar.POW, 0)

        def getRuleIndex(self):
            return CartoSymCSSGrammar.RULE_arithmeticOperatorExp

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterArithmeticOperatorExp" ):
                listener.enterArithmeticOperatorExp(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitArithmeticOperatorExp" ):
                listener.exitArithmeticOperatorExp(self)




    def arithmeticOperatorExp(self):

        localctx = CartoSymCSSGrammar.ArithmeticOperatorExpContext(self, self._ctx, self.state)
        self.enterRule(localctx, 52, self.RULE_arithmeticOperatorExp)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 335
            self.match(CartoSymCSSGrammar.POW)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ArithmeticOperatorMulContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def MUL(self):
            return self.getToken(CartoSymCSSGrammar.MUL, 0)

        def DIV(self):
            return self.getToken(CartoSymCSSGrammar.DIV, 0)

        def IDIV(self):
            return self.getToken(CartoSymCSSGrammar.IDIV, 0)

        def MOD(self):
            return self.getToken(CartoSymCSSGrammar.MOD, 0)

        def getRuleIndex(self):
            return CartoSymCSSGrammar.RULE_arithmeticOperatorMul

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterArithmeticOperatorMul" ):
                listener.enterArithmeticOperatorMul(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitArithmeticOperatorMul" ):
                listener.exitArithmeticOperatorMul(self)




    def arithmeticOperatorMul(self):

        localctx = CartoSymCSSGrammar.ArithmeticOperatorMulContext(self, self._ctx, self.state)
        self.enterRule(localctx, 54, self.RULE_arithmeticOperatorMul)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 337
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 251658240) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ArithmeticOperatorAddContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def MINUS(self):
            return self.getToken(CartoSymCSSGrammar.MINUS, 0)

        def PLUS(self):
            return self.getToken(CartoSymCSSGrammar.PLUS, 0)

        def getRuleIndex(self):
            return CartoSymCSSGrammar.RULE_arithmeticOperatorAdd

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterArithmeticOperatorAdd" ):
                listener.enterArithmeticOperatorAdd(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitArithmeticOperatorAdd" ):
                listener.exitArithmeticOperatorAdd(self)




    def arithmeticOperatorAdd(self):

        localctx = CartoSymCSSGrammar.ArithmeticOperatorAddContext(self, self._ctx, self.state)
        self.enterRule(localctx, 56, self.RULE_arithmeticOperatorAdd)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 339
            _la = self._input.LA(1)
            if not(_la==29 or _la==30):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class RelationalOperatorContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EQ(self):
            return self.getToken(CartoSymCSSGrammar.EQ, 0)

        def LT(self):
            return self.getToken(CartoSymCSSGrammar.LT, 0)

        def LTEQ(self):
            return self.getToken(CartoSymCSSGrammar.LTEQ, 0)

        def GT(self):
            return self.getToken(CartoSymCSSGrammar.GT, 0)

        def GTEQ(self):
            return self.getToken(CartoSymCSSGrammar.GTEQ, 0)

        def IN(self):
            return self.getToken(CartoSymCSSGrammar.IN, 0)

        def NOT(self):
            return self.getToken(CartoSymCSSGrammar.NOT, 0)

        def IS(self):
            return self.getToken(CartoSymCSSGrammar.IS, 0)

        def LIKE(self):
            return self.getToken(CartoSymCSSGrammar.LIKE, 0)

        def getRuleIndex(self):
            return CartoSymCSSGrammar.RULE_relationalOperator

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRelationalOperator" ):
                listener.enterRelationalOperator(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRelationalOperator" ):
                listener.exitRelationalOperator(self)




    def relationalOperator(self):

        localctx = CartoSymCSSGrammar.RelationalOperatorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 58, self.RULE_relationalOperator)
        try:
            self.state = 355
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,33,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 341
                self.match(CartoSymCSSGrammar.EQ)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 342
                self.match(CartoSymCSSGrammar.LT)
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 343
                self.match(CartoSymCSSGrammar.LTEQ)
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 344
                self.match(CartoSymCSSGrammar.GT)
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 345
                self.match(CartoSymCSSGrammar.GTEQ)
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 346
                self.match(CartoSymCSSGrammar.IN)
                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 347
                self.match(CartoSymCSSGrammar.NOT)
                self.state = 348
                self.match(CartoSymCSSGrammar.IN)
                pass

            elif la_ == 8:
                self.enterOuterAlt(localctx, 8)
                self.state = 349
                self.match(CartoSymCSSGrammar.IS)
                pass

            elif la_ == 9:
                self.enterOuterAlt(localctx, 9)
                self.state = 350
                self.match(CartoSymCSSGrammar.IS)
                self.state = 351
                self.match(CartoSymCSSGrammar.NOT)
                pass

            elif la_ == 10:
                self.enterOuterAlt(localctx, 10)
                self.state = 352
                self.match(CartoSymCSSGrammar.LIKE)
                pass

            elif la_ == 11:
                self.enterOuterAlt(localctx, 11)
                self.state = 353
                self.match(CartoSymCSSGrammar.NOT)
                self.state = 354
                self.match(CartoSymCSSGrammar.LIKE)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class BetweenOperatorContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def BETWEEN(self):
            return self.getToken(CartoSymCSSGrammar.BETWEEN, 0)

        def NOT(self):
            return self.getToken(CartoSymCSSGrammar.NOT, 0)

        def getRuleIndex(self):
            return CartoSymCSSGrammar.RULE_betweenOperator

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBetweenOperator" ):
                listener.enterBetweenOperator(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBetweenOperator" ):
                listener.exitBetweenOperator(self)




    def betweenOperator(self):

        localctx = CartoSymCSSGrammar.BetweenOperatorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 60, self.RULE_betweenOperator)
        try:
            self.state = 360
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [19]:
                self.enterOuterAlt(localctx, 1)
                self.state = 357
                self.match(CartoSymCSSGrammar.BETWEEN)
                pass
            elif token in [16]:
                self.enterOuterAlt(localctx, 2)
                self.state = 358
                self.match(CartoSymCSSGrammar.NOT)
                self.state = 359
                self.match(CartoSymCSSGrammar.BETWEEN)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx



    def sempred(self, localctx:RuleContext, ruleIndex:int, predIndex:int):
        if self._predicates == None:
            self._predicates = dict()
        self._predicates[5] = self.stylingRuleList_sempred
        self._predicates[9] = self.tuple_sempred
        self._predicates[10] = self.expression_sempred
        self._predicates[14] = self.lhValue_sempred
        self._predicates[16] = self.propertyAssignmentList_sempred
        self._predicates[18] = self.propertyAssignmentInferredList_sempred
        self._predicates[20] = self.arrayElements_sempred
        self._predicates[22] = self.arguments_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def stylingRuleList_sempred(self, localctx:StylingRuleListContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 1)
         

    def tuple_sempred(self, localctx:TupleContext, predIndex:int):
            if predIndex == 1:
                return self.precpred(self._ctx, 1)
         

    def expression_sempred(self, localctx:ExpressionContext, predIndex:int):
            if predIndex == 2:
                return self.precpred(self._ctx, 11)
         

            if predIndex == 3:
                return self.precpred(self._ctx, 10)
         

            if predIndex == 4:
                return self.precpred(self._ctx, 9)
         

            if predIndex == 5:
                return self.precpred(self._ctx, 8)
         

            if predIndex == 6:
                return self.precpred(self._ctx, 7)
         

            if predIndex == 7:
                return self.precpred(self._ctx, 6)
         

            if predIndex == 8:
                return self.precpred(self._ctx, 5)
         

            if predIndex == 9:
                return self.precpred(self._ctx, 18)
         

            if predIndex == 10:
                return self.precpred(self._ctx, 12)
         

    def lhValue_sempred(self, localctx:LhValueContext, predIndex:int):
            if predIndex == 11:
                return self.precpred(self._ctx, 2)
         

            if predIndex == 12:
                return self.precpred(self._ctx, 1)
         

    def propertyAssignmentList_sempred(self, localctx:PropertyAssignmentListContext, predIndex:int):
            if predIndex == 13:
                return self.precpred(self._ctx, 1)
         

    def propertyAssignmentInferredList_sempred(self, localctx:PropertyAssignmentInferredListContext, predIndex:int):
            if predIndex == 14:
                return self.precpred(self._ctx, 2)
         

            if predIndex == 15:
                return self.precpred(self._ctx, 1)
         

    def arrayElements_sempred(self, localctx:ArrayElementsContext, predIndex:int):
            if predIndex == 16:
                return self.precpred(self._ctx, 1)
         

    def arguments_sempred(self, localctx:ArgumentsContext, predIndex:int):
            if predIndex == 17:
                return self.precpred(self._ctx, 1)
         




