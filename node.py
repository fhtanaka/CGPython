import itertools
from collections import namedtuple

class Operation:
    def __init__(self, arity: int, operation: function):
        self.arity = arity
        self.func = operation

class Node:

    idC_cunter = itertools.count().__next__
    
    def __init__(self, terminal: bool,  operation: Operation, value = None) -> None:
        self.id = self.idCounter()
        self.terminal = terminal
        self.value = value
        self.operation = operation
        self.inputs = [] # List of node_ids
    
    def add_inputs(self, node_ids):
        for id in node_ids:
            self.inputs.append(id)
    
    def remove_inputs(self, ids_to_remove):
        new_inputs = []
        for id in self.inputs:
            if id not in ids_to_remove:
                new_inputs.append(id)
        self.inputs = new_inputs