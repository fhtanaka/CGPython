from population import Population
import matplotlib.pyplot as plt
import numpy as np
from docopt import docopt
from graph import Graph

addition = lambda x, y: x+y
multiplication = lambda x, y: x*y
subtraction = lambda x, y: x-y
constant = lambda x: x
protected_div = lambda x, y: 1 if y == 0 else x/y
increment = lambda x: x+1
invert = lambda x: -x

seed = 2002
n_function_evaluations = 1
Graph.rng = np.random.RandomState(seed)

Graph.add_operation(arity=1, func=constant, string="x")
Graph.add_operation(arity=1, func=increment, string="x+1")
Graph.add_operation(arity=1, func=invert, string="-x")
Graph.add_operation(arity=2, func=addition, string="x+y")
Graph.add_operation(arity=2, func=multiplication, string="x*y")
Graph.add_operation(arity=2, func=subtraction, string="x-y")
Graph.add_operation(arity=2, func=protected_div, string="*x/y")

def f1_target(x, y):
    return x ** 2 + 2*y

def f2_target(x, y):
    return (x+3)*(y-5)

def fitness_func(individual: Graph, tests):

    fitness = 0
    for t in tests:
#         pred1, pred2 = individual.operate(t[0])
#         fitness += (t[1][0] - pred1)**2 + (t[1][1] - pred2)**2
        pred1 = individual.operate(t[0])[0]
      
        fitness += (t[1][0] - pred1)**2
    return  fitness

def test_population (pop: Population, goal_fit):
    fit_achieved = False
    tests = []
    for i in range(n_function_evaluations):
        x = np.random.uniform(-10, +10)
        y = np.random.uniform(-10, +10)
        target1 = f1_target(x, y)
        target2 = f2_target(x, y)
        tests.append(([x,y], (target1, target2)))
    for i in range(pop.gens):
        print("generation ", i)
        min_fitness = 1000000000
        for ind in pop.indvs:
            fitness = fitness_func(ind, tests)
            print(ind.id, " fit: ", fitness)
            ind.fitness = fitness
            if fitness < min_fitness:
                min_fitness = fitness
            if fitness <= goal_fit:
                fit_achieved = True
        if fit_achieved:
            break
        print("min fitness of gen: ", min_fitness)
        pop.iterate_one_plus_lambda()

    print("finish")

def main():
    population = Population (
        population_size = 4,
        n_in = 2,
        n_out = 1,
        n_row = 8,
        n_col = 8,
        levels_back = 3,
        n_champions = 1,
        mutation_strategy = "prob",
        generations = 1000,
        minimize_fitness = True,
        point_mut_qnt = 10,
        prob_mut_chance = .05,
        mutate_active_only = False
    )
    test_population(population, 0.1)

if __name__ == "__main__":
    main()