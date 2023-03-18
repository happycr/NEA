import StackTrace

"""
Syntax error class. 
"""


class SyntaxErrorClass(Exception):
    pass


"""
Translation error class. Contains a stack trace, and a custom message describing the error.
"""


class TranslationError(Exception):
    def __init__(self, msg):
        self.__stack_trace = StackTrace.StackTrace()

        # Error message field.
        self.__msg = msg

    # Method to get a message describing the error.
    def formatted_output_msg(self):
        return self.__stack_trace.getText() + f"\nError: {self.__msg}"
