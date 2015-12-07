#!/usr/bin/python

'''
program: lib_sudoku.py
author: tc
created: 2015-12-06 -- 20

Energy is defined as .. #FIXME

'''
from __future__ import print_function
from builtins import range
from builtins import object


import sys
import numpy
import random
import math


class Sudoku(object):

    def __init__(self, input_file, seed=0):
        '''
        args... #FIXME
        '''

        print('[]')

        # set random seed
        if seed == 0:
            seed = random.randrange(99999999)
        random.seed(seed)
        print('[sudoku] random seed: %i' % seed)

        # initialize and fill puzzle
        self._load_puzzle(input_file)
        self._fill_puzzle()
        assert self.puzzle.min() >= 1
        assert self.puzzle.max() <= 9

        # other utils
        self.beta = 1.0e4
        self.energy = self._compute_energy()

    def _load_puzzle(self, filename):
        ''' Reads puzzle from file
        '''
        x = numpy.loadtxt(filename, dtype=numpy.int)
        assert x.shape == (9, 9)
        assert x.max() <= 9
        assert x.min() >= 0
        self.puzzle = x[:, :]
        number_clues = (x > 0).sum()
        print('[sudoku] read puzzle from %s (%i clues)' % (filename,
                                                           number_clues))

    def _fill_puzzle(self):
        ''' Replaces zeros with random numbers.
        '''
        tot = list(range(1, 10)) * 9
        for n in self.puzzle[numpy.nonzero(self.puzzle)].flatten():
            tot.pop(tot.index(n))
        self.non_clues = []
        for i in range(9):
            for j in range(9):
                if not self.puzzle[i, j]:
                    self.non_clues.append([i, j])
                    self.puzzle[i, j] = tot.pop(random.randrange(len(tot)))
        assert tot == []
        assert self.puzzle.min() > 0

    def _get_box(self, i, j):
        return self.puzzle[(i // 3) * 3:(i // 3 + 1) * 3,
                           (j // 3) * 3:(j // 3 + 1) * 3]

    def _compute_energy(self):
        E = 0
        list_i = list(range(9))
        list_j = [0, 3, 6, 1, 4, 7, 2, 5, 8]
        for ind in range(9):
            E += self._local_energy(list_i[ind], list_j[ind])
        return E

    def _local_energy(self, i, j):
        E = 0
        # check row
        row = self.puzzle[i, :]
        occ = numpy.bincount(row)
        occ = occ[occ > 1]
        E += sum(occ)
        # check column
        col = self.puzzle[:, j]
        occ = numpy.bincount(col)
        occ = occ[occ > 1]
        # check box
        E += sum(occ)
        box = self._get_box(i, j).flatten()
        occ = numpy.bincount(box)
        occ = occ[occ > 1]
        E += sum(occ)
        return E

    # methods to be called from outside

    def set_beta(self, beta):
        self.beta = beta

    def MC_move(self):
        i, j = random.choice(self.non_clues)
        E_ij_old = self._local_energy(i, j)
        n_old = self.puzzle[i, j]
        self.puzzle[i, j] = random.randrange(1, 10)
        E_ij_new = self._local_energy(i, j)
        dE = E_ij_new - E_ij_old
        if dE < 0.0 or random.uniform(0.0, 1.0) < math.exp(- self.beta * dE):
            self.energy += dE
            return
        else:
            self.puzzle[i, j] = n_old

    def print_puzzle(self):
        for i in range(9):
            for j in range(9):
                print(self.puzzle[i, j], end=' ')
            print()


if __name__ == '__main__':
    args = {'init': 'read', 'input_file': 'puzzle.dat'}
    S = Sudoku(args)
    S.print_puzzle()
    print(S.energy)
