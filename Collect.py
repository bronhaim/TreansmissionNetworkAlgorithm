# This module implements probability collect algorithm

import numpy


def collect(nodes, indx, prob_table):
    if nodes[indx].degree == 0:
        nodes[indx].psi = nodes[indx].get_configuration()
    else:
        for neighbor in nodes[indx].neighbors:
            m = collect(nodes, neighbor, prob_table)
            nodes[indx].psi = numpy.multiply(nodes[indx].psi, m)
        if nodes[indx].is_leaf():
            nodes[indx].psi = numpy.multiply(nodes[indx].psi, nodes[indx].get_configuration())

    if nodes[indx].is_root:
        return nodes[indx].psi
    else:
        bit_was_changed = prob_table[indx - 1][nodes[indx].parent - 1]
        bit_stayed = 1- prob_table[indx - 1][nodes[indx].parent - 1]
        psi_edge = ([[bit_stayed, bit_was_changed],
                     [bit_was_changed, bit_stayed]])
        # save collected matrix as part of node info
        ret = nodes[indx].collected_m[nodes[indx].parent] = psi_edge * nodes[indx].psi
        return ret


def collect_max(nodes, indx, prob_table):
    if nodes[indx].degree == 0:
        nodes[indx].psi = nodes[indx].get_configuration()
    else:
        for neighbor in nodes[indx].neighbors:
            m = collect_max(nodes, neighbor, prob_table)
            nodes[indx].psi = numpy.multiply(nodes[indx].psi, m)

        # in case the node is a leaf, that is observed
        if nodes[indx].is_leaf():
            nodes[indx].psi = numpy.multiply(nodes[indx].psi,
                                             nodes[indx].get_configuration())

    if nodes[indx].is_root:
        return nodes[indx].psi
    else:
        bit_was_changed = prob_table[indx - 1][nodes[indx].parent - 1]
        bit_stayed = 1 - prob_table[indx - 1][nodes[indx].parent - 1]
        psi_edge = ([[bit_stayed, bit_was_changed],
                     [bit_was_changed, bit_stayed]])
        item_00 = (psi_edge[0][0] * nodes[indx].psi[0]).item()
        item_01 = (psi_edge[0][1] * nodes[indx].psi[1]).item()
        item_10 = (psi_edge[1][0] * nodes[indx].psi[0]).item()
        item_11 = (psi_edge[1][1] * nodes[indx].psi[1]).item()

        nodes[indx].max_assignments[nodes[indx].parent] = [[max(item_00, item_01), numpy.argmax([item_00, item_01])],
                                                           [max(item_10, item_11), numpy.argmax([item_10, item_11])]]
        return numpy.matrix([[nodes[indx].max_assignments[nodes[indx].parent][0][0]],
                             [nodes[indx].max_assignments[nodes[indx].parent][1][0]]])