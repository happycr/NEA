from SymbolTableVisitor import SymbolTableVisitor


class GenericVisitor:
    def __init__(self):
        self.__indent = 0

    def create_scope(self, indent=4) -> None:
        self.__indent += indent

    def destroy_scope(self, indent=4) -> None:
        self.__indent -= indent

    def indent(self, string) -> str:
        return " " * self.__indent + string

    def visit_list(self, ctx_list, sep='\n') -> str:
        string = ""
        if not ctx_list:
            return ""
        for i in ctx_list[:-1]:
            string += self.visit(i) + sep
        return string + self.visit(ctx_list[-1])
