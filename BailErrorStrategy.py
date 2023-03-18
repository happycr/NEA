from antlr4.error.ErrorStrategy import DefaultErrorStrategy  # type: ignore
from antlr4.error.ErrorListener import ErrorListener
from antlr4.error.Errors import InputMismatchException

from Errors import SyntaxErrorClass  # type: ignore
from gen.pseudoLexer import pseudoLexer
import antlr4
import sys

"""
This class modifies the default error strategy for ANTLR, for syntax errors.
ANTLR default error strategy is to try and recover and find other syntax errors.
Here we override that error strategy by raising a syntax error on the first error found and aborting the program.
"""


class BailErrorStrategy(DefaultErrorStrategy):

    # Override recover method to raise syntax error and abort translation on first error found
    def recover(self, recognizer, e):
        raise SyntaxErrorClass()

    # Override recoverInline method to raise syntax error and abort translation on first error found
    def recoverInline(self, recognizer):
        raise InputMismatchException(recognizer)

    # Prevent any syncing
    def sync(self, recognizer): pass


"""
This class modifies the default error strategy for ANTLR, similarly as BailErrorStrategy. 
However, this class deals with lexical syntax errors.
"""


class BailLexer(pseudoLexer):
    def __init__(self, _input):
        super().__init__(_input)

    # Override recover method to raise syntax error and abort translation on first lexcial error found
    def recover(self, e):
        raise SyntaxErrorClass()


"""
This class print out syntax errors to the standard error stream
It overrides the default ErrorListener ANTLR class.
"""


class BailErrorListener(ErrorListener):
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        print("Syntax Error: ", file=sys.stderr)
        print("line " + str(line) + ":" + str(column) + " " + msg, file=sys.stderr)
