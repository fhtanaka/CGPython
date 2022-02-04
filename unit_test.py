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
Population.rng = np.random.RandomState(seed)
Population.add_operation(arity=1, func=constant, string="x")
Population.add_operation(arity=1, func=increment, string="x+1")
Population.add_operation(arity=1, func=invert, string="-x")
Population.add_operation(arity=2, func=addition, string="x+y")
Population.add_operation(arity=2, func=multiplication, string="x*y")
Population.add_operation(arity=2, func=subtraction, string="x-y")
Population.add_operation(arity=2, func=protected_div, string="*x/y")

def test_get_node_value():
    g = Graph(
        n_in=3,
        n_out=5,
        n_middle=0,
        available_operations=Population.operations,
        initialize=False,
        rng=Population.rng)

    _ = g._add_node(0, 5)
    _ = g._add_node(1, 10)
    _ = g._add_node(2, 0)

    addition_node = g._add_node(3, operation=3/7)
    g.nodes[addition_node].inputs = [0/3, 1/3]

    multiplication_node = g._add_node(4, operation=4/7)
    g.nodes[multiplication_node].inputs = [0/4, 1/4]
    
    p_div_node = g._add_node(5, operation=6/7)
    g.nodes[p_div_node].inputs = [0/5, 2/5]
    
    subtraction_node = g._add_node(6, operation=5/7)
    g.nodes[subtraction_node].inputs = [5/6, 3/6]

    aux_node = g._add_node(7, operation=4/7)
    g.nodes[aux_node].inputs = [6/7, 4/7]

    assert g.get_node_value(addition_node) == 15
    g.reset_graph_value()

    assert g.get_node_value(multiplication_node) == 50
    g.reset_graph_value()

    assert g.get_node_value(p_div_node) == 1
    g.reset_graph_value()

    assert g.get_node_value(aux_node) == -700

def test_graph_construction():
    ## set up ##

    indv = Graph(
        n_in = 5,
        n_out = 4,
        n_middle = 9,
        available_operations = Population.operations,
        rng=Population.rng)

    inputs = [4, 2, -5 , 1 ,0]
    result = indv.operate(inputs)

    assert result[0] == -4
    assert result[1] == -10
    assert result[2] == 2
    assert result[3] == -5

def test_clone():
    g = Graph(
        n_in=3,
        n_out=3,
        n_middle=9,
        available_operations=Population.operations,
        rng=Population.rng)
    clone = g.clone_graph()
    for n in g.nodes:
        clone_node = clone.nodes[n.id]
        assert clone_node.global_id != n.global_id
        assert clone_node.id == n.id
        assert clone_node.active == n.active
        assert clone_node.operation == n.operation
        assert clone_node.inputs == n.inputs

def test_draw():
    g = Graph(
        n_in = 3,
        n_out = 3,
        n_middle = 9,
        available_operations = Population.operations, 
        rng=Population.rng)
    g.draw_graph()

def main():
    test_get_node_value()
    test_graph_construction()
    test_clone()
    # test_draw()
    print("If this message appears, there are no errors!! \o/")

if __name__ == "__main__":
    main()