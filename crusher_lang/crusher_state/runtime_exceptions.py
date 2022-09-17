class CrusherRuntimeError(Exception):
    """Crusher runtime exception"""

    pass


class ReturnException(Exception):
    """The return exception is used to implement the return statement
    Where self.value is the returned value from the called function.
    """

    def __init__(self, value):
        self.value = value
