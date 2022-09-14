from .expression import Assignment
from .expression import Binary
from .expression import Call
from .expression import Grouping
from .expression import Literal
from .expression import Logical
from .expression import Unary
from .expression import Variable
from .statement import ExpressionStatement
from .statement import BlockStatement
from .statement import FunctionStatement
from .statement import IfStatement
from .statement import PrintStatement
from .statement import ReturnStatement
from .statement import LetStatement
from .statement import WhileStatement
from lexer.token_type import TokenType


class ParserException(Exception):
    """Crusher parser exception"""

    pass


class Parser:
    def __init__(self):
        self.tokens = []
        self.current = 0

    def __init_parser(self, tokens):
        self.tokens = tokens
        self.current = 0

    def parse(self, tokens):
        self.__init_parser(tokens)
        statements = []

        while not self.__is_at_end:
            statements.append(self.__declaration())

        return statements

    def __declaration(self):
        if self.__match(TokenType.FN):
            return self.__function_declaration()

        if self.__match(TokenType.LET):
            return self.__let_declaration()

        return self.__statement()

    def __statement(self):
        if self.__match(TokenType.WHILE):
            return self.__while_statement()

        if self.__match(TokenType.IF):
            return self.__if_statement()

        if self.__match(TokenType.PRINT):
            return self.__print_statement()

        if self.__match(TokenType.RETURN):
            return self.__return_statement()

        if self.__match(TokenType.LEFT_BRACE):
            return BlockStatement(self.__block())

        return self.__expression_statement()

    def __let_declaration(self):
        name = self.__assert_match(TokenType.IDENTIFIER, "Expect variable name")

        initializer = None

        if self.__match(TokenType.EQUAL):
            initializer = self.__expression()

        self.__assert_match(TokenType.SEMICOLON, "Expects ';' after a declaration.")

        return LetStatement(name, initializer)

    def __function_declaration(self):
        name = self.__assert_match(TokenType.IDENTIFIER, "Expect function name")

        self.__assert_match(TokenType.LEFT_PAREN, "Expect '(' after function name.")
        parameters = []

        if not self.__match_not_advance(TokenType.RIGHT_PAREN):
            parameters.append(self.__expression())

            while self.__match(TokenType.COMMA):
                parameters.append(self.__expression())

        self.__assert_match(
            TokenType.RIGHT_PAREN, "Expect ')' after function parameters."
        )

        self.__assert_match(TokenType.LEFT_BRACE, "Expect '{' before function body.")
        body = self.__block()

        return FunctionStatement(name, parameters, body)

    def __block(self):
        statements = []

        while (
            not self.__match_not_advance(TokenType.RIGHT_BRACE) and not self.__is_at_end
        ):
            statements.append(self.__declaration())

        self.__assert_match(TokenType.RIGHT_BRACE, "Expect '}' after block.")

        return statements

    def __print_statement(self):
        expr = self.__expression()
        self.__assert_match(TokenType.SEMICOLON, "Expects ';' after a value.")

        return PrintStatement(expr)

    def __return_statement(self):
        expr = None

        if not self.__match_not_advance(TokenType.SEMICOLON):
            expr = self.__expression()

        self.__assert_match(TokenType.SEMICOLON, "Expects ';' after a return.")

        return ReturnStatement(expr)

    def __if_statement(self):
        self.__assert_match(TokenType.LEFT_PAREN, "Expect '(' after if statement.")
        condition = self.__expression()
        self.__assert_match(TokenType.RIGHT_PAREN, "Expect ')' after if condition.")

        then_branch = self.__statement()
        else_branch = None

        if self.__match(TokenType.ELSE):
            else_branch = self.__statement()

        return IfStatement(condition, then_branch, else_branch)

    def __expression_statement(self):
        expr = self.__expression()
        self.__assert_match(TokenType.SEMICOLON, "Expects ';' after an expression.")

        return ExpressionStatement(expr)

    def __while_statement(self):
        self.__assert_match(TokenType.LEFT_PAREN, "Expect '(' after while statement.")
        condition = self.__expression()
        self.__assert_match(TokenType.RIGHT_PAREN, "Expect ')' after while condition.")

        body = self.__statement()

        return WhileStatement(condition, body)

    def __expression(self):
        return self.__assignment()

    def __assignment(self):
        expr = self.__or()

        if self.__match(TokenType.EQUAL):
            if not isinstance(expr, Variable):
                raise ParserException(f"Invalid assignment target")

            value = self.__assignment()
            return Assignment(expr.name, value)

        return expr

    def __or(self):
        expr = self.__and()

        while self.__match(TokenType.OR):
            operator = self.__previous
            right = self.__and()
            expr = Logical(expr, operator, right)

        return expr

    def __and(self):
        expr = self.__equality()

        while self.__match(TokenType.AND):
            operator = self.__previous
            right = self.__equality()
            expr = Logical(expr, operator, right)

        return expr

    def __equality(self):
        expr = self.__comparison()

        while self.__match_many(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self.__previous
            right = self.__comparison()
            expr = Binary(expr, operator, right)

        return expr

    def __comparison(self):
        expr = self.__term()

        while self.__match_many(
            TokenType.GREATER,
            TokenType.GREATER_EQUAL,
            TokenType.LESS,
            TokenType.LESS_EQUAL,
        ):
            operator = self.__previous
            right = self.__term()
            expr = Binary(expr, operator, right)

        return expr

    def __term(self):
        expr = self.__factor()

        while self.__match_many(TokenType.PLUS, TokenType.MINUS):
            operator = self.__previous
            right = self.__factor()
            expr = Binary(expr, operator, right)

        return expr

    def __factor(self):
        expr = self.__unary()

        while self.__match_many(TokenType.SLASH, TokenType.STAR):
            operator = self.__previous
            right = self.__unary()
            expr = Binary(expr, operator, right)

        return expr

    def __unary(self):
        if self.__match_many(TokenType.BANG, TokenType.MINUS):
            operator = self.__previous
            right = self.__unary()

            return Unary(operator, right)

        return self.__call()

    def __call(self):
        expr = self.__primary()

        if self.__match(TokenType.LEFT_PAREN):
            expr = self.__process_call(expr)

        return expr

    def __process_call(self, callee):
        args = []

        if not self.__match_not_advance(TokenType.RIGHT_PAREN):
            args.append(self.__expression())

            while self.__match(TokenType.COMMA):
                args.append(self.__expression())

        self.__assert_match(
            TokenType.RIGHT_PAREN, "Expect ')' after function arguments"
        )

        return Call(callee=callee, arguments=args)

    def __primary(self):
        if self.__match(TokenType.TRUE):
            return Literal(True)

        if self.__match(TokenType.FALSE):
            return Literal(False)

        if self.__match(TokenType.NULL):
            return Literal(None)

        if self.__match(TokenType.IDENTIFIER):
            return Variable(self.__previous)

        if self.__match_many(TokenType.NUMBER, TokenType.STRING):
            return Literal(self.__previous.literal)

        if self.__match(TokenType.LEFT_PAREN):
            expr = self.__expression()
            self.__assert_match(
                TokenType.RIGHT_PAREN, "Expect closing ')' after an expression"
            )

            return Grouping(expr)

        raise ParserException("Unexpected expression")

    @property
    def __current(self):
        return self.tokens[self.current]

    @property
    def __previous(self):
        return self.tokens[self.current - 1]

    def __advance(self):
        if not self.__is_at_end:
            self.current += 1

        return self.__previous

    @property
    def __is_at_end(self):
        return self.current == len(self.tokens)

    def __match(self, token_type):
        if self.__is_at_end:
            return False

        if self.__current.token_type != token_type:
            return False

        self.__advance()
        return True

    def __match_not_advance(self, token_type):
        if self.__is_at_end:
            return False

        if self.__current.token_type != token_type:
            return False

        return True

    def __match_many(self, *token_type):
        for type in token_type:
            if self.__match(type):
                return True

        return False

    def __assert_match(self, token_type, message=None):
        if self.__match(token_type=token_type):
            return self.tokens[self.current - 1]

        raise ParserException(
            message
            if not None
            else f"Unexpected {self.__current.lexeme} in line {self.__current.line}"
        )
