#!/usr/bin/env python3
"""
Nelly Kane
"""
import unittest
import pathlib
filepath = pathlib.Path(__file__).parent.absolute()

import os
import sys

sys.path.append(os.path.join(filepath, '..'))
from test_setup import setup
setup()

from util.enu_to_ecef import MoreTransfers
'''
enu2ecef(e1: float, n1: float, u1: float,
             lat0: float, lon0: float, h0: float,
             deg: bool = True) -> Tuple[float, float, float]:
'''
EARTH_RADIUS_M = 6378137.0


########################################################################################################################
class Test_enu_to_ecef(unittest.TestCase):

    ####################################################################################################################
    def test_prime_meridian(self):
        e0 = 0
        n0 = 0
        u0 = 0
        lat0 = 0
        lon0 = 0
        h0 = 0
        deg0 = True

        xECEF, yECEF, zECEF = MoreTransfers.enu2ecef(e0, n0, u0, lat0, lon0, h0, deg0)

        self.assertAlmostEqual(xECEF, EARTH_RADIUS_M, 3)
        self.assertAlmostEqual(yECEF, 0, 3)
        self.assertAlmostEqual(zECEF, 0, 3)


########################################################################################################################
if __name__ == '__main__':
    unittest.main()