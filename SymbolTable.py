from __future__ import annotations

import Errors
import Types
from Scope import Scope
from Variable import Variable
from Variable import BranchVariable
from Function import Function
from Scope import Scope
import copy
from Stack import Stack

"""
Branch: stores information about variables and return types in a specific code path.
We can think of the program as a tree of branches, with a global branch at the top, which corresponds to the symbol table,
and new branches being created for each IF / ELSE IF / ELSE block.
We will be loosely performing a depth first search on that tree.
"""


class Branch:
    """
    Fields:
    parent_branch: reference to the parent branch in the tree of branches
    scopes: list of Scope object, which in turn each store a list of variables.
    A new scope is created whenever a new code block is encountered, eg  WHILE loops / FOR loops / subroutines etc...
    return_types: If we are inside a subroutine, we need to keep track of the possible return types.
    If a parent branch exists, return_types is automatically set to the parent branch's return_types.
    """

    def __init__(self, parent_branch: Branch):
        self.__parent_branch = parent_branch
        self.__scopes = Stack()
        self.__return_types = []
        if self.__parent_branch: self.__return_types = copy.deepcopy(parent_branch.__return_types)
        # Create new scope to begin with
        self.create_scope()

    """
    Method to create new variable object and add it to branch.
    """

    def add_var(self, variable: Variable) -> None:
        self.__scopes.top().add_var(variable)

    """
    Method to create scope
    """

    def create_scope(self) -> None:
        self.__scopes.push(Scope())

    """
    Method to destroy scope
    """

    def destroy_scope(self) -> None:
        self.__scopes.pop()

    """
    Method to get variable given its name. Implemented as a linear search.
    """

    def find_var(self, name: str) -> None | Variable:
        # Search variable in all scopes, in reverse order, as we want the variable in the innermost scope.
        for scope in self.__scopes.getStack()[::-1]:
            # Search for variable in scope using find_var method. If found return it.
            var = scope.find_var(name)
            if var: return var

        # If variable not found first, check parent branch exists and search variable in it.
        if self.__parent_branch:
            # Search for variable in parent branch. Here, we call the find_var method recursively.
            # The find_var method will be recursively called to move up the branch tree until the top most global level.
            outer = self.__parent_branch.find_var(name)

            # If the variable was found, create a new dummy branch variable, add it to this local branch.
            # The dummy branch variable makes sure any changes to made to it are only reflected locally in this branch.
            # The local changes  will only be merged into the parent branch when the local branch is completely visited.
            if outer:
                # Creation of dummy branch variable.
                new_var = BranchVariable(name, outer.getType())
                # Add branch variable to this branch.
                self.add_var(new_var)
                # Return branch variable.
                return new_var

    """
    Method to get variable given its index in the symbol table.
    """

    def getVar(self, index) -> Variable:
        return self.__scopes.getStack()[index[0]].getVariables()[index[1]]

    """
    Method to create a new frame when a subroutine is entered.
    This method needs to create a new scope, add the arguments onto it, and initially set the return type to None.
    """

    def create_frame(self, arguments, func):
        # Create scope
        self.create_scope()
        # Get name of arguments
        func_param = func.getArgsName()
        # Create new variable corresponding to the arguments and add them to the scope.
        for i in range(len(arguments)):
            self.add_var(Variable(func_param[i], arguments[i]))

        # Initially set return type to None.
        self.__return_types.append(Types.none)

    """
    Method do destroy frame.
    """

    def destroy_frame(self):
        self.destroy_scope()
        return self.__return_types.pop()

    """
    Method to add return type.
    """

    def setReturnType(self, expr):
        # Check that we are inside a function.
        if self.__return_types:
            # Check whether return statement is reachable.
            # If the return statement is reachable:
            # There will be at least one code path where the function has not returned anything.
            # In this code path  the return type is none.
            if Types.none in self.__return_types[-1]:
                # Get type of expression.
                return_type = expr.getUnderlyingType()
                # Update return type:
                # remove the None type ( Function is guaranteed to return something ) and add new type.
                self.__return_types[-1] = self.__return_types[-1].add_type(return_type)
                self.__return_types[-1].remove(Types.none)

        # If we are not inside a function raise an error.
        else:
            raise Errors.TranslationError(f"Cannot have a return statement outside of a function")

    """
    Method to get index of a variable in the branch given its name.
    Implemented using linear search.
    The index of a variable will function as an equivalent to a variable pointer.
    Variable pointers are used by Reference types which needs to access and modify the branch.
    """

    def getIndex(self, name):
        for scope in self.__scopes.getStack()[::-1]:
            for var in scope.getVariables():
                if name == var.getName():
                    return [self.__scopes.getStack().index(scope), scope.getVariables().index(var)]

    def debug_print(self) -> None:
        for scope in self.__scopes:
            scope.debug_print()

    """
    Method to destroy a branch.
    The method has three purposes:
    1) Destroy the final scope in the branch
    2) Merge the local variable type information with the type information in the parent branch.
    3) Merge the return type information with the return type information in the parent branch.
    
    In this method, any type information in the parent branch is completely overwritten by the local type information.
    """

    def destroy_first(self, branches) -> None:
        # Collect all branch variables and append them to the list branch_variables.
        branch_variables = []
        # Iterate over all scopes
        for scope in self.__scopes:
            # Iterate over all variables
            for variable in scope.getVariables():
                # If variable is a branch variable, append it to the list.
                if isinstance(variable, BranchVariable):
                    branch_variables.append(variable)

        # Merge the local variable type information with the parent branch.
        for variable in branch_variables:
            # Make sure branches have created a branch variable if the variable has not been redefined in that branch.
            for branch in branches[1:]:
                branch.find_var(variable.getName())
            # Merge type information for that branch variable.
            self.__parent_branch.merge_branch_variable_first(variable.getName(), variable.getType())

        # Destroy scope.
        self.destroy_scope()

        # Merge return type information.
        for i in range(len(self.__return_types)):
            self.__parent_branch.__return_types[i] = self.__return_types[i]

    """
    Method do destroy a branch similarly to destroy_first.
    The only difference is that we preserve the type information in the parent branch.
    We do not completely overwriting it, contrary to destroy_first.
    """

    def destroy(self) -> None:
        # Collect all branch variable similarly to destroy_first
        branch_variables = []
        for scope in self.__scopes:
            for variable in scope.getVariables():
                if isinstance(variable, BranchVariable):
                    branch_variables.append(variable)
        # Merge all branch variable type information.
        for variable in branch_variables:
            self.__parent_branch.merge_branch_variable(variable.getName(), variable.getType())
        # Merge all return type information
        for i in range(len(self.__return_types)):
            self.__parent_branch.__return_types[i] = self.__parent_branch.__return_types[i].add_type(self.__return_types[i])
        # Destroy scope.
        self.destroy_scope()
    """
    Method to merge a single branch variable, preserving the original type information.
    In this method we add the new type to the existing type of the variable.
    """
    def merge_branch_variable(self, name: str, _type):
        # Get index of variable.
        index = self.getIndex(name)
        # Add _type to the already existing type of the variable.
        self.getVar(index).assign(self.getVar(index).getType().add_type(_type.getUnderlyingType()))
    """
    Method to merge a single branch variable, completely overwriting the type information.
    """

    def merge_branch_variable_first(self, name: str, _type):
        # Get index of variable
        index = self.getIndex(name)
        # Set new type.
        self.getVar(index).assign(_type)


"""
Symbol table, used to store functions, types, variables, and return types.
Can be thought as the top level branch, which is why it inherits from Branch.
Additionally, contains list of functions and types. 
"""


class SymbolTable(Branch):
    def __init__(self):
        super().__init__(None)
        # Dictionary to store functions
        self.functions: {str: Function} = {}
        # Dictionary to store types.
        self.types: {str: Types.Type} = {_type.getName(): _type for _type in Types.primitive_types}
    """
    Method to add new type.
    """
    def add_type(self, _type: Types.Type) -> None:
        self.types[_type.getName()] = _type
    """
    Method to add function.
    """
    def add_func(self, func: Function) -> None:
        self.functions[func.getName()] = func

    """
    Method to find a function given its name.
    """
    def find_func(self, name: str) -> None | Function:
        return self.functions.get(name)

    """
    Method to find a type given its name.
    """

    def find_type(self, name: str):
        return self.types.get(name)
