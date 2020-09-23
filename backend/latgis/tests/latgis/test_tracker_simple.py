"""
Nelly Kane
"""
import pathlib
filepath = pathlib.Path(__file__).parent.absolute()

import os
import sys

sys.path.append(os.path.join(filepath, '..'))
from test_setup import setup
setup()
from track import TargetTracker
import numpy as np

sys.path.append(os.path.join(sys.path[0],'..','..','Src','Tracking'))
sys.path.append(os.path.join(sys.path[0],'..','..','Src','Utilities'))

# tests pass function
tol = 1e-6
def test(name: str, passed: bool):
    print('Function: ' + name)
    if (passed == True):
        print('PASSED')
    else:
        print('FAILED')

trackerObj = TargetTracker(gateSize = 5, distToDVec = 5)
#==============================================================================
# tests full overlap
overlapPred = trackerObj.gate(prediction = [5,5], observation = [5, 5])
test('Overlap', (np.abs(overlapPred - np.pi*5**2) < tol))

#==============================================================================
# tests that at least result is reasonable, TODO: Legit unit tests here.
overlapPred = trackerObj.gate(prediction = [5,5], observation = [3, 5])
test('Partial Overlap', (overlapPred < np.pi*5**2) and (overlapPred > 0 ))

#==============================================================================
# tests zero
overlapPred = trackerObj.gate(prediction = [5,5], observation = [35, 5])
test('Zero Overlap', (overlapPred == 0 ))
#==============================================================================

# cost matrix stuff
obs = [[90, 5], [50, 92], [50, 50], [5, 90]]
trks = [[5, 5], [50, 50], [50, 90]]
costMat = trackerObj.build_cost_matrix(observations = obs, predictions = trks, printMatrix = True)

