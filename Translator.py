from gen.pseudoVisitor import pseudoVisitor
from gen.pseudoParser import pseudoParser
from GenericVisitor import GenericVisitor

"""
This class is responsible for translating the pseudocode into python.
It inherits from both pseudoVisitor (the ANTLR generated visitor class), 
and Generic visitor, which contains some utility methods.
"""


class Translator(pseudoVisitor, GenericVisitor):

    def __init__(self):
        super(pseudoVisitor, self).__init__()
        super(GenericVisitor, self).__init__()

    def visitProg(self, ctx: pseudoParser.ProgContext):
        return self.visit_list(list(ctx.getChildren()))

    def visitUser_input(self, ctx: pseudoParser.User_inputContext) -> str:
        return "input()"

    def visitBinary_expr(self, ctx: pseudoParser.Binary_exprContext) -> str:
        # Convert pseudocode operator to corresponding python operator.
        operator = ctx.op.text.lower()
        operators = {'=': '==', '≠': '!=', '≤': '<=', '≥': '>=', 'mod': '%', 'div': '//'}
        if operator in operators.keys():
            operator = operators[operator]
        # Get context nodes for lhs and rhs
        lhs = ctx.expr()[0]
        rhs = ctx.expr()[1]
        return f"{self.visit(lhs)} {operator} {self.visit(rhs)}"

    def visitInt(self, ctx: pseudoParser.IntContext) -> str:
        return ctx.getText()

    def visitBool(self, ctx: pseudoParser.BoolContext) -> str:
        return ctx.getText()

    def visitReal(self, ctx: pseudoParser.RealContext) -> str:
        return ctx.getText()

    def visitString(self, ctx: pseudoParser.StringContext) -> str:
        return ctx.getText()

    def visitVariable(self, ctx: pseudoParser.VariableContext) -> str:
        return ctx.getText()

    def visitArg(self, ctx: pseudoParser.ArgContext) -> str:
        return ctx.getText()

    def visitSubroutine(self, ctx: pseudoParser.SubroutineContext) -> str:

        # Get name of the subroutine
        name = ctx.IDENTIFIER().getText()
        # Get translated text for arguments. We use visit_list instead of visit since there are multiple arguments.
        args = self.visit_list(ctx.arg(), sep=', ')
        # Create new scope to indent the body
        self.create_scope()
        # Again, use visit_list instead of visit since there are multiple blocks.
        body = self.visit_list(ctx.block())
        if not body: body = self.indent("pass")
        # Destroy scope to remove indentation
        self.destroy_scope()

        # Translate to python syntax
        return f"def {name}({args}):\n" + body

    def visitBlock(self, ctx: pseudoParser.BlockContext):
        # We simply make sure to appropriately indent code blocks.
        return self.indent(self.visitChildren(ctx))

    def visitVariable_assignment(self, ctx: pseudoParser.Variable_assignmentContext):
        # Two cases for variable assignment: assigning to an IDENTIFIER or to an expression.
        if ctx.IDENTIFIER():
            return ctx.IDENTIFIER().getText() + " = " + self.visit(ctx.expr()[0])
        else:
            return self.visit(ctx.expr()[0]) + " = " + self.visit(ctx.expr()[1])

    def visitReturn_stat(self, ctx: pseudoParser.Return_statContext):
        return f"return {self.visit(ctx.expr())}"

    def visitArray_expr(self, ctx: pseudoParser.Array_exprContext):
        return f"[{self.visit_list(ctx.expr(), sep=', ')}]"

    def visitElse_block(self, ctx: pseudoParser.Else_blockContext):
        header = self.indent("else:\n")
        # Create scope to indent body
        self.create_scope()
        body = self.visit_list(ctx.block())
        # If the body is empty, we need to use the keyword pass, since python does not support empty bodies.
        if not body: body = self.indent("pass")
        # Destroy scope to remove indentation
        self.destroy_scope()
        return header + body

    def visitElse_if_block(self, ctx: pseudoParser.Else_if_blockContext):
        header = self.indent(f"elif {self.visit(ctx.expr())}:\n")
        self.create_scope()
        body = self.visit_list(ctx.block())
        if not body: body = self.indent("pass")
        self.destroy_scope()
        return header + body

    def visitIf_block(self, ctx: pseudoParser.If_blockContext):
        header = f"if {self.visit(ctx.expr())}:\n"
        self.create_scope()
        body = self.visit_list(ctx.block())
        if not body: body = self.indent("pass")
        self.destroy_scope()
        return header + body

    def visitFor_loop(self, ctx: pseudoParser.For_loopContext):
        header = f"for {ctx.IDENTIFIER().getText()} in {self.visit(ctx.expr())}:\n"
        self.create_scope()
        body = self.visit_list(ctx.block())
        if not body: body = self.indent("pass")
        self.destroy_scope()
        return header + body

    def visitFor_loop_step(self, ctx: pseudoParser.For_loop_stepContext):
        # Get start expression
        start = self.visit(ctx.expr()[0])
        # Get end expression
        end = self.visit(ctx.expr()[1])
        # Get header of for loop, depending on whether a step was specified
        header = ""
        if ctx.step:
            step = self.visit(ctx.step)
            # Add one to the end so that the for loop goes up to and including the end number.
            header = f"for {ctx.IDENTIFIER().getText()} in range({start}, {end} + 1, {step}):\n"
        else:
            header = f"for {ctx.IDENTIFIER().getText()} in range({start}, {end} + 1):\n"

        # Get body, with appropriate indentation
        self.create_scope()
        body = self.visit_list(ctx.block())
        if not body: body = self.indent("pass")
        self.destroy_scope()
        # Return total text
        return header + body

    def visitWhile_loop(self, ctx: pseudoParser.While_loopContext):
        # Get while loop header.
        while_loop_header = f"while {self.visit(ctx.expr())}:\n"
        self.create_scope()
        # Visit body.
        body = self.visit_list(ctx.block())
        # If body is empty, we need to use the python pass keyword.
        if not body: body = self.indent("pass")
        self.destroy_scope()
        return while_loop_header + body

    def visitField_access(self, ctx: pseudoParser.Field_accessContext):
        return f"{self.visit(ctx.expr())}.{ctx.IDENTIFIER().getText()}"

    def visitRepeat_until(self, ctx: pseudoParser.Repeat_untilContext):
        # Get the text of the boolean condition
        condition = self.visit(ctx.expr())
        self.create_scope()
        # Visit body
        blocks = self.visit_list(ctx.block(), sep='\n')
        # If body is empty, we need to use the python pass keyword.
        if not blocks: blocks = self.indent("pass")
        # The body consists of the blocks and an if condition with a break statement to implement the repeat until loop.
        body = blocks + '\n' + self.indent(f"if {condition}:\n") + self.indent(
            "    break")
        self.destroy_scope()
        return "while True:\n" + body

    def visitOutput(self, ctx: pseudoParser.OutputContext):
        return f"print({self.visit_list(ctx.expr(), sep=',')})"

    def visitFunction_call(self, ctx: pseudoParser.Function_callContext):
        # Get the name of the function call
        function_call_name = ctx.IDENTIFIER().getText()
        # Deal with special function call names, and convert to python
        match function_call_name:
            case "Integer":
                function_call_name = "int"
            case "String":
                function_call_name = "str"
            case "Real":
                function_call_name = "float"
            case "Bool":
                function_call_name = "bool"
            case "append":
                array = self.visit(ctx.expr()[0])
                obj = self.visit(ctx.expr()[1])
                return f"{array}.append({obj})"
            case _:
                pass

        return f"{function_call_name}({self.visit_list(ctx.expr(), sep=', ')})"

    def visitRecord(self, ctx: pseudoParser.RecordContext):
        # Records are implemented using classes in python
        header = self.indent(f"class {ctx.IDENTIFIER().getText()}:\n")
        # Create scope to appropriately indent the code
        self.create_scope()
        # Get name of the fields in record
        field_names = [field.IDENTIFIER()[0].getText() for field in ctx.field()]

        # Define the __init__ method for the python class
        constructor_header = self.indent(f"def __init__(self, {','.join(field_names)}):\n")
        self.create_scope()
        # Visit fields to create body of __init__ method
        fields_initializer = self.visit_list(ctx.field(), sep='')
        body = constructor_header + fields_initializer
        self.destroy_scope()
        if not field_names: body = self.indent("pass")

        self.destroy_scope()
        return header + body

    def visitField(self, ctx: pseudoParser.FieldContext):
        name = ctx.IDENTIFIER()[0].getText()
        # This will go in the body of the __init__ method
        return self.indent(f"self.{name} = {name}\n")

    def visitIndex_expr(self, ctx: pseudoParser.Index_exprContext):
        return f"{self.visit(ctx.expr()[0])}[{self.visit(ctx.expr()[1])}]"

    def visitParenthesis_expr(self, ctx: pseudoParser.Parenthesis_exprContext):
        return '(' + self.visit(ctx.expr()) + ')'

    def visitUnary_expr(self, ctx: pseudoParser.Unary_exprContext):
        return ctx.op.text.lower() + self.visit(ctx.expr())

    def visitStat(self, ctx: pseudoParser.StatContext):
        return self.visitChildren(ctx)

    def visitFunction_call_expr(self, ctx: pseudoParser.Function_call_exprContext):
        return self.visitChildren(ctx)

    def visitReveal_type(self, ctx: pseudoParser.Reveal_typeContext):
        return ""

    def visitCondition_sequence(self, ctx: pseudoParser.Condition_sequenceContext):
        control_blocks = self.visit_list(ctx.children[:-1])
        return control_blocks
