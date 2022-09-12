from enum import Enum


class TokenType(Enum):
    """This enum contains the Crusher token types
    """

    # single character tokens
    LEFT_PAREN = 0
    RIGHT_PAREN = 1
    LEFT_BRACE = 2
    RIGHT_BRACE = 3
    COMMA = 4
    MINUS = 5
    PLUS = 6
    SLASH = 7
    STAR = 8
    BANG = 9
    EQUAL = 10
    GREATER = 11
    LESS = 12
    SEMICOLON = 13

    # two character tokens
    BANG_EQUAL = 14
    EQUAL_EQUAL = 15
    GREATER_EQUAL = 16
    LESS_EQUAL = 17

    # literals
    IDENTIFIER = 18
    STRING = 19
    NUMBER = 20

    # keywords
    LET = 21
    AND = 22
    OR = 23
    IF = 24
    ELSE = 25
    NULL = 26
    TRUE = 27
    FALSE = 28
    FN = 29
    RETURN = 30
    WHILE = 31
    FOR = 32
    PRINT = 33 # technically isn't a keyword, but since I might not be adding a standard library, I'm hacking print in.

    # The ubiquitous, yet discreet end-of-line
    EOF = 44
