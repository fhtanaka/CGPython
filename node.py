import itertools
from typing import Any
from operation import Operation
import random

class Node:
    id_counter = itertools.count().__next__
    
    def __init__(self, col_num: int,  operation: Operation, value: Any = None, active: bool = False):
        self.id = self.id_counter()
        self.col_num = col_num
        self.value = value
        self.operation = operation
        self.active = active
        self.inputs = [] # List of node_ids
    
    def add_inputs(self, node_ids):
        for ids in node_ids:
            self.inputs.append(ids)
    
    def remove_inputs(self, ids_to_remove):
        self.inputs = [i for i in self.inputs if i not in ids_to_remove]
