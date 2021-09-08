from population import Population
import numpy as np
from graph import Graph
import cProfile
import pstats

addition = lambda x, y: x+y
multiplication = lambda x, y: x*y
subtraction = lambda x, y: x-y
constant = lambda x: x
protected_div = lambda x, y: 1 if y == 0 else x/y
increment = lambda x: x+1
invert = lambda x: -x

seed = 2002
n_function_evaluations = 10
Graph.rng = np.random.RandomState(seed)

Population.add_operation(arity=1, func=constant, string="x")
Population.add_operation(arity=1, func=increment, string="x+1")
Population.add_operation(arity=1, func=invert, string="-x")
Population.add_operation(arity=2, func=addition, string="x+y")
Population.add_operation(arity=2, func=multiplication, string="x*y")
Population.add_operation(arity=2, func=subtraction, string="x-y")
Population.add_operation(arity=2, func=protected_div, string="*x/y")

def f1_target(x, y):
    return x ** 2 + 2*y

def f2_target(x, y):
    return (x+3)*(y-5)

def fitness_func(individual: Graph, tests):

    fitness = 0
    for t in tests:
        pred1, pred2 = individual.operate([t[0][0], t[0][1]])
        fitness += (t[1][0] - pred1)**2 + (t[1][1] - pred2)**2

        # pred1 = individual.operate(t[0])[0]
        # fitness += (t[1][0] - pred1)**2
    return  fitness

def create_tests(n):
    tests = []
    for i in range(n):
        x = np.random.uniform(-10, +10)
        y = np.random.uniform(-10, +10)
        target1 = f1_target(x, y)
        target2 = f2_target(x, y)
        tests.append(([x,y], (target1, target2)))
    return tests

def main():
    tests = create_tests(n_function_evaluations)
    population = Population (
        population_size = 4,
        n_in = 2,
        n_out = 2,
        n_row = 8,
        n_col = 8,
        levels_back = 3,
        mutation_strategy = "prob",
        fitness_func = lambda x: fitness_func(x, tests),
        minimize_fitness = True,
        point_mut_qnt = 10,
        prob_mut_chance = .05,
        mutate_active_only = False
    )
    profile = cProfile.Profile()
    profile.runcall(lambda: population.one_plus_lamda(1000, 1, 0.1, False))
    ps = pstats.Stats(profile)
    ps.print_stats()
    print()
    
    # test_population(population, 0.1)

if __name__ == "__main__":
    main()