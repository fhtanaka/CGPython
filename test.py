from graph import Graph

def addition(x ,y):
    return x+y
def multiplication(x ,y):
    return x*y
def protected_division(x ,y):
    if y == 0:
        return 1
    return x/y
def subtraction(x ,y):
    return x-y
def constant(x):
    def f():
        return x
    return f

def test_get_node_value():
    g = Graph()

    five_node = g._add_node(5, terminal=True)
    ten_node = g._add_node(operation=constant(10))
    zero_node = g._add_node(0, terminal=True)

    addition_node = g._add_node(operation=addition)
    g.nodes[addition_node].inputs = [five_node, ten_node]
    assert g.get_node_value(addition_node) == 15
    g.reset_graph_value()

    multiplication_node = g._add_node(operation=multiplication)
    g.nodes[multiplication_node].inputs = [five_node, ten_node]
    assert g.get_node_value(multiplication_node) == 50
    g.reset_graph_value()

    p_div_node = g._add_node(operation=protected_division)
    g.nodes[p_div_node].inputs = [five_node, zero_node]
    assert g.get_node_value(p_div_node) == 1
    g.reset_graph_value()

    subtraction_node = g._add_node(operation=subtraction)
    g.nodes[subtraction_node].inputs = [p_div_node, addition_node]
    aux_node = g._add_node(operation=multiplication)
    g.nodes[aux_node].inputs = [subtraction_node, multiplication_node]
    assert g.get_node_value(aux_node) == -700



def main():
    test_get_node_value()
    print("If this message appears, there is on errors!! \o/")

if __name__ == "__main__":
    main()