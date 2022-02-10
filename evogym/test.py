from copyreg import constructor
from evogym import is_connected, has_actuator, get_full_connectivity, hashable
from evogym.envs import WalkingFlat
import struct
from typing import List, Tuple
import numpy as np
import dill
from graph import Graph
from evolution_strategies import tournament_selection
from population import Population
from arg_parser import parse_args


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

node_names = ['empty', 'rigid', 'soft', 'hori', 'vert']


def eval_genome_constraint(robot, robot_dict):
    validity = is_connected(robot) and has_actuator(robot)
    if validity:
        robot_hash = hashable(robot)
        if robot_hash in robot_dict:
            validity = True
        else:
            robot_dict[robot_hash] = True
    return validity

def generate_robot(g: Graph, structure):
    robot = np.zeros(structure)
    for i in range(structure[0]):
        for j in range(structure[1]):
            input = (i, j)
            graph_out = g.operate(input)
            node = np.argmax(graph_out)
            robot[i][j] = node
    return robot

def get_observation(env):
    a = env.get_vel_com_obs("robot")
    b = env.get_pos_com_obs("robot")
    return np.concatenate((a, b))

def calculate_reward(env: WalkingFlat, controller: Graph, n_steps: int):
    reward = 0
    
    actuators = env.get_actuator_indices("robot")

    for _ in range(n_steps):
        obs = get_observation(env)

        action_by_actuator = controller.operate(obs)
        action = [action_by_actuator[i] for i in actuators]
        
        _, r, done, _ = env.step(np.array(action))
        reward += r

        if done:
            break
    return reward

def structure_fitness_func(individual: Graph, structure: Tuple, n_steps: int, controllers: Population, robot_dict):

    robot = generate_robot(individual, structure)    

    if not eval_genome_constraint(robot, robot_dict):
        return -10000

    connections = get_full_connectivity(robot)
    env = WalkingFlat(body=robot, connections=connections)
    env.reset()

    fitness = []
    for controller in controllers.indvs:
        reward = calculate_reward(env, controller, n_steps)
        fitness.append(reward)

    return max(fitness)


def controller_fitness_func(individual: Graph, structure: Tuple, n_steps: int, contructors: Population, robot_dict):
    fitness = []
    for builder in contructors.indvs:
        robot = generate_robot(builder, structure)

        if not eval_genome_constraint(robot, robot_dict):
            fitness.append(-1000)
            continue

        connections = get_full_connectivity(robot)
        env = WalkingFlat(body=robot, connections=connections)
        env.reset()

        reward = calculate_reward(env, individual, n_steps)
        fitness.append(reward)

    return max(fitness)


def main():
    strucure = (5, 5)
    n_steps = 100
    gens = 1
    robot_dict = {}
    args = parse_args()


    structure_pop = Population(
        population_size=args["pop_size"],
        n_in=2,
        n_out=5,
        n_middle=args["n_middle_nodes"]
    )

    controller_pop = Population(
        population_size=args["pop_size"],
        n_in=4,
        n_out=25,
        n_middle=args["n_middle_nodes"]
    )

    def s_fit_func(x): return structure_fitness_func(x, strucure, n_steps, controller_pop, robot_dict)
    def ts_select(): return tournament_selection(
        population=structure_pop,
        generations=gens,
        goal_fit=.1,
        fitness_func=s_fit_func,
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
    )

    def c_fit_func(x): return controller_fitness_func(x, strucure, n_steps, structure_pop, robot_dict)
    def tc_select(): return tournament_selection(
        population=controller_pop,
        generations=gens,
        goal_fit=.1,
        fitness_func=c_fit_func,
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
    )

    for i in range(args["max_gens"]):
        print(i)
        ts_select()
        tc_select()


if __name__ == "__main__":
    main()
