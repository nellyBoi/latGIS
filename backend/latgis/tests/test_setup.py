"""
Script to run prior to unit-testing to setup environment
"""
import sys
import os

import pathlib
filepath = pathlib.Path(__file__).parent.absolute()

ROOT = os.path.join(filepath, '..', '..')
PYTHONPATH_ADDS = [os.path.join(ROOT, 'latgis')]  # add sub-directories as unit tests appear in them


########################################################################################################################
def setup() -> None:

    for path in PYTHONPATH_ADDS:

        subPaths = os.walk(path)
        for subPath in subPaths:

            if 'pycache' not in subPath and 'test' not in subPath:
                sys.path.extend(subPath)


########################################################################################################################
if __name__ == '__main__':
    setup()
