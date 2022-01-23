from collections import namedtuple
from copy import deepcopy
from xmlrpc.client import Boolean
from graph import Graph
from population import Population
from typing import Callable, List

c1 = 1
c2 = 1
b1 = 2
b2 = 1
b3 = .5
species_threshold = 24
Specie = namedtuple('Specie', ['representant', 'members'])

def separate_species(pop: Population, species_arr: List[Specie]):

    for k, v in enumerate(species_arr):
        species_arr[k] = v._replace(members=[])

    for indv in pop.indvs:
        has_species = False
        for k, v in enumerate(species_arr):
            rep = v.representant
            delta = pop.graph_species_delta(indv, rep, c1, c2, b1, b2, b3)
            if delta <= species_threshold:
                has_species = True
                species_arr[k].members.append(indv)
                break
        if not has_species:
            sp = Specie(indv, [indv])
            species_arr.append(sp)

    new_species_arr = []
    for sp in species_arr:
        if len(sp.members) > 0:
            new_rep = pop.rng.choice(sp.members)
            sp = sp._replace(representant=new_rep.clone_graph())
            new_species_arr.append(sp)

    species_arr = new_species_arr

    return species_arr



def order_by_fitness(fitness_modifier):
    def func(x: Graph):
        return (x.fitness * fitness_modifier, x.id)
    return func

def tournament_selection_iteration(
    pop: Population, 
    minimize_fit: Boolean, 
    mutate_active_only: Boolean,
    mutation_rate: float,
    elitism: int,
    crossover_rate: float,
    tournament_size: int,
    ):

    mod = 1
    if minimize_fit:
        mod = -1

    # This order the indvs first by ID (lesser IDs first) and then by fitness
    # Since these sorts are stable, the indvs at the end of the array are the champions
    pop.indvs.sort(key=order_by_fitness(mod))

    champions = pop.indvs[-1*elitism:]
    if elitism == 0:
        champions=[]

    new_population: List[Graph] = []
    for parent in champions:
        # I think this reset is unnecessary but it is here just to make sure
        parent.reset_graph_value()
        new_population.append(parent)

    for _ in range(pop.population_size - elitism):
        tourney = pop.rng.choice(pop.indvs, tournament_size, replace=False).tolist()
        tourney.sort(key=order_by_fitness(mod))
        indv = None

        if pop.rng.rand() <= crossover_rate:
            indv, _ = pop.traditional_crossover(tourney[-1], tourney[-2])
        else:
            indv = tourney[-1].clone_graph()

        indv.probabilistic_mutation(mutation_rate, mutate_active_only)

        new_population.append(indv)
    pop.indvs = new_population

def one_plus_lambda_iteration(
    pop: Population,
    minimize_fit: Boolean,
    n_champions,
    mutate_active_only: Boolean,
    mutation_rate: float,
):
    mod = 1
    if minimize_fit:
        mod = -1

    # This order the indvs first by ID (lesser IDs first) and then by fitness
    # Since these sorts are stable, the indvs at the end of the array are the champions
    pop.indvs.sort(key=order_by_fitness(mod))
    champions = pop.indvs[-1*n_champions:]

    new_population: List[Graph] = []
    children_per_parent = int(pop.population_size/len(champions))

    for parent in champions:
        # I think this reset is unnecessary but it is here just to make sure
        parent.reset_graph_value()
        new_population.append(parent)

    for _ in range(children_per_parent):
        for parent in champions:
            parent.reset_graph_value()
            indv = parent.clone_graph()
            indv.probabilistic_mutation(mutation_rate, mutate_active_only)
            new_population.append(indv)

    pop.indvs = new_population

def run(
    pop: Population,
    selection_function,
    fitness_func,
    generations,
    goal_fit,
    minimize_fitness,
    stagnation,
    report
):
    species_arr: List[Specie] = []
    fit_mod = 1
    global_best_fitness = float('-inf')
    if minimize_fitness:
        fit_mod = -1
        global_best_fitness = float('inf')

    stagnation_count = 0
    for i in range(generations):            
        gen_best_fitness = float('-inf') * fit_mod
        for ind in pop.indvs:
            fitness = fitness_func(ind)
            ind.fitness = fitness
            if fit_mod * fitness > fit_mod * gen_best_fitness:
                gen_best_fitness = fitness

        if report and i % 10 == 0:
            species_arr = separate_species(pop, species_arr)
            print(f"Gen {i}\t Best fitness: {gen_best_fitness}\t Number of species: {len(species_arr)}")

        if fit_mod*gen_best_fitness > fit_mod*global_best_fitness:
            global_best_fitness = gen_best_fitness
            stagnation_count = 0
        
        if fit_mod*gen_best_fitness >= fit_mod*goal_fit:
            break

        if stagnation_count > stagnation:
            print(f"Generation {i}: Fitness stagnated, reseting population")
            stagnation_count = 0
            global_best_fitness = float('-inf') * fit_mod
            pop.indvs = pop.create_individuals()
        else: 
            # self.one_plus_lambda(n_champions, fit_mod)
            selection_function(pop)
            stagnation_count += 1

    print("\nFinished execution")
    print("Total generations: {}".format(i))
    print("Best Fitness: {}".format(global_best_fitness))

def one_plus_lambda(
    population: Population,

    generations: int,
    goal_fit: float,
    fitness_func: Callable[[Graph], float],
    minimize_fitness: bool = False,
    stagnation: int = 100,
    report=False,

    n_champions: int = 1,
    mutate_active_only: Boolean = False,
    mutation_rate: float = .1,
):
    f = lambda pop : one_plus_lambda_iteration(
        pop,
        minimize_fitness,
        n_champions,
        mutate_active_only,
        mutation_rate
    )
        
    run(
        population,
        f,
        fitness_func,
        generations,
        goal_fit,
        minimize_fitness,
        stagnation,
        report,
    )


def tournament_selection(
    population: Population,

    generations: int,
    goal_fit: float,
    fitness_func: Callable[[Graph], float],
    minimize_fitness: bool = False,
    stagnation: int = 100,
    report=False,

    mutate_active_only: bool = False,
    mutation_rate: float = 0.1,
    elitism: int = 1,
    crossover_rate: float = .5,
    tournament_size: int = 2,
):
    f = lambda pop: tournament_selection_iteration(
        pop,
        minimize_fitness,
        mutate_active_only,
        mutation_rate,
        elitism,
        crossover_rate,
        tournament_size
    )

    run(
        population,
        f,
        fitness_func,
        generations,
        goal_fit,
        minimize_fitness,
        stagnation,
        report,
    )
