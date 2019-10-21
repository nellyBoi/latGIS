# -*- coding: utf-8 -*-
"""
Nelly Kane
10.18.2019

TargetTrackerTest.py
"""
from latgis.track import TrackData as td
from latgis.location import CameraData, ObjectLocation

from util.coord_transfers import CoordTransfers
CT = CoordTransfers()

metersTraveled = [0, 10, 0]
# TRACK 1 Data ###################################################
LatLonEl0 = [0, 0, 10]
heading0 = 0
pitch0 = 0
pixel0 = [500, 500]

camData = CameraData(LatLonEl = LatLonEl0, heading = heading0, pitch = pitch0)

# FOR APPEND ###############

ECEF0 = CT.LLE_to_ECEF(LatLonEl0)
ECEF1 = [ECEF0[0] + metersTraveled[0], ECEF0[1] + metersTraveled[1], ECEF0[2] + metersTraveled[2]]
LatLonEl1 = CT.ECEF_to_LLE(ECEF1)

camDataForAppend = CameraData(LatLonEl1, heading0, pitch0)
pixelForAppend = [480, 500]

# TRACK 1 Data ###################################################
LatLonEl1 = [2, 2, 2]
heading1 = 0
pitch1 = 0

camData1 = CameraData(LatLonEl = LatLonEl1, heading = heading1, pitch = pitch1)

pixel1 = [512, 490]
##################################################################

tdObj1 = td(name = 'Test object')
tdObj1.print_data()

print('No IDs')
noIds = tdObj1.get_ids() # shouldn't be any IDs yet
print(noIds)

# testing add to track
objObj0 = ObjectLocation(origCameraData = camData, origPixel = pixel0)
tdObj1.add_track(objectLocation = objObj0)
print('One ID')
oneId = tdObj1.get_ids()
print(oneId)

# adding another track
camData1 = CameraData(LatLonEl = LatLonEl1, heading = heading1, pitch = pitch1)
objObj1 = ObjectLocation(origCameraData = camData1, origPixel = pixel1)
tdObj1.add_track(objectLocation = objObj1)
print('Two IDs')
twoId = tdObj1.get_ids()
print(twoId)

# print data
tdObj1.print_data()

# append to data with the first ID
tdObj1.append_to_data_by_id(objObj1.getObjectID(), cameraData = camDataForAppend, pixel = pixelForAppend)

# print data again with append
tdObj1.print_data()

# removing a track
objObj2 = tdObj1.remove_by_id(objObj0.getObjectID())
print('One ID again')
twoId = tdObj1.get_ids()
print(twoId)

# print data
tdObj1.print_data()

# pass data back from ID
obj = tdObj1.get_data_by_id(objObj1.getObjectID())
print(' /////////// DATA PASSED BACK //////////////////')
obj.printResults()