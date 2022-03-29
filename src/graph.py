from typing import Dict, List
from .node import Node
from .operation import Operation
import numpy as np
import itertools


def cte_op(x):
    return x

cte = Operation(arity=1, operation=cte_op, string="x")

class Graph:
    id_counter = itertools.count().__next__

    def __init__(self, n_in: int, n_out: int, n_middle: int, available_operations: List[Operation] =[cte], initialize: bool = True, rng = np.random.default_rng()):
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
        
        if initialize:
            for n_id in range(self.total_nodes):
                op_value = None
                if n_in <= n_id < n_in + n_middle: # if it is a middle node
                    op_value = rng.uniform()

                new_node = Node(n_id, op_value, active=False)

                if n_in + n_middle <= n_id: # if it is an output node add a single input
                    new_node.add_inputs([rng.uniform()])
                elif n_in <= n_id:
                    op = self.decode_operation(op_value)
                    new_node.add_inputs([rng.uniform() for _ in range(op.arity)])
                
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
            print("Input size does not match the arity of the operation")

        node.value = operation(*inputs)

        return node.value

    def nodes_eligible_for_mutation(self, only_active):
        return [n for n in self.nodes[self.n_in:] if not only_active or n.active]

    def probabilistic_mutation(self, percentage, only_active=False, rng=None):
        possible_nodes = self.nodes_eligible_for_mutation(only_active)
        for n in possible_nodes:
            #mutating the connections
            for k, v in enumerate(n.inputs):
                n.inputs[k] = v
                if rng.random() < percentage:
                    n.inputs[k] = rng.uniform()
            # mutating the operation
            if rng.random() < percentage:
                self.mutate_operation(n, rng)

    def mutate_operation(self, node, rng=np.random.default_rng()):
        if node.operation is None:
            return

        old_op = self.decode_operation(node.operation)

        node.operation = rng.uniform()
        new_op = self.decode_operation(node.operation)

        # in this case we should add connections
        if new_op.arity > old_op.arity:
            new_inputs = [rng.uniform() for _ in range(new_op.arity - old_op.arity)]
            node.add_inputs(new_inputs)

        # in this case we should remove connections    
        elif new_op.arity < old_op.arity:
            qtd = old_op.arity - new_op.arity
            inputts_to_remove = rng.choice(node.inputs, qtd, replace=False)
            node.remove_inputs(inputts_to_remove)
            
    
    def clone_graph(self, rng = np.random.default_rng()):
        clone = Graph(self.n_in, self.n_out, self.n_middle, self.available_operations, initialize=False, rng=rng)
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
    def _add_node(self, n_id, value=None, operation=None, rng=np.random.default_rng()):
        if operation == None and value == None:
            operation = rng.uniform()
        new_node = Node(n_id, operation, value)
        self.nodes[new_node.id] = new_node
        return new_node.id

    def crossover(self, second_parent, ratio: float, rng=np.random.default_rng()):
        child = Graph(self.n_in, self.n_out, self.n_middle, self.available_operations, initialize=False)

        for n_id in range(self.total_nodes):
            n1 = self.nodes[n_id]
            n2 = second_parent.nodes[n_id]
            child.nodes[n_id] = n1.crossover(ratio, n_id, n2, self.available_operations, rng)

        return child