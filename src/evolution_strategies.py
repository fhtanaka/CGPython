import time
import numpy as np
from .diversity_measures import *
from .graph import Graph
from .population import Population
from typing import Callable, List
from operator import attrgetter
from pathos.multiprocessing import ProcessPool
import errno
import dill

c1 = 1
c2 = 1
b1 = 1
b2 = 1
b3 = .25

alfa = 1
beta = 2.5

def explicit_fit_sharing(pop: Population, minimize_fitness: bool, species_threshold: float):
    pop.separate_species(c1, c2, b1, b2, b3, species_threshold, 0)
    for _, sp in pop.species_dict.items():
        for indv in sp.members:
            if minimize_fitness:
                indv.fitness = (indv.fitness**alfa) * (len(sp.members)**beta)
            else:
                indv.fitness = (indv.fitness**alfa) / (len(sp.members)**beta)

def update_pop_fitness(pop, gen, fitness_func, fit_share, minimize_fitness, species_threshold):
    for ind in pop.indvs:
        fit = fitness_func(ind, gen)
        ind.fitness = np.clip(fit, -1*(10**10), 10**10)
        ind.original_fit = ind.fitness
    if fit_share:
        explicit_fit_sharing(pop, minimize_fitness, species_threshold)


def update_pop_fitness_thread(indvs, gen, fitness_func):
    results_dict = {}
    for ind in indvs:
        fit = fitness_func(ind, gen)
        fit = np.clip(fit, -1*(10**10), 10**10)
        results_dict[ind.id] = fit
    return results_dict

def parallel_update_pop_fitness(pop, gen, fitness_func, fit_share, minimize_fitness, species_threshold, n_workers):
    try:
        pool = ProcessPool(nodes=n_workers)
        results = pool.map(
            update_pop_fitness_thread, 
            np.array_split(pop.indvs, n_workers),
            [gen for _ in range(n_workers)],
            [fitness_func for _ in range(n_workers)]
        )
        
        fitness_dict = {}
        for result_dict in results:
            for k, v in result_dict.items():
                fitness_dict[k] = v

        for ind in pop.indvs:
            ind.fitness = fitness_dict[ind.id]
            ind.original_fit = ind.fitness

        if fit_share:
            explicit_fit_sharing(pop, minimize_fitness, species_threshold)
            
    except IOError as e:
        if e.errno == errno.EPIPE:
            print("Problem with broken pipe")
        else:
            raise(IOError)

def print_csv(gen, champion, pop, species_threshold, fit_partition_size, csv_file):
    deltas = pop.separate_species(c1, c2, b1, b2, b3, species_threshold)
    fit_div, entropy = pop_entropy_and_fitness_diversity(pop, fit_partition_size)
    struc_div = structural_diversity(pop)
    species_div = len(pop.species_dict)
    _, global_gen_markers = population_genetic_marks(pop, 2)

    active_cont = 0
    inactive_cont = 0
    for qtd in global_gen_markers.values():
        if qtd[0] > 0:
            active_cont += 1
        if qtd[1] > 0:
            inactive_cont += 1

    csv_file.write(f"{gen};{champion.original_fit};{species_div};{struc_div};{fit_div};{entropy};{len(global_gen_markers)};{active_cont};{inactive_cont};{np.average(deltas)};{np.std(deltas)}\n")


