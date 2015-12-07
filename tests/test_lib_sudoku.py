'''
created: 2015-12-07 -- 20 CEST
author: tc
'''
from builtins import object

import sys
sys.path.append('..')

from lib_sudoku import Sudoku


class test_lib_sudoku(object):

    def test_init(self):
        input_file = 'almost_complete_puzzle.dat'
        S = Sudoku(input_file, seed=1)
