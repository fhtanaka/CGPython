from .graph import Graph
from .population import Population
from typing import Callable, List

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
        c.reset_graph_value(reset_fit=False)
        new_population.append(c)

    for _ in range(pop.population_size - elitism):
        tourney = pop.rng.choice(
            pop.indvs, tournament_size, replace=False).tolist()
        tourney.sort(key=lambda x: (x.fitness * mod, x.id))
        indv = None

        if pop.rng.random() <= crossover_rate:
            indv, _ = pop.traditional_crossover(tourney[-1], tourney[-2])
        else:
            indv = tourney[-1].clone_graph(pop.rng)

        indv.probabilistic_mutation(
            mutation_rate, mutate_active_only, rng=pop.rng)

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
            indv.probabilistic_mutation(
                mutation_rate, mutate_active_only, pop.rng)
            new_population.append(indv)

    pop.indvs = new_population
