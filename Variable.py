import Errors
import SymbolTable
import Types

from Errors import CustomError


class Variable:
    def __init__(self, name: str, _type):
        self.name = name
        self.type = _type

    def assign(self, _type):
        if isinstance(self.type, Types.VariableReferenceType):
            self.type.assign(_type.getUnderlyingType())
        else:
            self.type = _type

    def getType(self):
        return self.type

    def getName(self):
        return self.name


class BranchVariable(Variable):
    def __init__(self, name: str, _type):
        super().__init__(name, _type.getUnderlyingType())

    def assign(self, _type):
        if isinstance(self.type, Types.VariableReferenceType):
            self.type.assign(_type)
        else:
            self.type = _type

    def getType(self):
        return self.type

    def getName(self):
        return self.name

    def destroy(self, parent_branch):
        parent_branch.add_branch_variable(self.name, self.type)

    def destroy_first(self, parent_branch):
        parent_branch.add_branch_variable_first(self.name, self.type)




class ConstVariable(Variable):
    def __init__(self, name: str, _type):
        super().__init__(name, Types.ConstType(_type))

    def assign(self, _type):
        raise Errors.CustomError(f"Cannot assign value to const variable {self.name}")
