import numpy as np
from graph import Graph
from population import Population
from typing import Callable, List
from operator import attrgetter

c1 = 1
c2 = 1
b1 = 1
b2 = .75
b3 = .5

alfa = 1
beta = 2

def explicit_fit_sharing(pop: Population, minimize_fitness: bool, species_threshold:float):
    pop.separate_species(c1, c2, b1, b2, b3, species_threshold)
    for sp in pop.species_arr:
        for indv in sp.members:
            if minimize_fitness:
                indv.fitness = (indv.fitness**alfa) * (len(sp.members)**beta)
            else:
                indv.fitness = (indv.fitness**alfa) / (len(sp.members)**beta)

def update_pop_fitness(pop, fitness_func, fit_share, minimize_fitness, species_threshold):
    for ind in pop.indvs:
        ind.fitness = fitness_func(ind)
        ind.original_fit = ind.fitness
    if fit_share:
        explicit_fit_sharing(pop, minimize_fitness, species_threshold)


def print_report(gen, champion, pop, species_threshold):
    # deltas = pop.separate_species(c1, c2, b1, b2, b3, species_threshold)
    print(f"best_in_gen: {gen};\t original_fit: {champion.original_fit:.2f};\t shared_fit: {champion.fitness:.2f};\t specie: {champion.species_id};")
    
    pop.species_arr.sort(key=lambda x: x.representant.species_id)
    print(f"Species ({len(pop.species_arr)}): [", end="")
    for sp in pop.species_arr:
        print(f"{sp.representant.species_id}({len(sp.members)})", end=", ")
    print("]\n")
    
    # print(f"Deltas ;\t min: {min(deltas)};\t max: {max(deltas)}\t avg: {np.average(deltas)} \n")
    # pp.update([[len(pop.species_arr)]])

def run(
    pop: Population,
    selection_function,
    fitness_func,
    generations,
    goal_fit,
    minimize_fitness,
    fit_share,
    stagnation,
    stag_preservation,
    report,
    species_threshold
):
    fit_mod = 1
    last_gen_fitness = float('-inf')
    if minimize_fitness:
        fit_mod = -1
        last_gen_fitness = float('inf')

    stagnation_count = 0
    stag_preservation *= -1

    for i in range(generations+1):
        update_pop_fitness(pop, fitness_func, fit_share, minimize_fitness, species_threshold)

        if minimize_fitness:
            champion = min(pop.indvs, key=attrgetter('original_fit'))
        else:
            champion = max(pop.indvs, key=attrgetter('original_fit'))
        gen_best_fitness = champion.original_fit

        if fit_mod*gen_best_fitness > fit_mod*last_gen_fitness:
            stagnation_count = 0
        else:
            stagnation_count += 1
        last_gen_fitness = gen_best_fitness

        if fit_mod*gen_best_fitness >= fit_mod*goal_fit or i == generations-1:
            break

        if report is not None and i % report == 0:
            print_report(i, champion, pop, species_threshold)

        if stagnation_count > stagnation:
            print(f"Generation {i}: Fitness stagnated, reseting population")
            stagnation_count = 0
            pop.indvs.sort(key=lambda x: (x.original_fit * fit_mod, x.id))
            pop.indvs[:stag_preservation] = pop.create_individuals()[:stag_preservation]
            update_pop_fitness(pop, fitness_func, False, minimize_fitness, species_threshold)
        
        selection_function(pop)

    pop.indvs.sort(key=lambda x: (x.fitness * fit_mod, x.id))
    print("\nFinished execution")
    print("Total generations: {}".format(i))
    print("Best Shared Fitness: {}".format(pop.indvs[-1].fitness))
    print("Best Original Fitness: {}".format(pop.indvs[-1].original_fit))

def tournament_selection_iteration(
    pop: Population, 
    minimize_fit: bool, 
    mutate_active_only: bool,
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
    pop.indvs.sort(key=lambda x: (x.original_fit * mod, x.id))

    champions = pop.indvs[-1*elitism:]
    if elitism == 0:
        champions = []

    new_population: List[Graph] = []
    for c in champions:
        # I think this reset is unnecessary but it is here just to make sure
        c.reset_graph_value()
        new_population.append(c)

    for _ in range(pop.population_size - elitism):
        tourney = pop.rng.choice(pop.indvs, tournament_size, replace=False).tolist()
        tourney.sort(key=lambda x: (x.fitness * mod, x.id))
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
    minimize_fit: bool,
    n_champions,
    mutate_active_only: bool,
    mutation_rate: float,
):
    mod = 1
    if minimize_fit:
        mod = -1

    # This order the indvs first by ID (lesser IDs first) and then by fitness
    # Since these sorts are stable, the indvs at the end of the array are the champions
    pop.indvs.sort(key=lambda x: (x.fitness * mod, x.id))
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

def one_plus_lambda(
    population: Population,

    generations: int,
    goal_fit: float,
    fitness_func: Callable[[Graph], float],
    minimize_fitness: bool = False,
    fit_share = True,
    stagnation: int = 100,
    stag_preservation: int = 2,
    report=False,

    n_champions: int = 1,
    mutate_active_only: bool = False,
    mutation_rate: float = .1,

    species_threshold:float = .8,
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
        fit_share,
        stagnation,
        stag_preservation,
        report,
        species_threshold,
    )


def tournament_selection(
    population: Population,

    generations: int,
    goal_fit: float,
    fitness_func: Callable[[Graph], float],
    minimize_fitness: bool = False,
    fit_share = True,
    stagnation: int = 100,
    stag_preservation: int = 2,
    report=None,

    mutate_active_only: bool = False,
    mutation_rate: float = 0.1,
    elitism: int = 1,
    crossover_rate: float = .5,
    tournament_size: int = 2,

    species_threshold: float = .8
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
        fit_share,
        stagnation,
        stag_preservation,
        report,
        species_threshold,
    )
