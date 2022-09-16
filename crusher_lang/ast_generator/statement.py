from abc import ABC, abstractmethod


class StatementVisitor(ABC):
    @abstractmethod
    def visit_expression(self, expression_stmt):
        pass

    @abstractmethod
    def visit_block(self, block_stmt):
        pass

    @abstractmethod
    def visit_function(self, function_stmt):
        pass

    @abstractmethod
    def visit_if(self, if_stmt):
        pass

    @abstractmethod
    def visit_print(self, print_stmt):
        pass

    @abstractmethod
    def visit_return(self, return_stmt):
        pass

    @abstractmethod
    def visit_let(self, let_stmt):
        pass

    @abstractmethod
    def visit_while(self, while_stmt):
        pass


class Statement(ABC):
    @abstractmethod
    def accept(self, visitor):
        pass


class ExpressionStatement(Statement):
    def __init__(self, expr):
        self.expr = expr

    def accept(self, visitor):
        return visitor.visit_expression(self)

    def __str__(self):
        return f"{self.expr}"


class BlockStatement(Statement):
    def __init__(self, statements):
        self.statements = statements

    def accept(self, visitor):
        return visitor.visit_block(self)

    def __str__(self):
        return f"{[str(stmt) for stmt in self.statements]}"


class FunctionStatement(Statement):
    def __init__(self, name, parameters, body):
        self.name = name
        self.parameters = parameters
        self.body = body

    def accept(self, visitor):
        return visitor.visit_function(self)

    def __str__(self):
        return f"fn {self.name.lexeme}({[str(param) for param in self.parameters]}) |{[str(stmt) for stmt in self.body]}|"


class IfStatement(Statement):
    def __init__(self, condition, then_branch, else_branch):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

    def accept(self, visitor):
        return visitor.visit_if(self)

    def __str__(self):
        return f"if {self.condition} |{self.then_branch}| else |{self.else_branch}|"


class PrintStatement(Statement):
    def __init__(self, expr):
        self.expr = expr

    def accept(self, visitor):
        return visitor.visit_print(self)

    def __str__(self):
        return f"print {self.expr}"


class ReturnStatement(Statement):
    def __init__(self, expr):
        self.expr = expr

    def accept(self, visitor):
        return visitor.visit_return(self)

    def __str__(self):
        return f"return {self.expr}"


class LetStatement(Statement):
    def __init__(self, name, initializer):
        self.name = name
        self.initializer = initializer

    def accept(self, visitor):
        return visitor.visit_let(self)

    def __str__(self):
        return f"let {self.name.lexeme} = {self.initializer}"


class WhileStatement(Statement):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def accept(self, visitor):
        return visitor.visit_while(self)

    def __str__(self):
        return f"while ({self.condition}) |{self.body}|"
