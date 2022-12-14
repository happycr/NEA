from Argument import Argument
from gen.pseudoParser import pseudoParser


class Function:
    def __init__(self, ctx: pseudoParser.SubroutineContext):
        self.name = ctx.IDENTIFIER().getText()
        self.ctx = ctx

    def getArgs(self):
        return self.ctx.arg()

    def getArgsName(self):
        return [arg.IDENTIFIER().getText() for arg in self.ctx.arg()]
