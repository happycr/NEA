class TranslationError(Exception):
    pass


class VariableNotDefined(TranslationError):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def output_msg(self):
        return f"Variable {self.name} not defined"


class FunctionNotDefined(TranslationError):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def output_msg(self):
        return f"Function {self.name} not defined"


class WrongNumberOfArguments(TranslationError):
    def __init__(self, ctx):
        super().__init__()
        self.ctx = ctx

    def output_msg(self):
        return f"Wrong number of arguments for function {self.ctx.IDENTIFIER().getText()}"
