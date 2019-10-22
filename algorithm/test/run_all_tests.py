"""

"""
import os
import unittest
import test_setup

TEST_SUB_DIRS = ['.']#['util', 'latgis']
########################################################################################################################
class UnitTestLauncher(object):
    """
    A class to run all unittests within the test framework.
    """
    def run_tests(self):

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
    test_setup.setup()
    testRunner = UnitTestLauncher()
    testRunner.run_tests()
