import itertools
from operation import Operation


class Node:
    id_counter = itertools.count().__next__
    
    def __init__(self, terminal: bool,  operation: Operation, value = None) -> None:
        self.id = self.id_counter()
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