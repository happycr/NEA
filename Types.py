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

    def getField(self, name):
        pass

    def getName(self):
        return self.name

    def assign(self, expr):
        raise Errors.CustomError(f"Type {self.getName()} is not assignable.")

    def getUnderlyingType(self):
        return self

    def getElement(self):
        if self.getName() == "Char":
            return ArrayType(Char).getElement()
        raise Errors.CustomError(f"Type {self.getName()} does not support indexing.")

    def add_type(self, other_type):
        if self == other_type:
            return self
        else:
            return UnionType([self, other_type])


class UnionType(Type):
    def __init__(self, types_list):
        self.types_list = remove_duplicates(types_list)

    def __iter__(self):
        for i in self.types_list:
            yield i

    def getName(self):
        return "(" + "|".join((x.getName() for x in self.types_list)) + ")"

    def add_type(self, _type: Type):
        for possible_type in _type:
            if possible_type not in self.types_list:
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

    def getField(self, name):
        inner_type = self._type.getField(name)
        if inner_type: return ConstType(inner_type)

    def getUnderlyingType(self):
        return self._type


class ReferenceType(Type):
    def __init__(self, _type: Types.Type):
        self.name = _type.getName() + "&"
        self.type = _type

    def assign(self, expr):
        if expr.getUnderlyingType() != self.type.getUnderlyingType():
            raise Errors.CustomError(f"Cannot asign value of type {expr.getName()} to type {self.getName()}")

    def getUnderlyingType(self):
        return self.type


class FieldAccess(ReferenceType):

    def __init__(self, field_name: str, _type: Type):
        super().__init__(_type)
        self.field_name = field_name

    def assign(self, expr: Type):
        if expr != self.type:
            raise Errors.CustomError(
                f"Cannot assign value of type {expr.getName()} to field {self.field_name} which is of "
                f"type {self.type.getName()}")


class VariableReferenceType(Type):
    def __init__(self, variable_name: str, symbol_table: SymbolTable.SymbolTable, index: (int, int)):
        self.variable_name = variable_name
        self.symbol_table = symbol_table
        self.index = index


    def getName(self):
        return self.symbol_table.getVar(self.index).type.getUnderlyingType().getName() + "&"

    def __iter__(self):
        for i in self.getUnderlyingType():
            yield i

    def getField(self, name):
        return self.getUnderlyingType().getField(name)

    def assign(self, expr):
        self.symbol_table.getVar(self.index).assign(expr)

    def getUnderlyingType(self) -> Types.Type:
        return self.symbol_table.getVar(self.index).type.getUnderlyingType()  # type: ignore

    def getElement(self):
        def access_type():
            return self.getUnderlyingType().getElement()

        def _set_type(new_type):
            self.assign(ArrayType(new_type))

        return ArrayElementType(access_type, _set_type)


class ArrayElementType(Type):
    def __init__(self, access_type, set_type):
        self.access_type = access_type
        self.set_type = set_type

    def getName(self):
        return self.access_type().getName() + "&"

    def assign(self, expr):
        _type: Types.Type = self.access_type()
        return _type.add_type(expr)

    def getElement(self):
        def _access_type():
            _type = self.access_type()
            return _type.getElement()

        def _set_type(new_type):
            self.set_type(ArrayType(new_type))

        return ArrayElementType(_access_type, _set_type)

    def getUnderlyingType(self):
        return self.access_type()


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


class ErrorType(Type):
    pass


class PrimitiveType(Type):
    pass


Int = PrimitiveType("Integer")
Real = PrimitiveType("Real")
Bool = PrimitiveType("Bool")
Char = PrimitiveType("Char")
none = PrimitiveType("None")
String = StringType()
primitive_types = [Int, Real, Bool, String, none]
