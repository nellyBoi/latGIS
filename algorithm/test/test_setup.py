"""
Script to run prior to unit-testing to setup environment
"""
import sys
import os
ROOT = 'C:\\Nelly\\latGIS\\latGIS'
PYTHONPATH_ADDS = [os.path.join(ROOT, 'algorithm') ]

def setup() -> None:

    for path in PYTHONPATH_ADDS:

        subPaths = os.walk(path)
        for subPath in subPaths:

            if 'pycache' not in subPath:
                sys.path.extend(subPath)


if __name__ == '__main__':
    setup()