from gen.pseudoVisitor import pseudoVisitor
from gen.pseudoParser import pseudoParser


# This class is NOT used by the type checker: only used in text translator
class Record:
    def __init__(self, ctx: pseudoParser.RecordContext):
        self.fields = []
        for field in ctx.field():
            self.fields.append(field.IDENTIFIER()[0].getText())
