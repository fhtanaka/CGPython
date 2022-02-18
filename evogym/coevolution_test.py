from evogym import is_connected, has_actuator, get_full_connectivity, hashable
from evogym.envs import WalkingFlat, StepsUp
from typing import Dict, List, Tuple
import numpy as np
import dill
from graph import Graph
from evolution_strategies import tournament_selection
from population import Population
from arg_parser import parse_args
from operator import attrgetter

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


class  RobotController:
    def __init__(self, controllers: Population) -> None:
        self.population = controllers
        self.best_fit = None
        self.gen = -1


def eval_genome_constraint(robot, robot_dict):
    validity = is_connected(robot) and has_actuator(robot)
    return validity


def generate_robot(g: Graph, structure):
    robot = np.zeros(structure)
    for i in range(structure[0]):
        for j in range(structure[1]):
            input = (i - (structure[0] // 2),
                     j - (structure[1] // 2))
            graph_out = g.operate(input)
            node = np.argmax(graph_out)
            robot[i][j] = node
    return robot


def get_observation_with_floor(env):
    a = env.get_vel_com_obs("robot")
    b = env.get_pos_com_obs("robot")
    c = env.get_floor_obs("robot", ["ground"], 5)
    return np.concatenate((a, b, c))


def get_observation(env):
    a = env.get_vel_com_obs("robot")
    b = env.get_pos_com_obs("robot")
    c = env.get_floor_obs("robot", ["ground"], 5)
    return np.concatenate((a, b, c))


def calculate_reward(env: StepsUp, controller: Graph, n_steps: int, env_name:str):
    reward = 0
    env.reset()
    actuators = env.get_actuator_indices("robot")

    for _ in range(n_steps):
        if env_name == "StepsUp":
            obs = get_observation_with_floor(env)
        else:
            obs = get_observation(env)

        action_by_actuator = controller.operate(obs)
        action = [action_by_actuator[i] for i in actuators]

        obs, r, done, _ = env.step(np.array(action))
        reward += r

        if done:
            return reward, True

    return reward, False


def get_controller_population(robot: np.array, robot_dict: Dict[str, RobotController], args):
    robot_hash = hashable(robot)
    if robot_hash not in robot_dict:
        controller_pop = Population(
            population_size=args["pop_size"],
            n_in=15,
            n_out=25,
            n_middle=args["n_middle_nodes"]
        )
        robot_dict[robot_hash] = RobotController(controller_pop)
    return robot_dict[robot_hash]

def optimize_control(controller_pop, robot, args):
    def c_fit_func(indv, gen): return controller_fitness_func(indv, gen, robot, args["n_steps"], args["env_name"])
    tournament_selection(
        population=controller_pop,
        generations=1,
        goal_fit=args["goal_fit"],
        fitness_func=c_fit_func,
        minimize_fitness=False,
        fit_share=args["fit_share"],
        stagnation=args["stagnation"],
        stag_preservation=args["stag_preservation"],
        report=None,
        mutate_active_only=args["mut_active_only"],
        mutation_rate=args["mut_rate"],
        elitism=args["elitism"],
        crossover_rate=args["crossover_rate"],
        tournament_size=args["tourney_size"],
        species_threshold=args["species_threshold"],
        n_threads=args["n_threads"],
    )
    
def structure_fitness_func(individual: Graph, gen: int, structure: Tuple, robot_dict: Dict[str, RobotController], args, minimize_fitness):

    robot = generate_robot(individual, structure)
    if not eval_genome_constraint(robot, robot_dict):
        return -10000

    robot_controllers = get_controller_population(robot, robot_dict, args)
    
    if robot_controllers.best_fit is not None and robot_controllers.gen == gen:
        return robot_controllers.best_fit

    optimize_control(robot_controllers.population, robot, args)

    if minimize_fitness:
        champion = min(robot_controllers.population.indvs, key=attrgetter('original_fit'))
    else:
        champion = max(robot_controllers.population.indvs, key=attrgetter('original_fit'))

    result = champion.original_fit
    robot_controllers.best_fit = result 
    robot_controllers.gen = gen
    
    return result


def controller_fitness_func(individual: Graph, gen: int, robot: np.array, n_steps: int, env_name: str):
    connections = get_full_connectivity(robot)
    if env_name == "StepsUp":
        env = StepsUp(body=robot, connections=connections)
    else:
        env = WalkingFlat(body=robot, connections=connections)

    reward, _ = calculate_reward(env, individual, n_steps, env_name)

    return reward

def get_top_robots(top, robot_dict):
    ordered_robots = {k: v for k, v in sorted(robot_dict.items(), key=lambda item: -1*item[1].best_fit)}
    best_robots = {}
    cont = 0
    for k, v in ordered_robots.items():
        if cont >= top:
            break
        best_robots[k] = v
        cont+=1
    return best_robots

def main():
    strucure = (5, 5)
    save_top = 50
    robot_dict = {}
    args = parse_args()

    structure_pop = Population(
        population_size=args["pop_size"],
        n_in=2,
        n_out=5,
        n_middle=args["n_middle_nodes"]
    )

    minimize_fitness = False

    def s_fit_func(indv, gen): return structure_fitness_func(indv, gen, strucure, robot_dict, args, minimize_fitness)
    tournament_selection(
        population=structure_pop,
        generations=args["max_gens"],
        goal_fit=args["goal_fit"],
        fitness_func=s_fit_func,
        minimize_fitness=minimize_fitness,
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
        n_threads=1,
    )

    if args["save_to"] is not None:
        best_robots = get_top_robots(save_top, robot_dict)
        for indv in structure_pop.indvs:
            robot = generate_robot(indv, strucure)
            h = hashable(robot) 
            if h not in best_robots and h in robot_dict:
                best_robots[h] = robot_dict[h]
        s = (structure_pop, best_robots)
        dill.dump(s, open(args["save_to"], mode='wb'))

if __name__ == "__main__":
    main()
