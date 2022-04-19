from evogym import is_connected, has_actuator, get_full_connectivity, hashable
from evogym.envs import WalkingFlat, StepsUp
from typing import Dict, List, Tuple
import numpy as np
import dill
from src.graph import Graph
from src.evolution_strategies import tournament_selection
from src.population import Population
from src.arg_parser import parse_args
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

node_names = ['empty', 'rigid', 'soft', 'hori', 'vert']

def eval_genome_constraint(robot):
    validity = is_connected(robot) and has_actuator(robot)
    return validity


def generate_robot(g: Graph, structure):
    robot = np.zeros(structure)
    for i in range(structure[0]):
        for j in range(structure[1]):
            input = (i - (structure[0] // 2),
                     j - (structure[1] // 2))

            pad = np.zeros(get_obs_size())
            full_input = np.concatenate((input, pad))
            graph_out = g.operate(full_input)

            node = np.argmax(graph_out[:len(node_names)])
            robot[i][j] = node

    return robot

def calculate_reward(env: StepsUp, controller: Graph, n_steps: int):
    reward = 0
    env.reset()
    actuators = env.get_actuator_indices("robot")

    input_pad = np.zeros(2)

    for _ in range(n_steps):
        obs = get_observation(env)
        
        input = np.concatenate((input_pad, obs))
        action_by_actuator = controller.operate(input)[len(node_names):]

        action = np.array([action_by_actuator[i] for i in actuators]) 

        obs, r, done, _ = env.step(action)
        reward += r

        if done:
            return reward, True

    return reward, False

def get_obs_size():
    return 2 + 1 + 2 + 11 + 11

def get_observation(env):
    a = env.get_vel_com_obs("robot"),
    robot_ort_final = env.object_orientation_at_time(env.get_time(), "robot")
    b = np.array([robot_ort_final]),
    c = env.get_pos_com_obs("robot"),
    try:
        d = env.get_floor_obs("robot", ["terrain"], 5),
        e = env.get_ceil_obs("robot", ["terrain"], 5),
    except:
        d = env.get_floor_obs("robot", ["ground"], 5),
        e = env.get_ceil_obs("robot", ["ground"], 5),
        # e = np.zeros(11),
    
    return np.concatenate((*a, *b, *c, *d, *e))
    
def structure_fitness_func(individual: Graph, gen: int, structure: Tuple, args):

    robot = generate_robot(individual, structure)
    if not eval_genome_constraint(robot):
        return -10000
    connections = get_full_connectivity(robot)

    env_name = args["env_name"]
    if env_name == "StepsUp":
        env = StepsUp(body=robot, connections=connections)
    else:
        env = WalkingFlat(body=robot, connections=connections)

    reward, _ = calculate_reward(env, individual, args["n_steps"])
  
    return reward

def main():

    structure = (5, 5)
    args = parse_args()
    Population.rng = np.random.default_rng(args["seed"])

    pop = Population(
        population_size=args["pop_size"],
        n_in=2 + get_obs_size(),
        n_out=len(node_names) + structure[0]*structure[1],
        n_middle=args["n_middle_nodes"]
    )

    minimize_fitness = False

    def s_fit_func(indv, gen): return structure_fitness_func(indv, gen, structure, args)
    tournament_selection(
        population=pop,
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
        save_pop=args["save_to"],
        n_threads=1,
        csv_file=args["csv"],
    )

    if args["save_to"] is not None:
        # best_robots = get_top_robots(save_top, robot_dict)
        # for indv in structure_pop.indvs:
        #     robot = generate_robot(indv, strucure)
        #     h = hashable(robot) 
        #     if h not in best_robots and h in robot_dict:
        #         best_robots[h] = robot_dict[h]
        s = (pop)
        dill.dump(s, open(args["save_to"], mode='wb'))

if __name__ == "__main__":
    main()
