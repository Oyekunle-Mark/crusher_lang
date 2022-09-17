class CrusherFunction:
    """Allows capture of the function statement and symbol table
    at the time of the function declaration.
    Also allows easier symbol table
    value type checking when asserting that a callee is actually a function.
    """

    def __init__(self, function_stmt, table):
        self.function_stmt = function_stmt
        self.table = table

    @property
    def arity(self):
        return len(self.function_stmt.parameters)

    def __str__(self):
        return f"<function {self.function_stmt.name.lexeme}>"
