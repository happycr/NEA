from typing import Callable, Any

import Operations
from SymbolTable import SymbolTable
from gen.pseudoVisitor import pseudoVisitor
from gen.pseudoParser import pseudoParser
from Errors import *
from Variable import Variable
from Function import Function
import Types
from antlr4 import *


def ErrorManage(func: Callable[[pseudoVisitor, ParserRuleContext], Any]):
    def inner(self, ctx):
        try:
            return func(self, ctx)
        except TranslationError as e:
            if e.line is None:
                e.line = ctx.start.line
            raise e

    return inner


class SymbolTableVisitor(pseudoVisitor):

    def __init__(self):
        super().__init__()
        self.symbol_table = SymbolTable()

    def create_scope(self) -> None:
        self.symbol_table.create_scope()

    def destroy_scope(self) -> None:
        self.symbol_table.destroy_scope()

    @ErrorManage
    def visitVariable(self, ctx: pseudoParser.VariableContext) -> Types.Type:
        name = ctx.getText()
        var = self.symbol_table.find_var(name)
        if not var: raise VariableNotDefined(name)
        return var.type

    @ErrorManage
    def visitFunction_call(self, ctx: pseudoParser.Function_callContext):
        name = ctx.IDENTIFIER().getText()
        func = self.symbol_table.find_func(name)
        _type = self.symbol_table.find_type(name)
        if _type: return self.visitConstructorCall(_type, ctx.expr())

        if not func: raise FunctionNotDefined(name)
        if len(ctx.expr()) != len(func.getArgs()): raise WrongNumberOfArguments(ctx)

    def visitConstructorCall(self, _type: Types.Type, arguments):
        argument_types = [self.visit(arg) for arg in arguments]
        if isinstance(_type, Types.UserDefinedType):
            field_types = list(_type.fields.items())
            if len(argument_types) != len(field_types):
                raise CustomError(f"Wrong number arguments for record {_type.name}")
            for i in range(len(argument_types)):
                if argument_types[i] != field_types[i][1]:
                    raise CustomError(
                        f"Wrong type in call to constructor for record {_type.name}, for field {field_types[i][0]}.")

        elif isinstance(_type, Types.PrimitiveType):
            if len(argument_types) > 1:
                raise CustomError(f"Wrong number arguments to initialize type {_type.name}")
        return _type

    def visitVariable_assignment(self, ctx: pseudoParser.Variable_assignmentContext) -> None:
        if ctx.IDENTIFIER():
            name = ctx.IDENTIFIER().getText()
            variable = self.symbol_table.find_var(name)
            expr = self.visit(ctx.expr()[0])
            if not variable:
                self.symbol_table.add_var(Variable(name, expr))
            else:
                variable.type = expr

    @ErrorManage
    def visitSubroutine(self, ctx: pseudoParser.SubroutineContext) -> None:
        name = ctx.IDENTIFIER().getText()
        func = self.symbol_table.find_func(name)
        if func: raise FunctionAlreadyDefined(name)
        self.symbol_table.add_func(Function(ctx))

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

    @ErrorManage
    def visitRecord(self, ctx: pseudoParser.RecordContext) -> None:
        fields = {}
        record_name = ctx.IDENTIFIER().getText()
        for field in ctx.field():
            name = field.IDENTIFIER()[0].getText()
            _type_name = field.IDENTIFIER()[1].getText()
            _type = self.symbol_table.find_type(_type_name)
            if _type is None:
                raise CustomError(f"Invalid type for field {name} in record {record_name}")
            fields[name] = _type

        self.symbol_table.add_type(Types.UserDefinedType(record_name, fields))

    def visitArg(self, ctx: pseudoParser.ArgContext):
        name = ctx.getText()

        # ERROR, NEED TO PUT TYPE
        self.symbol_table.add_var(Variable(name))
        self.visitChildren(ctx)

    def visitReveal_type(self, ctx: pseudoParser.Reveal_typeContext):
        expr = self.visit(ctx.expr())
        print(expr.name)

    def visitInt(self, ctx: pseudoParser.IntContext):
        return Types.Int

    def visitReal(self, ctx: pseudoParser.RealContext):
        return Types.Real

    def visitBool(self, ctx: pseudoParser.BoolContext):
        return Types.Bool

    def visitString(self, ctx: pseudoParser.StringContext):
        return Types.String

    @ErrorManage
    def visitBinary_expr(self, ctx: pseudoParser.Binary_exprContext):
        lhs = self.visit(ctx.expr()[0])
        rhs = self.visit(ctx.expr()[1])
        operand = ctx.op.text
        dict_of_operations = {
            '+': Operations.add,
            '*': Operations.multiply,
            '-': Operations.subtract,
            '/': Operations.divide,
            'MOD': Operations.mod,
            'DIV': Operations.div,
            '<': Operations.compare,
            '>': Operations.compare,
            '=': Operations.compare,
            '≠': Operations.compare,
            '≤': Operations.compare,
            '≥': Operations.compare,
            'AND': Operations.bool_operation,
            'OR': Operations.bool_operation
        }
        return dict_of_operations[operand](lhs, rhs)

    @ErrorManage
    def visitUnary_expr(self, ctx: pseudoParser.Unary_exprContext):
        arg = self.visit(ctx.expr())
        operand = ctx.op.text

        dict_of_operations = {
            'NOT': Operations.Not,
            '-': Operations.minus
        }
        return dict_of_operations[operand](arg)

    @ErrorManage
    def visitField_access(self, ctx: pseudoParser.Field_accessContext):
        _object = self.visit(ctx.expr())
        field_name = ctx.IDENTIFIER().getText()
        @Operations.Unionize
        def getField(_type):
            return_type = _type.getField(field_name)
            if return_type is None: raise CustomError(f"Type  {_type.name} does not have field {field_name}.")
            return return_type

        return getField(_object)

    def visitParenthesis_expr(self, ctx: pseudoParser.Parenthesis_exprContext):
        return self.visit(ctx.expr())
