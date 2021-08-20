from typing import Dict
import random
from .node import Node, Operation

class Graph:
    def __init__(self):
        self.operations = []
        self.nodes: Dict[str, Node] = {}
        self.columns = []

    def add_operation(self, arity, func):
        op = Operation(arity, func)
        self.operations.append(op)
    
    def initializate_graph(self, n_in, n_out, n_row, n_col):
        for i in range(n_col):
            col = []
            for j in range(n_row):
                op = random.choice(self.operations)
                new_node = Node(False, op)
                self.nodes[new_node.id] = new_node
                col.append(new_node.id)
            self.columns.append(col)
    
    def get_node_value(self, node_id: int):
        node = self.nodes[node_id]
        if node.value != None:
            return node.value

        inputs = []
        for i in range(node.inputs):
            value = self.get_node_value(node.inputs[i])
            inputs.append(value)
        
        result = node.operation(*inputs)
        node.value = result # this may help avoid recalculating nodes in the same execution
        
        return result
