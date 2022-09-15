class CrusherFunction:
    def __init__(self, name, parameters, body):
        self.name = name
        self.parameters = parameters
        self.body = body

    @property
    def arity(self):
        return len(self.parameters)

    def call(self, arguments):
        pass
