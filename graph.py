from typing import Dict, List
from node import Node
from operation import Operation
import numpy as np

cte = Operation(arity=1, operation=lambda x:x, string="x")

class Graph:
    operations: List[Operation] = []
    rng = np.random
    
    @staticmethod
    def add_operation(arity, func, string):
        op = Operation(arity, func, string)
        Graph.operations.append(op)

    def __init__(self, n_in: int, n_out: int, n_row: int, n_col: int, levels_back: int):
        self.nodes: Dict[str, Node] = {}
        self.columns = []

        self.n_in = n_in
        self.n_out = n_out
        self.n_row = n_row
        self.n_col = n_col
        self.levels_back = levels_back
        
        self.add_input_layer()
        self.add_middle_layers()
        self.add_output_layer()

    def create_node_column(self, size, terminal = False, active = False, operation = None):
        col = []
        for i in range(size):
            op = operation if operation is not None else Graph.rng.choice(Graph.operations)
            new_node = Node(terminal=terminal, operation=op, active=active)
            self.nodes[new_node.id] = new_node
            col.append(new_node.id)
        return col

    def add_input_layer(self):
        inputs = self.create_node_column(self.n_in, terminal=True, operation=cte)
        self.columns.append(inputs)    

    def add_middle_layers(self):    
        for _ in range(self.n_col):
            col = self.create_node_column(self.n_row)
            self.columns.append(col)
            
    def add_output_layer(self):    
        outputs = self.create_node_column(self.n_out, operation=cte, active=True)
        self.columns.append(outputs)

    def make_connections(self, full: bool): # only active nodes have connections
        # for each column, from output layer to input layer
        start = len(self.columns)-1
        for i in range(start, 0, -1):
            # list of all previous nodes flattened
            min_col = np.maximum(0, i - self.levels_back)
            previous_cols = [value for col in self.columns[min_col:i] for value in col]
            
            # for each node in the layer i
            for j in self.columns[i]:
                current_node = self.nodes[j]

                if full or current_node.active:
                    arity  = current_node.operation.arity
                    
                    # pick n=arity nodes randomly
                    inodes_idlist = Graph.rng.choice(previous_cols, arity)
                    
                    # add to the list of inputs
                    current_node.add_inputs(inodes_idlist)
                    
                    # mark picked nodes as active
                    # (another option, we could process active nodes only)
                    if current_node.active:
                        for nodeid in inodes_idlist:
                            self.nodes[nodeid].active = True

    def set_inputs(self, input_values):
        if len(input_values) != self.n_in:
            msg = "Expected %d inputs but received %d values" % (self.n_in, len(input_values))
            raise RuntimeError(msg)
        for nodeid, value in zip(self.columns[0], input_values):
            self.nodes[nodeid].value = value

    # this function is mostly for testing purposes
    def _add_node(self, value = None, operation = None, terminal = False):
        if operation == None and value == None:
            operation = Graph.rng.choice(Graph.operations)
        new_node = Node(terminal, operation, value)
        self.nodes[new_node.id] = new_node
        return new_node.id

    def reset_graph_value(self):
        for n_id in self.nodes:
            if not self.nodes[n_id].terminal:
                self.nodes[n_id].value = None
    
    def operate(self, input_values):
        self.set_inputs(input_values)
        results = [self.get_node_value(out) for out in self.columns[-1]]
        return results

    def get_node_value(self, node_id):
        node = self.nodes[node_id]
        if node.value is not None:
            return node.value
        
        node.value = node.operation(*[self.get_node_value(x) for x in node.inputs])
        
        return node.value