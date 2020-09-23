

# add all necessary code to the path
import os
import sys

PYTHON_PATH_ADDS = ['backend', 'data_collect', 'gui']


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
    from gui import run_ipview
    run_ipview.run()

