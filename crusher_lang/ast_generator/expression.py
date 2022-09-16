from abc import ABC, abstractmethod


class ExpressionVisitor(ABC):
    @abstractmethod
    def visit_assignment(self, assignment_expr):
        pass

    @abstractmethod
    def visit_binary(self, binary_expr):
        pass

    @abstractmethod
    def visit_call(self, call_expr):
        pass

    @abstractmethod
    def visit_grouping(self, grouping_expr):
        pass

    @abstractmethod
    def visit_literal(self, literal_expr):
        pass

    @abstractmethod
    def visit_logical(self, logical_expr):
        pass

    @abstractmethod
    def visit_unary(self, unary_expr):
        pass

    @abstractmethod
    def visit_variable(self, variable_expr):
        pass


class Expression(ABC):
    @abstractmethod
    def accept(self, visitor):
        pass


class Assignment(Expression):
    def __init__(self, identifier, value):
        self.identifier = identifier
        self.value = value

    def accept(self, visitor):
        return visitor.visit_assignment(self)

    def __str__(self):
        return f"{self.identifier.lexeme} = {self.value}"


class Binary(Expression):
    def __init__(self, left, token, right):
        self.left = left
        self.token = token
        self.right = right

    def accept(self, visitor):
        return visitor.visit_binary(self)

    def __str__(self):
        return f"({self.left} {self.token.lexeme} {self.right})"


class Call(Expression):
    def __init__(self, callee, arguments):
        self.callee = callee
        self.arguments = arguments

    def accept(self, visitor):
        return visitor.visit_call(self)

    def __str__(self):
        return f"{self.callee}({[str(x) for x in self.arguments]})"


class Grouping(Expression):
    def __init__(self, expr):
        self.expr = expr

    def accept(self, visitor):
        return visitor.visit_grouping(self)

    def __str__(self):
        return f"({self.expr})"


class Literal(Expression):
    def __init__(self, value):
        self.value = value

    def accept(self, visitor):
        return visitor.visit_literal(self)

    def __str__(self):
        return f"{self.value}"


class Logical(Expression):
    def __init__(self, left, token, right):
        self.left = left
        self.token = token
        self.right = right

    def accept(self, visitor):
        return visitor.visit_logical(self)

    def __str__(self):
        return f"({self.left} {self.token.lexeme} {self.right})"


class Unary(Expression):
    def __init__(self, token, right):
        self.token = token
        self.right = right

    def accept(self, visitor):
        return visitor.visit_unary(self)

    def __str__(self):
        return f"{self.token.lexeme}({self.right})"


class Variable(Expression):
    def __init__(self, name):
        self.name = name

    def accept(self, visitor):
        return visitor.visit_variable(self)

    def __str__(self):
        return f"{self.name.lexeme}"
