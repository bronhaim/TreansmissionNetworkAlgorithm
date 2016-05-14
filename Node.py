#  this module represent node interface

import numpy


class Node(object):

    def __init__(self, index, neighbors):
        self._index = index
        self._neighbors = neighbors
        self._degree = len(neighbors)

        self._value = 0
        self._parent = 0
        self._is_root = False

        self._psi = numpy.ones((2, 1))
        self.collected_m = {}

        self._max_assignments = {}

    @property
    def max_assignments(self):
        return self._max_assignments

    @property
    def psi(self):
        return self._psi

    @psi.setter
    def psi(self, value):
        self._psi = value

    @property
    def degree(self):
        return self._degree

    @property
    def index(self):
        return self._index

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, value):
        self._parent = value

    @property
    def neighbors(self):
        return self._neighbors

    def get_configuration(self):
        if self.value == 0:
            return numpy.matrix([[1], [0]])
        else:
            return numpy.matrix([[0], [1]])

    def is_leaf(self):
        if self.index in (9, 10, 4, 3, 6, 7):
            return True
        else:
            return False

    @property
    def is_root(self):
        return self._is_root

    @is_root.setter
    def is_root(self, value):
        self._is_root = value