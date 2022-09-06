# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

from IO import IO
from Translator import Translator
from Errors import *


def main():
    stream = IO.get_stream()
    try:
        output = Translator.translate(stream)
        IO.write(output)

    except TranslationError as e:
        print(e.output_msg())


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
