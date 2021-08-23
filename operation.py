class Operation:
    def __init__(self, arity: int, operation: callable):
        self.arity = arity
        self.func = operation
        
    def __call__(self, *args):
        return self.func(*args)