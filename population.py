import itertools
from graph import Graph
from node import Node
from operation import Operation 
from typing import Callable, List


def order_by_fitness(fitness_modifier):
    def func(x: Graph):
        return (x.fitness * fitness_modifier, x.id)
    return func

class Population:

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
        fitness_func: Callable[[Graph], float],
        minimize_fitness: bool = False,
        mutate_active_only: bool = False,
        mutation_strategy: str = "prob",
        prob_mut_chance: float = 0.1,
        ):
        
        # self.n_champions = n_champions
        # self.gens = generations

        self.population_size = population_size
        self.fitness_func = fitness_func
        self.minimize_fitness = minimize_fitness

        if mutation_strategy != "prob":
            raise NameError("Mutation strategy should be \"prob\" ")
        self.mutation_strategy = mutation_strategy
        self.prob_mut_chance = prob_mut_chance
        self.mutate_active = mutate_active_only

        self.n_in = n_in
        self.n_out = n_out
        self.n_middle = n_middle
        self.total_genes = n_in + n_out + n_middle

        self.indvs: List[Graph] = []
        for _ in range(population_size): 
            indv = Graph(n_in, n_out, n_middle, self.operations)
            self.indvs.append(indv)
    
    def iterate_one_plus_lambda(self, n_champions, fitness_modifier):
        # This order the indvs first by ID (lesser IDs first) and then by fitness
        # Since these sorts are stable, the indvs at the end of the array are the champions
        self.indvs.sort(key=order_by_fitness(fitness_modifier))
        champions = self.indvs[-1*n_champions:]

        new_population: List[Graph] = []
        children_per_parent = int(self.population_size/len(champions))

        for parent in champions:
            # I think this reset is unnecessary but it is here just to make sure
            parent.reset_graph_value()
            new_population.append(parent)

        for _ in range(children_per_parent):
            for parent in champions:
                parent.reset_graph_value()
                indv = parent.clone_graph()
                if self.mutation_strategy == "prob":
                    indv.probabilistic_mutation(self.prob_mut_chance, self.mutate_active)
                new_population.append(indv)

        self.indvs = new_population

    def one_plus_lamda(self, generations: int, n_champions: int, goal_fit: float, report=False):

        fit_mod = 1
        compare_fit = float('-inf')
        if self.minimize_fitness:
            compare_fit = float('inf')
            fit_mod = -1

        for i in range(generations):            
            best_fitness = compare_fit
            for ind in self.indvs:
                fitness = self.fitness_func(ind)
                ind.fitness = fitness
                if fit_mod * fitness > fit_mod * best_fitness:
                    best_fitness = fitness

            if report and i%100 == 0:
                print(f"Best fitness of gen {i}: {best_fitness}")
            
            if fit_mod*fitness >= fit_mod*goal_fit:
                break
            
            self.iterate_one_plus_lambda(n_champions, fit_mod)

        print("Finished execution")
        print("Total generations: {}".format(i))
        print("Best Fitness: {}".format(best_fitness))
    
    def get_best_indvs(self, n):
        self.indvs.sort(key=lambda x: (x.fitness * self.minimize_fitness, x.id))
        return self.indvs[-1*n:]

    def get_operation(self, op_value):
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

    def graph_species_delta(self, g1: Graph, g2: Graph):
        if g1.total_nodes != g2.total_nodes:
            raise AttributeError("Graphs should have the same number of nodes when calculating especies delta")
        delta = 0
        g1.active_graph()
        g2.active_graph()
        for n1, n2 in zip(g1.nodes, g2.nodes):
            n_diff = self.node_difference(n1, n2)
            n_active_diff = self.node_activation_difference(n1, n2)
            delta += n_diff + n_active_diff
        
        return delta
            
    def node_activation_difference(self, n1: Node, n2: Node):
        if n1.active and n2.active:
            return self.b1
        if not n1.active and not n2.active:
            return self.b3
        return self.b2

    def node_difference(self, n1: Node, n2: Node):
        n_diff = 0


        for g1, g2 in itertools.zip_longest(n1.inputs, n2.inputs):
            if g1 == None:
                n_diff += max(abs(1-g2), abs(g2))
            elif g2 == None:
                n_diff += max(abs(1-g1), abs(g1))
            else:
                n_diff += abs(g1-g2)        
        n_diff *= self.c2

        if self.get_operation(n1.operation) != self.get_operation(n2.operation):
            n_diff += self.c1 ##############

        return n_diff