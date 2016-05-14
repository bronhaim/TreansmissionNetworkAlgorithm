# This module implements probability distribution algorithm

import numpy


def distribute(nodes, indx, m, prob_table, likelihood):
    f = None
    if m == []:
        f = nodes[indx].psi
    else:
        f = numpy.multiply(nodes[indx].psi, m)

    if not nodes[indx].is_leaf():
        print "Marginal conditional distribution of node", indx, ":"
        print f / likelihood

    for neighbor in nodes[indx].neighbors:
        bit_was_changed = prob_table[indx - 1][neighbor - 1]
        bit_stayed = 1 - prob_table[indx - 1][neighbor - 1]
        psi_edge = ([[bit_stayed, bit_was_changed],
                     [bit_was_changed, bit_stayed]])
        m = psi_edge * numpy.divide(f, nodes[neighbor].collected_m[indx])
        distribute(nodes, neighbor, m, prob_table, likelihood)


def distribute_max(nodes, indx, assignment):
    if not nodes[indx].is_leaf():
        print "x%d = %.0f" % (indx, assignment)

    for neighbor in nodes[indx].neighbors:
        neighbor_assignment = nodes[neighbor].max_assignments[indx][assignment][1]
        distribute_max(nodes, neighbor, neighbor_assignment)