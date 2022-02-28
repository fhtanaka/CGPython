from collections import namedtuple
import itertools
import numpy as np
from .graph import Graph
from .node import Node
from .operation import Operation 
from typing import Dict, List
from sklearn.utils import shuffle
from .specie import Specie

def order_by_fitness(fitness_modifier):
    def func(x: Graph):
        return (x.fitness * fitness_modifier, x.id)
    return func

class Population:

    rng = np.random
    species_id_count = itertools.count().__next__

    operations: List[Operation] = []
    @staticmethod
    def add_operation(arity, func, string):
        op = Operation(arity, func, string)
        Population.operations.append(op)

    def __init__(
        self, 
        population_size: int,
        n_in: int, 
        n_out: int,
        n_middle: int,
        ):
        
        self.population_size = population_size

        self.n_in = n_in
        self.n_out = n_out
        self.n_middle = n_middle
        self.total_genes = n_in + n_out + n_middle

        self.indvs: List[Graph] = self.create_individuals()
        self.species_dict: Dict[str, Specie] = {}

    def create_individuals(self):
        indvs: List[Graph] = []
        for _ in range(self.population_size): 
            g = Graph(self.n_in, self.n_out, self.n_middle, self.operations)
            indvs.append(g)
        return indvs
    
    def get_best_indvs(self, n):
        def f(x): return (x.fitness * self.minimize_fitness, x.id)
        self.indvs.sort(key=f)
        return self.indvs[-1*n:]

    def get_operation(self, op_value):
        if op_value == None:
            return None
        op_index = int(op_value*len(self.operations))
        return self.operations[op_index]

    def traditional_crossover(self, parent1: Graph, parent2: Graph):
        r = parent1.rng.uniform() # TODO: change this to not depend on only one parent
        child1 = self.graph_crossover(parent1, parent2, r)
        child2 = self.graph_crossover(parent1, parent2, 1-r)

        return (child1, child2)

    def graph_crossover(self, parent1: Graph, parent2: Graph, r):
        child = Graph(self.n_in, self.n_out, self.n_middle, self.operations, initialize=False)

        for n_id in range(self.total_genes):
            n1 = parent1.nodes[n_id]
            n2 = parent2.nodes[n_id]
            child.nodes[n_id] = self.node_crossover(r, n_id, child.rng, n1, n2)

        return child

    def node_crossover(self, r, n_id, rng, n1: Node, n2: Node):
        inputs = []
        for g1, g2 in itertools.zip_longest(n1.inputs, n2.inputs):
            if g1 == None:
                inputs.append(g2)
            elif g2 == None:
                inputs.append(g1)
            else:
                inputs.append(((1 - r) * g1) + (r * g2))

        op_value = None
        if n1.operation != None and n2.operation != None:
            op_value = ((1 - r) * n1.operation) + (r * n2.operation)
            op = self.get_operation(op_value)

            if len(inputs) < op.arity: # Adding more inputs if necessary
                for _ in range(op.arity-len(inputs)):
                    inputs.append(rng.uniform())
            elif len(inputs) > op.arity: # removing inputs if necessary
                inputs = inputs[:op.arity]

        child_node = Node(n_id, op_value)
        child_node.add_inputs(inputs)

        return child_node

    def graph_species_delta(self, g1: Graph, g2: Graph, c1, c2, b1, b2, b3, normalize_delta = True):
        if g1.total_nodes != g2.total_nodes:
            raise AttributeError("Graphs should have the same number of nodes when calculating especies delta")
        delta = 0
        g1.active_graph()
        g2.active_graph()
        for n1, n2 in zip(g1.nodes, g2.nodes):
            n_diff = self.node_difference(n1, n2, c1, c2)
            n_active_diff = self.node_activation_difference(n1, n2, b1, b2, b3)
            delta += n_diff + n_active_diff
        
        delta = delta/g1.total_nodes
        if normalize_delta:
            delta = delta/(c1+c2)/max(b1, b2, b3)
        return delta
            
    def node_activation_difference(self, n1: Node, n2: Node, b1, b2, b3):
        if n1.active and n2.active:
            return b1
        if not n1.active and not n2.active:
            return b3
        return b2

    def node_difference(self, n1: Node, n2: Node, c1, c2):
        n_diff = 0

        for g1, g2 in itertools.zip_longest(n1.inputs, n2.inputs):
            if g1 == None:
                n_diff += max(abs(1-g2), abs(g2))
            elif g2 == None:
                n_diff += max(abs(1-g1), abs(g1))
            else:
                n_diff += abs(g1-g2)

        n_inputs = max(1, len(n1.inputs), len(n2.inputs)) # Put 1 to avoid division by 0
        n_diff = c2*n_diff/n_inputs

        if self.get_operation(n1.operation) != self.get_operation(n2.operation):
            n_diff += c1

        return n_diff

    def separate_species(self, c1, c2, b1, b2, b3, sp_threshold, age = 1):
        deltas = []
        for _, sp in self.species_dict.items():
            sp.remove_members()
        
        for indv in self.indvs:
            has_species = False
            if indv.species_id in self.species_dict:
                sp = self.species_dict[indv.species_id]
                delta = self.graph_species_delta(indv,  sp.representant, c1, c2, b1, b2, b3)
                if delta <= sp_threshold:
                    has_species = True
                    indv.species_id = sp.id
                    sp.add_member(indv)
                    
            if not has_species:
                for sp_id, sp in self.species_dict.items():
                    delta = self.graph_species_delta(indv, sp.representant, c1, c2, b1, b2, b3)
                    deltas.append(delta)
                    if delta <= sp_threshold:
                        has_species = True
                        indv.species_id = sp_id
                        sp.add_member(indv)
                        break

                if not has_species:
                    sp = Specie(indv, [indv])
                    indv.species_id = sp.id
                    self.species_dict[sp.id] = sp 

        new_species_dict = {}
        for _, sp in self.species_dict.items():
            if len(sp.members) > 0:
                sp.new_representant_random(self.rng)
                sp.age += age
                new_species_dict[sp.id] = sp

        self.species_dict = new_species_dict

        return deltas