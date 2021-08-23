from typing import Dict
import random
from node import Node
from operation import Operation

class Graph:
    operations = []
    
    def __init__(self):
        self.nodes: Dict[str, Node] = {}
        self.columns = []
        
    @staticmethod
    def add_operation(arity, func):
        op = Operation(arity, func)
        Graph.operations.append(op)
    
    def initializate_graph(self, n_in, n_out, n_row, n_col):
        for i in range(n_col):
            col = []
            for j in range(n_row):
                op = random.choice(Graph.operations)
                new_node = Node(False, op)
                self.nodes[new_node.id] = new_node
                col.append(new_node.id)
            self.columns.append(col)
    
    # this function is mostly for testing purposes
    def _add_node(self, value = None, operation = None, terminal = False):
        if operation == None and value == None:
            operation = random.choice(Graph.operations)
        new_node = Node(terminal, operation, value)
        self.nodes[new_node.id] = new_node
        return new_node.id

    def reset_graph_value(self):
        for n_id in self.nodes:
            if not self.nodes[n_id].terminal:
                self.nodes[n_id].value = None

    def get_node_value(self, node_id: int):
        node = self.nodes[node_id]
        if node.value != None:
            return node.value

        inputs = []
        for i in node.inputs:
            value = self.get_node_value(i)
            inputs.append(value)
        
        result = node.operation(*inputs)
        node.value = result # this may help avoid recalculating nodes in the same execution
                            # remember to make this value null when reseting the graph
        
        return result
