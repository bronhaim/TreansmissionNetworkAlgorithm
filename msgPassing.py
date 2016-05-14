#!/bin/python

import numpy
from Node import Node
from Collect import collect, collect_max
from Distribute import distribute, distribute_max


def get_probabilities_table():
    table = numpy.zeros((10, 10))
    # index 0 == node.index 1
    # table [0] [1] describes the edge between node index 1 to node index 2

    table[0][1] = 0.1
    table[0][4] = 0.1
    table[0][7] = 0.1

    table[1][2] = 0.1
    table[1][3] = 0.2

    table[4][5] = 0.1
    table[4][6] = 0.4

    table[7][8] = 0.5
    table[7][9] = 0.3

    table = table + table.T - numpy.diag(table.diagonal())
    return table


def set_leaves_values(setting, nodes):
    if setting == 1:
        nodes[3].value = 0
        nodes[4].value = 1
        nodes[6].value = 1
        nodes[7].value = 0
        nodes[9].value = 0
        nodes[10].value = 1
    elif setting == 2:
        nodes[3].value = 0
        nodes[4].value = 0
        nodes[6].value = 1
        nodes[7].value = 0
        nodes[9].value = 0
        nodes[10].value = 1
    elif setting == 3:
        nodes[3].value = 1
        nodes[4].value = 1
        nodes[6].value = 1
        nodes[7].value = 1
        nodes[9].value = 1
        nodes[10].value = 1


def get_init_nodes():
    nodes = {}
    nodes[1] = Node(1, [2, 5, 8])
    nodes[2] = Node(2, [1, 4, 3])
    nodes[3] = Node(3, [2,])
    nodes[4] = Node(4, [2,])
    nodes[5] = Node(5, [1, 6, 7])
    nodes[6] = Node(6, [5,])
    nodes[7] = Node(7, [5,])
    nodes[8] = Node(8, [1, 9, 10])
    nodes[9] = Node(9, [8,])
    nodes[10] = Node(10, [8,])
    return nodes


def calc_nodes_parents(nodes, root):
    for idx in nodes[root].neighbors:
        nodes[idx].neighbors.remove(root)
        nodes[idx].parent = root
        calc_nodes_parents(nodes, idx)
    return nodes


def init_setting(setting, root):
    nodes = get_init_nodes()
    set_leaves_values(setting, nodes)
    nodes[root].is_root = True
    return calc_nodes_parents(nodes, root)


def calculate_conditionals(setting):
    ###############
    # calculating data likelihood by running collect from source node 4
    root = 4
    nodes = init_setting(setting, root)
    likelihood = collect(nodes, root, get_probabilities_table())
    if nodes[root].get_configuration()[0].A1[0] == 1:
        likelihood = likelihood[0].A1[0]
    else:
        likelihood = likelihood[1].A1[0]
    print "likelihood for setting %s: %s when starting from source node 4" % (setting, likelihood)

    # calculating data likelihood by running collect from source node 10
    root = 10
    nodes = init_setting(setting, root)
    likelihood = collect(nodes, root, get_probabilities_table())
    if nodes[root].get_configuration()[0].A1[0] == 1:
        likelihood = likelihood[0].A1[0]
    else:
        likelihood = likelihood[1].A1[0]
    print "likelihood for setting %s: %s when starting from source node 10" % (setting, likelihood)

    ###############
    # Initialization - Setting 1. Source Node = 1
    print "With the likelihood above the following are the results of the conditionals P(xi = {1,0}|setting %d)" % \
          (setting)
    print "[[v=0\nv=1]]"
    print "---Source node is 1---"
    root = 1
    nodes = init_setting(setting, root)
    collect(nodes, root, get_probabilities_table())
    distribute(nodes, root, [], get_probabilities_table(), likelihood)

    ###############
    # Initialization - Setting 1. Source Node = 2
    print "---Source node is 2---"
    root = 2
    nodes = init_setting(setting, root)
    collect(nodes, root, get_probabilities_table())
    distribute(nodes, root, [], get_probabilities_table(), likelihood)

    ###############
    # Initialization - Setting 1. Source Node = 6
    print "---Source node is 6---"
    root = 6
    nodes = init_setting(setting, root)
    collect(nodes, root, get_probabilities_table())
    distribute(nodes, root, [], get_probabilities_table(), likelihood)


def calculate_assignment(setting):
    print "Most probable assignment with setting: ", setting
    ###############
    # Initialization - Setting 1. Source Node = 1
    root = 1
    nodes = init_setting(setting, root)
    max_probability = collect_max(nodes, root, get_probabilities_table())
    root_max = max(max_probability)
    root_argmax = numpy.argmax(max_probability)
    print "The highest probability is: ", root_max
    print "For the following assignments: "
    distribute_max(nodes, root, root_argmax)

    ###############
    # Initialization - Setting 1. Source Node = 2
    root = 2
    nodes = init_setting(setting, root)
    max_probability = collect_max(nodes, root, get_probabilities_table())
    root_max = max(max_probability)
    root_argmax = numpy.argmax(max_probability)
    print "The highest probability is: ", root_max
    print "For the following assignments: "
    distribute_max(nodes, root, root_argmax)

    ###############
    # Initialization - Setting 1. Source Node = 6
    root = 6
    nodes = init_setting(setting, root)
    max_probability = collect_max(nodes, root, get_probabilities_table())
    root_max = max(max_probability)
    root_argmax = numpy.argmax(max_probability)
    print "The highest probability is: ", root_max
    print "For the following assignments: "
    distribute_max(nodes, root, root_argmax)

if __name__ == '__main__':
    calculate_conditionals(1)
    calculate_conditionals(2)
    calculate_conditionals(3)

    calculate_assignment(1)
    calculate_assignment(2)
    calculate_assignment(3)