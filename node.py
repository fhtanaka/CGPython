import itertools
from typing import Any, Optional
from operation import Operation

class Node:
    id_counter = itertools.count().__next__
    
    def __init__(self, col_num: int,  operation: Operation, value: Any = None, active: bool = False, n_id: Optional[int] = None):
        self.global_id = self.id_counter()
        if n_id is None:
            self.id = self.global_id
        else:
            self.id = n_id
        self.col_num = col_num
        self.value = value
        self.operation = operation
        self.active = active
        self.inputs = [] # List of node_ids
    
    def add_inputs(self, node_ids):
        for ids in node_ids:
            self.inputs.append(ids)
    
    # TODO: fix this hack. The problem is that if i have the self.inputs[2, 2] and 
    # I have to remove [2] I want only to remove one of the inputs, not both
    def remove_inputs(self, ids_to_remove):
        new_inputs = []
        for r in ids_to_remove:
            flag = True
            for id in self.inputs:
                if id == r and flag:
                    flag = False
                    continue
                new_inputs.append(id)
        self.inputs = new_inputs
