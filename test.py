from population import Population
from operation import Operation
from graph import Graph
import numpy as np

addition = lambda x, y: x+y
multiplication = lambda x, y: x*y
subtraction = lambda x, y: x-y
constant = lambda x: x
protected_div = lambda x, y: 1 if y == 0 else x/y
increment = lambda x: x+1
invert = lambda x: -x

addition_op = Operation(2, addition, "x+y")
multiplication_op = Operation(2, multiplication, "x*y")
subtraction_op = Operation(2, subtraction, "x-y")
protected_div_op = Operation(2, protected_div, "*x/y")
constant_op = Operation(1, constant, "x")
increment_op = Operation(1, increment, "x+1")
invert_op = Operation(1, invert, "-x")

seed = 2002
Graph.rng = np.random.RandomState(seed)
Population.add_operation(arity=1, func=constant, string="x")
Population.add_operation(arity=1, func=increment, string="x+1")
Population.add_operation(arity=1, func=invert, string="-x")
Population.add_operation(arity=2, func=addition, string="x+y")
Population.add_operation(arity=2, func=multiplication, string="x*y")
Population.add_operation(arity=2, func=subtraction, string="x-y")
Population.add_operation(arity=2, func=protected_div, string="*x/y")

def test_get_node_value():
    g = Graph(0, 0, 0 ,0 , 0, Population.operations)

    five_node = g._add_node(5, col_num=0)
    ten_node = g._add_node(10, col_num=0)
    zero_node = g._add_node(0, col_num=0)

    addition_node = g._add_node(operation=addition_op)
    g.nodes[addition_node].inputs = [five_node, ten_node]
    assert g.get_node_value(addition_node) == 15
    g.reset_graph_value()

    multiplication_node = g._add_node(operation=multiplication_op)
    g.nodes[multiplication_node].inputs = [five_node, ten_node]
    assert g.get_node_value(multiplication_node) == 50
    g.reset_graph_value()

    p_div_node = g._add_node(operation=protected_div_op)
    g.nodes[p_div_node].inputs = [five_node, zero_node]
    assert g.get_node_value(p_div_node) == 1
    g.reset_graph_value()

    subtraction_node = g._add_node(operation=subtraction_op)
    g.nodes[subtraction_node].inputs = [p_div_node, addition_node]
    aux_node = g._add_node(operation=multiplication_op)
    g.nodes[aux_node].inputs = [subtraction_node, multiplication_node]
    assert g.get_node_value(aux_node) == -700

def test_graph_construction():
    ## set up ##

    indv = Graph(5, 4, 3, 3, 2, Population.operations)

    inputs = [5, 0, -5 ,3 ,0]
    result = indv.operate(inputs)

    assert result[0] == 16
    assert result[1] == 11
    assert result[2] == 11
    assert result[3] == 5

def test_clone():
    g = Graph(3, 3, 3, 3, 2, Population.operations)
    clone = g.clone_graph()
    for id, node in g.nodes.items():
        clone_node = clone.nodes[id]
        assert clone_node.global_id != node.id
        assert clone_node.id == node.id
        assert clone_node.active == node.active
        assert clone_node.operation == node.operation
        assert clone_node.inputs == node.inputs

def main():
    test_get_node_value()
    test_graph_construction()
    test_clone()

    print("If this message appears, there are no errors!! \o/")

if __name__ == "__main__":
    main()