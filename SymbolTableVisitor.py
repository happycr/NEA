from SymbolTable import SymbolTable
from gen.pseudoVisitor import pseudoVisitor
from gen.pseudoParser import pseudoParser
from Errors import *
from Variable import Variable
from Function import Function
from record import Record
from Argument import Argument
from antlr4 import *


class SymbolTableVisitor(pseudoVisitor):
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
        self.visitChildren(ctx)

    def visitFunction_call(self, ctx: pseudoParser.Function_callContext):
        name = ctx.IDENTIFIER().getText()
        func = self.symbol_table.find_func(name)
        if not func: raise FunctionNotDefined(name)
        if len(ctx.expr()) != len(func.getArgs()): raise WrongNumberOfArguments(ctx)
        self.visitChildren(ctx)

    def visitVariable_assignment(self, ctx: pseudoParser.Variable_assignmentContext) -> None:
        if ctx.IDENTIFIER():
            name = ctx.IDENTIFIER().getText()
            self.symbol_table.add_var(Variable(name))
        self.visitChildren(ctx)

    def visitSubroutine(self, ctx: pseudoParser.SubroutineContext) -> None:
        name = ctx.IDENTIFIER().getText()
        func = self.symbol_table.find_func(name)
        if func: raise FunctionAlreadyDefined(name)
        self.symbol_table.add_func(Function(ctx))
        self.create_scope()
        self.visitChildren(ctx)
        self.destroy_scope()

    def visitIf_block(self, ctx: pseudoParser.If_blockContext) -> None:
        self.create_scope()
        self.visitChildren(ctx)
        self.destroy_scope()

    def visitFor_loop(self, ctx: pseudoParser.For_loopContext):
        self.create_scope()
        self.visitChildren(ctx)
        self.destroy_scope()

    def visitElse_block(self, ctx: pseudoParser.Else_blockContext):
        self.create_scope()
        self.visitChildren(ctx)
        self.destroy_scope()

    def visitElse_if_block(self, ctx: pseudoParser.Else_if_blockContext):
        self.create_scope()
        self.visitChildren(ctx)
        self.destroy_scope()

    def visitFor_loop_step(self, ctx: pseudoParser.For_loop_stepContext):
        self.create_scope()
        self.visitChildren(ctx)
        self.destroy_scope()

    def visitRepeat_until(self, ctx: pseudoParser.RecordContext):
        self.create_scope()
        self.visitChildren(ctx)
        self.destroy_scope()

    def visitWhile_loop(self, ctx: pseudoParser.While_loopContext):
        self.create_scope()
        self.visitChildren(ctx)
        self.destroy_scope()

    def visitRecord(self, ctx: pseudoParser.RecordContext):
        self.symbol_table.add_record(Record(ctx))
        self.visitChildren(ctx)

    def visitArg(self, ctx: pseudoParser.ArgContext):
        name = ctx.getText()
        self.symbol_table.add_var(Variable(name))
        self.visitChildren(ctx)
