from typing import Dict, List
from node import Node
from operation import Operation
import numpy as np
import itertools
import networkx as nx
import matplotlib.pyplot as plt


def cte_op(x):
    return x


cte = Operation(arity=1, operation=cte_op, string="x")

class Graph:
    rng = np.random
    id_counter = itertools.count().__next__

    def __init__(self, n_in: int, n_out: int, n_middle: int, available_operations: List[Operation] =[cte], initialize: bool = True):
        self.id = self.id_counter()
        
        self.nodes: Dict[int, Node] = {}
        self.columns: List[List[int]] = []
        self.possible_connections_per_col: List[List[int]] = []

        self.n_in = n_in
        self.n_out = n_out
        self.n_middle = n_middle

        self.total_nodes = n_in + n_out + n_middle
        self.available_operations = available_operations
        self.fitness: int = 0
        
        if initialize:
            for n_id in range(self.total_nodes):
                op_float = Graph.rng.uniform()
                op_index = int(op_float*len(self.available_operations))
                op_arity = self.available_operations[op_index].arity

                active = False
                if n_id >= n_in+ n_out: # Checking if it is output
                    active = True 

                new_node = Node(n_id, op_float, active=active)
                new_node.add_inputs([Graph.rng.uniform() for _ in range(op_arity)])
                
                self.nodes[new_node.id] = new_node
            

    def set_inputs(self, input_values):
        if len(input_values) != self.n_in:
            msg = "Expected %d inputs but received %d values" % (self.n_in, len(input_values))
            raise RuntimeError(msg)
        for i in range(self.n_in):
            self.nodes[i].value = input_values[i]

    # this function is mostly for testing purposes
    def _add_node(self, n_id, value = None, operation = None, col_num = 1):
        if operation == None and value == None:
            operation = Graph.rng.uniform()
        new_node = Node(n_id, operation, value)
        self.nodes[new_node.id] = new_node
        return new_node.id

    def reset_graph_value(self):
        for n_id in self.nodes:
            n = self.nodes[n_id]
            if n.col_num != 0:
                n.value = None
                n.active = False
        for n_id in self.columns[-1]:
            self.activate_node(n_id)
    
    def operate(self, input_values):
        self.set_inputs(input_values)
        results = [self.get_node_value(out) for out in self.columns[-1]]
        self.reset_graph_value()
        return results

    def get_node_value(self, node_id):
        node = self.nodes[node_id]
        if node.value is not None:
            return node.value

        inputs = [self.get_node_value(int(x*node.id)) for x in node.inputs]
        if len(inputs) != node.operation.arity:
            print("something went wrong")

        op_index = int(node.operation*len(self.available_operations))
        operation = self.available_operations[op_index]
        node.value = operation(*inputs)

        return node.value

    # # TODO: check if its bottleneck, if it is, change to one liner 
    # def nodes_eligible_for_mutation(self, only_active):
    #     nodes = []
    #     for n_id in self.nodes:
    #         if self.nodes[n_id].col_num != 0 and (not only_active or self.nodes[n_id].active):
    #             nodes.append(n_id)
    #     return nodes

    # # percentage in [0, 1]
    # def probabilistic_mutation(self, percentage, only_active = False):
    #     possible_nodes = self.nodes_eligible_for_mutation(only_active)
    #     for n_id in possible_nodes:
    #         if Graph.rng.rand() <= percentage:
    #             self.mutate_node_gene(n_id)

    # def point_mutation(self, n_nodes, only_active = False):
    #     possible_nodes = self.nodes_eligible_for_mutation(only_active)
    #     nodes_to_mutate = Graph.rng.choice(possible_nodes, n_nodes, replace=False)
    #     for n_id in nodes_to_mutate:
    #         self.mutate_node_gene(n_id)

    # def mutate_node_gene(self, node_id):
    #     node = self.nodes[node_id]
    #     n_genes = len(node.inputs) + 1 # n connections genes plus the operation gene
    #     mutation = Graph.rng.randint(0, n_genes)

    #     if mutation < len(node.inputs): # mutates the connection
    #         previous_cols = self.possible_connections_per_col[node.col_num]
    #         node.inputs[mutation] = Graph.rng.choice(previous_cols)
    #     else: # mutates the operation
    #         self.mutate_operation(node_id)

    # def mutate_operation(self, node_id):
    #     node = self.nodes[node_id]
    #     possible_ops = [op for op in self.available_operations if op != node.operation]
    #     new_op = Graph.rng.choice(possible_ops)

    #     # in this case we should add connections
    #     if new_op.arity > node.operation.arity: 
    #         inputs_to_add = new_op.arity - node.operation.arity
    #         previous_cols = self.possible_connections_per_col[node.col_num]
    #         inodes_idlist = Graph.rng.choice(previous_cols, inputs_to_add, replace=False)                    
    #         node.add_inputs(inodes_idlist)
    #     # in this case we should remove connections    
    #     elif new_op.arity < node.operation.arity:
    #         inputs_to_remove = node.operation.arity - new_op.arity
    #         inodes_idlist = Graph.rng.choice(node.inputs, inputs_to_remove, replace=False)
    #         node.remove_inputs(inodes_idlist)
            
    #     node.operation = new_op
    
    def clone_graph(self):
        clone = Graph(self.n_in, self.n_out, self.n_middle, self.available_operations, initialize=False)

        for n_id, n in self.nodes.items():
            new_node = Node(n.id, n.operation, n.value, n.active)
            new_node.add_inputs(n.inputs)
            clone.nodes[n_id] = new_node

        clone.reset_graph_value()
        return clone
    
    def activate_node(self, node_id):
        n = self.nodes[node_id]
        n.active = True
        for i in n.inputs:
            self.activate_node(i)

    def draw_graph(self, only_active=True):
        plt.rcParams["figure.figsize"] = (15, 20)
        graph = nx.Graph()
        pos = {}
        labels = {}
        color_dict = {
            0: "tab:purple",
            1: "tab:red",
            3: "tab:olive",
            2: "tab:orange",
            4: "tab:green",
            5: "tab:blue",
        }


        col_num = len(self.columns) - 1
        for col in reversed(self.columns):
            row = 0
            for n_id in col:
                node = self.nodes[n_id]
                if only_active and not node.active:
                    continue
                pos[node.id] = (col_num, row)

                if col_num == 0:
                    labels[node.id] = "In_" + str(row)
                elif col_num == len(self.columns)-1:
                    labels[node.id] = "Out_" + str(row)
                elif node.operation != None:
                    labels[node.id] = node.operation.string

                graph.add_node(node.id)    
                for input in node.inputs:
                    graph.add_edge(input, node.id, color=color_dict[col_num%len(color_dict)])
        
                row += 1
            col_num -= 1
        
        options = {
            "font_size": 12,
            "node_size": 1500,
            "node_color": "white",
            "edgecolors": "black",
            "edge_color": nx.get_edge_attributes(graph,'color').values(),
            "linewidths": 2,
            "width": 2,
            "labels": labels,
            "pos": pos
        }
        nx.draw_networkx(graph, **options)

        # Set margins for the axes so that nodes aren't clipped
        ax = plt.gca()
        ax.margins(0.20)
        plt.axis("off")
        plt.show()