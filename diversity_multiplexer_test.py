import numpy as np
import dill
import math
from src.graph import Graph
from src.evolution_strategies import one_plus_lambda, tournament_selection
from src.population import Population
from src.arg_parser import parse_args
import cProfile
import pstats


def bool_if(x, y, z): return x if z else y
def bool_and(x, y): return x and y
def bool_or(x, y): return x or y
def bool_not(x): return not x


Population.add_operation(arity=2, func=bool_and, string="AND")
Population.add_operation(arity=2, func=bool_or, string="OR")
Population.add_operation(arity=1, func=bool_not, string="NOT")
Population.add_operation(arity=3, func=bool_if, string="IF")
Population.rng = np.random.RandomState(10)


def eleven_multiplexer(arr):
    if len(arr) != 11:
        print("AAAAAAAAAAAAAAAAAAAAAAA")
        raise 
    d = arr[0:8]
    a = arr[8:11]
    index = (int(a[0]) * 4) + (int(a[1]) * 2) + (int(a[2]) * 1)
    if d[index] == "1":
        return True
    return False


def create_tests():
    tests = []

    for i in range(1024):
        base_2_v = bin(i).replace("0b", "").zfill(11)
        input_arr = []
        for c in base_2_v:
            inp = True if c == "1" else False
            input_arr.append(inp)
        response = eleven_multiplexer(base_2_v)
        tests.append((input_arr, [response]))
    return tests


def fitness_func(individual: Graph, gen: int, tests):
    fitness = 0
    for t in tests:
        inputs = t[0]
        expected_out = t[1]

        graph_out = individual.operate(inputs)

        for h, y in zip(graph_out, expected_out):
            if h == y:
                fitness += 1

    return fitness/len(tests)


def main():
    args = parse_args()

    tests = create_tests()
    def fit_func(indv, gen): return fitness_func(indv, gen, tests)

    population = Population(
        population_size=args["pop_size"],
        n_in=11,
        n_out=1,
        n_middle=args["n_middle_nodes"]
    )

    def t_select(): return tournament_selection(
        population=population,
        generations=args["max_gens"],
        goal_fit=1,
        fitness_func=fit_func,
        minimize_fitness=False,
        fit_share=args["fit_share"],
        stagnation=args["stagnation"],
        stag_preservation=args["stag_preservation"],
        report=args["report"],
        mutate_active_only=args["mut_active_only"],
        mutation_rate=args["mut_rate"],
        elitism=args["elitism"],
        crossover_rate=args["crossover_rate"],
        tournament_size=args["tourney_size"],
        species_threshold=args["species_threshold"],
        n_threads=args["n_threads"],
        csv_file=args["csv"],
        fit_partition_size=args["fit_partition"]
    )

    def p_lambda(): return one_plus_lambda(
        population=population,
        generations=args["max_gens"],
        goal_fit=1,
        fitness_func=fit_func,
        minimize_fitness=False,
        fit_share=args["fit_share"],
        stagnation=args["stagnation"],
        stag_preservation=args["stag_preservation"],
        report=args["report"],
        n_champions=args["elitism"],
        mutate_active_only=args["mut_active_only"],
        mutation_rate=args["mut_rate"],
        species_threshold=args["species_threshold"],
        n_threads=args["n_threads"],
        csv_file=args["csv"],
        fit_partition_size=args["fit_partition"]
    )

    exec_func = t_select
    if args["selection_method"] == "lambda":
        exec_func = p_lambda

    profile = cProfile.Profile()
    profile.runcall(exec_func)
    ps = pstats.Stats(profile)
    ps.print_stats()
    print()

    if args["save_to"] is not None:
        dill.dump(population, open(args["save_to"], mode='wb'))


if __name__ == "__main__":
    main()
