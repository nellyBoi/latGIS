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

import track
from location import CameraData
from location import ItemLocation
from util.coord_transfers import CoordTransfers
from util.constants import Constants
CT = CoordTransfers()

# tests pass function
tol = 1e-6


def test(name: str, passed: bool):
    print('Function: ' + name)
    if passed:
        print('PASSED')
    else:
        print('FAILED')
        
HALF_ROW = Constants.SENSOR_SIZE[0] / 2
HALF_COL = Constants.SENSOR_SIZE[1] / 2

trackerObj = track.TargetTracker(gateSize = 5, distToDVec = 5)

LatLonEl0 = [0, 0, 10]
metersTraveled = [0, 10, 0]

# DATA 0 ==============================
heading0 = 0
pitch0 = 0
obs0 = [[HALF_ROW, HALF_COL], [HALF_ROW / 2, HALF_COL / 2]]

# DATA 1 ==============================
heading1 = 0
pitch1 = 0
obs1 = [[HALF_ROW, HALF_COL]]

# DATA 2 ==============================
heading2 = 0
pitch2 = 0
obs2 = [[HALF_ROW, HALF_COL]]

pixel0 = [512, 512]
pixel1 = [512, 490]
pixel2 = [512, 475]
# ---------------------------------------------------------------------------------
ECEF0 = CT.LLE_to_ECEF(LatLonEl0)

# first frame ob observations
camData0 = CameraData(LatLonEl0, heading0, pitch0)
trackerObj.add_frame_observations(observations = obs0, curCameraData = camData0)

# second frame of observations 
ECEF1 = [ECEF0[0] + metersTraveled[0], ECEF0[1] + metersTraveled[1], ECEF0[2] + metersTraveled[2]]
LatLonEl1 = CT.ECEF_to_LLE(ECEF1)
camData1 = CameraData(LatLonEl1, heading1, pitch1)
trackerObj.add_frame_observations(observations = obs1, curCameraData = camData1)

# third frame of observations
ECEF2 = [ECEF1[0] + metersTraveled[0], ECEF1[1] + metersTraveled[1], ECEF1[2] + metersTraveled[2]]
LatLonEl2 = CT.ECEF_to_LLE(ECEF2)
camData2 = CameraData(LatLonEl2, heading2, pitch2)
trackerObj.add_frame_observations(observations = obs2, curCameraData = camData2)

print('CURRENT TRACKS')
trackerObj.print_current_track_results()

print('FINAL TRACKS')
trackerObj.print_final_track_results()