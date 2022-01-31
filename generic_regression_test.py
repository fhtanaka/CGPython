import numpy as np
import dill
from graph import Graph
from evolution_strategies import one_plus_lambda, tournament_selection
from population import Population
from arg_parser import parse_args
import cProfile
import pstats

def addition(x, y): return x+y
def multiplication(x, y): return x*y
def subtraction(x, y): return x-y
def constant(x): return x
def protected_div(x, y): return 1 if y == 0 else x/y
def increment(x): return x+1
def invert(x): return -x

Population.add_operation(arity=1, func=constant, string="x")
Population.add_operation(arity=1, func=increment, string="x+1")
Population.add_operation(arity=1, func=invert, string="-x")
Population.add_operation(arity=2, func=addition, string="x+y")
Population.add_operation(arity=2, func=multiplication, string="x*y")
Population.add_operation(arity=2, func=subtraction, string="x-y")
Population.add_operation(arity=2, func=protected_div, string="*x/y")
Population.rng = np.random.RandomState(10)


def generate_functions(n_tests=100):
    n_inputs = 2

    def f1(x, y): return x**6 - 2*x**4 + x**2
    def f2(x, y): return x+y
    def f3(x, y): return y**4 - 2*y**3 + 5*x
    # def f4(x, y): return x**6 - 2*y*x**4 + y**2

    funcs = [f1, f2, f3]

    tests = create_tests(n_tests, n_inputs, funcs)

    return n_inputs, funcs, tests


def create_tests(n_tests, n_inputs, funcs):
    tests = []
    for _ in range(n_tests):
        inputs = [np.random.uniform(-10, +10) for _ in range(n_inputs)]
        responses = [f(*inputs) for f in funcs]
        tests.append((inputs, responses))
    return tests


def fitness_func(individual: Graph, tests):
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
    fit_func = lambda x: fitness_func(x, tests)
    
    population = Population(
        population_size = args["pop_size"],
        n_in = inputs,
        n_out = len(funcs),
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
