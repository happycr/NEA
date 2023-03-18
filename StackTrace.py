from gen.pseudoParser import pseudoParser

"""
Class for stack traces. Contains a list of strings, which is appended to as an error is bubbled up.
"""


class StackTrace:
    def __init__(self):
        self.__stacktrace = []

    """
    This method is called each time an error bubbles up a new context node.
    Depending on the type of the context node, we append different strings to the stack trace.
    """
    def add_ctx(self, ctx):
        # Get source text corresponding to the context node.
        # Here we get the exact, complete text corresponding from the context node.
        # This includes extra white spaces, comments which have been thrown out by the lexer, not present in the AST.

        # First get the token source of the context node.
        token_source = ctx.start.getTokenSource()
        # Get the input stream.
        input_stream = token_source.inputStream
        # Get start and stop tokens.
        start, stop = ctx.start.start, ctx.stop.stop
        # Get the original text corresponding to the context node.
        # Use the split method to only get the first line of the text. This is useful for block context nodes.
        original_text = input_stream.getText(start, stop).split('\n')[0]

        # Depending on type of context node, append different strings.

        # Case when ctx is a function call. This provides the stack trace through different function calls.
        if isinstance(ctx, pseudoParser.Function_callContext):
            stacktrace_text = f"In function call: {original_text}"
        # Case when ctx is a statement.
        elif isinstance(ctx, pseudoParser.StatContext):
            stacktrace_text = f"In line {ctx.start.line}: {original_text}"
        # Case when ctx is a block. We only append a string if the block node is the initial node in the error bubbling.
        elif isinstance(ctx, pseudoParser.BlockContext) and not self.__stacktrace:
            stacktrace_text = f"In line {ctx.start.line}: {original_text}"
        # Case when ctx is a subroutine. Again, we only append a string if the subroutine node is the initial node.
        elif isinstance(ctx, pseudoParser.SubroutineContext) and not self.__stacktrace:
            stacktrace_text = f"In line {ctx.start.line}: {original_text}"
        # Otherwise, do not append anything.
        else:
            return self
        self.__stacktrace.append(stacktrace_text)
        # Return self to allow for method chaining.
        return self

    """
    Method to convert the stack trace into an error message.
    """
    def getText(self):
        return '\n'.join(self.__stacktrace[::-1])
