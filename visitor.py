from SymbolTableVisitor import SymbolTableVisitor
from record import Record

from gen.pseudoVisitor import pseudoVisitor
from gen.pseudoParser import pseudoParser
from GenericVisitor import GenericVisitor


# TO DO PUT IN A CLASS


class Visitor(pseudoVisitor, GenericVisitor):

    def __init__(self):
        super(pseudoVisitor, self).__init__()
        super(GenericVisitor, self).__init__()

    def visitUser_input(self, ctx: pseudoParser.User_inputContext) -> str:
        return "input()"

    def visitBinary_expr(self, ctx: pseudoParser.Binary_exprContext) -> str:
        operator = ctx.op.text
        if operator == '=':
            operator = '=='

        return self.visit(ctx.expr()[0]) + " " + operator + " " + self.visit(ctx.expr()[1])

    def visitLiteral(self, ctx: pseudoParser.LiteralContext) -> str:
        return ctx.getText()

    def visitVariable(self, ctx: pseudoParser.VariableContext) -> str:
        return ctx.getText()

    def visitArg(self, ctx: pseudoParser.ArgContext) -> str:
        return ctx.getText()

    def visitSubroutine(self, ctx: pseudoParser.SubroutineContext):
        name = ctx.IDENTIFIER().getText()
        self.create_scope(indent=0)
        args = self.visit_list(ctx.arg(), sep=', ')
        self.create_scope()
        body = self.visit_list(ctx.block())
        self.destroy_scope()
        self.destroy_scope(indent=0)
        return f"def {name}({args}):\n" + body

    def visitProg(self, ctx: pseudoParser.ProgContext):
        return self.visit_list(ctx.block())

    def visitBlock(self, ctx: pseudoParser.BlockContext):
        return self.indent(self.visitChild(ctx))

    def visitVariable_assignment(self, ctx: pseudoParser.Variable_assignmentContext):
        if ctx.IDENTIFIER():
            return ctx.IDENTIFIER().getText() + " = " + self.visit(ctx.expr()[0])
        else:
            return self.visit(ctx.expr()[0]) + " = " + self.visit(ctx.expr()[1])

    def visitReturn_stat(self, ctx: pseudoParser.Return_statContext):
        return f"return {self.visit(ctx.expr())}"

    def visitArray_expr(self, ctx: pseudoParser.Array_exprContext):
        return f"[{self.visit_list(ctx.expr(), sep=', ')}]"

    def visitElse_block(self, ctx: pseudoParser.Else_blockContext):
        header = "else:\n"
        self.create_scope()
        body = self.visit_list(ctx.block())
        self.destroy_scope()
        return header + body

    def visitElse_if_block(self, ctx: pseudoParser.Else_if_blockContext):
        header = f"elif {self.visit(ctx.expr())}:\n"
        self.create_scope()
        body = self.visit_list(ctx.block())
        self.destroy_scope()
        return header + body

    def visitIf_block(self, ctx: pseudoParser.If_blockContext):
        header = f"if {self.visit(ctx.expr())}:\n"
        self.create_scope()
        body = self.visit_list(ctx.block())
        self.destroy_scope()
        return header + body

    def visitField_access(self, ctx: pseudoParser.Field_accessContext):
        return f"{self.visit(ctx.expr())}.{ctx.IDENTIFIER().getText()}"

    def visitFor_loop(self, ctx: pseudoParser.For_loopContext):
        header = f"for {ctx.IDENTIFIER().getText()} in {self.visit(ctx.expr())}:\n"
        self.create_scope()
        body = self.visit_list(ctx.block())
        self.destroy_scope()
        return header + body

    def visitFor_loop_step(self, ctx: pseudoParser.For_loop_stepContext):
        start = self.visit(ctx.expr()[0])
        end = self.visit(ctx.expr()[1])
        header = ""

        if ctx.step:
            header = f"for {ctx.IDENTIFIER().getText()} in range({start}, {end}, {self.visit(ctx.step)}):\n"
        else:
            header = f"for {ctx.IDENTIFIER().getText()} in range({start}, {end}):\n"
        self.create_scope()
        body = self.visit_list(ctx.block())
        self.destroy_scope()
        return header + body

    def visitField(self, ctx: pseudoParser.FieldContext):
        name = ctx.IDENTIFIER()[0].getText()
        return self.indent(f"self.{name} = {name}\n")

    def visitOutput(self, ctx: pseudoParser.OutputContext):
        return f"print({self.visit(ctx.expr()[0])})"

    def visitFunction_call(self, ctx: pseudoParser.Function_callContext):
        return f"{ctx.IDENTIFIER().getText()}({self.visit_list(ctx.expr(), sep=', ')})"

    def visitRecord(self, ctx: pseudoParser.RecordContext):
        record = Record(ctx)
        header = self.indent(f"class {ctx.IDENTIFIER().getText()}:\n")
        self.create_scope()
        constructor_header = self.indent(f"def __init__(self, {','.join(record.fields)}):\n")
        self.create_scope()
        fields_initializer = self.visit_list(ctx.field(), sep='')
        self.destroy_scope()
        self.destroy_scope()
        return header + constructor_header + fields_initializer

    def visitIndex_expr(self, ctx: pseudoParser.Index_exprContext):
        return f"{self.visit(ctx.expr()[0])}[{self.visit(ctx.expr()[1])}]"

    def visitWhile_loop(self, ctx: pseudoParser.While_loopContext):
        while_loop_header = f"while {self.visit(ctx.expr())}:\n"
        self.create_scope()
        body = self.visit_list(ctx.block(), sep='')
        self.destroy_scope()
        return while_loop_header + body

    def visitParenthesis_expr(self, ctx: pseudoParser.Parenthesis_exprContext):
        return '(' + self.visit(ctx.expr()) + ')'

    def visitUnary_expr(self, ctx: pseudoParser.Unary_exprContext):
        return ctx.op.text + self.visit(ctx.expr())

    def visitRepeat_until(self, ctx: pseudoParser.Repeat_untilContext):
        condition = self.visit(ctx.expr())
        self.create_scope()
        body = self.visit_list(ctx.block(), sep='\n') + '\n' + self.indent(f"if {condition}:\n") + self.indent(
            "    break")
        self.destroy_scope()
        return "while True:\n" + body

    def visitStat(self, ctx: pseudoParser.StatContext):
        return self.visitChild(ctx)

    def visitFunction_call_expr(self, ctx: pseudoParser.Function_call_exprContext):
        return self.visitChild(ctx)

    def visitChild(self, node):
        child = node.getChild(0)
        return self.visit(child)
