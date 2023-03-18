from __future__ import annotations

from Function import Function
from Variable import Variable

"""
Scope class. Contains all type information for variables within that scope.
"""


class Scope:
    def __init__(self):
        self.__variables = []

    """
    Method to add a new variable object to the scope.
    """
    def add_var(self, variable: Variable) -> None:
        self.__variables.append(variable)

    """
    Method to return a variable object from its name in the given scope.
    Implemented as a linear search.
    Return None if the variable was not found. 
    """
    def find_var(self, name: str) -> Variable | None:
        for var in self.__variables:
            if var.getName() == name:
                return var

    """
    Method to print out contents of the scope.
    Used for debug purposes only.
    """
    def debug_print(self) -> None:
        for var in self.__variables:
            print(var.getName(), end=", ")

    """
    Getter variable method.
    """
    def getVariables(self):
        return self.__variables
