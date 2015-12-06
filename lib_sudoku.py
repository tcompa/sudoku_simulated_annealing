#!/usr/bin/python

'''
program: lib_sudoku.py
author: tc
created: 2015-12-06 -- 20

Energy is defined as .. #FIXME

'''


import sys
import numpy
import random
import math


class Sudoku():

    def __init__(self, args):
        '''
        args... #FIXME
        '''

        # random seed
        if 'random_seed' in args.keys():
            seed = args['random_seed']
        else:
            seed = random.randrange(99999999)
        random.seed(seed)
        print '[sudoku] random seed: %i' % seed

        # initialize and fill puzzle
        if args['init'] == 'random':
            number_clues = args['number_clues']
            self._generate_puzzle(number_clues)
        elif args['init'] == 'read':
            self._load_puzzle(args['input_file'])
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
        print '[sudoku] read puzzle from %s (%i clues)' % (filename,
                                                           number_clues)

    def _generate_puzzle(self, number_clues, max_trials=10 ** 4):
        print '[sudoku] start generating puzzle (%i clues)' % number_clues
        self.puzzle = numpy.zeros((9, 9), dtype=numpy.int)
        trials = 0
        while (self.puzzle > 0).sum() < number_clues:
            trials += 1
            i = random.randrange(9)
            j = random.randrange(9)
            if self.puzzle[i, j]:
                continue
            n = random.randrange(1, 10)
            if n in self.puzzle[i, :]:
                continue
            if n in self.puzzle[:, j]:
                continue
            if n in self._get_box(i, j):
                continue
            self.puzzle[i, j] = n
            # check number of trials
            if trials > max_trials:
                sys.exit('[sudoku] ERROR: could not generate puzzle with ' +
                         '%i clues' % number_clues)
        print '[sudoku] generated puzzle (%i clues)' % number_clues

    def _fill_puzzle(self):
        ''' Replaces zeros with random numbers.
        '''
        tot = range(1, 10) * 9
        for n in self.puzzle[numpy.nonzero(self.puzzle)].flatten():
            tot.pop(tot.index(n))
        self.non_clues = []
        for i in xrange(9):
            for j in xrange(9):
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
        list_i = range(9)
        list_j = [0, 3, 6, 1, 4, 7, 2, 5, 8]
        for ind in xrange(9):
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

    def print_puzzle(self, Fancy=True):
        if Fancy:
            print 29 * '-'
        for i in xrange(9):
            for j in xrange(9):
                print self.puzzle[i, j],
                if (j + 1) % 3 == 0 and Fancy:
                    print '|',
                else:
                    print '',
            print
            if (i + 1) % 3 == 0 and Fancy:
                print 29 * '-'


if __name__ == '__main__':
    args = {'init': 'read', 'input_file': 'puzzle.dat'}
    S = Sudoku(args)
    S.print_puzzle()
    print S.energy
