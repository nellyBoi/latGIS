"""
Nelly Kane
10.21.2019

run_all_tests.py

Unit test framework to run all tests associated with latgis. To run additional tests, file must be pre-pended with
'test_' and contain tests in a unittest.TestCase derived object.

TODO:
    - finish unit tests
    - pass data print boolean
"""
import os
import unittest

from test_setup import setup

TEST_SUB_DIRS = ['.']#['util', 'latgis']
########################################################################################################################
class UnitTestLauncher(object):
    """
    A class to run all unittests within the test framework.
    """

    ####################################################################################################################
    def run_tests(self):
        """
        run unit tests
        """

        lsPaths = []

        # Find all relevant subdirectories that contain unit tests
        for path, subdirs, files in os.walk('.'):
            if "pycache" not in path:
                lsPaths.append(path)

        # loop through subdirectories and run individually
        for path in lsPaths:
            loader = unittest.TestLoader()
            suite = unittest.TestSuite()
            suite = loader.discover(path)
            unittest.TextTestRunner().run(suite)


########################################################################################################################
if __name__ == '__main__':
    setup()
    testRunner = UnitTestLauncher()
    testRunner.run_tests()
