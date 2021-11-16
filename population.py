from graph import Graph
from operation import Operation 
from typing import Callable, List


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
        n_row: int, 
        n_col: int, 
        levels_back: int,
        mutation_strategy: str,
        fitness_func: Callable[[Graph], float],
        minimize_fitness: bool = False,
        point_mut_qnt: int = 1,
        prob_mut_chance: float = 0.2,
        mutate_active_only: bool = True,
        ):
        
        # self.n_champions = n_champions
        # self.gens = generations
        self.population_size = population_size
        self.fitness_func = fitness_func
        self.minimize_fitness = minimize_fitness

        if mutation_strategy != "point" and  mutation_strategy != "prob":
            raise NameError("Mutation strategy should be \"point\" or \"prob\" ")
        self.mutation_strategy = mutation_strategy
        self.point_mut_qnt = point_mut_qnt             
        self.prob_mut_chance = prob_mut_chance
        self.mutate_active = mutate_active_only

        self.indvs: List[Graph] = []
        for _ in range(population_size): 
            indv = Graph(n_in, n_out, n_row, n_col, levels_back, self.operations)
            self.indvs.append(indv)
    
    def iterate_one_plus_lambda(self, n_champions, fitness_modifier):
        # This order the indvs first by ID (lesser IDs first) and then by fitness
        # Since these sorts are stable, the indvs at the end of the array are the champions
        self.indvs.sort(key=lambda x: (x.fitness * fitness_modifier, x.id))
        champions = self.indvs[-1*n_champions:]

        new_population: List[Graph] = []
        children_per_parent = int(self.population_size/len(champions))
        for parent in champions:
            parent.reset_graph_value() # I think this reset is unnecessary but it is here just to make sure
            new_population.append(parent)
            for _ in range(children_per_parent):
                indv = parent.clone_graph()
                if self.mutation_strategy == "point":
                    indv.point_mutation(self.point_mut_qnt, self.mutate_active)
                elif self.mutation_strategy == "prob":
                    indv.probabilistic_mutation(self.prob_mut_chance, self.mutate_active)
                new_population.append(indv)
        
        self.indvs = new_population

    def one_plus_lamda(self, generations: int, n_champions: int, goal_fit: float, report=False):

        fitness_modifier = 1
        compare_fit = float('-inf')
        if self.minimize_fitness:
            compare_fit = float('inf')
            fitness_modifier = -1

        fit_achieved = False
        for i in range(generations):
            if report:
                print("generation ", i)
            best_fitness = compare_fit
            for ind in self.indvs:
                fitness = self.fitness_func(ind)
                ind.fitness = fitness
                if report:
                    print(ind.id, " fit: ", fitness)
                if self.minimize_fitness:
                    if fitness < best_fitness:
                        best_fitness = fitness
                        if fitness <= goal_fit:
                            fit_achieved = True
                else:
                    if fitness > best_fitness:
                        best_fitness = fitness
                        if fitness >= goal_fit:
                            fit_achieved = True
            if report:
                print("Best fitness of gen: ", best_fitness)
            if fit_achieved:
                break
            self.iterate_one_plus_lambda(n_champions, fitness_modifier)

        print("Finished execution")
        print("Total generations: {}".format(i))
        print("Best Fitness: {}".format(best_fitness))
    

    def get_best_indvs(self, n):
        self.indvs.sort(key=lambda x: (x.fitness * self.minimize_fitness, x.id))
        return self.indvs[-1*n:]
