import numpy as np
import dill
from src.graph import Graph
from src.evolution_strategies import one_plus_lambda, tournament_selection
from src.population import Population
from src.arg_parser import parse_args
import gym

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

def fitness_func(individual: Graph, gen:int,  n_steps):
    env = gym.make('BipedalWalker-v3')
    fitness = 0

    observation = env.reset()
    for t in range(n_steps):
        action = individual.operate(observation)
        observation, reward, done, info = env.step(action)
        fitness += reward
        if done:
                break
    
    return np.clip(fitness, -1*(10**10), 10**10)


def main():
    args = parse_args()
    Population.rng = np.random.default_rng(args["seed"])

    def fit_func(indv, gen): return fitness_func(indv, gen, args["n_steps"])

    population = Population(
        population_size=args["pop_size"],
        n_in=24,
        n_out=4,
        n_middle=args["n_middle_nodes"]
    )

    def t_select(): return tournament_selection(
        population=population,
        generations=args["max_gens"],
        goal_fit=250,
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
