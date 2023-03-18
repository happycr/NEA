from __future__ import annotations

from antlr4 import *
from gen.pseudoLexer import pseudoLexer
from gen.pseudoParser import pseudoParser
from gen.pseudoVisitor import pseudoVisitor
from Translator import Translator
from BailErrorStrategy import BailErrorStrategy, BailLexer, BailErrorListener

"""
This class is responsible for the front end. It needs to produce an AST from an input stream.
"""


class Frontend:
    """
    This method creates the AST.
    """

    @staticmethod
    def get_tree(stream: InputStream | FileStream):  # type: ignore
        # Use Bail lexer, which aborts on first syntax error instead of pseudoLexer
        lexer = BailLexer(stream)
        # lexer = pseudoLexer(stream)
        # Disable error reporting from ANTLR, as we are already handling it
        lexer.removeErrorListeners()

        # Add our custom error listener to report syntax errors to the standard error stream.
        lexer.addErrorListener(BailErrorListener())

        common_token_stream = CommonTokenStream(lexer)
        parser = pseudoParser(common_token_stream)
        # Modify error handling strategy, to abort on first syntax error.
        parser._errHandler = BailErrorStrategy()
        parser.removeErrorListeners()
        parser.addErrorListener(BailErrorListener())
        # Create AST
        tree = parser.prog()
        return tree
