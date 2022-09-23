from typing import Callable, Any

import Errors
import Operations
import Util
import StackTrace
from SymbolTable import SymbolTable, Branch
from gen.pseudoVisitor import pseudoVisitor
from gen.pseudoParser import pseudoParser
from Errors import *
from Variable import Variable, ConstVariable
from Function import Function
import Types
from antlr4 import *
import copy
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
        self.stack_trace = StackTrace.StackTrace()
        self.current_branch = self.symbol_table

    def create_scope(self) -> None:
        self.symbol_table.create_scope()

    def destroy_scope(self) -> None:
        self.symbol_table.destroy_scope()

    def visitVariable(self, ctx: pseudoParser.VariableContext) -> Types.Type:
        name = ctx.getText()
        var = self.symbol_table.find_var(name)
        index = self.symbol_table.getIndex(name)
        if not var: raise VariableNotDefined(name)
        return Types.VariableReferenceType(name, self.symbol_table, index)
        # return_type = Types.String

    def visitSubroutineAtCallTime(self, ctx: pseudoParser.SubroutineContext):
        for i in ctx.block():
            self.visit(i)

    def visitFunction_call(self, ctx: pseudoParser.Function_callContext):
        name = ctx.IDENTIFIER().getText()
        func = self.symbol_table.find_func(name)
        _type = self.symbol_table.find_type(name)
        if _type: return self.visitConstructorCall(_type, ctx.expr())

        if not func: raise FunctionNotDefined(name)
        if len(ctx.expr()) != len(func.getArgs()): raise WrongNumberOfArguments(ctx)
        arguments = [self.visit(arg) for arg in ctx.expr()]
        self.create_scope()
        self.current_branch.create_frame(arguments, func)
        self.visitSubroutineAtCallTime(func.ctx)
        return_type = self.current_branch.destroy_frame()
        return return_type

    def visitConstructorCall(self, _type: Types.Type, arguments):
        argument_types = [self.visit(arg) for arg in arguments]
        if isinstance(_type, Types.UserDefinedType):
            field_types = list(_type.fields.items())
            if len(argument_types) != len(field_types):
                raise CustomError(f"Wrong number arguments for record {_type.getName()}")
            for i in range(len(argument_types)):
                if argument_types[i] != field_types[i][1]:
                    raise CustomError(
                        f"Wrong type in call to constructor for record {_type.getName()}, for field {field_types[i][0]}.")

        elif isinstance(_type, Types.PrimitiveType):
            if len(argument_types) > 1:
                raise CustomError(f"Wrong number arguments to initialize type {_type.getName()}")
        return _type

    def visitVariable_assignment(self, ctx: pseudoParser.Variable_assignmentContext) -> None:
        if ctx.IDENTIFIER():
            name = ctx.IDENTIFIER().getText()
            variable = self.current_branch.find_var(name)
            expr = self.visit(ctx.expr()[0]).getUnderlyingType()
            if not variable and not ctx.CONSTANT():
                self.current_branch.add_var(Variable(name, expr))
            elif not variable:
                self.current_branch.add_var(ConstVariable(name, expr))
            else:
                variable.assign(expr)
        else:
            lhs = self.visit(ctx.expr()[0])
            rhs = self.visit(ctx.expr()[1])
            lhs.assign(rhs)

    @ErrorManage
    def visitSubroutine(self, ctx: pseudoParser.SubroutineContext) -> None:
        name = ctx.IDENTIFIER().getText()
        func = self.symbol_table.find_func(name)
        if func: raise FunctionAlreadyDefined(name)
        self.symbol_table.add_func(Function(ctx))

    def visitCondition_sequence(self, ctx:pseudoParser.Condition_sequenceContext):
        parent_branch = self.current_branch
        branches = []
        for block in ctx.getChildren():
            branch = self.visit(block)
            self.current_branch = parent_branch
            branches.append(branch)
        for branch in branches:
            branch.destroy(parent_branch)


    @ErrorManage
    def visitIf_block(self, ctx: pseudoParser.If_blockContext) -> Branch:
        self.current_branch = Branch(self.current_branch)
        self.visitChildren(ctx)
        return self.current_branch


    def visitElse_block(self, ctx: pseudoParser.Else_blockContext):
        self.current_branch = Branch(self.current_branch)
        self.visitChildren(ctx)
        return self.current_branch

    @ErrorManage
    def visitElse_if_block(self, ctx: pseudoParser.Else_if_blockContext):
        self.current_branch = Branch(self.current_branch)
        self.visitChildren(ctx)
        return self.current_branch

    @ErrorManage
    def visitFor_loop(self, ctx: pseudoParser.For_loopContext):
        self.create_scope()
        self.visitChildren(ctx)
        self.destroy_scope()

    @ErrorManage
    def visitFor_loop_step(self, ctx: pseudoParser.For_loop_stepContext):
        self.create_scope()

        start, end = self.visit(ctx.expr()[0]), self.visit(ctx.expr()[1])
        step = Types.Int
        if ctx.step: step = self.visit(ctx.step)
        if (start, end, step) != (Types.Int, Types.Int, Types.Int):
            raise CustomError(f"For loops need to have start, step and end to be integers")

        new_var = Variable(ctx.IDENTIFIER().getText(), Types.Int)
        self.current_branch.add_var(new_var)
        self.visitChildren(ctx)
        self.destroy_scope()


    @ErrorManage
    def visitRepeat_until(self, ctx: pseudoParser.RecordContext):
        self.create_scope()
        self.visitChildren(ctx)
        self.destroy_scope()

    @ErrorManage
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

    def visitReveal_type(self, ctx: pseudoParser.Reveal_typeContext):
        expr = self.visit(ctx.expr())
        print(expr.getName())

    def visitInt(self, ctx: pseudoParser.IntContext):
        return Types.Int

    def visitReal(self, ctx: pseudoParser.RealContext):
        return Types.Real

    def visitBool(self, ctx: pseudoParser.BoolContext):
        return Types.Bool

    def visitString(self, ctx: pseudoParser.StringContext):
        if len(ctx.getText()) == 3: return Types.Char
        return Types.String

    def visitBinary_expr(self, ctx: pseudoParser.Binary_exprContext):
        lhs = self.visit(ctx.expr()[0]).getUnderlyingType()
        rhs = self.visit(ctx.expr()[1]).getUnderlyingType()
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

    def visitUnary_expr(self, ctx: pseudoParser.Unary_exprContext):
        arg = self.visit(ctx.expr())
        operand = ctx.op.text

        dict_of_operations = {
            'NOT': Operations.Not,
            '-': Operations.minus
        }
        return dict_of_operations[operand](arg)

    def visitField_access(self, ctx: pseudoParser.Field_accessContext):
        _object = self.visit(ctx.expr()).getUnderlyingType()
        field_name = ctx.IDENTIFIER().getText()

        @Util.Unionize
        def getField(_type):
            return_type = _type.getField(field_name)
            if return_type is None: raise CustomError(f"Type  {_type.getName()} does not have field {field_name}.")
            return return_type

        return Types.FieldAccess(field_name, getField(_object))

    def visitParenthesis_expr(self, ctx: pseudoParser.Parenthesis_exprContext):
        return self.visit(ctx.expr())

    @ErrorManage
    def visitStat(self, ctx: pseudoParser.StatContext):
        self.stack_trace.add_line(ctx.start.line, ctx.getText())
        return self.visitChildren(ctx)

    def visitArray_expr(self, ctx: pseudoParser.Array_exprContext):
        expr_set = Util.remove_duplicates([self.visit(expression).getUnderlyingType() for expression in ctx.expr()])
        if len(expr_set) == 1:
            return Types.ArrayType(expr_set.pop())
        else:
            return Types.ArrayType(Types.UnionType(expr_set))

    def visitIndex_expr(self, ctx: pseudoParser.Index_exprContext):
        first_expr = self.visit(ctx.expr()[0])
        second_expr = self.visit(ctx.expr()[1])

        if second_expr != Types.Int:
            raise Errors.CustomError(
                f"Indexing only supported with type Integer, not with type {second_expr.getName()}")

        getElement = first_expr.getElement()
        return getElement

    def visitReturn_stat(self, ctx: pseudoParser.Return_statContext):
        expr = self.visit(ctx.expr())
        self.current_branch.setReturnType(expr)
