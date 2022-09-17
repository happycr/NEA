from gen.pseudoParser import pseudoParser


class Type:
    def __init__(self, name):
        self.name = name

    def __iter__(self):
        yield self

    def getField(self, name):
        pass


class UnionType(Type):
    def __init__(self, types_list):
        self.types_list = set(types_list)
        name = "|".join((x.name for x in self.types_list))
        super().__init__(name)

    def __iter__(self):
        for i in self.types_list:
            yield i


class UserDefinedType(Type):
    def __init__(self, name, fields: {str: Type}):
        self.fields = fields
        super().__init__(name)

    def getField(self, name) -> Type | None:
        return self.fields.get(name)


class ErrorType(Type):
    pass


class PrimitiveType(Type):
    pass


Int = PrimitiveType("Integer")
Real = PrimitiveType("Real")
Bool = PrimitiveType("Bool")
String = PrimitiveType("String")

primitive_types = [Int, Real, Bool, String]
