from .token import Token
from .token_type import TokenType


class CrusherException(Exception):
    pass


KEYWORDS_MAPPING = {
    "let": TokenType.LET,
    "and": TokenType.AND,
    "or": TokenType.OR,
    "if": TokenType.IF,
    "else": TokenType.ELSE,
    "null": TokenType.NULL,
    "true": TokenType.TRUE,
    "false": TokenType.FALSE,
    "fn": TokenType.FN,
    "return": TokenType.RETURN,
    "while": TokenType.WHILE,
    "for": TokenType.FOR,
    "print": TokenType.PRINT,
}


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
            self.raw_text = file.read()
            self.raw_text += "\0"

    def scan(self):
        if self.file_name is not None:
            self.__load_file()

        while not self.__at_end_of_file:
            self.start = self.current
            self.__scan_line()

        return self.tokens

    def __scan_line(self):
        currentChar = self.__advance_char()

        # FIXME: A match statement would improve these mountain of madness
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
        elif currentChar == '"':
            self.__process_string()
        elif currentChar == ";":
            self.__add_token(TokenType.SEMICOLON)
        elif currentChar in [" ", "\r", "\t"]:
            pass
        elif currentChar == "\n":
            self.line += 1
        elif currentChar == "\0":
            self.__add_token(TokenType.EOF)
        else:
            if self.__is_digit(currentChar):
                self.__process_number()
            elif self.__is_alpha_numeric(currentChar):
                self.__process_identifier()
            else:
                raise CrusherException(f"Invalid character on line {self.line}")

    def __process_string(self):
        while self.__current_char != '"' and not self.__at_end_of_file:
            self.__advance_char()

        if self.__at_end_of_file:
            raise CrusherException(f"Unterminated string on line {self.line}")

        self.__advance_char()

        literal = self.raw_text[self.start : self.current]
        self.__add_token(token_type=TokenType.STRING, literal=literal)

    def __process_number(self):
        while self.__is_digit(self.__current_char):
            self.__advance_char()

        if self.__current_char == "." and self.__is_digit(self.__peek_ahead()):
            self.__advance_char()

            while self.__is_digit(self.__current_char):
                self.__advance_char()

        literal = float(self.raw_text[self.start : self.current])
        self.__add_token(TokenType.NUMBER, literal=literal)

    def __process_identifier(self):
        while self.__is_alpha_numeric(self.__current_char):
            self.__advance_char()

        lexeme = self.raw_text[self.start : self.current]
        token_type = TokenType.IDENTIFIER

        if lexeme in KEYWORDS_MAPPING:
            token_type = KEYWORDS_MAPPING[lexeme]

        self.__add_token(token_type=token_type)

    @property
    def __current_char(self):
        if self.__at_end_of_file:
            return "\0"

        return self.raw_text[self.current]

    def __peek_ahead(self):
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
        lexeme = self.raw_text[self.start : self.current]
        self.tokens.append(
            Token(
                token_type=token_type,
                lexeme=lexeme,
                literal=literal,
                line=self.line,
                column=self.current,
            )
        )

    def __is_digit(self, char):
        return char >= "0" and char <= "9"

    def __is_alpha(self, char):
        return (
            (char >= "a" and char <= "z")
            or (char >= "A" and char <= "Z")
            or char == "_"
        )

    def __is_alpha_numeric(self, char):
        return self.__is_alpha(char) or self.__is_digit(char)
