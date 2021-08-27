from graph import Graph
from typing import List


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
        mutation_strategy,
        generations:int,
        minimize_fitness: bool = False,
        ):
        
        self.n_champions = n_champions
        self.mutation_strategy = mutation_strategy
        self.gens = generations
        self.population_size = population_size
        self.population: List[Graph] = []
        for _ in range(population_size):
            indv = Graph(n_in, n_out, n_row, n_col, levels_back)
            self.population.append(indv)
    
    def iterate_one_plus_lambda(self):
        self.population.sort(key=lambda x: (x.id, x.fitness))
        champions = self.population[-1*self.n_champions:]

        new_population: List[Graph] = []

        children_per_parent = int(self.population/len(champions) - 1)
        for parent in champions:
            new_population.append(parent)
            for _ in range(children_per_parent):
                indv = parent.clone_graph()
                indv.point_mutation(1, True) # TODO: adjust this to different types of mutation
                new_population.append(indv)
        
        self.population = new_population