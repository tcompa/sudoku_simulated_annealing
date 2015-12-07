#!/usr/bin/python

from __future__ import print_function
from builtins import range

from lib_simulated_annealing import simulated_annealing
from lib_sudoku import Sudoku
import matplotlib.pyplot as plt

S = Sudoku('puzzle.dat')

cooling_rate = 2e-2
beta_min = 0.25
beta_max = 1e2
S, E, e_time = simulated_annealing(S,
                                   beta_min=beta_min, beta_max=beta_max,
                                   cooling_rate=cooling_rate,
                                   n_steps_per_T=1000, E_min=0)
S.print_puzzle()

plt.title('cooling_rate=%g' % cooling_rate)
plt.xlabel('step', fontsize=18)
plt.ylabel('energy', fontsize=18)
plt.plot(E)
plt.ylim(bottom=0)
plt.savefig('fig.pdf', bbox_inches='tight')
plt.show()
