from .expression import Assignment
from .expression import Binary
from .expression import Call
from .expression import Grouping
from .expression import Literal
from .expression import Logical
from .expression import Unary
from .expression import Variable
from lexer.token_type import TokenType


class ParserException(Exception):
    """Crusher parser exception"""

    pass


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.expressions = []
        self.current = 0

    def parse(self):
        while not self.__is_at_end:
            self.expressions.append(self.__expression())

        return self.expressions

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

        self.__assert_match(TokenType.RIGHT_PAREN, "Expect ')' after function arguments")

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
            return

        raise ParserException(
            message
            if not None
            else f"Unexpected {self.__current.lexeme} in line {self.__current.line}"
        )
