from xmlrpc.client import Boolean
from graph import Graph
from population import Population
from typing import Callable, List

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

    new_population: List[Graph] = []
    for parent in champions:
        # I think this reset is unnecessary but it is here just to make sure
        parent.reset_graph_value()
        new_population.append(parent)

    for _ in range(pop.population_size - elitism):
        tourney = Population.rng.choice(
            pop.indvs, tournament_size, replace=False).tolist()
        tourney.sort(key=order_by_fitness(mod))
        indv = None

        if Population.rng.rand() <= crossover_rate:
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
            print(f"Best fitness of gen {i}: {gen_best_fitness}")

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

    print("Finished execution")
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
    elitism: int = 0,
    crossover_rate: float = .5,
    tournament_size: int = 2,
):
    def f(pop): return tournament_selection_iteration(
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
