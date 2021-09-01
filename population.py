from graph import Graph
from typing import List, Optional


class Population:
    def __init__(
        self, 
        population_size: int,
        n_in: int, 
        n_out: int, 
        n_row: int, 
        n_col: int, 
        levels_back: int,
        n_champions: int,
        mutation_strategy: str,
        generations:int,
        minimize_fitness: bool = False,
        point_mut_qnt: int = 1,
        prob_mut_chance: float = 0.2,
        mutate_active_only: bool = True,
        ):
        
        self.n_champions = n_champions
        self.mutation_strategy = mutation_strategy
        self.gens = generations
        self.population_size = population_size

        self.minimize_fitness = 1
        if minimize_fitness:
            self.minimize_fitness = -1
        if mutation_strategy != "point" and  mutation_strategy != "prob":
            raise NameError("Mutation strategy should be \"point\" or \"prob\" ")
        self.mutation_strategy = mutation_strategy
        self.point_mut_qnt = point_mut_qnt             
        self.prob_mut_chance = prob_mut_chance
        self.mutate_active = mutate_active_only

        self.indvs: List[Graph] = []
        for _ in range(population_size + n_champions): 
            indv = Graph(n_in, n_out, n_row, n_col, levels_back)
            self.indvs.append(indv)
    
    def iterate_one_plus_lambda(self):
        # This order the indvs first by ID (lesser IDs first) and then by fitness
        # Since these sorts are stable, the indvs at the end of the array are the champions
        self.indvs.sort(key=lambda x: (x.fitness * self.minimize_fitness, x.id))
        champions = self.indvs[-1*self.n_champions:]

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
    
    def get_best_indvs(self, n):
        self.indvs.sort(key=lambda x: (x.fitness * self.minimize_fitness, x.id))
        return self.indvs[-1*n:]
