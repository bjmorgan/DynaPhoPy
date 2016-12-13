#!/usr/bin/env python

import numpy as np
import dynaphopy.interface.iofile as io
import dynaphopy
from phonopy.file_IO import parse_FORCE_CONSTANTS

import unittest

class TestDynaphopy(unittest.TestCase):

    def setUp(self):
        structure = io.read_from_file_structure_poscar('GaN_data/POSCAR')
        structure.set_force_constants(parse_FORCE_CONSTANTS(filename='GaN_data/FORCE_CONSTANTS'))

        structure.set_primitive_matrix([[1.0, 0.0, 0.0],
                                        [0.0, 1.0, 0.0],
                                        [0.0, 0.0, 1.0]])
        structure.set_supercell_phonon([[3, 0, 0],
                                        [0, 3, 0],
                                        [0, 0, 3]])

        trajectory = io.generate_test_trajectory(structure, supercell=[3, 3, 3], total_time=6, silent=False)
        self.calculation = dynaphopy.Quasiparticle(trajectory)

    def test_force_constants_self_consistency(self):
        self.calculation.select_power_spectra_algorithm(2)
        renormalized_force_constants = self.calculation.get_renormalized_force_constants()
        harmonic_force_constants = self.calculation.dynamic.structure.get_force_constants()
        self.assertEqual(np.allclose(renormalized_force_constants, harmonic_force_constants, rtol=1, atol=1.e-2), True)

if __name__ == '__main__':
    unittest.main()