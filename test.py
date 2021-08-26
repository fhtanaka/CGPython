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

def test_get_node_value():
    g = Graph(0, 0, 0 ,0 , 0)

    five_node = g._add_node(5, terminal=True)
    ten_node = g._add_node(10, terminal=True)
    zero_node = g._add_node(0, terminal=True)

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
    seed = 2002

    Graph.rng = np.random.RandomState(seed)
    Graph.add_operation(arity=1, func=lambda x: x+1,   string="x+1")
    Graph.add_operation(arity=2, func=lambda x,y: x+y, string="x+y")
    Graph.add_operation(arity=1, func=lambda x: -x,    string="-x")

    indv = Graph(5, 4, 3, 3, 2)

    indv.make_connections(True)

    inputs = [5, 0, -5 ,3 ,0]
    result = indv.operate(inputs)

    assert result[0] == 4
    assert result[1] == 10
    assert result[2] == 10
    assert result[3] == -2

def main():
    test_get_node_value()
    test_graph_construction()
    print("If this message appears, there are no errors!! \o/")

if __name__ == "__main__":
    main()