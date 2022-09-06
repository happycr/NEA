from __future__ import annotations

from antlr4 import *
from gen.pseudoLexer import pseudoLexer
from gen.pseudoParser import pseudoParser
from gen.pseudoVisitor import pseudoVisitor
from visitor import Visitor


class Translator:
    @staticmethod
    def translate(stream: InputStream | FileStream) -> str:
        lexer = pseudoLexer(stream)
        common_token_stream = CommonTokenStream(lexer)
        parser = pseudoParser(common_token_stream)
        tree = parser.prog()
        return Visitor().visit(tree)
