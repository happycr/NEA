// Generated from pseudo.g4 by ANTLR 4.9.2
import org.antlr.v4.runtime.tree.ParseTreeListener;

/**
 * This interface defines a complete listener for a parse tree produced by
 * {@link pseudoParser}.
 */
public interface pseudoListener extends ParseTreeListener {
	/**
	 * Enter a parse tree produced by {@link pseudoParser#prog}.
	 * @param ctx the parse tree
	 */
	void enterProg(pseudoParser.ProgContext ctx);
	/**
	 * Exit a parse tree produced by {@link pseudoParser#prog}.
	 * @param ctx the parse tree
	 */
	void exitProg(pseudoParser.ProgContext ctx);
	/**
	 * Enter a parse tree produced by {@link pseudoParser#block}.
	 * @param ctx the parse tree
	 */
	void enterBlock(pseudoParser.BlockContext ctx);
	/**
	 * Exit a parse tree produced by {@link pseudoParser#block}.
	 * @param ctx the parse tree
	 */
	void exitBlock(pseudoParser.BlockContext ctx);
	/**
	 * Enter a parse tree produced by {@link pseudoParser#repeat_until}.
	 * @param ctx the parse tree
	 */
	void enterRepeat_until(pseudoParser.Repeat_untilContext ctx);
	/**
	 * Exit a parse tree produced by {@link pseudoParser#repeat_until}.
	 * @param ctx the parse tree
	 */
	void exitRepeat_until(pseudoParser.Repeat_untilContext ctx);
	/**
	 * Enter a parse tree produced by {@link pseudoParser#while_loop}.
	 * @param ctx the parse tree
	 */
	void enterWhile_loop(pseudoParser.While_loopContext ctx);
	/**
	 * Exit a parse tree produced by {@link pseudoParser#while_loop}.
	 * @param ctx the parse tree
	 */
	void exitWhile_loop(pseudoParser.While_loopContext ctx);
	/**
	 * Enter a parse tree produced by {@link pseudoParser#for_loop_step}.
	 * @param ctx the parse tree
	 */
	void enterFor_loop_step(pseudoParser.For_loop_stepContext ctx);
	/**
	 * Exit a parse tree produced by {@link pseudoParser#for_loop_step}.
	 * @param ctx the parse tree
	 */
	void exitFor_loop_step(pseudoParser.For_loop_stepContext ctx);
	/**
	 * Enter a parse tree produced by {@link pseudoParser#for_loop}.
	 * @param ctx the parse tree
	 */
	void enterFor_loop(pseudoParser.For_loopContext ctx);
	/**
	 * Exit a parse tree produced by {@link pseudoParser#for_loop}.
	 * @param ctx the parse tree
	 */
	void exitFor_loop(pseudoParser.For_loopContext ctx);
	/**
	 * Enter a parse tree produced by {@link pseudoParser#condition_sequence}.
	 * @param ctx the parse tree
	 */
	void enterCondition_sequence(pseudoParser.Condition_sequenceContext ctx);
	/**
	 * Exit a parse tree produced by {@link pseudoParser#condition_sequence}.
	 * @param ctx the parse tree
	 */
	void exitCondition_sequence(pseudoParser.Condition_sequenceContext ctx);
	/**
	 * Enter a parse tree produced by {@link pseudoParser#if_block}.
	 * @param ctx the parse tree
	 */
	void enterIf_block(pseudoParser.If_blockContext ctx);
	/**
	 * Exit a parse tree produced by {@link pseudoParser#if_block}.
	 * @param ctx the parse tree
	 */
	void exitIf_block(pseudoParser.If_blockContext ctx);
	/**
	 * Enter a parse tree produced by {@link pseudoParser#record}.
	 * @param ctx the parse tree
	 */
	void enterRecord(pseudoParser.RecordContext ctx);
	/**
	 * Exit a parse tree produced by {@link pseudoParser#record}.
	 * @param ctx the parse tree
	 */
	void exitRecord(pseudoParser.RecordContext ctx);
	/**
	 * Enter a parse tree produced by {@link pseudoParser#field}.
	 * @param ctx the parse tree
	 */
	void enterField(pseudoParser.FieldContext ctx);
	/**
	 * Exit a parse tree produced by {@link pseudoParser#field}.
	 * @param ctx the parse tree
	 */
	void exitField(pseudoParser.FieldContext ctx);
	/**
	 * Enter a parse tree produced by {@link pseudoParser#else_if_block}.
	 * @param ctx the parse tree
	 */
	void enterElse_if_block(pseudoParser.Else_if_blockContext ctx);
	/**
	 * Exit a parse tree produced by {@link pseudoParser#else_if_block}.
	 * @param ctx the parse tree
	 */
	void exitElse_if_block(pseudoParser.Else_if_blockContext ctx);
	/**
	 * Enter a parse tree produced by {@link pseudoParser#else_block}.
	 * @param ctx the parse tree
	 */
	void enterElse_block(pseudoParser.Else_blockContext ctx);
	/**
	 * Exit a parse tree produced by {@link pseudoParser#else_block}.
	 * @param ctx the parse tree
	 */
	void exitElse_block(pseudoParser.Else_blockContext ctx);
	/**
	 * Enter a parse tree produced by {@link pseudoParser#arg}.
	 * @param ctx the parse tree
	 */
	void enterArg(pseudoParser.ArgContext ctx);
	/**
	 * Exit a parse tree produced by {@link pseudoParser#arg}.
	 * @param ctx the parse tree
	 */
	void exitArg(pseudoParser.ArgContext ctx);
	/**
	 * Enter a parse tree produced by {@link pseudoParser#subroutine}.
	 * @param ctx the parse tree
	 */
	void enterSubroutine(pseudoParser.SubroutineContext ctx);
	/**
	 * Exit a parse tree produced by {@link pseudoParser#subroutine}.
	 * @param ctx the parse tree
	 */
	void exitSubroutine(pseudoParser.SubroutineContext ctx);
	/**
	 * Enter a parse tree produced by {@link pseudoParser#stat}.
	 * @param ctx the parse tree
	 */
	void enterStat(pseudoParser.StatContext ctx);
	/**
	 * Exit a parse tree produced by {@link pseudoParser#stat}.
	 * @param ctx the parse tree
	 */
	void exitStat(pseudoParser.StatContext ctx);
	/**
	 * Enter a parse tree produced by {@link pseudoParser#reveal_type}.
	 * @param ctx the parse tree
	 */
	void enterReveal_type(pseudoParser.Reveal_typeContext ctx);
	/**
	 * Exit a parse tree produced by {@link pseudoParser#reveal_type}.
	 * @param ctx the parse tree
	 */
	void exitReveal_type(pseudoParser.Reveal_typeContext ctx);
	/**
	 * Enter a parse tree produced by {@link pseudoParser#return_stat}.
	 * @param ctx the parse tree
	 */
	void enterReturn_stat(pseudoParser.Return_statContext ctx);
	/**
	 * Exit a parse tree produced by {@link pseudoParser#return_stat}.
	 * @param ctx the parse tree
	 */
	void exitReturn_stat(pseudoParser.Return_statContext ctx);
	/**
	 * Enter a parse tree produced by {@link pseudoParser#function_call}.
	 * @param ctx the parse tree
	 */
	void enterFunction_call(pseudoParser.Function_callContext ctx);
	/**
	 * Exit a parse tree produced by {@link pseudoParser#function_call}.
	 * @param ctx the parse tree
	 */
	void exitFunction_call(pseudoParser.Function_callContext ctx);
	/**
	 * Enter a parse tree produced by {@link pseudoParser#output}.
	 * @param ctx the parse tree
	 */
	void enterOutput(pseudoParser.OutputContext ctx);
	/**
	 * Exit a parse tree produced by {@link pseudoParser#output}.
	 * @param ctx the parse tree
	 */
	void exitOutput(pseudoParser.OutputContext ctx);
	/**
	 * Enter a parse tree produced by {@link pseudoParser#variable_assignment}.
	 * @param ctx the parse tree
	 */
	void enterVariable_assignment(pseudoParser.Variable_assignmentContext ctx);
	/**
	 * Exit a parse tree produced by {@link pseudoParser#variable_assignment}.
	 * @param ctx the parse tree
	 */
	void exitVariable_assignment(pseudoParser.Variable_assignmentContext ctx);
	/**
	 * Enter a parse tree produced by the {@code binary_expr}
	 * labeled alternative in {@link pseudoParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterBinary_expr(pseudoParser.Binary_exprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code binary_expr}
	 * labeled alternative in {@link pseudoParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitBinary_expr(pseudoParser.Binary_exprContext ctx);
	/**
	 * Enter a parse tree produced by the {@code index_expr}
	 * labeled alternative in {@link pseudoParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterIndex_expr(pseudoParser.Index_exprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code index_expr}
	 * labeled alternative in {@link pseudoParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitIndex_expr(pseudoParser.Index_exprContext ctx);
	/**
	 * Enter a parse tree produced by the {@code bool}
	 * labeled alternative in {@link pseudoParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterBool(pseudoParser.BoolContext ctx);
	/**
	 * Exit a parse tree produced by the {@code bool}
	 * labeled alternative in {@link pseudoParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitBool(pseudoParser.BoolContext ctx);
	/**
	 * Enter a parse tree produced by the {@code string}
	 * labeled alternative in {@link pseudoParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterString(pseudoParser.StringContext ctx);
	/**
	 * Exit a parse tree produced by the {@code string}
	 * labeled alternative in {@link pseudoParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitString(pseudoParser.StringContext ctx);
	/**
	 * Enter a parse tree produced by the {@code real}
	 * labeled alternative in {@link pseudoParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterReal(pseudoParser.RealContext ctx);
	/**
	 * Exit a parse tree produced by the {@code real}
	 * labeled alternative in {@link pseudoParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitReal(pseudoParser.RealContext ctx);
	/**
	 * Enter a parse tree produced by the {@code parenthesis_expr}
	 * labeled alternative in {@link pseudoParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterParenthesis_expr(pseudoParser.Parenthesis_exprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code parenthesis_expr}
	 * labeled alternative in {@link pseudoParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitParenthesis_expr(pseudoParser.Parenthesis_exprContext ctx);
	/**
	 * Enter a parse tree produced by the {@code int}
	 * labeled alternative in {@link pseudoParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterInt(pseudoParser.IntContext ctx);
	/**
	 * Exit a parse tree produced by the {@code int}
	 * labeled alternative in {@link pseudoParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitInt(pseudoParser.IntContext ctx);
	/**
	 * Enter a parse tree produced by the {@code array_expr}
	 * labeled alternative in {@link pseudoParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterArray_expr(pseudoParser.Array_exprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code array_expr}
	 * labeled alternative in {@link pseudoParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitArray_expr(pseudoParser.Array_exprContext ctx);
	/**
	 * Enter a parse tree produced by the {@code unary_expr}
	 * labeled alternative in {@link pseudoParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterUnary_expr(pseudoParser.Unary_exprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code unary_expr}
	 * labeled alternative in {@link pseudoParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitUnary_expr(pseudoParser.Unary_exprContext ctx);
	/**
	 * Enter a parse tree produced by the {@code field_access}
	 * labeled alternative in {@link pseudoParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterField_access(pseudoParser.Field_accessContext ctx);
	/**
	 * Exit a parse tree produced by the {@code field_access}
	 * labeled alternative in {@link pseudoParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitField_access(pseudoParser.Field_accessContext ctx);
	/**
	 * Enter a parse tree produced by the {@code user_input}
	 * labeled alternative in {@link pseudoParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterUser_input(pseudoParser.User_inputContext ctx);
	/**
	 * Exit a parse tree produced by the {@code user_input}
	 * labeled alternative in {@link pseudoParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitUser_input(pseudoParser.User_inputContext ctx);
	/**
	 * Enter a parse tree produced by the {@code variable}
	 * labeled alternative in {@link pseudoParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterVariable(pseudoParser.VariableContext ctx);
	/**
	 * Exit a parse tree produced by the {@code variable}
	 * labeled alternative in {@link pseudoParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitVariable(pseudoParser.VariableContext ctx);
	/**
	 * Enter a parse tree produced by the {@code function_call_expr}
	 * labeled alternative in {@link pseudoParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterFunction_call_expr(pseudoParser.Function_call_exprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code function_call_expr}
	 * labeled alternative in {@link pseudoParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitFunction_call_expr(pseudoParser.Function_call_exprContext ctx);
}