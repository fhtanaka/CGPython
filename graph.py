from typing import Dict
from node import Node
from operation import Operation
import numpy as np

class Graph:
    operations = []
    rng = np.random
    
    def __init__(self):
        self.nodes: Dict[str, Node] = {}
        self.columns = []

    def add_input_layer(self, n_in):
        self.n_in = n_in
        
        cte = Operation(arity=1, operation=lambda x:x, string="x")
        
        inputs = []
        for i in range(self.n_in):
            new_node = Node(terminal=True, operation=cte)
            new_node.active = False
            self.nodes[new_node.id] = new_node
            inputs.append(new_node.id)
        self.columns.append(inputs)    

    def add_middle_layers(self, n_row, n_col):
        self.n_row = n_row
        self.n_col = n_col
    
        for i in range(self.n_col):
            col = []
            for j in range(self.n_row):
                new_node = Node(terminal=False, operation=Graph.rng.choice(Graph.operations))
                new_node.active = False
                self.nodes[new_node.id] = new_node
                col.append(new_node.id)
            self.columns.append(col)
            
    def add_output_layer(self, n_out):
        self.n_out = n_out
    
        cte = Operation(arity=1, operation=lambda x:x, string="x")
        
        outputs = []
        for i in range(self.n_out):
            new_node = Node(terminal=False, operation=cte)
            new_node.active = True
            self.nodes[new_node.id] = new_node
            outputs.append(new_node.id)
        self.columns.append(outputs)

    def make_connections(self):
        # for each column, from output layer to input layer
        start = len(self.columns)-1
        for i in range(start, 0, -1):
            # list of all previous nodes flattened
            previous_cols = [value for col in self.columns[:i] for value in col]
            
            # for each node in the layer i
            for j in self.columns[i]:
                current_node = self.nodes[j]

                if current_node.active:
                    arity  = current_node.operation.arity
                    
                    # pick n=arity nodes randomly
                    inodes_idlist = Graph.rng.choice(previous_cols, arity)
                    
                    # add to the list of inputs
                    current_node.add_inputs(inodes_idlist)
                    
                    # mark picked nodes as active
                    # (another option, we could process active nodes only)
                    for nodeid in inodes_idlist:
                        self.nodes[nodeid].active = True

    def inputs(self, input_values):
        for nodeid, value in zip(self.columns[0], input_values):
            self.nodes[nodeid].value = value

    @staticmethod
    def add_operation(arity, func, string):
        op = Operation(arity, func, string)
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
        return node.value
        
    def get_value(self, node_id):
        node = self.nodes[node_id]
        if node.value is not None:
            return node.value
        
        node.value = node.operation(*[self.get_value(x) for x in node.inputs])
        
        return node.value