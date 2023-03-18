import Errors
import SymbolTable
import Types

from Errors import TranslationError

"""
Variable class which is used to represent variable objects.
"""


class Variable:
    def __init__(self, name: str, _type):
        self.__name = name
        self.__type = _type

    """
    Method to assign a new type to the variable.
    """

    def assign(self, _type):
        # Check if type is a variable reference type. If so assign underlying type.
        if isinstance(self.__type, Types.VariableReferenceType):
            self.__type.assign(_type.getUnderlyingType())
        else:
            self.__type = _type

    def getType(self):
        return self.__type

    def getName(self):
        return self.__name


"""
Branch variable, used to deal with condition sequences.
Branch variable is used in the Branch class, to make sure local changes do not affect the parent branch.
"""


class BranchVariable(Variable):
    def __init__(self, name: str, _type):
        super().__init__(name, _type.getUnderlyingType())


"""
Const variable, used to represent const variables.
"""


class ConstVariable(Variable):
    def __init__(self, name: str, _type):
        super().__init__(name, Types.ConstType(_type))

    """
    As you cannot assign a new type to a const variable, this method always raises an error.
    """

    def assign(self, _type):
        raise Errors.TranslationError(f"Cannot assign value to const variable {self.__name}")
