#!/usr/bin/python

'''
program: lib_simulated_annealing.py
author: tc
created: 20-12-06 -- 21 CEST
'''

import time


def simulated_annealing(problem, beta_min=1e-2, beta_max=1e2,
                        cooling_rate=1e-2,
                        n_steps_per_T=2500, E_min=-float('inf')):
    '''
    Simple general-purpose simulated-annealing optimization function.
    Input:
      *problem*       : object with methods:
                            self.set_beta()
                            self.MC_move()
                        and members
                            self.energy
                            self.beta
      *beta_min*      : minimum inverse temperature
      *beta_max*      : maximum inverse temperature
      *cooling_rate*  : cooling rate
      *n_steps_per_T* : number of MC moves before the temperature is decreased
      *E_min*         : the global energy minimum (if known)

    Output:

      *problem*       : updated version
      *E*             : list of the final energies for each temperatures
      *elapsed_time*  : time it took, in seconds
    '''

    time_start = time.clock()
    print '[sa] start'
    problem.set_beta(beta_min)
    E = []
    while problem.beta < beta_max:
        # TODO: add a message after a while
        print '[sa] beta = %g\tE = %g' % (problem.beta, problem.energy)
        for step in xrange(n_steps_per_T):
            problem.MC_move()
        E.append(problem.energy)
        if problem.energy <= E_min:
            print '[sa] reached E=%g' % problem.energy
            break
        problem.set_beta(problem.beta * (1.0 + cooling_rate))
    print '[sa] end'
    elapsed_time = time.clock() - time_start
    print '[sa] elapsed: %.2f s' % elapsed_time
    return problem, E, elapsed_time


if __name__ == '__main__':

    import random
    import math
    import matplotlib.pyplot as plt

    class Potential_1d():
        '''
        Naive class, to test the simulated-annealing function.
        '''

        def __init__(self):
            self.x = 10.0
            self.beta = 100000.0
            self.dx = 0.2
            self.energy = self._compute_energy(self.x)

        def set_beta(self, beta):
            self.beta = beta

        def MC_move(self):
            xnew = random.uniform(self.x - self.dx, self.x + self.dx)
            E_old = self.energy
            E_new = self._compute_energy(xnew)
            dE = E_new - E_old
            if dE < 0.0 or random.random() < math.exp(- self.beta * dE):
                self.x = xnew
                self.energy = E_new

        def _compute_energy(self, pos):
            return 0.5 * pos ** 2

    problem = Potential_1d()
    problem, E, e_time = simulated_annealing(problem, cooling_rate=0.02,
                                             beta_min=1e-2, beta_max=5e2)
    print problem.x, problem.energy
    plt.xlabel('step', fontsize=18)
    plt.ylabel('energy', fontsize=18)
    plt.plot(range(len(E)), E)
    plt.ylim(bottom=0.0)
    plt.show()
