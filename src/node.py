import itertools
import numpy as np
from typing import Any, List


def get_operation(op_value, available_operations):
    if op_value == None:
        return None
    op_index = int(op_value*len(available_operations))
    return available_operations[op_index]

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

    def decode_inputs(self):
        return [int(x*self.id) for x in self.inputs]

    def crossover(self, r, n_id, second_parent, available_operations, rng=np.random.default_rng()):
        inputs = []
        for g1, g2 in itertools.zip_longest(self.inputs, second_parent.inputs):
            if g1 == None:
                inputs.append(g2)
            elif g2 == None:
                inputs.append(g1)
            else:
                inputs.append(((1 - r) * g1) + (r * g2))

        op_value = None
        if self.operation != None and second_parent.operation != None:
            op_value = ((1 - r) * self.operation) + (r * second_parent.operation)
            op = get_operation(op_value, available_operations)

            if len(inputs) < op.arity:  # Adding more inputs if necessary
                for _ in range(op.arity-len(inputs)):
                    inputs.append(rng.uniform())
            elif len(inputs) > op.arity:  # removing inputs if necessary
                inputs = inputs[:op.arity]

        child_node = Node(n_id, op_value)
        child_node.add_inputs(inputs)

        return child_node
