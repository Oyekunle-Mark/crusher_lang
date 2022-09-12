from lexer.token import Token
from lexer.token_type import TokenType


class Scanner:
    """Scans a source file and returns the tokens"""

    def __init__(self, file_name):
        self.file_name = file_name
        self.raw_text = ""
        self.start = 0
        self.current = 0
        self.line = 0
        self.tokens = []
        self.current_token_index = 0
        self.input_scanned = False

    def __load_file(self):
        """Loads the source file and writes the entire file content
        to the raw_text property as string
        """

        with open(self.file_name) as file:
            self.raw_text = file.read

    def scan(self):
        self.__load_file

    @property
    def __current_char(self):
        return self.raw_text[self.current]

    @property
    def __peek_char(self):
        if self.current == len(self.raw_text):
            return TokenType.EOF

        return self.raw_text[self.current + 1]

    def __advance_char(self):
        previous = self.__current_char
        self.current += 1

        return previous

    def __match_char(self, char):
        if char != self.__current_char:
            return False

        self.__advance_char()
        return True

    @property
    def __at_end_of_tokens(self):
        return self.input_scanned and self.current_token_index == len(self.tokens)

    @property
    def current_token(self):
        return self.tokens[self.current_token_index]

    @property
    def peek(self):
        return self.tokens[self.current_token_index + 1]

    def advance(self):
        previous = self.current_token
        self.current_token_index += 1

        return previous

    def match(self, token):
        if token != self.current_token:
            return False

        self.advance()
        return True