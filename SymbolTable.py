from __future__ import annotations

import Types
from Argument import Argument
from Scope import Scope
from Variable import Variable
from Function import Function
from Scope import Scope
from Types import Type


class SymbolTable:
    def __init__(self):
        self.scopes: [Scope] = []
        self.functions: {str: Function} = {}
        self.types: {str: Type} = {_type.name: _type for _type in Types.primitive_types}
        self.create_scope()

    def add_var(self, variable: Variable) -> SymbolTable:
        if not self.find_var(variable.name):
            self.scopes[-1].add_var(variable)
        return self

    def add_type(self, _type: Type) -> SymbolTable:
        self.types[_type.name] = _type
        return self

    def add_func(self, func: Function) -> SymbolTable:
        self.functions[func.name] = func
        return self

    def create_scope(self) -> None:
        self.scopes.append(Scope())

    def destroy_scope(self) -> None:
        self.scopes.pop()

    def find_var(self, name: str) -> None | Variable:
        for scope in self.scopes[::-1]:
            var = scope.find_var(name)
            if var: return var

    def find_func(self, name: str) -> None | Function:
        return self.functions.get(name)

    def find_type(self, name: str):
        return self.types.get(name)

    def debug_print(self) -> None:
        for scope in self.scopes:
            scope.debug_print()
