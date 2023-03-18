import Errors
import SymbolTable
import Types
from Unionise import Unionise

"""
This class represents a type object, which is used by the type checker.
"""


class Type:
    def __init__(self, name):
        self.__name = name

    """
    Default implementation of the __iter__ method, which generates a stream of the concrete types contained here.
    This means that we can iterate over our type, and use standard algorithms such as from itertools over it.
    See Util.Unionize as an example. 
    Here we simply yield ourself.
    """

    def __iter__(self):
        yield self

    """
    Method to compare two types together.
    """

    def __eq__(self, other) -> bool:
        return self.getName() == other.getName()

    """
    Default implementation of the getField method, which is used to access the type of a given field, given its name. 
    """

    def getField(self, name: str):
        pass

    """
    Getter function for self.name
    """

    def getName(self) -> str:
        return self.__name

    """
    Default implementation of the assign method, which is used in assignment statements. 
    The default implementation raise an error, since the vast majority of types are not assignable.
    For example, 5 <- 10 or [1,3,4] <- 20 makes no sense.
    Assignment will only be valid for types which are a ReferenceType.
    There are only three cases where assignment is valid. These include:
    
    1) Assignment to a variable: x <- 10. Here, x will be of type VariableReferenceType.
    2) Assignment to a field: obj.field <- 20. Here obj.field will be of type FieldAccess
    3) Assignment to an array element: x[0] <- 42. Here, x[0] will of type ArrayElementType.
    """

    def assign(self, expr) -> None:
        raise Errors.TranslationError(f"Type {self.getName()} is not assignable.")

    """
    Default implementation for getUnderlyingType. This method removes any reference / wrapper over a type.
    """

    def getUnderlyingType(self):
        return self

    """
    Default implementation for getElement. This method will be called when accessing an element of an array.
    """

    def getElement(self):
        raise Errors.TranslationError(f"Type {self.getName()} does not support indexing.")

    """
    Method which returns the current type plus the new type added. The type returned will be a union type. 
    """

    def add_type(self, other_type):
        return UnionType([self, other_type])


"""
This class defines types for object which can have multiple concrete types.
"""


class UnionType(Type):
    def __init__(self, types_list):
        self.__types_list = []
        for _type in types_list:
            self.add_type(_type)

    """
    Method to remove a type of types_list
    """
    def remove(self, _type):
        self.__types_list.remove(_type)

    """
    Overriden __iter__ method. We yield all the types in the types_list.
    """

    def __iter__(self):
        for i in self.__types_list:
            yield i

    """
    Overriden getName method. Union types are denoted as T | U | ...
    """

    def getName(self):
        return "|".join((x.getName() for x in self.__types_list))

    """
    Overriden add_type method to add a new type to this union type.
    We need to make sure that no duplicates are added. 
    We also need to make sure that all types are flattened out, ie types_list does not any union types.
    """

    def add_type(self, _type: Type):
        # Iterate over actual concrete types given in _type
        for possible_type in _type:
            # Check whether possible_type is already in self.types_list or not
            for i in self.__types_list:
                if i.getUnderlyingType() == possible_type.getUnderlyingType():
                    break
                if isinstance(possible_type, ArrayType) and isinstance(i, ArrayType):
                    # Merge array types together, ie instead of [Char] | [Integer] we would have [Char | Integer]
                    i.setElement(i.getElement().add_type(possible_type.getElement()))
                    break
            # If no break statements were encountered, add possible_type to types_list
            else:
                self.__types_list.append(possible_type)
        return self

    """
    Overriden getElement method to access element type.
    We need to deal with union types, so we use @Unionize.
    """

    def getElement(self):
        @Unionise
        def inner(_type):
            return _type.getElement()

        return inner(self)


"""
Class which represents record types, which are defined by the user, as opposed to primitive types such Integer.
"""


class UserDefinedType(Type):
    def __init__(self, name, fields: {str: Type}):
        self.__fields = fields
        super().__init__(name)

    def getField(self, name) -> Type | None:
        return self.__fields.get(name)

    def getFields(self):
        return self.__fields


"""
Class which represents CONST types. This can be thought as a wrapper over types.
"""


