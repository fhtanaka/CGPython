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

    def __init__(self, n_in: int, n_out: int, n_row: int, n_col: int, levels_back: int, initialize: bool = True):
        self.nodes: Dict[str, Node] = {}
        self.columns: List[List[int]] = []

        self.n_in = n_in
        self.n_out = n_out
        self.n_row = n_row
        self.n_col = n_col
        self.levels_back = levels_back
        
        if initialize:
            self.add_input_layer()
            self.add_middle_layers()
            self.add_output_layer()

            self.make_connections(True)

    def create_node_column(self, size, col_num, active = False, operation = None):
        col = []
        for i in range(size):
            op = operation if operation is not None else Graph.rng.choice(Graph.operations)
            new_node = Node(col_num=col_num, operation=op, active=active)
            self.nodes[new_node.id] = new_node
            col.append(new_node.id)
        return col

    def add_input_layer(self):
        inputs = self.create_node_column(self.n_in, 0, operation=cte)
        self.columns.append(inputs)    

    def add_middle_layers(self):    
        for i in range(self.n_col):
            col = self.create_node_column(self.n_row, i+1)
            self.columns.append(col)
            
    def add_output_layer(self):
        col_num = 1 + self.n_col
        outputs = self.create_node_column(self.n_out, col_num, operation=cte, active=True)
        self.columns.append(outputs)

    # list of all previous nodes flattened
    def get_possible_previous_nodes(self, col_num):
        min_col = np.maximum(0, col_num - self.levels_back)
        previous_cols = [value for col in self.columns[min_col:col_num] for value in col]
        return previous_cols

    def make_connections(self, full): # only active nodes have connections
        # for each column, from output layer to input layer
        start = len(self.columns)-1
        for i in range(start, 0, -1):
            previous_cols = self.get_possible_previous_nodes(i)
            
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
    def _add_node(self, value = None, operation = None, col_num = 1):
        if operation == None and value == None:
            operation = Graph.rng.choice(Graph.operations)
        new_node = Node(col_num, operation, value)
        self.nodes[new_node.id] = new_node
        return new_node.id

    def reset_graph_value(self):
        for n_id in self.nodes:
            if self.nodes[n_id].col_num != 0:
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

    # percentage in [0, 1]
    def probabilistic_mutation(self, percentage, only_active = False):
        possible_nodes = [n_id for n_id in self.nodes if not only_active or self.nodes[n_id].active]
        for n_id in possible_nodes:
            if percentage <= Graph.rng.rand():
                self.mutate_node_gene(n_id)

    def point_mutation(self, n_nodes, only_active = False):
        possible_nodes = [n_id for n_id in self.nodes if not only_active or self.nodes[n_id].active]
        nodes_to_mutate = Graph.rng.choice(possible_nodes, n_nodes)
        for n_id in nodes_to_mutate:
            self.mutate_node_gene(n_id)

    def mutate_node_gene(self, node_id):
        node = self.nodes[node_id]
        n_genes = len(node.inputs) + 1 # n connections genes plus the operation gene
        mutation = Graph.rng.randint(0, n_genes)

        if mutation < len(node.inputs): # mutates the connection
            previous_cols = self.get_possible_previous_nodes(node.col_num)
            node.inputs[mutation] = Graph.rng.choice(previous_cols)
        else: # mutates the operation
            self.mutate_operation(node_id)

    def mutate_operation(self, node_id):
        node = self.nodes[node_id]
        possible_ops = [op for op in Graph.operations if op != node.operation]
        new_op = Graph.rng.choice(possible_ops)

        # in this case we should add connections
        if new_op.arity > node.operation.arity: 
            inputs_to_add = new_op.arity - node.operation.arity
            previous_cols = self.get_possible_previous_nodes(node.col_num)
            inodes_idlist = Graph.rng.choice(previous_cols, inputs_to_add)                    
            node.add_inputs(inodes_idlist)
        # in this case we should remove connections    
        elif new_op.arity < node.operation.arity:
            inputs_to_remove = node.operation.arity - new_op.arity
            inodes_idlist = Graph.rng.choice(node.inputs, inputs_to_remove) 
            node.remove_inputs(inodes_idlist)
            
        node.operation = new_op
    
    def clone_graph(self):
        clone = Graph(self.n_in, self.n_out, self.n_row, self.n_col, self.levels_back, initialize=False)
        for n_id, n in self.nodes.items():
            new_node = Node(n.col_num, n.operation,  n.value, n.active, n_id)
            new_node.add_inputs(n.inputs)
            clone.nodes[n_id] = new_node
        for col in self.columns:
            clone.columns.append([val for val in col])
        
        return clone
