import unittest
import numpy as np
import sys
import os

# Add core to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'core')))
import field_dynamics

class TestRCFTOperators(unittest.TestCase):

    def setUp(self):
        self.psi_t = np.array([0.1, 0.4, 0.5, 0.7])
        self.psi_prev = np.array([0.1, 0.3, 0.45, 0.6])
        self.psi_history = [self.psi_prev, self.psi_t]
        self.weights = [1.0, 1.0]
        self.neighbor_map = {
            0: [1],
            1: [0, 2],
            2: [1, 3],
            3: [2]
        }

    def test_delta_psi(self):
        result = field_dynamics.delta_psi(self.psi_t[1], self.psi_prev[1])
        self.assertAlmostEqual(result, 0.1)

    def test_fidelity(self):
        result = field_dynamics.fidelity(self.psi_t[1], self.psi_prev[1])
        self.assertAlmostEqual(result, 0.9)

    def test_entropy(self):
        dpsi = field_dynamics.delta_psi(self.psi_t[2], self.psi_prev[2])
        result = field_dynamics.entropy(self.psi_t[2], self.psi_prev[2])
        self.assertAlmostEqual(result, np.log(1 + 2 * dpsi))

    def test_reentry_delay(self):
        result = field_dynamics.reentry_delay(self.psi_history, 1)
        self.assertTrue(np.isinf(result) or isinstance(result, int))

    def test_collapse_integrity(self):
        f = 0.8
        s = 0.5
        dpsi = 0.2
        result = field_dynamics.collapse_integrity(f, s, dpsi)
        self.assertTrue(0 <= result <= 1)

    def test_collapse_curvature(self):
        psi_field = self.psi_t
        result = field_dynamics.collapse_curvature(psi_field, 2, self.neighbor_map[2], self.weights)
        self.assertTrue(result >= 0)

    def test_survival_probability(self):
        ic = 0.7
        curvature = 0.3
        result = field_dynamics.survival_probability(ic, curvature)
        self.assertAlmostEqual(result, ic / (ic + curvature))

    def test_collapse_index(self):
        s = 0.5
        dpsi = 0.1
        f = 0.8
        result = field_dynamics.collapse_index(s, dpsi, f)
        self.assertAlmostEqual(result, s * dpsi * (1 - f))

    def test_is_alive(self):
        self.assertTrue(field_dynamics.is_alive(0.1, 0.9, 0.2))
        self.assertFalse(field_dynamics.is_alive(0.3, 0.1, 4.0))

if __name__ == '__main__':
    unittest.main()
