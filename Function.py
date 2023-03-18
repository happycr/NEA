from gen.pseudoParser import pseudoParser

"""
Responsible for storing function objects to be used in the symbol table.
Stores the name of the function, and context node. 
Also contains methods to get the name of the arguments or their context nodes.
"""


class Function:
    def __init__(self, ctx: pseudoParser.SubroutineContext):
        # Name of function
        self.__name = ctx.IDENTIFIER().getText()
        # Context node representing function
        self.__ctx = ctx
    """
    Method to get context nodes of arguments.
    """
    def getArgs(self):
        return self.__ctx.arg()
    """
    Method to get names of arguments.
    """
    def getArgsName(self):
        return [arg.IDENTIFIER().getText() for arg in self.__ctx.arg()]
    """
    Getter function name
    """
    def getName(self):
        return self.__name

    def getCtx(self):
        return self.__ctx
