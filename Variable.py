from Types import Type


class Variable:
    def __init__(self, name, _type):

        self.name = name
        self.types = [_type]
