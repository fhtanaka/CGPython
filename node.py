import itertools
from typing import Any, List

class Node:
    id_counter = itertools.count().__next__
    
    def __init__(self, local_id: int, operation: float, value: Any = None, active: bool = False):
        self.global_id = self.id_counter()
        self.id = local_id
        self.value = value
        self.operation = operation
        self.active = active
        self.inputs: List[float] = [] # List of node_ids
    
    def add_inputs(self, node_ids):
        for ids in node_ids:
            self.inputs.append(ids)

    def remove_inputs(self, ids_to_remove):
        for r in ids_to_remove:
            if r in self.inputs:
                self.inputs.remove(r)
