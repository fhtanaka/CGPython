import argparse

def parse_args():
    args_dict = {}

    # Default Values
    # saving_to = "cache/tourney_cross_spec.pkl"
    report = None
    csv_file = None
    pop_size = 96
    n_middle_nodes = 32
    max_gens = 100
    fit_share = True
    stagnation = 100
    elitism = 2
    mut_active_only = False
    mut_rate = .1
    crossover_rate = .9
    tourney_size = 10
    selection_method = "tournament"
    n_tests = 100
    stag_preservation = 2
    species_threshold = .7
    cpus = 4
    n_steps = 400
    env_name = "StepsUp"
    goal_fit = 4
    fit_partition = 1

    parser = argparse.ArgumentParser()

    parser.add_argument("-r", "--report", nargs="?", default=report, help="report", type=int) 
    parser.add_argument("-p", "--pop", nargs="?", default=pop_size, help="pop_size", type=int) 
    parser.add_argument("-n", "--n_nodes", nargs="?", default=n_middle_nodes, help="n_middle_nodes", type=int) 
    parser.add_argument("-g", "--gens", nargs="?", default=max_gens, help="max_gens", type=int) 
    parser.add_argument("-s", "--stagnation", nargs="?", default=stagnation, help="stagnation", type=int) 
    parser.add_argument("-e", "--elitism", nargs="?", default=elitism, help="elitism", type=int)
    parser.add_argument("-m", "--mut_rate", nargs="?", default=mut_rate, help="mut_rate", type=float) 
    parser.add_argument("-c", "--cross_rate", nargs="?", default=crossover_rate, help="crossover_rate", type=float) 
    parser.add_argument("-t", "--t_size", nargs="?", default=tourney_size, help="tourney_size", type=int) 
    parser.add_argument("-f", "--save_to", nargs="?", default=None, help="file to save the population")

    parser.add_argument("--steps", nargs="?", default=n_steps, help="n_steps", type=int)
    parser.add_argument("--env_name", nargs="?", default=env_name, help="env_name")
    parser.add_argument("--n_tests", nargs="?", default=n_tests, help="n_tests", type=int) 
    parser.add_argument("--cpu", nargs="?", default=cpus, help="selection_method", type=int)
    parser.add_argument("--stag_preservation", nargs="?", default=stag_preservation, help="stag_preservation", type=int) 
    parser.add_argument("--goal_fit", nargs="?", default=goal_fit, help="goal_fit", type=int) 
    parser.add_argument("--species_threshold", nargs="?", default=species_threshold, help="species_threshold", type=float) 
    parser.add_argument("--fit_partition", nargs="?", default=fit_partition, help="fit_partition", type=float) 
    parser.add_argument("--selection_method", nargs="?", default=selection_method, help="selection_method")
    parser.add_argument("--mut_active", nargs="?", default=mut_active_only, help="mut_active_only") 
    parser.add_argument("--no_fit_share", nargs="?", default=fit_share, help="fit_share")
    parser.add_argument("--csv", nargs="?", default=csv_file, help="fit_share")

    command_line_args = parser.parse_args()

    args_dict["report"] = command_line_args.report
    args_dict["pop_size"] = command_line_args.pop
    args_dict["n_middle_nodes"] = command_line_args.n_nodes
    args_dict["max_gens"] = command_line_args.gens
    args_dict["stagnation"] = command_line_args.stagnation
    args_dict["elitism"] = command_line_args.elitism
    args_dict["mut_rate"] = command_line_args.mut_rate
    args_dict["crossover_rate"] = command_line_args.cross_rate
    args_dict["tourney_size"] = command_line_args.t_size
    args_dict["selection_method"] = command_line_args.selection_method
    args_dict["n_tests"] = command_line_args.n_tests
    args_dict["stag_preservation"] = command_line_args.stag_preservation
    args_dict["save_to"] = command_line_args.save_to
    args_dict["species_threshold"] = command_line_args.species_threshold
    args_dict["n_threads"] = command_line_args.cpu
    args_dict["n_steps"] = command_line_args.steps
    args_dict["env_name"] = command_line_args.env_name
    args_dict["goal_fit"] = command_line_args.goal_fit
    args_dict["csv"] = command_line_args.csv
    args_dict["fit_partition"] = command_line_args.fit_partition

    args_dict["fit_share"] = command_line_args.no_fit_share
    if args_dict["fit_share"] != True:
        args_dict["fit_share"] = False

    args_dict["mut_active_only"] = command_line_args.mut_active
    if args_dict["mut_active_only"] != False:
        args_dict["mut_active_only"] = True

    # if report is not None:
    for k, v in args_dict.items():
        print(f"{k}: {v}")
    print()

    return args_dict

