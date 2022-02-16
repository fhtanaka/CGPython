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


def generate_robot():
    robot = np.array([[0, 0, 0, 0, 0],
                      [0, 3, 3, 3, 0],
                      [3, 3, 3, 3, 3],
                      [3, 3, 3, 3, 3],
                      [3, 3, 3, 3, 3]])

    return robot, get_full_connectivity(robot)


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
        # action = np.clip(action, .6, 1.6)
        _, r, done, _ = env.step(np.array(action))
        reward += r

        if done:
            break
    return reward


def controller_fitness_func(individual: Graph, structure: Tuple, n_steps: int, robot_dict):
    robot, connections = generate_robot()

    # connections = get_full_connectivity(robot)

    env = WalkingFlat(body=robot, connections=connections)
    env.reset()

    reward = calculate_reward(env, individual, n_steps)

    return reward


def main():
    strucure = (5, 5)
    n_steps = 200
    robot_dict = {}
    args = parse_args()

    controller_pop = Population(
        population_size=args["pop_size"],
        n_in=4,
        n_out=25,
        n_middle=args["n_middle_nodes"]
    )
    dill.dump(controller_pop, open("results.pkl", mode='wb'))

    def c_fit_func(x): return controller_fitness_func(
        x, strucure, n_steps, robot_dict)

    tournament_selection(
        population=controller_pop,
        generations=args["max_gens"],
        goal_fit=3,
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

    dill.dump(controller_pop, open("results.pkl", mode='wb'))


if __name__ == "__main__":
    main()
