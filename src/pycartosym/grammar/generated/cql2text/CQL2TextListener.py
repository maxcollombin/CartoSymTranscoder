# Generated from vendor/cartosymcss-grammar/CQL2Text.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .CQL2TextParser import CQL2TextParser
else:
    from CQL2TextParser import CQL2TextParser

# This class defines a complete listener for a parse tree produced by CQL2TextParser.
class CQL2TextListener(ParseTreeListener):

    # Enter a parse tree produced by CQL2TextParser#cql2Text.
    def enterCql2Text(self, ctx:CQL2TextParser.Cql2TextContext):
        pass

    # Exit a parse tree produced by CQL2TextParser#cql2Text.
    def exitCql2Text(self, ctx:CQL2TextParser.Cql2TextContext):
        pass


    # Enter a parse tree produced by CQL2TextParser#booleanExpression.
    def enterBooleanExpression(self, ctx:CQL2TextParser.BooleanExpressionContext):
        pass

    # Exit a parse tree produced by CQL2TextParser#booleanExpression.
    def exitBooleanExpression(self, ctx:CQL2TextParser.BooleanExpressionContext):
        pass


    # Enter a parse tree produced by CQL2TextParser#booleanTerm.
    def enterBooleanTerm(self, ctx:CQL2TextParser.BooleanTermContext):
        pass

    # Exit a parse tree produced by CQL2TextParser#booleanTerm.
    def exitBooleanTerm(self, ctx:CQL2TextParser.BooleanTermContext):
        pass


    # Enter a parse tree produced by CQL2TextParser#booleanFactor.
    def enterBooleanFactor(self, ctx:CQL2TextParser.BooleanFactorContext):
        pass

    # Exit a parse tree produced by CQL2TextParser#booleanFactor.
    def exitBooleanFactor(self, ctx:CQL2TextParser.BooleanFactorContext):
        pass


    # Enter a parse tree produced by CQL2TextParser#primary.
    def enterPrimary(self, ctx:CQL2TextParser.PrimaryContext):
        pass

    # Exit a parse tree produced by CQL2TextParser#primary.
    def exitPrimary(self, ctx:CQL2TextParser.PrimaryContext):
        pass


    # Enter a parse tree produced by CQL2TextParser#comparisonTail.
    def enterComparisonTail(self, ctx:CQL2TextParser.ComparisonTailContext):
        pass

    # Exit a parse tree produced by CQL2TextParser#comparisonTail.
    def exitComparisonTail(self, ctx:CQL2TextParser.ComparisonTailContext):
        pass


    # Enter a parse tree produced by CQL2TextParser#likeTail.
    def enterLikeTail(self, ctx:CQL2TextParser.LikeTailContext):
        pass

    # Exit a parse tree produced by CQL2TextParser#likeTail.
    def exitLikeTail(self, ctx:CQL2TextParser.LikeTailContext):
        pass


    # Enter a parse tree produced by CQL2TextParser#betweenTail.
    def enterBetweenTail(self, ctx:CQL2TextParser.BetweenTailContext):
        pass

    # Exit a parse tree produced by CQL2TextParser#betweenTail.
    def exitBetweenTail(self, ctx:CQL2TextParser.BetweenTailContext):
        pass


    # Enter a parse tree produced by CQL2TextParser#inTail.
    def enterInTail(self, ctx:CQL2TextParser.InTailContext):
        pass

    # Exit a parse tree produced by CQL2TextParser#inTail.
    def exitInTail(self, ctx:CQL2TextParser.InTailContext):
        pass


    # Enter a parse tree produced by CQL2TextParser#isNullTail.
    def enterIsNullTail(self, ctx:CQL2TextParser.IsNullTailContext):
        pass

    # Exit a parse tree produced by CQL2TextParser#isNullTail.
    def exitIsNullTail(self, ctx:CQL2TextParser.IsNullTailContext):
        pass


    # Enter a parse tree produced by CQL2TextParser#comparisonOperator.
    def enterComparisonOperator(self, ctx:CQL2TextParser.ComparisonOperatorContext):
        pass

    # Exit a parse tree produced by CQL2TextParser#comparisonOperator.
    def exitComparisonOperator(self, ctx:CQL2TextParser.ComparisonOperatorContext):
        pass


    # Enter a parse tree produced by CQL2TextParser#inList.
    def enterInList(self, ctx:CQL2TextParser.InListContext):
        pass

    # Exit a parse tree produced by CQL2TextParser#inList.
    def exitInList(self, ctx:CQL2TextParser.InListContext):
        pass


    # Enter a parse tree produced by CQL2TextParser#spatialPredicate.
    def enterSpatialPredicate(self, ctx:CQL2TextParser.SpatialPredicateContext):
        pass

    # Exit a parse tree produced by CQL2TextParser#spatialPredicate.
    def exitSpatialPredicate(self, ctx:CQL2TextParser.SpatialPredicateContext):
        pass


    # Enter a parse tree produced by CQL2TextParser#spatialFunction.
    def enterSpatialFunction(self, ctx:CQL2TextParser.SpatialFunctionContext):
        pass

    # Exit a parse tree produced by CQL2TextParser#spatialFunction.
    def exitSpatialFunction(self, ctx:CQL2TextParser.SpatialFunctionContext):
        pass


    # Enter a parse tree produced by CQL2TextParser#temporalPredicate.
    def enterTemporalPredicate(self, ctx:CQL2TextParser.TemporalPredicateContext):
        pass

    # Exit a parse tree produced by CQL2TextParser#temporalPredicate.
    def exitTemporalPredicate(self, ctx:CQL2TextParser.TemporalPredicateContext):
        pass


    # Enter a parse tree produced by CQL2TextParser#temporalFunction.
    def enterTemporalFunction(self, ctx:CQL2TextParser.TemporalFunctionContext):
        pass

    # Exit a parse tree produced by CQL2TextParser#temporalFunction.
    def exitTemporalFunction(self, ctx:CQL2TextParser.TemporalFunctionContext):
        pass


    # Enter a parse tree produced by CQL2TextParser#arrayPredicate.
    def enterArrayPredicate(self, ctx:CQL2TextParser.ArrayPredicateContext):
        pass

    # Exit a parse tree produced by CQL2TextParser#arrayPredicate.
    def exitArrayPredicate(self, ctx:CQL2TextParser.ArrayPredicateContext):
        pass


    # Enter a parse tree produced by CQL2TextParser#arrayFunction.
    def enterArrayFunction(self, ctx:CQL2TextParser.ArrayFunctionContext):
        pass

    # Exit a parse tree produced by CQL2TextParser#arrayFunction.
    def exitArrayFunction(self, ctx:CQL2TextParser.ArrayFunctionContext):
        pass


    # Enter a parse tree produced by CQL2TextParser#operand.
    def enterOperand(self, ctx:CQL2TextParser.OperandContext):
        pass

    # Exit a parse tree produced by CQL2TextParser#operand.
    def exitOperand(self, ctx:CQL2TextParser.OperandContext):
        pass


    # Enter a parse tree produced by CQL2TextParser#arithmeticExpr.
    def enterArithmeticExpr(self, ctx:CQL2TextParser.ArithmeticExprContext):
        pass

    # Exit a parse tree produced by CQL2TextParser#arithmeticExpr.
    def exitArithmeticExpr(self, ctx:CQL2TextParser.ArithmeticExprContext):
        pass


    # Enter a parse tree produced by CQL2TextParser#arithmeticTerm.
    def enterArithmeticTerm(self, ctx:CQL2TextParser.ArithmeticTermContext):
        pass

    # Exit a parse tree produced by CQL2TextParser#arithmeticTerm.
    def exitArithmeticTerm(self, ctx:CQL2TextParser.ArithmeticTermContext):
        pass


    # Enter a parse tree produced by CQL2TextParser#powerTerm.
    def enterPowerTerm(self, ctx:CQL2TextParser.PowerTermContext):
        pass

    # Exit a parse tree produced by CQL2TextParser#powerTerm.
    def exitPowerTerm(self, ctx:CQL2TextParser.PowerTermContext):
        pass


    # Enter a parse tree produced by CQL2TextParser#arithmeticFactor.
    def enterArithmeticFactor(self, ctx:CQL2TextParser.ArithmeticFactorContext):
        pass

    # Exit a parse tree produced by CQL2TextParser#arithmeticFactor.
    def exitArithmeticFactor(self, ctx:CQL2TextParser.ArithmeticFactorContext):
        pass


    # Enter a parse tree produced by CQL2TextParser#atom.
    def enterAtom(self, ctx:CQL2TextParser.AtomContext):
        pass

    # Exit a parse tree produced by CQL2TextParser#atom.
    def exitAtom(self, ctx:CQL2TextParser.AtomContext):
        pass


    # Enter a parse tree produced by CQL2TextParser#booleanLiteral.
    def enterBooleanLiteral(self, ctx:CQL2TextParser.BooleanLiteralContext):
        pass

    # Exit a parse tree produced by CQL2TextParser#booleanLiteral.
    def exitBooleanLiteral(self, ctx:CQL2TextParser.BooleanLiteralContext):
        pass


    # Enter a parse tree produced by CQL2TextParser#propertyName.
    def enterPropertyName(self, ctx:CQL2TextParser.PropertyNameContext):
        pass

    # Exit a parse tree produced by CQL2TextParser#propertyName.
    def exitPropertyName(self, ctx:CQL2TextParser.PropertyNameContext):
        pass


    # Enter a parse tree produced by CQL2TextParser#functionCall.
    def enterFunctionCall(self, ctx:CQL2TextParser.FunctionCallContext):
        pass

    # Exit a parse tree produced by CQL2TextParser#functionCall.
    def exitFunctionCall(self, ctx:CQL2TextParser.FunctionCallContext):
        pass


    # Enter a parse tree produced by CQL2TextParser#argumentList.
    def enterArgumentList(self, ctx:CQL2TextParser.ArgumentListContext):
        pass

    # Exit a parse tree produced by CQL2TextParser#argumentList.
    def exitArgumentList(self, ctx:CQL2TextParser.ArgumentListContext):
        pass


    # Enter a parse tree produced by CQL2TextParser#arrayExpr.
    def enterArrayExpr(self, ctx:CQL2TextParser.ArrayExprContext):
        pass

    # Exit a parse tree produced by CQL2TextParser#arrayExpr.
    def exitArrayExpr(self, ctx:CQL2TextParser.ArrayExprContext):
        pass


    # Enter a parse tree produced by CQL2TextParser#characterClause.
    def enterCharacterClause(self, ctx:CQL2TextParser.CharacterClauseContext):
        pass

    # Exit a parse tree produced by CQL2TextParser#characterClause.
    def exitCharacterClause(self, ctx:CQL2TextParser.CharacterClauseContext):
        pass


    # Enter a parse tree produced by CQL2TextParser#characterClauseArg.
    def enterCharacterClauseArg(self, ctx:CQL2TextParser.CharacterClauseArgContext):
        pass

    # Exit a parse tree produced by CQL2TextParser#characterClauseArg.
    def exitCharacterClauseArg(self, ctx:CQL2TextParser.CharacterClauseArgContext):
        pass


    # Enter a parse tree produced by CQL2TextParser#geometryLiteral.
    def enterGeometryLiteral(self, ctx:CQL2TextParser.GeometryLiteralContext):
        pass

    # Exit a parse tree produced by CQL2TextParser#geometryLiteral.
    def exitGeometryLiteral(self, ctx:CQL2TextParser.GeometryLiteralContext):
        pass


    # Enter a parse tree produced by CQL2TextParser#pointTaggedText.
    def enterPointTaggedText(self, ctx:CQL2TextParser.PointTaggedTextContext):
        pass

    # Exit a parse tree produced by CQL2TextParser#pointTaggedText.
    def exitPointTaggedText(self, ctx:CQL2TextParser.PointTaggedTextContext):
        pass


    # Enter a parse tree produced by CQL2TextParser#linestringTaggedText.
    def enterLinestringTaggedText(self, ctx:CQL2TextParser.LinestringTaggedTextContext):
        pass

    # Exit a parse tree produced by CQL2TextParser#linestringTaggedText.
    def exitLinestringTaggedText(self, ctx:CQL2TextParser.LinestringTaggedTextContext):
        pass


    # Enter a parse tree produced by CQL2TextParser#polygonTaggedText.
    def enterPolygonTaggedText(self, ctx:CQL2TextParser.PolygonTaggedTextContext):
        pass

    # Exit a parse tree produced by CQL2TextParser#polygonTaggedText.
    def exitPolygonTaggedText(self, ctx:CQL2TextParser.PolygonTaggedTextContext):
        pass


    # Enter a parse tree produced by CQL2TextParser#multipointTaggedText.
    def enterMultipointTaggedText(self, ctx:CQL2TextParser.MultipointTaggedTextContext):
        pass

    # Exit a parse tree produced by CQL2TextParser#multipointTaggedText.
    def exitMultipointTaggedText(self, ctx:CQL2TextParser.MultipointTaggedTextContext):
        pass


    # Enter a parse tree produced by CQL2TextParser#multilinestringTaggedText.
    def enterMultilinestringTaggedText(self, ctx:CQL2TextParser.MultilinestringTaggedTextContext):
        pass

    # Exit a parse tree produced by CQL2TextParser#multilinestringTaggedText.
    def exitMultilinestringTaggedText(self, ctx:CQL2TextParser.MultilinestringTaggedTextContext):
        pass


    # Enter a parse tree produced by CQL2TextParser#multipolygonTaggedText.
    def enterMultipolygonTaggedText(self, ctx:CQL2TextParser.MultipolygonTaggedTextContext):
        pass

    # Exit a parse tree produced by CQL2TextParser#multipolygonTaggedText.
    def exitMultipolygonTaggedText(self, ctx:CQL2TextParser.MultipolygonTaggedTextContext):
        pass


    # Enter a parse tree produced by CQL2TextParser#geometryCollectionTaggedText.
    def enterGeometryCollectionTaggedText(self, ctx:CQL2TextParser.GeometryCollectionTaggedTextContext):
        pass

    # Exit a parse tree produced by CQL2TextParser#geometryCollectionTaggedText.
    def exitGeometryCollectionTaggedText(self, ctx:CQL2TextParser.GeometryCollectionTaggedTextContext):
        pass


    # Enter a parse tree produced by CQL2TextParser#pointText.
    def enterPointText(self, ctx:CQL2TextParser.PointTextContext):
        pass

    # Exit a parse tree produced by CQL2TextParser#pointText.
    def exitPointText(self, ctx:CQL2TextParser.PointTextContext):
        pass


    # Enter a parse tree produced by CQL2TextParser#point.
    def enterPoint(self, ctx:CQL2TextParser.PointContext):
        pass

    # Exit a parse tree produced by CQL2TextParser#point.
    def exitPoint(self, ctx:CQL2TextParser.PointContext):
        pass


    # Enter a parse tree produced by CQL2TextParser#lineStringText.
    def enterLineStringText(self, ctx:CQL2TextParser.LineStringTextContext):
        pass

    # Exit a parse tree produced by CQL2TextParser#lineStringText.
    def exitLineStringText(self, ctx:CQL2TextParser.LineStringTextContext):
        pass


    # Enter a parse tree produced by CQL2TextParser#linearRingText.
    def enterLinearRingText(self, ctx:CQL2TextParser.LinearRingTextContext):
        pass

    # Exit a parse tree produced by CQL2TextParser#linearRingText.
    def exitLinearRingText(self, ctx:CQL2TextParser.LinearRingTextContext):
        pass


    # Enter a parse tree produced by CQL2TextParser#polygonText.
    def enterPolygonText(self, ctx:CQL2TextParser.PolygonTextContext):
        pass

    # Exit a parse tree produced by CQL2TextParser#polygonText.
    def exitPolygonText(self, ctx:CQL2TextParser.PolygonTextContext):
        pass


    # Enter a parse tree produced by CQL2TextParser#multiPointText.
    def enterMultiPointText(self, ctx:CQL2TextParser.MultiPointTextContext):
        pass

    # Exit a parse tree produced by CQL2TextParser#multiPointText.
    def exitMultiPointText(self, ctx:CQL2TextParser.MultiPointTextContext):
        pass


    # Enter a parse tree produced by CQL2TextParser#multiLineStringText.
    def enterMultiLineStringText(self, ctx:CQL2TextParser.MultiLineStringTextContext):
        pass

    # Exit a parse tree produced by CQL2TextParser#multiLineStringText.
    def exitMultiLineStringText(self, ctx:CQL2TextParser.MultiLineStringTextContext):
        pass


    # Enter a parse tree produced by CQL2TextParser#multiPolygonText.
    def enterMultiPolygonText(self, ctx:CQL2TextParser.MultiPolygonTextContext):
        pass

    # Exit a parse tree produced by CQL2TextParser#multiPolygonText.
    def exitMultiPolygonText(self, ctx:CQL2TextParser.MultiPolygonTextContext):
        pass


    # Enter a parse tree produced by CQL2TextParser#geometryCollectionText.
    def enterGeometryCollectionText(self, ctx:CQL2TextParser.GeometryCollectionTextContext):
        pass

    # Exit a parse tree produced by CQL2TextParser#geometryCollectionText.
    def exitGeometryCollectionText(self, ctx:CQL2TextParser.GeometryCollectionTextContext):
        pass


    # Enter a parse tree produced by CQL2TextParser#bboxTaggedText.
    def enterBboxTaggedText(self, ctx:CQL2TextParser.BboxTaggedTextContext):
        pass

    # Exit a parse tree produced by CQL2TextParser#bboxTaggedText.
    def exitBboxTaggedText(self, ctx:CQL2TextParser.BboxTaggedTextContext):
        pass


    # Enter a parse tree produced by CQL2TextParser#bboxText.
    def enterBboxText(self, ctx:CQL2TextParser.BboxTextContext):
        pass

    # Exit a parse tree produced by CQL2TextParser#bboxText.
    def exitBboxText(self, ctx:CQL2TextParser.BboxTextContext):
        pass


    # Enter a parse tree produced by CQL2TextParser#signedNumber.
    def enterSignedNumber(self, ctx:CQL2TextParser.SignedNumberContext):
        pass

    # Exit a parse tree produced by CQL2TextParser#signedNumber.
    def exitSignedNumber(self, ctx:CQL2TextParser.SignedNumberContext):
        pass


    # Enter a parse tree produced by CQL2TextParser#temporalInstant.
    def enterTemporalInstant(self, ctx:CQL2TextParser.TemporalInstantContext):
        pass

    # Exit a parse tree produced by CQL2TextParser#temporalInstant.
    def exitTemporalInstant(self, ctx:CQL2TextParser.TemporalInstantContext):
        pass


    # Enter a parse tree produced by CQL2TextParser#dateInstant.
    def enterDateInstant(self, ctx:CQL2TextParser.DateInstantContext):
        pass

    # Exit a parse tree produced by CQL2TextParser#dateInstant.
    def exitDateInstant(self, ctx:CQL2TextParser.DateInstantContext):
        pass


    # Enter a parse tree produced by CQL2TextParser#timestampInstant.
    def enterTimestampInstant(self, ctx:CQL2TextParser.TimestampInstantContext):
        pass

    # Exit a parse tree produced by CQL2TextParser#timestampInstant.
    def exitTimestampInstant(self, ctx:CQL2TextParser.TimestampInstantContext):
        pass


    # Enter a parse tree produced by CQL2TextParser#intervalInstant.
    def enterIntervalInstant(self, ctx:CQL2TextParser.IntervalInstantContext):
        pass

    # Exit a parse tree produced by CQL2TextParser#intervalInstant.
    def exitIntervalInstant(self, ctx:CQL2TextParser.IntervalInstantContext):
        pass


    # Enter a parse tree produced by CQL2TextParser#instantParameter.
    def enterInstantParameter(self, ctx:CQL2TextParser.InstantParameterContext):
        pass

    # Exit a parse tree produced by CQL2TextParser#instantParameter.
    def exitInstantParameter(self, ctx:CQL2TextParser.InstantParameterContext):
        pass



del CQL2TextParser