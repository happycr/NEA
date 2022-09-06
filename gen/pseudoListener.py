# Generated from /Users/cyruslinden/PycharmProjects/NEA/pseudo.g4 by ANTLR 4.9.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .pseudoParser import pseudoParser
else:
    from pseudoParser import pseudoParser

# This class defines a complete listener for a parse tree produced by pseudoParser.
class pseudoListener(ParseTreeListener):

    # Enter a parse tree produced by pseudoParser#prog.
    def enterProg(self, ctx:pseudoParser.ProgContext):
        pass

    # Exit a parse tree produced by pseudoParser#prog.
    def exitProg(self, ctx:pseudoParser.ProgContext):
        pass


    # Enter a parse tree produced by pseudoParser#block.
    def enterBlock(self, ctx:pseudoParser.BlockContext):
        pass

    # Exit a parse tree produced by pseudoParser#block.
    def exitBlock(self, ctx:pseudoParser.BlockContext):
        pass


    # Enter a parse tree produced by pseudoParser#repeat_until.
    def enterRepeat_until(self, ctx:pseudoParser.Repeat_untilContext):
        pass

    # Exit a parse tree produced by pseudoParser#repeat_until.
    def exitRepeat_until(self, ctx:pseudoParser.Repeat_untilContext):
        pass


    # Enter a parse tree produced by pseudoParser#while_loop.
    def enterWhile_loop(self, ctx:pseudoParser.While_loopContext):
        pass

    # Exit a parse tree produced by pseudoParser#while_loop.
    def exitWhile_loop(self, ctx:pseudoParser.While_loopContext):
        pass


    # Enter a parse tree produced by pseudoParser#for_loop_step.
    def enterFor_loop_step(self, ctx:pseudoParser.For_loop_stepContext):
        pass

    # Exit a parse tree produced by pseudoParser#for_loop_step.
    def exitFor_loop_step(self, ctx:pseudoParser.For_loop_stepContext):
        pass


    # Enter a parse tree produced by pseudoParser#for_loop.
    def enterFor_loop(self, ctx:pseudoParser.For_loopContext):
        pass

    # Exit a parse tree produced by pseudoParser#for_loop.
    def exitFor_loop(self, ctx:pseudoParser.For_loopContext):
        pass


    # Enter a parse tree produced by pseudoParser#if_block.
    def enterIf_block(self, ctx:pseudoParser.If_blockContext):
        pass

    # Exit a parse tree produced by pseudoParser#if_block.
    def exitIf_block(self, ctx:pseudoParser.If_blockContext):
        pass


    # Enter a parse tree produced by pseudoParser#record.
    def enterRecord(self, ctx:pseudoParser.RecordContext):
        pass

    # Exit a parse tree produced by pseudoParser#record.
    def exitRecord(self, ctx:pseudoParser.RecordContext):
        pass


    # Enter a parse tree produced by pseudoParser#field.
    def enterField(self, ctx:pseudoParser.FieldContext):
        pass

    # Exit a parse tree produced by pseudoParser#field.
    def exitField(self, ctx:pseudoParser.FieldContext):
        pass


    # Enter a parse tree produced by pseudoParser#else_if_block.
    def enterElse_if_block(self, ctx:pseudoParser.Else_if_blockContext):
        pass

    # Exit a parse tree produced by pseudoParser#else_if_block.
    def exitElse_if_block(self, ctx:pseudoParser.Else_if_blockContext):
        pass


    # Enter a parse tree produced by pseudoParser#else_block.
    def enterElse_block(self, ctx:pseudoParser.Else_blockContext):
        pass

    # Exit a parse tree produced by pseudoParser#else_block.
    def exitElse_block(self, ctx:pseudoParser.Else_blockContext):
        pass


    # Enter a parse tree produced by pseudoParser#arg.
    def enterArg(self, ctx:pseudoParser.ArgContext):
        pass

    # Exit a parse tree produced by pseudoParser#arg.
    def exitArg(self, ctx:pseudoParser.ArgContext):
        pass


    # Enter a parse tree produced by pseudoParser#subroutine.
    def enterSubroutine(self, ctx:pseudoParser.SubroutineContext):
        pass

    # Exit a parse tree produced by pseudoParser#subroutine.
    def exitSubroutine(self, ctx:pseudoParser.SubroutineContext):
        pass


    # Enter a parse tree produced by pseudoParser#stat.
    def enterStat(self, ctx:pseudoParser.StatContext):
        pass

    # Exit a parse tree produced by pseudoParser#stat.
    def exitStat(self, ctx:pseudoParser.StatContext):
        pass


    # Enter a parse tree produced by pseudoParser#return_stat.
    def enterReturn_stat(self, ctx:pseudoParser.Return_statContext):
        pass

    # Exit a parse tree produced by pseudoParser#return_stat.
    def exitReturn_stat(self, ctx:pseudoParser.Return_statContext):
        pass


    # Enter a parse tree produced by pseudoParser#function_call.
    def enterFunction_call(self, ctx:pseudoParser.Function_callContext):
        pass

    # Exit a parse tree produced by pseudoParser#function_call.
    def exitFunction_call(self, ctx:pseudoParser.Function_callContext):
        pass


    # Enter a parse tree produced by pseudoParser#output.
    def enterOutput(self, ctx:pseudoParser.OutputContext):
        pass

    # Exit a parse tree produced by pseudoParser#output.
    def exitOutput(self, ctx:pseudoParser.OutputContext):
        pass


    # Enter a parse tree produced by pseudoParser#variable_assignment.
    def enterVariable_assignment(self, ctx:pseudoParser.Variable_assignmentContext):
        pass

    # Exit a parse tree produced by pseudoParser#variable_assignment.
    def exitVariable_assignment(self, ctx:pseudoParser.Variable_assignmentContext):
        pass


    # Enter a parse tree produced by pseudoParser#unary_expr.
    def enterUnary_expr(self, ctx:pseudoParser.Unary_exprContext):
        pass

    # Exit a parse tree produced by pseudoParser#unary_expr.
    def exitUnary_expr(self, ctx:pseudoParser.Unary_exprContext):
        pass


    # Enter a parse tree produced by pseudoParser#binary_expr.
    def enterBinary_expr(self, ctx:pseudoParser.Binary_exprContext):
        pass

    # Exit a parse tree produced by pseudoParser#binary_expr.
    def exitBinary_expr(self, ctx:pseudoParser.Binary_exprContext):
        pass


    # Enter a parse tree produced by pseudoParser#index_expr.
    def enterIndex_expr(self, ctx:pseudoParser.Index_exprContext):
        pass

    # Exit a parse tree produced by pseudoParser#index_expr.
    def exitIndex_expr(self, ctx:pseudoParser.Index_exprContext):
        pass


    # Enter a parse tree produced by pseudoParser#field_access.
    def enterField_access(self, ctx:pseudoParser.Field_accessContext):
        pass

    # Exit a parse tree produced by pseudoParser#field_access.
    def exitField_access(self, ctx:pseudoParser.Field_accessContext):
        pass


    # Enter a parse tree produced by pseudoParser#user_input.
    def enterUser_input(self, ctx:pseudoParser.User_inputContext):
        pass

    # Exit a parse tree produced by pseudoParser#user_input.
    def exitUser_input(self, ctx:pseudoParser.User_inputContext):
        pass


    # Enter a parse tree produced by pseudoParser#variable.
    def enterVariable(self, ctx:pseudoParser.VariableContext):
        pass

    # Exit a parse tree produced by pseudoParser#variable.
    def exitVariable(self, ctx:pseudoParser.VariableContext):
        pass


    # Enter a parse tree produced by pseudoParser#parenthesis_expr.
    def enterParenthesis_expr(self, ctx:pseudoParser.Parenthesis_exprContext):
        pass

    # Exit a parse tree produced by pseudoParser#parenthesis_expr.
    def exitParenthesis_expr(self, ctx:pseudoParser.Parenthesis_exprContext):
        pass


    # Enter a parse tree produced by pseudoParser#function_call_expr.
    def enterFunction_call_expr(self, ctx:pseudoParser.Function_call_exprContext):
        pass

    # Exit a parse tree produced by pseudoParser#function_call_expr.
    def exitFunction_call_expr(self, ctx:pseudoParser.Function_call_exprContext):
        pass


    # Enter a parse tree produced by pseudoParser#array_expr.
    def enterArray_expr(self, ctx:pseudoParser.Array_exprContext):
        pass

    # Exit a parse tree produced by pseudoParser#array_expr.
    def exitArray_expr(self, ctx:pseudoParser.Array_exprContext):
        pass


    # Enter a parse tree produced by pseudoParser#literal.
    def enterLiteral(self, ctx:pseudoParser.LiteralContext):
        pass

    # Exit a parse tree produced by pseudoParser#literal.
    def exitLiteral(self, ctx:pseudoParser.LiteralContext):
        pass



del pseudoParser