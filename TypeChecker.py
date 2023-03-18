from typing import Callable, Any

import Errors
from Operations import Operations
from SymbolTable import SymbolTable, Branch
from gen.pseudoVisitor import pseudoVisitor
from gen.pseudoParser import pseudoParser
from Errors import *
from Variable import Variable, ConstVariable
from Function import Function
import Types
from Unionise import Unionise
from antlr4 import *

"""
This higher order function defines a decorator in order for methods to deal with errors.
"""


def ErrorManage(func: Callable[[pseudoVisitor, ParserRuleContext], Any]):
    def inner(self, ctx):
        try:
            # Try to call function
            return func(self, ctx)
        except TranslationError as e:
            # If error, add ctx to stack trace
            e.__stack_trace.add_ctx(ctx)
            raise e

    return inner


"""
This class is responsible for raising any type errors
"""


class TypeChecker(pseudoVisitor):

    def __init__(self):
        super().__init__()
        # The symbol table, which stores types of variables and functions
        self.__symbol_table = SymbolTable()
        # The current branch we are in, initialized to the symbol table as a default.
        self.__current_branch = self.__symbol_table

    def create_scope(self) -> None:
        self.__current_branch.create_scope()

    def destroy_scope(self) -> None:
        self.__current_branch.destroy_scope()

    def visitVariable(self, ctx: pseudoParser.VariableContext) -> Types.Type:
        # Get name of variable
        name = ctx.getText()
        # Find variable object
        var = self.__current_branch.find_var(name)
        # Find index of variable object
        index = self.__current_branch.getIndex(name)
        # Raise an error if no variable exists
        if not var: raise TranslationError(f"Variable {name} not defined")
        # Return variable reference types to deal with assignment to variables.
        return Types.VariableReferenceType(self.__current_branch, index)

    def visitSubroutineAtCallTime(self, ctx: pseudoParser.SubroutineContext) -> None:
        # Visit each block of the subroutine when it is called.
        for i in ctx.block():
            self.visit(i)

    @ErrorManage
    def visitFunction_call(self, ctx: pseudoParser.Function_callContext) -> Types.Type:
        # Get name of function
        name = ctx.IDENTIFIER().getText()
        # Treat the append function specially
        if name == "append":
            self.visitAppend(ctx)
            return Types.none
        # Get function object from symbol table
        func = self.__symbol_table.find_func(name)
        # Get type object from symbol table. This is needed when we have a constructor call, for example Integer(5.0).
        # Integer is not a function but a type, so we need to retrieve it from the symbol table.
        _type = self.__symbol_table.find_type(name)
        # If we have a constructor call, then call appropriate method
        if _type: return self.visitConstructorCall(_type, ctx.expr())
        # At this point we are guaranteed that we do not have a constructor call but a function call
        # If the function does not exist, raise an error
        if not func: raise TranslationError(f"Function {name} not defined")

        # Make sure we have the right number of arguments.
        if len(ctx.expr()) != len(func.getArgs()):
            raise TranslationError(f"Wrong number of arguments for function {name}.")
        # Get arguments
        # Note that we do NOT use getUnderlyingType().
        # This is because we conserve references, and so any changes made to variables will be conserved.
        arguments = [self.visit(arg) for arg in ctx.expr()]
        # Create subroutine frame as we enter its body
        self.__current_branch.create_frame(arguments, func)
        # Visit body of subroutine
        self.visitSubroutineAtCallTime(func.getCtx())
        # Get return type
        return_type = self.__current_branch.destroy_frame()
        return return_type

    def visitConstructorCall(self, _type: Types.Type, arguments) -> Types.Type:
        # Get types of arguments
        argument_types = [self.visit(arg) for arg in arguments]
        # Case when the type is a user defined record
        if isinstance(_type, Types.UserDefinedType):
            # Get types of fields in the record
            field_types = list(_type.getFields().items())
            # Check we have the right number of arguments
            if len(argument_types) != len(field_types):
                raise TranslationError(f"Wrong number of arguments for record {_type.getName()}")
            # Check that each argument matches the required type for each field
            for i in range(len(argument_types)):
                name_of_field = field_types[i][0]
                _type_of_field = field_types[i][1]
                if argument_types[i] != _type_of_field:
                    raise TranslationError(
                        f"Wrong type in call to constructor for record {_type.getName()}, for field {name_of_field}.")
        # Case when the type is a primitive type: Integer, String, Real ...
        elif isinstance(_type, Types.PrimitiveType):
            if len(argument_types) > 1:
                raise TranslationError(f"Wrong number of arguments to initialize type {_type.getName()}")
            argument = argument_types[0]
            # Check that we can convert the argument to _type
            if isinstance(argument, Types.UserDefinedType):
                raise TranslationError(f"Cannot convert {argument.getName()} to a {_type.getName()}")
            # We can convert any primitive types to any primitive types: ie Integer(5.0), String(True)... are all valid
            # So there is no need to check in that case
        return _type

    @ErrorManage
    def visitAppend(self, ctx):
        arguments = [self.visit(arg) for arg in ctx.expr()]
        if len(arguments) != 2:
            raise TranslationError(f"Wrong number of arguments for function append.")
        array = arguments[0]
        obj_to_append = arguments[1]
        # Update element type of array
        element_type = array.getElement()
        if isinstance(element_type, Types.ReferenceType):
            element_type.assign(obj_to_append.getUnderlyingType())

    @ErrorManage
    def visitVariable_assignment(self, ctx: pseudoParser.Variable_assignmentContext) -> None:
        # Case when we are assigning to a variable, eg x <- 5
        if ctx.IDENTIFIER():
            # Get name of variable
            name = ctx.IDENTIFIER().getText()
            # Get variable object
            variable = self.__current_branch.find_var(name)
            # Get expression type
            expr = self.visit(ctx.expr()[0]).getUnderlyingType()
            if isinstance(expr, Types.ConstType): expr = expr.getType()  # type: ignore
            # If variable does not exist yet, and CONST was not specified, create a new normal variable.
            if not variable and not ctx.CONSTANT():
                self.__current_branch.add_var(Variable(name, expr))
            # If variable does not exist yet, and CONST was specified, create a new CONST variable
            elif not variable:
                self.__current_branch.add_var(ConstVariable(name, expr))
            # If variable already exists, but is marked CONST, raise an error
            elif variable and ctx.CONSTANT():
                raise Errors.TranslationError(f"Cannot redefine the constant variable {name}.")
            # If variable already exists, and is not CONST, assign new type to variable.
            else:
                # Not that we are using getUnderlyingType, we are deep copying here.
                variable.assign(expr.getUnderlyingType())
        # In this case we are assigning to an expression, eg x[0] <- 5
        else:
            # Get lhs
            lhs = self.visit(ctx.expr()[0])
            # Get rhs
            rhs = self.visit(ctx.expr()[1])
            if isinstance(rhs, Types.ConstType): expr = rhs.getType()  # type: ignore

            # Assign rhs to lhs
            lhs.assign(rhs)

    @ErrorManage
    def visitSubroutine(self, ctx: pseudoParser.SubroutineContext) -> None:
        # Get name
        name = ctx.IDENTIFIER().getText()
        # Get function object
        func = self.__symbol_table.find_func(name)
        # Raise an error if we are redefining a function
        if func: raise TranslationError(f"Function {name} already defined")
        # Add function to symbol table
        self.__symbol_table.add_func(Function(ctx))

    def visitCondition_sequence(self, ctx: pseudoParser.Condition_sequenceContext) -> None:
        # Store current branch into parent branch for later use.
        parent_branch = self.__current_branch
        branches = []
        for block in list(ctx.getChildren())[:-1]:
            # Get branch object from visiting block (which is an if/else if block)
            branch = self.visit(block)
            # Assign current branch back to parent branch ( that was changed while visiting the block)
            self.__current_branch = parent_branch
            # Append the branch we obtained and store for later use
            branches.append(branch)
        # Check whether we have an else block.
        # This is important because it determines whether we completely override the type of objects or not.
        # For example, in this program:
        # x <- 10
        # IF some_condition THEN x <- "Hello World"
        # ELSE x <- "Hello Again" ENDIF
        # The type of x here is String, since all code paths have assigned x to a string.
        # If there was no ELSE block, x could still be an Integer.
        if ctx.else_block():
            first_branch = branches[0]
            # In the first branch, completely overwrite the type of variables
            first_branch.destroy_first(branches)
        else:
            first_branch = branches[0]
            # Do not completely overwrite the type of variables if there was no else block
            first_branch.destroy()
        for branch in branches[1:]:
            # Add other types from other branches.
            # No need to overwrite type of variables since the first branch has already done that.
            branch.destroy()

    @ErrorManage
    def visitIf_block(self, ctx: pseudoParser.If_blockContext) -> Branch:
        # Create new branch and set current branch to it.
        self.__current_branch = Branch(self.__current_branch)
        self.visitChildren(ctx)
        # Return branch
        return self.__current_branch

    def visitElse_block(self, ctx: pseudoParser.Else_blockContext) -> Branch:
        self.__current_branch = Branch(self.__current_branch)
        self.visitChildren(ctx)
        return self.__current_branch

    @ErrorManage
    def visitElse_if_block(self, ctx: pseudoParser.Else_if_blockContext) -> Branch:
        self.__current_branch = Branch(self.__current_branch)
        self.visitChildren(ctx)
        return self.__current_branch

    @ErrorManage
    def visitFor_loop(self, ctx: pseudoParser.For_loopContext) -> None:
        self.create_scope()
        expr = self.visit(ctx.expr())
        # Check whether expression is an array, to iterate over it.
        if not isinstance(expr.getUnderlyingType(), Types.ArrayType):
            raise TranslationError(f"Cannot iterate on non iterable type {expr.getUnderlyingType().getName()}")
        # Create new iterable variable.
        new_var = Variable(ctx.IDENTIFIER().getText(), expr.getElement())
        self.__current_branch.add_var(new_var)

        # Visit body twice as the body of a for loop can be repeated during the execution of a program.
        # The state of the program types might be changed after the first execution of the loop.
        # So we visit the body twice:
        # 1) With the for loop not having been executed at all (first pass)
        # 2) With the for loop  having been executed at least once(second pass)
        # Two passes are sufficient as we consider all possible code paths each pass.

        self.visitChildren(ctx)
        self.visitChildren(ctx)
        self.destroy_scope()

    @ErrorManage
    def visitFor_loop_step(self, ctx: pseudoParser.For_loop_stepContext) -> None:
        self.create_scope()
        # Get start end
        start, end = self.visit(ctx.expr()[0]).getUnderlyingType(), self.visit(ctx.expr()[1]).getUnderlyingType()
        step = Types.Int
        if ctx.step: step = self.visit(ctx.step).getUnderlyingType()
        # Check start, end, step are all Integers.
        if (start, end, step) != (Types.Int, Types.Int, Types.Int):
            raise TranslationError(f"For loops need to have start, step and end to be integers")

        # Create new iterable variable.
        new_var = Variable(ctx.IDENTIFIER().getText(), Types.Int)
        self.__current_branch.add_var(new_var)

        # Visit body twice, just like for a FOR loop.
        self.visitChildren(ctx)
        self.visitChildren(ctx)
        self.destroy_scope()

    @ErrorManage
    def visitRepeat_until(self, ctx: pseudoParser.RecordContext) -> None:
        self.create_scope()

        # Visit body twice, just like for a FOR loop.
        self.visitChildren(ctx)
        self.visitChildren(ctx)
        self.destroy_scope()

    @ErrorManage
    def visitWhile_loop(self, ctx: pseudoParser.While_loopContext) -> None:
        self.create_scope()

        # Visit body twice, just like for a FOR loop.
        self.visitChildren(ctx)
        self.visitChildren(ctx)
        self.destroy_scope()

    @ErrorManage
    def visitRecord(self, ctx: pseudoParser.RecordContext) -> None:
        fields = {}
        record_name = ctx.IDENTIFIER().getText()
        # Create fields dict.
        for field in ctx.field():
            name = field.IDENTIFIER()[0].getText()
            _type_name = field.IDENTIFIER()[1].getText()
            _type = self.__symbol_table.find_type(_type_name)
            # Raise error if type of field is not defined
            if _type is None:
                raise TranslationError(f"Invalid type for field {name} in record {record_name}")
            fields[name] = _type
        # Define new type for the new record.
        self.__symbol_table.add_type(Types.UserDefinedType(record_name, fields))

    def visitReveal_type(self, ctx: pseudoParser.Reveal_typeContext) -> None:
        expr = self.visit(ctx.expr())
        print(expr.getName())

    def visitInt(self, ctx: pseudoParser.IntContext) -> Types.Type:
        return Types.Int

    def visitReal(self, ctx: pseudoParser.RealContext) -> Types.Type:
        return Types.Real

    def visitBool(self, ctx: pseudoParser.BoolContext) -> Types.Type:
        return Types.Bool

    def visitString(self, ctx: pseudoParser.StringContext) -> Types.Type:
        return Types.String

    def visitBinary_expr(self, ctx: pseudoParser.Binary_exprContext) -> Types.Type:
        lhs = self.visit(ctx.expr()[0]).getUnderlyingType()
        rhs = self.visit(ctx.expr()[1])
        operand = ctx.op.text
        # Call appropriate function depending on the operator.
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

    def visitUnary_expr(self, ctx: pseudoParser.Unary_exprContext) -> Types.Type:
        arg = self.visit(ctx.expr())
        operand = ctx.op.text
        dict_of_operations = {
            'NOT': Operations.Not,
            '-': Operations.minus
        }
        return dict_of_operations[operand](arg)

    def visitField_access(self, ctx: pseudoParser.Field_accessContext) -> Types.Type:
        # Get object and field name
        _object = self.visit(ctx.expr())
        field_name = ctx.IDENTIFIER().getText()

        # Define an inner function and use the Unionize decorator to deal with union types.
        @Unionise
        def getField(_type) -> Types.Type:
            # Get type of field
            return_type = _type.getField(field_name)
            # If field is not defined, raise error
            if return_type is None: raise TranslationError(f"Type  {_type.getName()} does not have field {field_name}.")
            return return_type

        # Create a Types.FieldAccess object to deal with assignment.
        return Types.FieldAccess(field_name, getField(_object))

    def visitParenthesis_expr(self, ctx: pseudoParser.Parenthesis_exprContext) -> Types.Type:
        return self.visit(ctx.expr())

    @ErrorManage
    def visitStat(self, ctx: pseudoParser.StatContext) -> None:
        self.visitChildren(ctx)

    @ErrorManage
    def visitBlock(self, ctx: pseudoParser.BlockContext) -> None:
        self.visitChildren(ctx)

    def visitArray_expr(self, ctx: pseudoParser.Array_exprContext) -> Types.Type:
        # Get type of every element in array.
        expressions = [self.visit(expression).getUnderlyingType() for expression in ctx.expr()]
        if len(expressions) == 1:
            # If array is already homogeneous, return appropriate type.
            return Types.ArrayType(expressions.pop())
        else:
            # Array element type is the union of all the types of the expressions
            return Types.ArrayType(Types.UnionType(expressions))

    def visitIndex_expr(self, ctx: pseudoParser.Index_exprContext) -> Types.Type:
        first_expr = self.visit(ctx.expr()[0])
        second_expr = self.visit(ctx.expr()[1])
        # Check index is an integer
        if second_expr.getUnderlyingType() != Types.Int:
            raise Errors.TranslationError(
                f"Indexing only supported with type Integer, not with type {second_expr.getName()}")
        # Get type using getElement method
        getElement = first_expr.getElement()
        return getElement

    def visitReturn_stat(self, ctx: pseudoParser.Return_statContext) -> None:
        expr = self.visit(ctx.expr())
        # Set return type.
        self.__current_branch.setReturnType(expr)

    def visitUser_input(self, ctx: pseudoParser.User_inputContext) -> Types.Type:
        return Types.String
