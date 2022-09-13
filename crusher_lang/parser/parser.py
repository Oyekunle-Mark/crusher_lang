from .expression import Assignment
from .expression import Binary
from .expression import Call
from .expression import Grouping
from .expression import Literal
from .expression import Logical
from .expression import Unary
from .expression import Variable


class ParserException(Exception):
    """Crusher parser exception"""

    pass


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def parse(self):
        pass

    @property
    def __current(self):
        return self.tokens[self.current]

    @property
    def __previous(self):
        return self.tokens[self.current - 1]

    def __advance(self):
        if not self.__is_at_end:
            self.__current += 1

        return self.__previous

    @property
    def __is_at_end(self):
        return self.__current == len(self.tokens)

    def __match(self, token_type):
        if self.__is_at_end:
            return False

        return self.__current.token_type == token_type

    def __assert_match(self, token_type):
        if self.__match(token_type=token_type):
            return self.__advance()

        raise ParserException(
            f"Unexpected {self.__current.lexeme} in line {self.__current.line}"
        )
