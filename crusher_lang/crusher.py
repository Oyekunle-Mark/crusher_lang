import sys

from lexer.scanner import CrusherException
from lexer.scanner import Scanner
from ast_generator.parser import Parser
from ast_generator.parser import ParserException


class Interpreter:
    """The Crusher Interpreter"""

    def __init__(self, arguments):
        self.args = arguments

    def run(self):
        """Run the interpreter"""

        if len(self.args) == 1:
            self.__run_repl()
        elif len(self.args) == 2:
            try:
                self.__run_file(self.args[1])
            except CrusherException as e:
                print("Error: " + str(e))
                sys.exit(1)
            except ParserException as e:
                print("Parser Error: " + str(e))
                sys.exit(1)
        else:
            print("Error!!!")
            print("Usage: python crusher.py [some_file.crush]")
            sys.exit(1)

    def __run_repl(self):
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

                self.__execute(tokens)
            except CrusherException as e:
                print("Error: " + str(e))
            except ParserException as e:
                print("Parser Error: " + str(e))

    def __run_file(self, file_name):
        """Run a crusher source file"""

        scanner = Scanner(file_name=file_name)
        tokens = scanner.scan()

        self.__execute(tokens)

    def __execute(self, tokens):
        parser = Parser(tokens=tokens)
        expressions = parser.parse()

        for expression in expressions:
            print(expression)


if __name__ == "__main__":
    interpreter = Interpreter(sys.argv)
    interpreter.run()
