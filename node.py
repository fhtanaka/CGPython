import itertools
from typing import Any, Optional
from operation import Operation


class Node:
    id_counter = itertools.count().__next__
    
    def __init__(self, terminal: bool,  operation: Operation, value: Any = None, active: bool = False) -> None:
        self.id = self.id_counter()
        self.terminal = terminal
        self.value = value
        self.operation = operation
        self.active = active
        self.inputs = [] # List of node_ids
    
    def add_inputs(self, node_ids: list) -> None:
        for ids in node_ids:
            self.inputs.append(ids)
    
    def remove_inputs(self, ids_to_remove: list) -> None:
        self.inputs = [i for i in self.inputs if i not in ids_to_remove]