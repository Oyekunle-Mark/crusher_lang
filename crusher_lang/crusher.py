import sys

from lexer.scanner import CrusherException
from lexer.scanner import Scanner


def execute(tokens):
    for token in tokens:
        print(token)


def run_file(file_name):
    """Run a crusher source file"""

    scanner = Scanner(file_name=file_name)
    tokens = scanner.scan()

    execute(tokens)


def run_repl():
    """Starts the crusher REPL"""

    print("\nWelcome to Crusher Lang. \nVersion 0.0.1 - Written by Oye Oloyede\n")

    while True:
        user_input = input("> ")

        if user_input == "exit":
            print("\nQuitting... \nGoodbye. Thank you for using Crusher Lang")
            sys.exit(0)

        try:
            scanner = Scanner(raw_text=user_input)
            tokens = scanner.scan()

            execute(tokens)
        except CrusherException as e:
            print("Error: " + str(e))


if __name__ == "__main__":
    if len(sys.argv) == 1:
        run_repl()
    elif len(sys.argv) == 2:
        try:
            run_file(sys.argv[1])
        except CrusherException as e:
            print("Error: " + str(e))
            sys.exit(1)
    else:
        print("Error!!!")
        print("Usage: python crusher.py [some_file.crush]")
        sys.exit(1)
