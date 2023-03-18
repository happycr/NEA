"""
Generic visitor which provides utility method to indent code, or visit multiple context nodes.
"""


class GenericVisitor:
    def __init__(self):
        self.__indent = 0

    # Method called when entering a scope and change the indent accordingly. Default indentation is set to 4
    # whitespaces.
    def create_scope(self, indent=4) -> None:
        self.__indent += indent

    # Method called when leaving the scope and change the indent accordingly.
    def destroy_scope(self, indent=4) -> None:
        self.__indent -= indent

    # Method to indent a block of code
    def indent(self, string) -> str:
        return " " * self.__indent + string

    # Method to visit multiple context nodes at once.
    # All the context nodes in ctx_list are visited. The returned string are then all joined using the separator.
    def visit_list(self, ctx_list, sep='\n') -> str:
        string = ""
        if not ctx_list:
            return ""
        for i in ctx_list[:-1]:
            string += self.visit(i) + sep
        return string + self.visit(ctx_list[-1])
