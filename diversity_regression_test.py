import numpy as np
import dill
import math
from src.graph import Graph
from src.evolution_strategies import one_plus_lambda, tournament_selection
from src.population import Population
from src.arg_parser import parse_args
import cProfile
import pstats


def addition(x, y): return x+y
def multiplication(x, y): return x*y
def subtraction(x, y): return x-y
def constant(x): return x
def protected_div(x, y): return 1 if y == 0 else x/y
def protected_log(x): return 0 if x <= 0.01 else math.log(x)
def increment(x): return x+1
def invert(x): return -x
def protected_exp(x): return 10**10 if x > 24 else math.exp(x)


Population.add_operation(arity=2, func=addition, string="+")
Population.add_operation(arity=2, func=multiplication, string="*")
Population.add_operation(arity=2, func=subtraction, string="-")
Population.add_operation(arity=2, func=protected_div, string="/")
Population.add_operation(arity=1, func=math.sin, string="SIN")
Population.add_operation(arity=1, func=math.cos, string="COS")
# Population.add_operation(arity=1, func=protected_exp, string="EXP")
Population.add_operation(arity=1, func=protected_log, string="RLOG")
Population.rng = np.random.RandomState(10)


def generate_functions(n_tests=20):
    n_inputs = 1

    def f1(x): return 4*x**4 + 3*x**3 + 2*x**2 + x

    funcs = [f1]

    tests = create_tests(n_tests, n_inputs, funcs)

    return n_inputs, funcs, tests


def create_tests(n_tests, n_inputs, funcs):
    tests = []
    for _ in range(n_tests):
        inputs = [np.random.uniform(-1, 1) for _ in range(n_inputs)]
        responses = [f(*inputs) for f in funcs]
        tests.append((inputs, responses))
    return tests


def fitness_func(individual: Graph, gen: int, tests):
    fitness = 0
    for t in tests:
        inputs = t[0]
        expected_out = t[1]

        graph_out = individual.operate(inputs)

        for h, y in zip(graph_out, expected_out):
            fitness += abs(y-h)

    return fitness


def main():
    args = parse_args()

    inputs, funcs, tests = generate_functions(args["n_tests"])
    def fit_func(indv, gen): return fitness_func(indv, gen, tests)

    population = Population(
        population_size=args["pop_size"],
        n_in=inputs,
        n_out=len(funcs),
        n_middle=args["n_middle_nodes"]
    )

    def t_select(): return tournament_selection(
        population=population,
        generations=args["max_gens"],
        goal_fit=.1,
        fitness_func=fit_func,
        minimize_fitness=True,
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
        goal_fit=.1,
        fitness_func=fit_func,
        minimize_fitness=True,
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

    # profile = cProfile.Profile()
    # profile.runcall(exec_func)
    # ps = pstats.Stats(profile)
    # ps.print_stats()
    # print()
    exec_func()

    if args["save_to"] is not None:
        dill.dump(population, open(args["save_to"], mode='wb'))


if __name__ == "__main__":
    main()
