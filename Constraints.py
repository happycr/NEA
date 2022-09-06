from gen.pseudoParser import pseudoParser
from Function import Function
from Errors import *


class Constraint:
    def __init__(self, func: Function): pass

    def check(self, ctx: pseudoParser.Function_callContext): pass


class NumberOfArguments(Constraint):
    def __init__(self, func: Function):
        super().__init__(func)
        self.number = len(func.args)

    def check(self, ctx: pseudoParser.Function_callContext):
        arguments = ctx.expr()
        if len(arguments) != self.number:
            raise WrongNumberOfArguments()
