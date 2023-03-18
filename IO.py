from __future__ import annotations

import sys

from antlr4 import *

"""
This class is responsible for dealing with IO operations with the user.
"""


class IO:
    def __init__(self, filename):
        self.__filename = filename

    """
    This method gets the input pseudocode from the user as a string from the console. 
    This method is called when the user uses a shell option by passing the -sh flag.
    """

    def get_input(self) -> str:
        pseudocode = ""

        # Get pseudocode from the user until the user enters an EOF character.
        while True:
            try:
                line = input()
                if line == "quit": break
            except EOFError:
                break
            pseudocode += line + '\n'
        return pseudocode

    """
    This method gets the input text file from the user and converts it into an antlr InputStream / FileStream.
    It also handles the special case where the user has passed the -sh flag, in which case it gets input from the console.
    It also handles errors if the file is not found, and exits the program if so.
    """

    def get_stream(self) -> (InputStream | FileStream):  # type: ignore
        # Check if user has passed -sh flag and get input from the console if so.
        if self.__filename == "-sh":
            return InputStream(self.get_input())  # type: ignore
        # If not, convert the file into an ANTLR file stream.
        # If the file is not found, print an error message and end the program.
        else:
            try:
                return FileStream(self.__filename)  # type: ignore
            except FileNotFoundError as e:
                print(e)
                sys.exit(1)

    """
    This method outputs the translated python program to the user.
    This method will either print the code to the console if the -sh flag was passed or write to the output file if not.
    """

    def write(self, string: str) -> None:
        # Check if -sh flag was passed. If so, print translated python code to console.
        if self.__filename == "-sh":
            print(string)
            return None
        # If -sh flag was not passed, write the translated python code to the file output.py.
        else:
            output = open(f"output.py", 'w')
            output.write(string)
            output.close()
