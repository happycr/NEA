from __future__ import annotations

from antlr4 import *


class IO:
    @staticmethod
    def get_input() -> str:
        print("Enter pseudocode:")
        pseudocode = ""
        while True:
            try:
                line = input()
            except EOFError:
                break
            pseudocode += line + '\n'
        return pseudocode

    @staticmethod
    def get_stream() -> (InputStream | FileStream):
        return InputStream(IO.get_input())

    @staticmethod
    def write(string: str) -> None:
        print(string)
