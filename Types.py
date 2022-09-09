from record import Record
from gen.pseudoParser import pseudoParser


class Type:
    def __init__(self, name):
        self.name = name


class UserDefinedType(Type):
    def __init__(self, ctx: pseudoParser.RecordContext):
        name = ctx.IDENTIFIER().getText()
        super().__init__(name)
        self.record = Record(ctx)


class PrimitiveType(Type):
    pass


primitive_types_names = ["int", "real", "bool", "char", "string"]
primitive_types = [PrimitiveType(x) for x in primitive_types_names]
