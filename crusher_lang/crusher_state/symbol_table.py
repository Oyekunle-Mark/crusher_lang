class CrusherRuntimeError(Exception):
    pass


class SymbolTable:
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
            return

        raise CrusherRuntimeError(f"Undefined variable {token.lexeme}.")

    def define(self, token, value):
        if token.lexeme in self.values:
            raise CrusherRuntimeError(f"Variable {token.lexeme} already defined.")

        self.values[token.lexeme] = value
