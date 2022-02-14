from population import Population
from operator import attrgetter

def fitness_diversity(pop: Population, interval_size: float):
    diversity_dict = {}
    
    for indv in pop.indvs:
        fingerprint = int(indv.original_fit/interval_size)
        diversity_dict[fingerprint] = True
    
    return len(diversity_dict)

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
