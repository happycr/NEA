import Errors
import Types

from Errors import CustomError
class Variable:
    def __init__(self, name, _type):

        self.name = name
        self.type = _type

    def assign(self, _type):
        self.type = _type

class ConstVariable:
    def __init__(self, name, _type):
        self.name = name
        self.type = Types.ConstType(_type)

    def assign(self, _type):
        raise Errors.CustomError(f"Cannot assign value to const variable {self.name}")

