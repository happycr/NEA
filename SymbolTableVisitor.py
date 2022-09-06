from SymbolTable import SymbolTable
from gen.pseudoVisitor import pseudoVisitor
from gen.pseudoParser import pseudoParser
from Errors import *
from Variable import Variable
from Function import Function
from Argument import  Argument
from antlr4 import *


class SymbolTableVisitor:
    def __init__(self):
        super().__init__()
        self.symbol_table = SymbolTable()

    def create_scope(self) -> None:
        self.symbol_table.create_scope()

    def destroy_scope(self) -> None:
        self.symbol_table.destroy_scope()

    def visitVariable(self, ctx: pseudoParser.VariableContext) -> None:
        name = ctx.getText()
        var = self.symbol_table.find_var(name)
        if not var: raise VariableNotDefined(name)

    def visitFunction_call(self, ctx: pseudoParser.Function_callContext):
        name = ctx.IDENTIFIER().getText()
        func = self.symbol_table.find_func(name)
        if not func: raise FunctionNotDefined(name)
        if len(ctx.expr()) != len(func.getArgs()): raise WrongNumberOfArguments(ctx)

    def visitVariable_assignment(self, ctx: pseudoParser.Variable_assignmentContext) -> None:
        if ctx.IDENTIFIER():
            name = ctx.IDENTIFIER().getText()
            self.symbol_table.add_var(Variable(name))

    def visitSubroutine(self, ctx: pseudoParser.SubroutineContext) -> None:
        self.symbol_table.add_func(Function(ctx))

    def visitArg(self, ctx: pseudoParser.ArgContext):
        name = ctx.getText()
        self.symbol_table.add_var(Variable(name))

    def visit(self, ctx):
        if isinstance(ctx, pseudoParser.Variable_assignmentContext):
            self.visitVariable_assignment(ctx)
        if isinstance(ctx, pseudoParser.VariableContext):
            self.visitVariable(ctx)
        if isinstance(ctx, pseudoParser.Function_callContext):
            self.visitFunction_call(ctx)
        if isinstance(ctx, pseudoParser.SubroutineContext):
            self.visitSubroutine(ctx)
        if isinstance(ctx, pseudoParser.ArgContext):
            self.visitArg(ctx)
