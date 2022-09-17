import sys

from lexer.scanner import CrusherException
from lexer.scanner import Scanner
from lexer.scanner import TokenType
from ast_generator.parser import Parser
from ast_generator.parser import ParserException
from ast_generator.expression import ExpressionVisitor
from ast_generator.expression import Variable
from ast_generator.expression import Literal
from ast_generator.statement import StatementVisitor
from ast_generator.statement import LetStatement
from crusher_state.crusher_function import CrusherFunction
from crusher_state.symbol_table import SymbolTable
from crusher_state.runtime_exceptions import CrusherRuntimeError
from crusher_state.runtime_exceptions import ReturnException


class Interpreter(ExpressionVisitor, StatementVisitor):
    """The Crusher Interpreter"""

    def __init__(self, arguments):
        self.args = arguments
        self.scanner = Scanner()
        self.parser = Parser()
        self.table = SymbolTable()

    def interpret(self):
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
            except CrusherRuntimeError as e:
                print("Runtime Error: " + str(e))
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
            except CrusherRuntimeError as e:
                print("Runtime Error: " + str(e))

    def __run_file(self, file_name):
        """Run a crusher source file"""

        self.__assert_crusher_extension(file_name=file_name)

        with open(file_name) as file:
            # Loads the source file and writes the entire file content
            # to the raw_text property as string.

            raw_text = file.read()

        self.__execute(raw_text)

    def __assert_crusher_extension(self, file_name):
        if not file_name.endswith(".crush"):
            raise CrusherException(f"Expect source code to end with .crush. Got a file named {file_name} instead.")

    def __execute(self, raw_text):
        tokens = self.scanner.scan(raw_text=raw_text)
        statements = self.parser.parse(tokens=tokens)

        for statement in statements:
            self.__execute_statement(statement)

    def __execute_statement(self, statement):
        return statement.accept(self)

    def visit_literal(self, literal_expr):
        return literal_expr.value

    def visit_variable(self, variable_expr):
        return self.table.get(variable_expr.name)

    def visit_unary(self, unary_expr):
        right = self.__execute_statement(unary_expr.right)

        if unary_expr.token.token_type == TokenType.BANG:
            return not self.__is_truthy(right)

        if unary_expr.token.token_type == TokenType.MINUS:
            self.__assert_operands_are_number(unary_expr.token, right)
            return -right

    def visit_logical(self, logical_expr):
        left = self.__execute_statement(logical_expr.left)
        right = self.__execute_statement(logical_expr.right)

        if logical_expr.token.token_type == TokenType.OR:
            if self.__is_truthy(left):
                return left

        if logical_expr.token.token_type == TokenType.AND:
            if not self.__is_truthy(left):
                return left

        return right

    def visit_grouping(self, grouping_expr):
        return self.__execute_statement(grouping_expr.expr)

    def visit_call(self, call_expr):
        callee = self.__execute_statement(call_expr.callee)
        arguments = []

        for argument in call_expr.arguments:
            arguments.append(self.__execute_statement(argument))

        if not isinstance(callee, CrusherFunction):
            raise CrusherRuntimeError("Call can only be done on functions.")

        if len(arguments) != callee.arity:
            raise CrusherRuntimeError(
                f"Expected {callee.arity} arguments, but got {len(arguments)}."
            )

        parameters_declarations = (
            self.__convert_arguments_and_parameters_to_declarations(
                callee.function_stmt.parameters, arguments
            )
        )
        body = parameters_declarations + callee.function_stmt.body

        try:
            self.__execute_block(body, SymbolTable(callee.table))
        except ReturnException as ret:
            return ret.value

    def __convert_arguments_and_parameters_to_declarations(self, parameters, arguments):
        declarations = []

        for parameter, argument in zip(parameters, arguments):
            if not isinstance(parameter, Variable):
                raise CrusherRuntimeError("Function parameters can only be identifiers")

            declarations.append(LetStatement(parameter.name, Literal(argument)))

        return declarations

    def visit_binary(self, binary_expr):
        left = self.__execute_statement(binary_expr.left)
        right = self.__execute_statement(binary_expr.right)

        if binary_expr.token.token_type == TokenType.EQUAL_EQUAL:
            return left == right

        if binary_expr.token.token_type == TokenType.BANG_EQUAL:
            return left != right

        if binary_expr.token.token_type == TokenType.GREATER:
            self.__assert_operands_are_number(binary_expr.token, left, right)
            return left > right

        if binary_expr.token.token_type == TokenType.GREATER_EQUAL:
            self.__assert_operands_are_number(binary_expr.token, left, right)
            return left >= right

        if binary_expr.token.token_type == TokenType.LESS:
            self.__assert_operands_are_number(binary_expr.token, left, right)
            return left < right

        if binary_expr.token.token_type == TokenType.LESS_EQUAL:
            self.__assert_operands_are_number(binary_expr.token, left, right)
            return left <= right

        if binary_expr.token.token_type == TokenType.MINUS:
            self.__assert_operands_are_number(binary_expr.token, left, right)
            return left - right

        if binary_expr.token.token_type == TokenType.SLASH:
            self.__assert_operands_are_number(binary_expr.token, left, right)
            return left / right

        if binary_expr.token.token_type == TokenType.STAR:
            self.__assert_operands_are_number(binary_expr.token, left, right)
            return left * right

        if binary_expr.token.token_type == TokenType.PLUS:
            if (isinstance(left, float) and isinstance(right, float)) or (
                isinstance(left, str) and isinstance(right, str)
            ):
                return left + right

            raise CrusherRuntimeError("Can only add two numbers or strings.")

    def visit_assignment(self, assignment_expr):
        value = self.__execute_statement(assignment_expr.value)
        return self.table.assign(assignment_expr.identifier, value)

    def visit_while(self, while_stmt):
        while self.__is_truthy(self.__execute_statement(while_stmt.condition)):
            self.__execute_statement(while_stmt.body)

    def visit_let(self, let_stmt):
        initializer = None

        if let_stmt.initializer is not None:
            initializer = self.__execute_statement(let_stmt.initializer)

        self.table.define(let_stmt.name, initializer)

    def visit_return(self, return_stmt):
        value = None

        if return_stmt.expr is not None:
            value = self.__execute_statement(return_stmt.expr)

        raise ReturnException(value)

    def visit_print(self, print_stmt):
        value = self.__execute_statement(print_stmt.expr)
        print(self.__stringify_to_crusher_format(value))

    def visit_if(self, if_stmt):
        if self.__is_truthy(self.__execute_statement(if_stmt.condition)):
            self.__execute_statement(if_stmt.then_branch)
        elif if_stmt.else_branch is not None:
            self.__execute_statement(if_stmt.else_branch)

    def visit_function(self, function_stmt):
        crusher_function = CrusherFunction(function_stmt, self.table)
        self.table.define(function_stmt.name, crusher_function)

    def visit_block(self, block_stmt):
        self.__execute_block(block_stmt.statements, SymbolTable(self.table))

    def visit_expression(self, expression_stmt):
        return self.__execute_statement(expression_stmt.expr)

    def __execute_block(self, statements, table):
        previous = self.table
        self.table = table

        try:
            for statement in statements:
                self.__execute_statement(statement)
        finally:
            self.table = previous

    def __stringify_to_crusher_format(self, value):
        if value is None:
            return "null"

        if isinstance(value, bool):
            return "true" if value else "false"

        if isinstance(value, float):
            if str(value).endswith(".0"):
                return int(value)

        return value

    def __is_truthy(self, value):
        if value is None:
            return False

        if isinstance(value, bool):
            return value

        return True

    def __assert_operands_are_number(self, operator, *operands):
        for operand in operands:
            if not isinstance(operand, float):
                raise CrusherRuntimeError(f"{operator.lexeme} expects a number.")


if __name__ == "__main__":
    Interpreter(sys.argv).interpret()
