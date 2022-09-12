from .token import Token
from .token_type import TokenType


class Scanner:
    """Scans a source file and returns the tokens"""

    def __init__(self, file_name=None, raw_text=None):
        self.file_name = file_name
        self.raw_text = raw_text
        self.start = 0
        self.current = 0
        self.line = 1
        self.tokens = []
        self.current_token_index = 0

    def __load_file(self):
        """Loads the source file and writes the entire file content
        to the raw_text property as string
        """

        with open(self.file_name) as file:
            self.raw_text = file.read

    def scan(self):
        if self.file_name is None and self.raw_text is None:
            return  # TODO: handle this weird case

        self.__load_file

        while not self.__at_end_of_file:
            self.start = self.current
            self.__scan_line()

        return self.tokens

    def __scan_line(self):
        currentChar = self.__advance_char()

        if currentChar == "(":
            self.__add_token(TokenType.LEFT_PAREN)
        elif currentChar == ")":
            self.__add_token(TokenType.RIGHT_PAREN)
        elif currentChar == "{":
            self.__add_token(TokenType.LEFT_BRACE)
        elif currentChar == "}":
            self.__add_token(TokenType.RIGHT_BRACE)
        elif currentChar == ",":
            self.__add_token(TokenType.COMMA)
        elif currentChar == "-":
            self.__add_token(TokenType.MINUS)
        elif currentChar == "+":
            self.__add_token(TokenType.PLUS)
        elif currentChar == "/":
            if self.__match_char("/"):
                while self.__current_char != "\n" and not self.__at_end_of_file:
                    self.__advance_char()

                return

            self.__add_token(TokenType.SLASH)
        elif currentChar == "*":
            self.__add_token(TokenType.STAR)
        elif currentChar == "!":
            token_type = (
                TokenType.BANG_EQUAL if self.__match_char("=") else TokenType.BANG
            )
            self.__add_token(token_type)
        elif currentChar == "=":
            token_type = (
                TokenType.EQUAL_EQUAL if self.__match_char("=") else TokenType.EQUAL
            )
            self.__add_token(token_type)
        elif currentChar == ">":
            token_type = (
                TokenType.GREATER_EQUAL if self.__match_char("=") else TokenType.GREATER
            )
            self.__add_token(token_type)
        elif currentChar == "<":
            token_type = (
                TokenType.LESS_EQUAL if self.__match_char("=") else TokenType.LESS
            )
            self.__add_token(token_type)
        elif currentChar == ";":
            self.__add_token(TokenType.SEMICOLON)
        elif currentChar in [" ", "\r", "\t"]:
            pass
        elif currentChar == "\n":
            self.line += 1
        else:
            pass  # TODO:  raise exception here

    @property
    def __current_char(self):
        if self.__at_end_of_file:
            return "\0"

        return self.raw_text[self.current]

    def __peek_char(self):
        if self.__at_end_of_file:
            return "\0"

        return self.raw_text[self.current + 1]

    def __advance_char(self):
        previous = self.__current_char
        self.current += 1

        return previous

    def __match_char(self, char):
        if self.__at_end_of_file:
            return False

        if char != self.__current_char:
            return False

        self.__advance_char()
        return True

    @property
    def __at_end_of_file(self):
        return self.current >= len(self.raw_text)

    def __add_token(self, token_type, literal=None):
        lexeme = self.raw_text[self.start : self.current + 1]
        self.tokens.append(
            Token(
                token_type=token_type,
                lexeme=lexeme,
                literal=literal,
                line=self.line,
                column=self.current,
            )
        )
