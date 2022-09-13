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


class Binary(Expression):
    def __init__(self, left, token, right):
        self.left = left
        self.token = token
        self.right = right

    def accept(self, visitor):
        return visitor.visit_binary(self)


class Call(Expression):
    def __init__(self, callee, arguments):
        self.callee = callee
        self.arguments = arguments

    def accept(self, visitor):
        return visitor.visit_call(self)


class Grouping(Expression):
    def __init__(self, expr):
        self.expr = expr

    def accept(self, visitor):
        return visitor.visit_grouping(self)


class Literal(Expression):
    def __init__(self, value):
        self.value = value

    def accept(self, visitor):
        return visitor.visit_literal(self)


class Logical(Expression):
    def __init__(self, left, token, right):
        self.left = left
        self.token = token
        self.right = right

    def accept(self, visitor):
        return visitor.visit_logical(self)


class Unary(Expression):
    def __init__(self, token, right):
        self.token = token
        self.right = right

    def accept(self, visitor):
        return visitor.visit_unary(self)


class Variable(Expression):
    def __init__(self, name):
        self.name = name

    def accept(self, visitor):
        return visitor.variable(self)
