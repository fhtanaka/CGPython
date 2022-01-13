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
        

        self.n_in = n_in
        self.n_out = n_out
        self.n_middle = n_middle
        self.total_nodes = n_in + n_out + n_middle

        self.nodes: List[Node] = [None for _ in range(self.total_nodes)]

        self.available_operations = available_operations
        self.fitness: int = 0
        
        if initialize:
            for n_id in range(self.total_nodes):
                op_float = Graph.rng.uniform()
                op_index = int(op_float*len(self.available_operations))
                op_arity = self.available_operations[op_index].arity

                active = False

                new_node = Node(n_id, op_float, active=active)

                if n_id >= n_in:
                    new_node.add_inputs([Graph.rng.uniform() for _ in range(op_arity)])
                
                self.nodes[new_node.id] = new_node

            self.active_graph()
            

    def set_inputs(self, input_values):
        if len(input_values) != self.n_in:
            msg = "Expected %d inputs but received %d values" % (self.n_in, len(input_values))
            raise RuntimeError(msg)
        for i in range(self.n_in):
            self.nodes[i].value = input_values[i]

    def reset_graph_value(self):
        for n_id in range(self.n_in, self.total_nodes): # reseting values for non-input nodes
            n = self.nodes[n_id]
            n.value = None
            n.active = False
        self.active_graph()
    
    def operate(self, input_values):
        self.set_inputs(input_values)
        results = [self.get_node_value(out) for out in range(self.n_in+self.n_middle, self.total_nodes)]
        self.reset_graph_value()
        return results

    def get_node_value(self, node_id):
        node = self.nodes[node_id]
        if node.value is not None:
            return node.value

        inputs = [self.get_node_value(int(x*node.id)) for x in node.inputs]
        
        op_index = int(node.operation*len(self.available_operations))
        operation = self.available_operations[op_index]
        
        if len(inputs) != operation.arity:
            print("sInput size does not match the arity of the operation")

        node.value = operation(*inputs)

        return node.value

    def nodes_eligible_for_mutation(self, only_active):
        return [n for n in self.nodes[self.n_in:] if not only_active or n.active]

    def probabilistic_mutation(self, percentage, only_active = False):
        possible_nodes = self.nodes_eligible_for_mutation(only_active)
        for n in possible_nodes:
            #mutating the connections
            for k, v in enumerate(n.inputs):
                n.inputs[k] = Graph.rng.uniform() if Graph.rng.rand() <= percentage else v
            # mutating the operation
            if Graph.rng.rand() <= percentage:
                self.mutate_operation(n)

    # def point_mutation(self, n_nodes, only_active = False):
    #     possible_nodes = self.nodes_eligible_for_mutation(only_active)
    #     nodes_to_mutate = Graph.rng.choice(possible_nodes, n_nodes, replace=False)
    #     for n_id in nodes_to_mutate:
    #         self.mutate_node_gene(n_id)

    def mutate_operation(self, node):

        op_index = int(node.operation*len(self.available_operations))
        old_op = self.available_operations[op_index]

        node.operation = Graph.rng.uniform()
        op_index = int(node.operation*len(self.available_operations))
        new_op = self.available_operations[op_index]

        # in this case we should add connections
        if new_op.arity > old_op.arity:
            new_inputs = [Graph.rng.uniform() for _ in range(new_op.arity - old_op.arity)]
            node.add_inputs(new_inputs)

        # in this case we should remove connections    
        elif new_op.arity < old_op.arity:
            qtd = old_op.arity - new_op.arity
            inputts_to_remove = Graph.rng.choice(node.inputs, qtd, replace=False)
            node.remove_inputs(inputts_to_remove)
            
    
    def clone_graph(self):
        clone = Graph(self.n_in, self.n_out, self.n_middle, self.available_operations, initialize=False)

        for n in self.nodes:
            new_node = Node(n.id, n.operation, n.value, n.active)
            new_node.add_inputs(n.inputs)
            clone.nodes[n.id] = new_node

        clone.reset_graph_value()
        return clone
    
    def active_graph(self):
        for n_id in range(self.n_in+self.n_middle, self.total_nodes):
            self.activate_node(n_id)

    def activate_node(self, node_id):
        n = self.nodes[node_id]
        n.active = True
        aux = [int(x*n.id) for x in n.inputs]
        for i in aux:
            self.activate_node(i)

    # this function is mostly for testing purposes
    def _add_node(self, n_id, value=None, operation=None):
        if operation == None and value == None:
            operation = Graph.rng.uniform()
        new_node = Node(n_id, operation, value)
        self.nodes[new_node.id] = new_node
        return new_node.id

    # def draw_graph(self, only_active=True):
    #     plt.rcParams["figure.figsize"] = (15, 20)
    #     graph = nx.Graph()
    #     pos = {}
    #     labels = {}
    #     color_dict = {
    #         0: "tab:purple",
    #         1: "tab:red",
    #         3: "tab:olive",
    #         2: "tab:orange",
    #         4: "tab:green",
    #         5: "tab:blue",
    #     }

    #     col_num = len(self.columns) - 1
    #     for col in reversed(self.columns):
    #         row = 0
    #         for n_id in col:
    #             node = self.nodes[n_id]
    #             if only_active and not node.active:
    #                 continue
    #             pos[node.id] = (col_num, row)

    #             if col_num == 0:
    #                 labels[node.id] = "In_" + str(row)
    #             elif col_num == len(self.columns)-1:
    #                 labels[node.id] = "Out_" + str(row)
    #             elif node.operation != None:
    #                 labels[node.id] = node.operation.string

    #             graph.add_node(node.id)
    #             for input in node.inputs:
    #                 graph.add_edge(
    #                     input, node.id, color=color_dict[col_num % len(color_dict)])

    #             row += 1
    #         col_num -= 1

    #     options = {
    #         "font_size": 12,
    #         "node_size": 1500,
    #         "node_color": "white",
    #         "edgecolors": "black",
    #         "edge_color": nx.get_edge_attributes(graph, 'color').values(),
    #         "linewidths": 2,
    #         "width": 2,
    #         "labels": labels,
    #         "pos": pos
    #     }
    #     nx.draw_networkx(graph, **options)

    #     # Set margins for the axes so that nodes aren't clipped
    #     ax = plt.gca()
    #     ax.margins(0.20)
    #     plt.axis("off")
    #     plt.show()
