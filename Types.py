from record import Record
from gen.pseudoParser import pseudoParser


class Type:
    def __init__(self, name):
        self.name = name

    def __iter__(self):
        yield self


class UnionType(Type):
    def __init__(self, types_list):
        self.types_list = set(types_list)
        name = "|".join((x.name for x in self.types_list))
        super().__init__(name)

    def __iter__(self):
        for i in self.types_list:
            yield i


class UserDefinedType(Type):
    def __init__(self, ctx: pseudoParser.RecordContext):
        name = ctx.IDENTIFIER().getText()
        super().__init__(name)
        self.record = Record(ctx)


class ErrorType(Type):
    pass


class PrimitiveType(Type):
    pass


Int = PrimitiveType("int")
Real = PrimitiveType("real")
Bool = PrimitiveType("bool")
Char = PrimitiveType("char")
String = PrimitiveType("string")
primitive_types = [Int, Real, Bool, Char, String]
