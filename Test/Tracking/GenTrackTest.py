# -*- coding: utf-8 -*-
import sys, os
#import numpy as np

sys.path.append(os.path.join(sys.path[0],'..','..','Src','Tracking'))
sys.path.append(os.path.join(sys.path[0],'..','..','Src','Utilities'))

from track import TargetTracker
from lat_gis import CameraData, ObjectLocation
from coord_transfers import CoordTransfers
from constants import Constants
CT = CoordTransfers()

# test pass function
tol = 1e-6
def test(name: str, passed: bool):
    print('Function: ' + name)
    if (passed == True):
        print('PASSED')
    else:
        print('FAILED')
        
HALF_ROW = Constants.SENSOR_SIZE[0] / 2
HALF_COL = Constants.SENSOR_SIZE[1] / 2

trackerObj = TargetTracker(gateSize = 5, distToDVec = 5)

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
trackerObj.addFrameObservations(observations = obs0, curCameraData = camData0)

# second frame of observations 
ECEF1 = [ECEF0[0] + metersTraveled[0], ECEF0[1] + metersTraveled[1], ECEF0[2] + metersTraveled[2]]
LatLonEl1 = CT.ECEF_to_LLE(ECEF1)
camData1 = CameraData(LatLonEl1, heading1, pitch1)
trackerObj.addFrameObservations(observations = obs1, curCameraData = camData1)

# third frame of observations
ECEF2 = [ECEF1[0] + metersTraveled[0], ECEF1[1] + metersTraveled[1], ECEF1[2] + metersTraveled[2]]
LatLonEl2 = CT.ECEF_to_LLE(ECEF2)
camData2 = CameraData(LatLonEl2, heading2, pitch2)
trackerObj.addFrameObservations(observations = obs2, curCameraData = camData2)

print('CURRENT TRACKS')
trackerObj.printCurrentTrackResults()

print('FINAL TRACKS')
trackerObj.printFinalTrackResults()