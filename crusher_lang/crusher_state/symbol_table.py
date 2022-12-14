from .runtime_exceptions import CrusherRuntimeError


class SymbolTable:
    """SymbolTable holds all the declarations in a block.
    Has a property `self.parent` which points to the symbol table of the current block.
    """

    def __init__(self, parent=None):
        self.parent = parent
        self.values = {}

    def get(self, token):
        if token.lexeme in self.values:
            return self.values[token.lexeme]

        if self.parent is not None:
            return self.parent.get(token)

        raise CrusherRuntimeError(f"Undefined variable {token.lexeme}.")

    def assign(self, token, value):
        if token.lexeme in self.values:
            self.values[token.lexeme] = value
            return value

        if self.parent is not None:
            return self.parent.assign(token, value)

        raise CrusherRuntimeError(f"Undefined variable {token.lexeme}.")

    def define(self, token, value):
        if token.lexeme in self.values:
            raise CrusherRuntimeError(f"Variable {token.lexeme} already defined.")

        self.values[token.lexeme] = value
