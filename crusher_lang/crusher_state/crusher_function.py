class CrusherFunction:
    def __init__(self, function_stmt, table):
        self.function_stmt = function_stmt
        self.table = table

    @property
    def arity(self):
        return len(self.function_stmt.parameters)

    def __str__(self):
        return f"<function {self.function_stmt.name.lexeme}>"
