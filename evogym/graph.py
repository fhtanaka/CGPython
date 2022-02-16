from typing import Dict, List
from node import Node
from operation import Operation
import numpy as np
import itertools


def cte_op(x):
    return x

cte = Operation(arity=1, operation=cte_op, string="x")

class Graph:
    id_counter = itertools.count().__next__

    def __init__(self, n_in: int, n_out: int, n_middle: int, available_operations: List[Operation] =[cte], initialize: bool = True, rng = np.random):
        self.id: int = self.id_counter()
        self.species_id: int = -1

        self.n_in = n_in
        self.n_out = n_out
        self.n_middle = n_middle
        self.total_nodes = n_in + n_out + n_middle

        self.nodes: List[Node] = [None for _ in range(self.total_nodes)]

        self.available_operations = available_operations
        self.fitness: float = 0
        self.original_fit: float = 0
        self.rng = rng
        
        if initialize:
            for n_id in range(self.total_nodes):
                op_value = None
                if n_in <= n_id < n_in + n_middle: # if it is a middle node
                    op_value = self.rng.uniform()

                new_node = Node(n_id, op_value, active=False)

                if n_in + n_middle <= n_id: # if it is an output node add a single input
                    new_node.add_inputs([self.rng.uniform()])
                elif n_in <= n_id:
                    op = self.decode_operation(op_value)
                    new_node.add_inputs([self.rng.uniform() for _ in range(op.arity)])
                
                self.nodes[new_node.id] = new_node

            self.active_graph()
            
    def decode_operation(self, op_value):
        op_index = int(op_value*len(self.available_operations))
        return self.available_operations[op_index]

    def set_inputs(self, input_values):
        if len(input_values) != self.n_in:
            msg = "Expected %d inputs but received %d values" % (self.n_in, len(input_values))
            raise RuntimeError(msg)
        for i in range(self.n_in):
            self.nodes[i].value = input_values[i]

    def reset_graph_value(self, reset_fit=True):
        if reset_fit:
            self.fitness = 0
            self.original_fit = 0
        for n_id in range(self.n_in, self.total_nodes): # reseting values for non-input nodes
            n = self.nodes[n_id]
            n.value = None
            n.active = False
        self.active_graph()
    
    def operate(self, input_values, reset_fit=True):
        self.set_inputs(input_values)
        results = [self.get_node_value(out) for out in range(self.n_in+self.n_middle, self.total_nodes)]
        self.reset_graph_value(reset_fit)
        return results

    def get_node_value(self, node_id):
        node = self.nodes[node_id]
        if node.value is not None:
            return node.value

        inputs = [self.get_node_value(x) for x in node.decode_inputs()]
        
        if node.operation == None:
            return inputs[0]  

        operation = self.decode_operation(node.operation)
        
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
                n.inputs[k] = self.rng.uniform() if self.rng.rand() <= percentage else v
            # mutating the operation
            if self.rng.rand() <= percentage:
                self.mutate_operation(n)

    # def point_mutation(self, n_nodes, only_active = False):
    #     possible_nodes = self.nodes_eligible_for_mutation(only_active)
    #     nodes_to_mutate = self.rng.choice(possible_nodes, n_nodes, replace=False)
    #     for n_id in nodes_to_mutate:
    #         self.mutate_node_gene(n_id)

    def mutate_operation(self, node):
        if node.operation is None:
            return

        old_op = self.decode_operation(node.operation)

        node.operation = self.rng.uniform()
        new_op = self.decode_operation(node.operation)

        # in this case we should add connections
        if new_op.arity > old_op.arity:
            new_inputs = [self.rng.uniform() for _ in range(new_op.arity - old_op.arity)]
            node.add_inputs(new_inputs)

        # in this case we should remove connections    
        elif new_op.arity < old_op.arity:
            qtd = old_op.arity - new_op.arity
            inputts_to_remove = self.rng.choice(node.inputs, qtd, replace=False)
            node.remove_inputs(inputts_to_remove)
            
    
    def clone_graph(self):
        clone = Graph(self.n_in, self.n_out, self.n_middle, self.available_operations, initialize=False, rng=self.rng)
        clone.species_id = self.species_id
        clone.fitness = self.fitness
        clone.original_fit = self.original_fit
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
        for i in n.decode_inputs():
            self.activate_node(i)

    # this function is mostly for testing purposes
    def _add_node(self, n_id, value=None, operation=None):
        if operation == None and value == None:
            operation = self.rng.uniform()
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