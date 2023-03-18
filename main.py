from IO import IO
from Frontend import Frontend
from TypeChecker import TypeChecker
import Translator
from Errors import *
import sys


def main():
    argv = sys.argv
    if len(argv) != 2:
        print("Wrong number of arguments. Need a filename or use -sh option.")
        sys.exit(1)
    io = IO(argv[1])
    # Get input stream from the user
    stream = io.get_stream()
    try:
        # Get AST from front end class
        tree = Frontend.get_tree(stream)

        # Create type checker visitor object
        type_checker = TypeChecker()
        # Check for any type errors.
        type_checker.visit(tree)
        # Create translator visitor object
        _translator = Translator.Translator()

        # Get translator python text
        python_text = _translator.visit(tree)

        # Output python text
        io.write(python_text)
    except SyntaxErrorClass:
        # An error message has already been printed to the console by BailErrorListener.
        # No need to do anything but terminate the program.
        pass
    # Deal with type errors.
    except TranslationError as e:
        # Print error message to console
        print(e.formatted_output_msg(), file = sys.stderr)


if __name__ == '__main__':
    main()
