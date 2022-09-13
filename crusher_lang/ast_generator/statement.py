from abc import ABC, abstractmethod


class StatementVisitor(ABC):
    @abstractmethod
    def visit_expression(self, assignment_stmt):
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
