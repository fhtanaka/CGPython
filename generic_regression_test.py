import numpy as np
import dill
from graph import Graph
from evolution_strategies import one_plus_lambda, tournament_selection
from population import Population

REPORT = 1
FILENAME = "cache/tourney_cross_spec.pkl"

POP_SIZE = 100
N_MIDDLE_NODES = 100
MAX_GENS = 1000
STAGNATION = 30
ELITISM = 2
MUT_ACTIVE_ONLY = False
MUT_RATE = .1
CROSSOVER_RATE = .5
TOURNEY_SIZE = 10

def generate_functions():
    n_tests = 100
    n_inputs = 2

    def f1(x, y): return x**6 - 2*x**4 + x**2
    def f2(x, y): return x+y
    def f3(x, y): return y**4 - 2*y**3 + 5*x

    funcs = [f1, f2, f3]

    tests = create_tests(n_tests, n_inputs, funcs)

    return n_inputs, funcs, tests


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
            fitness += (y-h)**2

    return fitness


def main():
    inputs, funcs, tests = generate_functions()
    fit_func = lambda x: fitness_func(x, tests)
    
    population = Population(
        population_size = POP_SIZE,
        n_in = inputs,
        n_out = len(funcs),
        n_middle = N_MIDDLE_NODES
    )

    tournament_selection(
        population = population,
        generations = MAX_GENS,
        goal_fit = .1,
        fitness_func = fit_func,
        minimize_fitness = True,
        stagnation = STAGNATION,
        report = REPORT,
        mutate_active_only = MUT_ACTIVE_ONLY,
        mutation_rate = MUT_RATE,
        elitism = ELITISM,
        crossover_rate = CROSSOVER_RATE,
        tournament_size = TOURNEY_SIZE,
    )

    dill.dump(population, open(FILENAME, mode='wb'))

if __name__ == "__main__":
    main()
