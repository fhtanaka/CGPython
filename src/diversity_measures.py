from typing import Dict
from .population import Population
from .graph import Graph
import math


def __diversity_dict(pop: Population, interval_size: float):
    diversity_dict = {}

    for indv in pop.indvs:
        fingerprint = int(indv.original_fit/interval_size)
        if fingerprint in diversity_dict:
            diversity_dict[fingerprint] += 1
        else:
            diversity_dict[fingerprint] = 1
    return diversity_dict

def fitness_diversity(pop: Population, interval_size: float):
    diversity_dict = __diversity_dict(pop, interval_size)
    return len(diversity_dict)


def pop_entropy(pop: Population, interval_size: float):
    diversity_dict = __diversity_dict(pop, interval_size)
    entropy = 0
    pop_len = len(pop.indvs)
    for k, v in diversity_dict.items():
        p = v/pop_len
        entropy -= p * math.log2(p)
    return entropy


def pop_entropy_and_fitness_diversity(pop: Population, interval_size: float):
    diversity_dict = __diversity_dict(pop, interval_size)
    entropy = 0
    pop_len = len(pop.indvs)
    for k, v in diversity_dict.items():
        p = v/pop_len
        entropy -= p * math.log2(p)
    return len(diversity_dict), entropy

# Calculate possible isomorphisms by the tuple: (n_active_nodes, total_inputs, n_operations)
# Obs: count inputs and operations of only active nodes
def structural_diversity(pop: Population):
    diversity_dict = {}
    for indv in pop.indvs:
        active_count = 0
        inputs_count = 0
        op_dict = {}
        for node in indv.nodes:
            if node.active: 
                active_count += 1
                inputs_count += len(node.inputs)
                if node.operation is not None:
                    op = indv.decode_operation(node.operation)
                    op_dict[op] = True

        fingerprint = (active_count, inputs_count, len(op_dict))
        diversity_dict[fingerprint] = True

    return len(diversity_dict)

def graph_genetic_marks(g: Graph):
    nodes_str = []
    for node in g.nodes:
        if node.operation == None:
            nodes_str.append(f"n_{node.id}")
        else:
            nodes_str.append(g.decode_operation(node.operation).string)


    markers: Dict[str, int] = {}
    for node in g.nodes:
        if len(node.inputs) == 0 or node.operation == None:
            continue

        mark = ""
        for input in node.decode_inputs():
            mark += nodes_str[input] + ", "
        op = g.decode_operation(node.operation).string
        mark = f"{op} ({mark[:-2]})"

        if mark not in markers:
            markers[mark] = [0, 0]

        if node.active:
            markers[mark][0] += 1
        else:
            markers[mark][1] += 1
    return markers

def population_genetic_marks(pop: Population):
    markers_by_indv = {}
    global_gen_markers = {}
    for indv in pop.indvs:
        g_mark = graph_genetic_marks(indv)
        markers_by_indv[indv.id] = g_mark
        for mark, qtd in g_mark.items():
            if mark not in global_gen_markers:
                global_gen_markers[mark] = [0, 0]
            global_gen_markers[mark][0] += qtd[0]
            global_gen_markers[mark][1] += qtd[1]

    return markers_by_indv, global_gen_markers