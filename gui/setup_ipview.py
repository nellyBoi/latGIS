"""
Script to run prior to unit-testing to setup environment
"""
import os
import sys

PYTHON_PATH_ADDS = ['image_containers', 'ip_view_ui']


########################################################################################################################
def setup() -> None:
    file_path = os.path.dirname(os.path.realpath(__file__))

    for folder in PYTHON_PATH_ADDS:
        full_path = os.path.join(file_path, folder)
        sub_paths = os.walk(full_path)
        for subPath in sub_paths:

            if 'pycache' not in subPath:
                sys.path.extend(subPath)


########################################################################################################################
if __name__ == '__main__':
    setup()
