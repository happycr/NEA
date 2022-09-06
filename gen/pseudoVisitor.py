# Generated from /Users/cyruslinden/PycharmProjects/NEA/pseudo.g4 by ANTLR 4.9.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .pseudoParser import pseudoParser
else:
    from pseudoParser import pseudoParser

# This class defines a complete generic visitor for a parse tree produced by pseudoParser.

class pseudoVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by pseudoParser#prog.
    def visitProg(self, ctx:pseudoParser.ProgContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pseudoParser#block.
    def visitBlock(self, ctx:pseudoParser.BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pseudoParser#repeat_until.
    def visitRepeat_until(self, ctx:pseudoParser.Repeat_untilContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pseudoParser#while_loop.
    def visitWhile_loop(self, ctx:pseudoParser.While_loopContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pseudoParser#for_loop_step.
    def visitFor_loop_step(self, ctx:pseudoParser.For_loop_stepContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pseudoParser#for_loop.
    def visitFor_loop(self, ctx:pseudoParser.For_loopContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pseudoParser#if_block.
    def visitIf_block(self, ctx:pseudoParser.If_blockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pseudoParser#record.
    def visitRecord(self, ctx:pseudoParser.RecordContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pseudoParser#field.
    def visitField(self, ctx:pseudoParser.FieldContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pseudoParser#else_if_block.
    def visitElse_if_block(self, ctx:pseudoParser.Else_if_blockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pseudoParser#else_block.
    def visitElse_block(self, ctx:pseudoParser.Else_blockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pseudoParser#arg.
    def visitArg(self, ctx:pseudoParser.ArgContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pseudoParser#subroutine.
    def visitSubroutine(self, ctx:pseudoParser.SubroutineContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pseudoParser#stat.
    def visitStat(self, ctx:pseudoParser.StatContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pseudoParser#return_stat.
    def visitReturn_stat(self, ctx:pseudoParser.Return_statContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pseudoParser#function_call.
    def visitFunction_call(self, ctx:pseudoParser.Function_callContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pseudoParser#output.
    def visitOutput(self, ctx:pseudoParser.OutputContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pseudoParser#variable_assignment.
    def visitVariable_assignment(self, ctx:pseudoParser.Variable_assignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pseudoParser#unary_expr.
    def visitUnary_expr(self, ctx:pseudoParser.Unary_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pseudoParser#binary_expr.
    def visitBinary_expr(self, ctx:pseudoParser.Binary_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pseudoParser#index_expr.
    def visitIndex_expr(self, ctx:pseudoParser.Index_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pseudoParser#field_access.
    def visitField_access(self, ctx:pseudoParser.Field_accessContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pseudoParser#user_input.
    def visitUser_input(self, ctx:pseudoParser.User_inputContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pseudoParser#variable.
    def visitVariable(self, ctx:pseudoParser.VariableContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pseudoParser#parenthesis_expr.
    def visitParenthesis_expr(self, ctx:pseudoParser.Parenthesis_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pseudoParser#function_call_expr.
    def visitFunction_call_expr(self, ctx:pseudoParser.Function_call_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pseudoParser#array_expr.
    def visitArray_expr(self, ctx:pseudoParser.Array_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pseudoParser#literal.
    def visitLiteral(self, ctx:pseudoParser.LiteralContext):
        return self.visitChildren(ctx)



del pseudoParser