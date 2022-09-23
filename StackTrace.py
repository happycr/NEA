class StackTrace:
    def __init__(self):
        self.stacktrace = []

    def add_expr(self, expr_text: str):
        stacktrace_text = f"In expr: {expr_text}"
        self.stacktrace.append(stacktrace_text)
        return self

    def add_line(self, line_no: int, line_text):
        stacktrace_text = f"In line {line_no}: {line_text}"
        self.stacktrace.append(stacktrace_text)
        return self

