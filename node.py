import itertools
from typing import Any, List, Optional
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
        self.inputs: List[int] = [] # List of node_ids
    
    def add_inputs(self, node_ids):
        for ids in node_ids:
            self.inputs.append(ids)

    def remove_inputs(self, ids_to_remove):
        for r in ids_to_remove:
            if r in self.inputs:
                self.inputs.remove(r)
