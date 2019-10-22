# -*- coding: utf-8 -*-

import sys, os

sys.path.append(os.path.join(os.getcwd(),'..','..','Src','Tracking'))
sys.path.append(os.path.join(os.getcwd(),'..','..','Src','Utilities'))


from latgis.location import CameraData, ObjectLocation
from latgis.util.coord_transfers import CoordTransfers
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

heading2 = 0
pitch2 = 0

pixel0 = [512, 512]
pixel1 = [512, 490]
pixel2 = [512, 475]
# ---------------------------------------------------------------------------------

camData0 = CameraData(LatLonEl0, heading0, pitch0)
ECEF0 = CT.LLE_to_ECEF(LatLonEl0)
ECEF1 = [ECEF0[0] + metersTraveled[0], ECEF0[1] + metersTraveled[1], ECEF0[2] + metersTraveled[2]]

LatLonEl1 = CT.ECEF_to_LLE(ECEF1)

objObj = ObjectLocation(origCameraData = camData0, origPixel = pixel0)

# add an observation
camData1 = CameraData(LatLonEl1, heading1, pitch1)
objObj.addNewObservation(cameraData = camData1, pixel = pixel1)

# print results
objObj.printResults()

# add another observation
ECEF2 = [ECEF1[0] + metersTraveled[0], ECEF1[1] + metersTraveled[1], ECEF1[2] + metersTraveled[2]]
LatLonEl2 = CT.ECEF_to_LLE(ECEF2)
camData2 = CameraData(LatLonEl2, heading2, pitch2)
objObj.addNewObservation(cameraData = camData2, pixel = pixel2)

# print results
objObj.printResults()
print(objObj.getResults())

# testing getter functions
print("Camera Data: ")
cam = objObj.getRecentCameraData()
print(str(cam.LatLonEl) + str(cam.heading) + str(cam.pitch))
print("Pixel: ")
print(objObj.getRecentPixel())

