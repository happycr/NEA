from __future__ import annotations

import Errors
import Types
from Argument import Argument
from Scope import Scope
from Variable import Variable
from Variable import BranchVariable
from Function import Function
from Scope import Scope


class SymbolTable:
    def __init__(self):
        self.scopes: [Scope] = []
        self.functions: {str: Function} = {}
        self.types: {str: Types.Type} = {_type.name: _type for _type in Types.primitive_types}
        self.return_types: [Types.Type] = []
        self.create_scope()

    def add_var(self, variable: Variable) -> SymbolTable:
        self.scopes[-1].add_var(variable)
        return self

    def add_type(self, _type: Types.Type) -> SymbolTable:
        self.types[_type.name] = _type
        return self

    def add_func(self, func: Function) -> SymbolTable:
        self.functions[func.name] = func
        return self

    def create_scope(self) -> None:
        self.scopes.append(Scope())

    def destroy_scope(self) -> None:
        self.scopes.pop()

    def find_var(self, name: str) -> None | Variable:  # type: ignore
        for scope in self.scopes[::-1]:
            var = scope.find_var(name)
            if var: return var

    def add_branch_variable(self, name: str, _type):
        index = self.getIndex(name)
        self.getVar(index).assign(self.getVar(index).getType().add_type(_type.getUnderlyingType()))
    def add_branch_variable_first(self, name: str, _type):
        variable = self.find_var(name)
        index = self.getIndex(name)
        self.getVar(index).assign(_type)


    def find_func(self, name: str) -> None | Function:
        return self.functions.get(name)

    def find_type(self, name: str):
        return self.types.get(name)

    def getVar(self, index) -> Variable:
        return self.scopes[index[0]].variables[index[1]]

    def create_frame(self, arguments, func):
        self.create_scope()
        func_param = func.getArgsName()
        for i in range(len(arguments)):
            self.add_var(Variable(func_param[i], arguments[i]))

        self.return_types.append(Types.none)

    def destroy_frame(self):
        self.destroy_scope()
        return self.return_types.pop()

    def setReturnType(self, expr):
        if self.return_types:
            self.return_types[-1] = expr
        else:
            raise Errors.CustomError(f"Cannot have a return statement outside of a function")

    def getIndex(self, name):
        for scope in self.scopes[::-1]:
            for var in scope.variables:
                if name == var.getName():
                    return [self.scopes.index(scope), scope.variables.index(var)]

    def debug_print(self) -> None:
        for scope in self.scopes:
            scope.debug_print()


class Branch:
    def __init__(self, parent_branch: Branch | SymbolTable):
        self.parent_branch = parent_branch
        self.scopes: [Scope] = []
        self.return_types: [Types.Type] = []
        self.create_scope()

    def add_var(self, variable: Variable) -> Branch:
        self.scopes[-1].add_var(variable)
        return self

    def create_scope(self) -> None:
        self.scopes.append(Scope())

    def destroy_scope(self) -> None:
        self.scopes.pop()

    def find_var(self, name: str) -> None | Variable:  # type: ignore
        for scope in self.scopes[::-1]:
            var = scope.find_var(name)
            if var: return var
        outer = self.parent_branch.find_var(name)
        if outer:
            new_var = BranchVariable(name, outer.getType())
            self.add_var(new_var)
            return new_var

    def getVar(self, index) -> Variable:
        return self.scopes[index[0]].variables[index[1]]

    def create_frame(self, arguments, func):
        self.create_scope()
        func_param = func.getArgsName()
        for i in range(len(arguments)):
            self.add_var(Variable(func_param[i], arguments[i]))

        self.return_types.append(Types.none)

    def destroy_frame(self):
        self.destroy_scope()
        return self.return_types.pop()

    def setReturnType(self, expr):
        if self.return_types:
            self.return_types[-1] = expr
        else:
            raise Errors.CustomError(f"Cannot have a return statement outside of a function")

    def getIndex(self, name):
        for scope in self.scopes[::-1]:
            for var in scope.variables:
                if name == var.getName():
                    return [self.scopes.index(scope), scope.variables.index(var)]

    def debug_print(self) -> None:
        for scope in self.scopes:
            scope.debug_print()

    def destroy(self, parent_branch) -> None:
        branch_variables = []
        for scope in self.scopes:
            for variable in scope.variables:
                if isinstance(variable, BranchVariable):
                    branch_variables.append(variable)
        for variable in branch_variables:
            variable.destroy(parent_branch)

    def destroy_first(self, parent_branch) -> None:
        branch_variables = []
        for scope in self.scopes:
            for variable in scope.variables:
                if isinstance(variable, BranchVariable):
                    branch_variables.append(variable)
        for variable in branch_variables:
            variable.destroy_first(parent_branch)


    def add_branch_variable(self, name: str, _type):
        variable = self.find_var(name)
        index = self.getIndex(name)
        self.getVar(index).assign(self.getVar(index).getType().add_type(_type.getUnderlyingType()))

    def add_branch_variable_first(self, name: str, _type):
        variable = self.find_var(name)
        index = self.getIndex(name)
        self.getVar(index).assign(_type)