def print_report(gen, champion, pop, species_threshold, fit_partition_size):
    deltas = pop.separate_species(c1, c2, b1, b2, b3, species_threshold)
    print(f"best_in_gen_{gen}: {champion.id};\t original_fit: {champion.original_fit:.2f};\t shared_fit: {champion.fitness:.2f};\t specie: {champion.species_id};")

    fit_div, entropy = pop_entropy_and_fitness_diversity(pop, fit_partition_size)
    struc_div = structural_diversity(pop)
    species_div = len(pop.species_dict)
    print(f"n_species: {species_div};\t structure_diversity: {struc_div};\t fit_diversity: {fit_div};\t entroypy: {entropy}")

    # if species_div < 20:
    #     print(f"Species: [", end="")
    #     for _, sp in sorted(pop.species_dict.items()):
    #         print(f"{sp.representant.species_id} ({sp.age}): {len(sp.members)}", end=", ")
    #     print("]")
    # else:
    #     print(f"Species: [...]")

    # print(f"Deltas ;\t min: {min(deltas)};\t max: {max(deltas)}\t avg: {np.average(deltas)} \n")
    # pp.update([[len(pop.species_dict)]])
    print()
    # if gen % 10 == 0:
    #     controller_fitness_func(champion, 200)


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
    species_threshold,
    csv_file,
    fit_partition_size,
    save_pop = None,
    n_threads = 1,
):
    fit_mod = 1
    last_gen_fitness = float('-inf')
    if minimize_fitness:
        fit_mod = -1
        last_gen_fitness = float('inf')

    break_by_stagnation = 0
    stagnation_count = 0
    stag_preservation *= -1

    file = None
    if csv_file is not None:
        file = open(csv_file, 'w')
        header = "gen;fitness;n_species;p_isomorphisms;unique_fitness;entropy;total_gen_markers;active_gen_markers;inactive_gen_markers;avg_delta;std_delta\n"
        file.write(header)


    for gen in range(generations+1):
        s = time.time()
        if n_threads > 1:
            parallel_update_pop_fitness(pop, gen, fitness_func, fit_share, minimize_fitness, species_threshold, n_threads)
        else:
            update_pop_fitness(pop, gen, fitness_func, fit_share, minimize_fitness, species_threshold)

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


        if csv_file is not None:
            print_csv(gen, champion, pop, species_threshold, fit_partition_size, file)

        if report is not None and gen % report == 0:
            print_report(gen, champion, pop, species_threshold, fit_partition_size)
            if save_pop != None:
                if ".pkl" in save_pop:
                    save_pop = save_pop.split(".pkl")[0]
                f = f"{save_pop}_g_{gen}.pkl"
                dill.dump(pop, open(f, mode='wb'))

        if fit_mod*gen_best_fitness >= fit_mod*goal_fit or gen == generations:
            break

        if stagnation_count > stagnation:
            if report is not None:
                print(f"Generation {gen}: Fitness stagnated, reseting population")
            stagnation_count = 0
            break_by_stagnation += 1
            if break_by_stagnation > 5:
                if report is not None:
                    print("Exiting because stagnated too many times")
                break
            pop.indvs.sort(key=lambda x: (x.original_fit * fit_mod, x.id))
            pop.indvs[:stag_preservation] = pop.create_individuals()[:stag_preservation]
            update_pop_fitness(pop, gen, fitness_func, False, minimize_fitness, species_threshold)
        
        selection_function(pop)
        if report is not None and gen % report == 0:
            print(f'Gen {gen} took {round(time.time()-s, 1)}s\n')

    if csv_file is not None:
        file.close()
    # pop.indvs.sort(key=lambda x: (x.fitness * fit_mod, x.id))
    # print("\nFinished execution")
    # print("Total generations: {}".format(i))
    # print("Best Shared Fitness: {}".format(pop.indvs[-1].fitness))
    # print("Best Original Fitness: {}".format(pop.indvs[-1].original_fit))

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
    fit_share=True,
    stagnation: int = 100,
    stag_preservation: int = 2,
    report=False,

    n_champions: int = 1,
    mutate_active_only: bool = False,
    mutation_rate: float = .1,

    species_threshold: float = .8,

    save_pop:str = None,
    n_threads=1,

    csv_file = None,
    fit_partition_size = 1,
):
    def f(pop): return one_plus_lambda_iteration(
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
        csv_file,
        fit_partition_size,
        save_pop,
        n_threads,
    )


def tournament_selection(
    population: Population,

    generations: int,
    goal_fit: float,
    fitness_func: Callable[[Graph], float],
    minimize_fitness: bool = False,
    fit_share=True,
    stagnation: int = 100,
    stag_preservation: int = 2,
    report=None,

    mutate_active_only: bool = False,
    mutation_rate: float = 0.1,
    elitism: int = 1,
    crossover_rate: float = .5,
    tournament_size: int = 2,

    species_threshold: float = .8,

    save_pop:str = None,
    n_threads = 1,

    csv_file = None,
    fit_partition_size = 1,
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
        csv_file,
        fit_partition_size,
        save_pop,
        n_threads,
    )
