// Generated from c:/Users/maxime.collombi/OneDrive - HESSO/Bureau/CartoSymTranscoder/schemas/CartoSymCSSGrammar.g4 by ANTLR 4.13.1
import org.antlr.v4.runtime.tree.ParseTreeListener;

/**
 * This interface defines a complete listener for a parse tree produced by
 * {@link CartoSymCSSGrammar}.
 */
public interface CartoSymCSSGrammarListener extends ParseTreeListener {
	/**
	 * Enter a parse tree produced by {@link CartoSymCSSGrammar#styleSheet}.
	 * @param ctx the parse tree
	 */
	void enterStyleSheet(CartoSymCSSGrammar.StyleSheetContext ctx);
	/**
	 * Exit a parse tree produced by {@link CartoSymCSSGrammar#styleSheet}.
	 * @param ctx the parse tree
	 */
	void exitStyleSheet(CartoSymCSSGrammar.StyleSheetContext ctx);
	/**
	 * Enter a parse tree produced by {@link CartoSymCSSGrammar#metadata}.
	 * @param ctx the parse tree
	 */
	void enterMetadata(CartoSymCSSGrammar.MetadataContext ctx);
	/**
	 * Exit a parse tree produced by {@link CartoSymCSSGrammar#metadata}.
	 * @param ctx the parse tree
	 */
	void exitMetadata(CartoSymCSSGrammar.MetadataContext ctx);
	/**
	 * Enter a parse tree produced by {@link CartoSymCSSGrammar#stylingRuleList}.
	 * @param ctx the parse tree
	 */
	void enterStylingRuleList(CartoSymCSSGrammar.StylingRuleListContext ctx);
	/**
	 * Exit a parse tree produced by {@link CartoSymCSSGrammar#stylingRuleList}.
	 * @param ctx the parse tree
	 */
	void exitStylingRuleList(CartoSymCSSGrammar.StylingRuleListContext ctx);
	/**
	 * Enter a parse tree produced by {@link CartoSymCSSGrammar#stylingRule}.
	 * @param ctx the parse tree
	 */
	void enterStylingRule(CartoSymCSSGrammar.StylingRuleContext ctx);
	/**
	 * Exit a parse tree produced by {@link CartoSymCSSGrammar#stylingRule}.
	 * @param ctx the parse tree
	 */
	void exitStylingRule(CartoSymCSSGrammar.StylingRuleContext ctx);
	/**
	 * Enter a parse tree produced by {@link CartoSymCSSGrammar#selector}.
	 * @param ctx the parse tree
	 */
	void enterSelector(CartoSymCSSGrammar.SelectorContext ctx);
	/**
	 * Exit a parse tree produced by {@link CartoSymCSSGrammar#selector}.
	 * @param ctx the parse tree
	 */
	void exitSelector(CartoSymCSSGrammar.SelectorContext ctx);
	/**
	 * Enter a parse tree produced by {@link CartoSymCSSGrammar#idOrConstant}.
	 * @param ctx the parse tree
	 */
	void enterIdOrConstant(CartoSymCSSGrammar.IdOrConstantContext ctx);
	/**
	 * Exit a parse tree produced by {@link CartoSymCSSGrammar#idOrConstant}.
	 * @param ctx the parse tree
	 */
	void exitIdOrConstant(CartoSymCSSGrammar.IdOrConstantContext ctx);
	/**
	 * Enter a parse tree produced by {@link CartoSymCSSGrammar#tuple}.
	 * @param ctx the parse tree
	 */
	void enterTuple(CartoSymCSSGrammar.TupleContext ctx);
	/**
	 * Exit a parse tree produced by {@link CartoSymCSSGrammar#tuple}.
	 * @param ctx the parse tree
	 */
	void exitTuple(CartoSymCSSGrammar.TupleContext ctx);
	/**
	 * Enter a parse tree produced by {@link CartoSymCSSGrammar#expression}.
	 * @param ctx the parse tree
	 */
	void enterExpression(CartoSymCSSGrammar.ExpressionContext ctx);
	/**
	 * Exit a parse tree produced by {@link CartoSymCSSGrammar#expression}.
	 * @param ctx the parse tree
	 */
	void exitExpression(CartoSymCSSGrammar.ExpressionContext ctx);
	/**
	 * Enter a parse tree produced by {@link CartoSymCSSGrammar#expConstant}.
	 * @param ctx the parse tree
	 */
	void enterExpConstant(CartoSymCSSGrammar.ExpConstantContext ctx);
	/**
	 * Exit a parse tree produced by {@link CartoSymCSSGrammar#expConstant}.
	 * @param ctx the parse tree
	 */
	void exitExpConstant(CartoSymCSSGrammar.ExpConstantContext ctx);
	/**
	 * Enter a parse tree produced by {@link CartoSymCSSGrammar#expString}.
	 * @param ctx the parse tree
	 */
	void enterExpString(CartoSymCSSGrammar.ExpStringContext ctx);
	/**
	 * Exit a parse tree produced by {@link CartoSymCSSGrammar#expString}.
	 * @param ctx the parse tree
	 */
	void exitExpString(CartoSymCSSGrammar.ExpStringContext ctx);
	/**
	 * Enter a parse tree produced by {@link CartoSymCSSGrammar#expInstance}.
	 * @param ctx the parse tree
	 */
	void enterExpInstance(CartoSymCSSGrammar.ExpInstanceContext ctx);
	/**
	 * Exit a parse tree produced by {@link CartoSymCSSGrammar#expInstance}.
	 * @param ctx the parse tree
	 */
	void exitExpInstance(CartoSymCSSGrammar.ExpInstanceContext ctx);
	/**
	 * Enter a parse tree produced by {@link CartoSymCSSGrammar#lhValue}.
	 * @param ctx the parse tree
	 */
	void enterLhValue(CartoSymCSSGrammar.LhValueContext ctx);
	/**
	 * Exit a parse tree produced by {@link CartoSymCSSGrammar#lhValue}.
	 * @param ctx the parse tree
	 */
	void exitLhValue(CartoSymCSSGrammar.LhValueContext ctx);
	/**
	 * Enter a parse tree produced by {@link CartoSymCSSGrammar#propertyAssignment}.
	 * @param ctx the parse tree
	 */
	void enterPropertyAssignment(CartoSymCSSGrammar.PropertyAssignmentContext ctx);
	/**
	 * Exit a parse tree produced by {@link CartoSymCSSGrammar#propertyAssignment}.
	 * @param ctx the parse tree
	 */
	void exitPropertyAssignment(CartoSymCSSGrammar.PropertyAssignmentContext ctx);
	/**
	 * Enter a parse tree produced by {@link CartoSymCSSGrammar#propertyAssignmentList}.
	 * @param ctx the parse tree
	 */
	void enterPropertyAssignmentList(CartoSymCSSGrammar.PropertyAssignmentListContext ctx);
	/**
	 * Exit a parse tree produced by {@link CartoSymCSSGrammar#propertyAssignmentList}.
	 * @param ctx the parse tree
	 */
	void exitPropertyAssignmentList(CartoSymCSSGrammar.PropertyAssignmentListContext ctx);
	/**
	 * Enter a parse tree produced by {@link CartoSymCSSGrammar#propertyAssignmentInferred}.
	 * @param ctx the parse tree
	 */
	void enterPropertyAssignmentInferred(CartoSymCSSGrammar.PropertyAssignmentInferredContext ctx);
	/**
	 * Exit a parse tree produced by {@link CartoSymCSSGrammar#propertyAssignmentInferred}.
	 * @param ctx the parse tree
	 */
	void exitPropertyAssignmentInferred(CartoSymCSSGrammar.PropertyAssignmentInferredContext ctx);
	/**
	 * Enter a parse tree produced by {@link CartoSymCSSGrammar#propertyAssignmentInferredList}.
	 * @param ctx the parse tree
	 */
	void enterPropertyAssignmentInferredList(CartoSymCSSGrammar.PropertyAssignmentInferredListContext ctx);
	/**
	 * Exit a parse tree produced by {@link CartoSymCSSGrammar#propertyAssignmentInferredList}.
	 * @param ctx the parse tree
	 */
	void exitPropertyAssignmentInferredList(CartoSymCSSGrammar.PropertyAssignmentInferredListContext ctx);
	/**
	 * Enter a parse tree produced by {@link CartoSymCSSGrammar#expArray}.
	 * @param ctx the parse tree
	 */
	void enterExpArray(CartoSymCSSGrammar.ExpArrayContext ctx);
	/**
	 * Exit a parse tree produced by {@link CartoSymCSSGrammar#expArray}.
	 * @param ctx the parse tree
	 */
	void exitExpArray(CartoSymCSSGrammar.ExpArrayContext ctx);
	/**
	 * Enter a parse tree produced by {@link CartoSymCSSGrammar#arrayElements}.
	 * @param ctx the parse tree
	 */
	void enterArrayElements(CartoSymCSSGrammar.ArrayElementsContext ctx);
	/**
	 * Exit a parse tree produced by {@link CartoSymCSSGrammar#arrayElements}.
	 * @param ctx the parse tree
	 */
	void exitArrayElements(CartoSymCSSGrammar.ArrayElementsContext ctx);
	/**
	 * Enter a parse tree produced by {@link CartoSymCSSGrammar#expCall}.
	 * @param ctx the parse tree
	 */
	void enterExpCall(CartoSymCSSGrammar.ExpCallContext ctx);
	/**
	 * Exit a parse tree produced by {@link CartoSymCSSGrammar#expCall}.
	 * @param ctx the parse tree
	 */
	void exitExpCall(CartoSymCSSGrammar.ExpCallContext ctx);
	/**
	 * Enter a parse tree produced by {@link CartoSymCSSGrammar#arguments}.
	 * @param ctx the parse tree
	 */
	void enterArguments(CartoSymCSSGrammar.ArgumentsContext ctx);
	/**
	 * Exit a parse tree produced by {@link CartoSymCSSGrammar#arguments}.
	 * @param ctx the parse tree
	 */
	void exitArguments(CartoSymCSSGrammar.ArgumentsContext ctx);
	/**
	 * Enter a parse tree produced by {@link CartoSymCSSGrammar#binaryLogicalOperator}.
	 * @param ctx the parse tree
	 */
	void enterBinaryLogicalOperator(CartoSymCSSGrammar.BinaryLogicalOperatorContext ctx);
	/**
	 * Exit a parse tree produced by {@link CartoSymCSSGrammar#binaryLogicalOperator}.
	 * @param ctx the parse tree
	 */
	void exitBinaryLogicalOperator(CartoSymCSSGrammar.BinaryLogicalOperatorContext ctx);
	/**
	 * Enter a parse tree produced by {@link CartoSymCSSGrammar#unaryLogicalOperator}.
	 * @param ctx the parse tree
	 */
	void enterUnaryLogicalOperator(CartoSymCSSGrammar.UnaryLogicalOperatorContext ctx);
	/**
	 * Exit a parse tree produced by {@link CartoSymCSSGrammar#unaryLogicalOperator}.
	 * @param ctx the parse tree
	 */
	void exitUnaryLogicalOperator(CartoSymCSSGrammar.UnaryLogicalOperatorContext ctx);
	/**
	 * Enter a parse tree produced by {@link CartoSymCSSGrammar#unaryArithmeticOperator}.
	 * @param ctx the parse tree
	 */
	void enterUnaryArithmeticOperator(CartoSymCSSGrammar.UnaryArithmeticOperatorContext ctx);
	/**
	 * Exit a parse tree produced by {@link CartoSymCSSGrammar#unaryArithmeticOperator}.
	 * @param ctx the parse tree
	 */
	void exitUnaryArithmeticOperator(CartoSymCSSGrammar.UnaryArithmeticOperatorContext ctx);
	/**
	 * Enter a parse tree produced by {@link CartoSymCSSGrammar#arithmeticOperatorExp}.
	 * @param ctx the parse tree
	 */
	void enterArithmeticOperatorExp(CartoSymCSSGrammar.ArithmeticOperatorExpContext ctx);
	/**
	 * Exit a parse tree produced by {@link CartoSymCSSGrammar#arithmeticOperatorExp}.
	 * @param ctx the parse tree
	 */
	void exitArithmeticOperatorExp(CartoSymCSSGrammar.ArithmeticOperatorExpContext ctx);
	/**
	 * Enter a parse tree produced by {@link CartoSymCSSGrammar#arithmeticOperatorMul}.
	 * @param ctx the parse tree
	 */
	void enterArithmeticOperatorMul(CartoSymCSSGrammar.ArithmeticOperatorMulContext ctx);
	/**
	 * Exit a parse tree produced by {@link CartoSymCSSGrammar#arithmeticOperatorMul}.
	 * @param ctx the parse tree
	 */
	void exitArithmeticOperatorMul(CartoSymCSSGrammar.ArithmeticOperatorMulContext ctx);
	/**
	 * Enter a parse tree produced by {@link CartoSymCSSGrammar#arithmeticOperatorAdd}.
	 * @param ctx the parse tree
	 */
	void enterArithmeticOperatorAdd(CartoSymCSSGrammar.ArithmeticOperatorAddContext ctx);
	/**
	 * Exit a parse tree produced by {@link CartoSymCSSGrammar#arithmeticOperatorAdd}.
	 * @param ctx the parse tree
	 */
	void exitArithmeticOperatorAdd(CartoSymCSSGrammar.ArithmeticOperatorAddContext ctx);
	/**
	 * Enter a parse tree produced by {@link CartoSymCSSGrammar#relationalOperator}.
	 * @param ctx the parse tree
	 */
	void enterRelationalOperator(CartoSymCSSGrammar.RelationalOperatorContext ctx);
	/**
	 * Exit a parse tree produced by {@link CartoSymCSSGrammar#relationalOperator}.
	 * @param ctx the parse tree
	 */
	void exitRelationalOperator(CartoSymCSSGrammar.RelationalOperatorContext ctx);
	/**
	 * Enter a parse tree produced by {@link CartoSymCSSGrammar#betweenOperator}.
	 * @param ctx the parse tree
	 */
	void enterBetweenOperator(CartoSymCSSGrammar.BetweenOperatorContext ctx);
	/**
	 * Exit a parse tree produced by {@link CartoSymCSSGrammar#betweenOperator}.
	 * @param ctx the parse tree
	 */
	void exitBetweenOperator(CartoSymCSSGrammar.BetweenOperatorContext ctx);
}