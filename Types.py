import SymbolTable
import Types

from Util import remove_duplicates, Unionize
import Errors


class Type:
    def __init__(self, name):
        self.name = name

    def __iter__(self):
        yield self

    def __eq__(self, other):
        return self.getName() == other.getName()

    def getField(self, name: str):
        pass

    def getName(self):
        return self.name

    def assign(self, expr) -> None:
        raise Errors.CustomError(f"Type {self.getName()} is not assignable.")

    def getUnderlyingType(self):
        return self

    def getElement(self):
        raise Errors.CustomError(f"Type {self.getName()} does not support indexing.")

    def add_type(self, other_type):
        return UnionType([self, other_type])


class UnionType(Type):
    def __init__(self, types_list):
        self.types_list = []
        for _type in types_list:
            self.add_type(_type)

    def __iter__(self):
        for i in self.types_list:
            yield i

    def getName(self):
        return "|".join((x.getName() for x in self.types_list))

    def add_type(self, _type: Type):
        for possible_type in _type:
            for i in self.types_list:
                if i.getUnderlyingType() == possible_type.getUnderlyingType():
                    break
                if isinstance(possible_type, ArrayType) and isinstance(i, ArrayType):
                    i.element_type = i.element_type.add_type(possible_type.element_type)
                    break
            else:
                self.types_list.append(possible_type)
        return self

    def getElement(self):
        @Unionize
        def inner(_type):
            return _type.getElement()

        return inner(self)


class UserDefinedType(Type):
    def __init__(self, name, fields: {str: Type}):
        self.fields = fields
        super().__init__(name)

    def getField(self, name) -> Type | None:
        return self.fields.get(name)


class ConstType(Type):
    def __init__(self, _type: Types.Type):
        self.name = "CONST " + _type.getName()
        self._type = _type

    def getField(self, name):
        inner_type = self._type.getField(name)
        if inner_type: return ConstType(inner_type)

    def getUnderlyingType(self):
        return self._type


class ReferenceType(Type):
    def __init__(self, access_type, set_type):
        self.access_type = access_type
        self.set_type = set_type

    def getName(self):
        return self.access_type().getName() + "&"

    def getElement(self):
        def new_access_type():
            return self.access_type().getElement()

        def new_set_type(_type):
            self.set_type(ArrayType(_type))

        return ArrayElementType(new_access_type, new_set_type)

    def getUnderlyingType(self):
        return self.access_type().getUnderlyingType()

    def getField(self, name: str):
        return self.access_type().getUnderlyingType().getField(name)

    def __iter__(self):
        for i in self.getUnderlyingType():
            yield i


class FieldAccess(ReferenceType):

    def __init__(self, field_name: str, _type: Type):
        self.field_name = field_name

        def access_type():
            return _type

        def set_type(new_type):
            if new_type != _type:
                raise Errors.CustomError(
                    f"Cannot assign value of type {new_type.getName()} to field {self.field_name} which is of "
                    f"type {self.access_type().getName()}")

        super().__init__(access_type, set_type)

    def assign(self, expr):
        self.set_type(expr)


class VariableReferenceType(ReferenceType):
    def __init__(self, variable_name: str, symbol_table: SymbolTable.Branch, index: (int, int)):
        self.symbol_table = symbol_table
        self.index = index
        def access_type():
            return self.symbol_table.getVar(self.index).type

        def set_type(new_type):
            self.symbol_table.getVar(self.index).type = new_type
        super().__init__(access_type, set_type)

    def assign(self, expr):
        self.symbol_table.getVar(self.index).assign(expr)


class ArrayElementType(ReferenceType):
    def __init__(self, access_type, set_type):
        super().__init__(access_type, set_type)

    def assign(self, expr):
        _type: Types.Type = self.access_type()
        self.set_type(_type.add_type(expr))


class ArrayType(Type):
    def __init__(self, element_type: Type):
        self.element_type = element_type

    def getElement(self):
        return self.element_type

    def getName(self):
        return "[" + self.element_type.getName() + "]"

    def __eq__(self, other):
        if not isinstance(other, ArrayType): return False
        return self.element_type == other.element_type


class StringType(ArrayType):
    def __init__(self):
        super().__init__(Char)
        self.name = "String"


class PrimitiveType(Type):
    pass


Int = PrimitiveType("Integer")
Real = PrimitiveType("Real")
Bool = PrimitiveType("Bool")
Char = PrimitiveType("Char")
none = PrimitiveType("None")
String = StringType()
primitive_types = [Int, Real, Bool, String, none]
