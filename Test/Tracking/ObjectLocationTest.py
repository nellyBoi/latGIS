# -*- coding: utf-8 -*-

import sys, os

sys.path.append(os.path.join(os.getcwd(),'..','..','Src','Tracking'))
sys.path.append(os.path.join(os.getcwd(),'..','..','Src','Utilities'))


from latGIS_containers import CameraData, ObjectLocation
from coord_transfers import CoordTransfers
CT = CoordTransfers()

# We will use the tranformations we wrote for the algorithm to make a realistic scenario
# in which we have an appropriate lat/lon/el and heading and only 'move' along
# some direction by a specified amount of meters

# ---------------------- VARIABLES TO CHANGE --------------------------------------
LatLonEl0 = [0, 0, 10]
metersTraveled = [0, 10, 0]

heading0 = 0
pitch0 = 0

heading1 = 0
pitch1 = 0

pixel0 = [512, 512]
pixel1 = [512, 490]
# ---------------------------------------------------------------------------------

camData0 = CameraData(LatLonEl0, heading0, pitch0)
ECEF0 = CT.LLE_to_ECEF(LatLonEl0)
ECEF1 = [ECEF0[0] + metersTraveled[0], ECEF0[1] + metersTraveled[1], ECEF0[2] + metersTraveled[2]]

LatLonEl1 = CT.ECEF_to_LLE(ECEF1)

objObj = ObjectLocation(origCameraData = camData0, origPixel = pixel0)

# add a couple of objects 
camData1 = CameraData(LatLonEl1, heading1, pitch1)
objObj.addNewObservation(cameraData = camData1, pixel = pixel1)

# camData1 = CameraData([0, 1.2, 0], 348, 0)
# objObj.addNewObservation(cameraData = camData1, pixel = [512,512])

# print results
objObj.printResults()





