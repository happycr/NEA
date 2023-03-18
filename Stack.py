"""
A custom LIFO (Last In First Out) stack data structure implementation.
This is used in Branch and SymbolTable class since they need to maintain a stack frame.
"""


class Stack:
    def __init__(self):
        self.__stack = []

    """
    Push method to add an element at the top of a stack.
    """

    def push(self, element):
        self.__stack.append(element)

    """
    Pop method to remove an element from the top of the stack.
    """

    def pop(self):
        if self.isEmpty(): raise Exception("pop() called on empty stack")
        return self.__stack.pop()

    """
    Top method which returns element at the top of the stack.
    """

    def top(self):
        if self.isEmpty(): raise Exception("top() called on empty stack")
        return self.__stack[-1]

    """
    Method to check whether the stack is empty.
    """

    def isEmpty(self):
        return len(self.__stack) == 0

    """
    __iter__ method to make the stack an iterable object.
    """
    def __iter__(self):
        for i in self.__stack:
            yield i
    """
    Getter stack method.
    """
    def getStack(self):
        return self.__stack
