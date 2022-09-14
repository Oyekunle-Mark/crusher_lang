import sys

from lexer.scanner import CrusherException
from lexer.scanner import Scanner
from ast_generator.parser import Parser
from ast_generator.parser import ParserException


class Interpreter:
    """The Crusher Interpreter"""

    def __init__(self, arguments):
        self.args = arguments
        self.scanner = Scanner()
        self.parser = Parser()

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
                self.__execute(user_input)
            except CrusherException as e:
                print("Error: " + str(e))
            except ParserException as e:
                print("Parser Error: " + str(e))

    def __run_file(self, file_name):
        """Run a crusher source file"""

        with open(file_name) as file:
            # Loads the source file and writes the entire file content
            # to the raw_text property as string.

            raw_text = file.read()

        self.__execute(raw_text)

    def __execute(self, raw_text):
        tokens = self.scanner.scan(raw_text=raw_text)
        statements = self.parser.parse(tokens=tokens)

        for statement in statements:
            print(statement)


if __name__ == "__main__":
    interpreter = Interpreter(sys.argv)
    interpreter.run()
