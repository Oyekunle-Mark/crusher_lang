import sys

from crusher_lang.lexer.scanner import Scanner


def execute(tokens):
    for token in tokens:
        print(token)


def run_file(file_name):
    scanner = Scanner(file_name=file_name)
    tokens = scanner.scan()

    execute(tokens)


def run_repl():
    while True:
        input = input("> ")

        if input == "exit":
            sys.exit(0)

        scanner = Scanner(raw_text=input)
        tokens = scanner.scan()

        execute(tokens)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        run_repl()
    elif len(sys.argv) == 2:
        run_file(sys.argv[1])
    else:
        print("Error!!!")
        print("Usage: ./crusher.py [some_file.crush]")

        sys.exit(64)