class ConstType(Type):
    def __init__(self, _type: Types.Type):
        self.__name = "CONST " + _type.getName()
        self.__type = _type

    def getElement(self):
        return ConstType(self.__type.getElement())

    def getType(self):
        return self.__type

    """
    Overriden getField method. Here, we make sure that fields accessed from a CONST variable are CONST.
    """

    def getField(self, name):
        inner_type = self.__type.getField(name)
        if inner_type: return ConstType(inner_type)



"""
Parent class which enables assignment. Only types which inherit from ReferenceType will be assignable. See Type.assign.
"""


class ReferenceType(Type):
    """
    ReferenceType has two fields:
    access_type, which is a function which returns the original type
    set_type, which is a function which allows you to assign a new type to the original type.

    access_type: () -> Types.Type
    set_type: (new_type: Types.Type) -> None
    """

    def __init__(self, access_type, set_type):
        self._access_type = access_type
        self._set_type = set_type

    def getName(self) -> str:
        return self._access_type().getName() + "&"

    """
    Overriden getElement method. We return an ArrayElementType, which deals with array elements and index expressions.  
    """

    def getElement(self) -> Types.Type:
        # This function makes sure ArrayElementType can access the original type.
        def new_access_type():
            return self._access_type().getElement()

        # This function determines how array types are updated.
        def new_set_type(_type):
            self._set_type(ArrayType(_type))

        return ArrayElementType(new_access_type, new_set_type)

    def getUnderlyingType(self) -> Types.Type:
        return self._access_type().getUnderlyingType()

    def getField(self, name: str) -> Types.Type:
        return self._access_type().getField(name)

    def __iter__(self):
        for i in self.getUnderlyingType():
            yield i


"""
Class which represents the types of objects when a field is accessed. For example, obj.field will have type FieldAccess.
This class enables assignment statement to fields such as obj.field <- 5.
"""


class FieldAccess(ReferenceType):

    def __init__(self, field_name: str, _type: Type):
        self.__field_name = field_name

        def access_type():
            return _type

        def set_type(new_type):
            if new_type != _type:
                # Fields in pseudocode are given an explicit type, so assigning a new type to a field is forbidden.
                raise Errors.TranslationError(
                    f"Cannot assign value of type {new_type.getName()} to field {self.__field_name} which is of "
                    f"type {self._access_type().getName()}")

        super().__init__(access_type, set_type)

    def assign(self, expr):
        self._set_type(expr)


"""
Reference type which allows assignment to variables.
"""


class VariableReferenceType(ReferenceType):
    def __init__(self, symbol_table: SymbolTable.Branch, index: (int, int)):
        self.__symbol_table = symbol_table
        self.__index = index

        def access_type():
            # Get type of variable from symbol table
            return self.__symbol_table.getVar(self.__index).getType()

        def set_type(new_type):
            # Get variable object from symbol table and set new type.
            self.__symbol_table.getVar(self.__index).assign(new_type)

        super().__init__(access_type, set_type)

    def assign(self, expr):
        # Get variable object from symbol table and assign new type.
        self.__symbol_table.getVar(self.__index).assign(expr)


"""
Reference type which allows assignment to array elements, like array[0] <- 5
"""


class ArrayElementType(ReferenceType):
    def __init__(self, access_type, set_type):
        super().__init__(access_type, set_type)

    def assign(self, expr):
        _type: Types.Type = self._access_type()
        self._set_type(_type.add_type(expr))


"""
Class which defines array type.
Contains element_type, which is the type of its elements.
"""


class ArrayType(Type):
    def __init__(self, element_type: Type):
        self.__element_type = element_type

    def getName(self):
        return "[" + self.__element_type.getName() + "]"

    def getElement(self):
        return self.__element_type

    def setElement(self, _type):
        self.__element_type = _type

    def __eq__(self, other):
        if not isinstance(other, ArrayType): return False
        return self.__element_type == other.__element_type


"""
Class which defines the StringType.
"""


class StringType(ArrayType):
    def __init__(self):
        super().__init__(Char)
        self.__name = "String"

    def getElement(self):
        return self

    def getName(self):
        return "String"


"""
Class for primitive types.
"""


class PrimitiveType(Type):
    pass


"""
Instances of primitive types.
"""
Int = PrimitiveType("Integer")
Real = PrimitiveType("Real")
Bool = PrimitiveType("Bool")
Char = PrimitiveType("Char")
none = PrimitiveType("None")
String = StringType()
primitive_types = [Int, Real, Bool, String, none]
