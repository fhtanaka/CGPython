class Operation:
    def __init__(self, arity:int, operation:callable, string:str):
        self.arity  = arity
        self.string = string
        self.func   = operation
        
    def __call__(self, *args):
        return self.func(*args)