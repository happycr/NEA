from __future__ import annotations

from Function import Function
from Variable import Variable
from Argument import Argument


class Scope:
    def __init__(self):
        self.variables = []

    def add_var(self, variable: Variable) -> Scope:
        self.variables.append(variable)
        return self

    def find_var(self, name: str) -> Variable | None:
        for var in self.variables:
            if var.name == name:
                return var

    def debug_print(self) -> None:
        for var in self.variables:
            print(var.name, end=", ")
