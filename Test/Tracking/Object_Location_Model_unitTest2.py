#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 24 20:06:30 2018

@author: johnnelsonkane

Object_Location_Model_unitTest.py

This unit test will check the 'Object_Location_Model' in which an objects 
movement from image to image is predicted.

"""
import sys, os
sys.path.append(os.path.join(sys.path[0],'..','..','Src','Tracking'))
sys.path.append(os.path.join(sys.path[0],'..','..','Src','Utilities'))

import numpy as np
import sys
sys.path.append('..//Utilities')
import matplotlib.pyplot as plt

from coord_transfers import CoordTransfers
CT = CoordTransfers()
# instantiate the class
from Object_Location_Model2 import Object_Location_Model, cameraData

def unitTest(expression: bool):
    if (expression == True):
        print("TEST PASSED")
    else:
        print("TEST FAILED")

'''
class cameraData:
    def __init__(self, LatLonEl: list, heading: float, pitch: float):
        # instance variable unique to each instance
        self.LatLonEl = LatLonEl   
        self.heading = heading
        self.pitch = pitch
    
'''
'''
IMPORT CALL:
    (self, objRowCol: list, camData1: cameraData, camData2: cameraData, degFlag : bool = False )-> list:
'''
print('TEST 1: Object along direction of travel (prime meridian')

objRowCol = [512, 512]

locModel = Object_Location_Model(2)
# We will start in ECEF for distance and convert to LLE for function input.
ecef1 = np.array((6378137, 0, 0)) # meters
ecef2 = np.array((6378137, 0, 50)) # meters, due north by 5 meters
LLE1 = CT.ECEF_to_LLE(ecef1)
LLE2 = CT.ECEF_to_LLE(ecef2)

cam1 = cameraData(LatLonEl = LLE1, heading = 0, pitch = 0)
cam2 = cameraData(LatLonEl = LLE2, heading = 0, pitch = 0)

PIXELS_OUT = locModel. objectLocationPredictor(objRowCol, cam1, cam2, degFlag = True)
unitTest(np.abs(PIXELS_OUT[0] - objRowCol[0]) < 1)
unitTest(np.abs(PIXELS_OUT[1] - objRowCol[1]) < 1)
plt.figure()
v = [1, 1024, 1, 1024]
plt.axis(v)
# maintaining camera coordinate system
plt.ylim(1024,1)
plt.scatter(objRowCol[1], objRowCol[0], color = 'b')
plt.scatter(PIXELS_OUT[1], PIXELS_OUT[0], color = 'r')
plt.legend(['Object t1', 'Object t2'])
plt.xlabel('COLUMN')
plt.ylabel('ROW')
plt.show()

print('Location Prediction' + str(PIXELS_OUT))

# =====================================================================================
print('TEST 2: Hand calculated pixels for a regular step')

locModel = Object_Location_Model(1)
objRowCol = [454, 454]

# We will start in ECEF for distance and convert to LLE for function input.
ecef1 = np.array((6378137, 0, 0)) # meters
ecef2 = np.array((6378137, 0, 30)) # meters, due north by 5 meters
LLE1 = CT.ECEF_to_LLE(ecef1)
LLE2 = CT.ECEF_to_LLE(ecef2)

cam1 = cameraData(LatLonEl = LLE1, heading = 0, pitch = 0)
cam2 = cameraData(LatLonEl = LLE2, heading = 0, pitch = 0)

PIXELS_OUT = locModel. objectLocationPredictor(objRowCol, cam1, cam2, degFlag = True)

unitTest(np.abs(PIXELS_OUT[0] - 66) < 1)
unitTest(np.abs(PIXELS_OUT[1] - 66) < 1)
print('Predicted Pixel: ' + str(PIXELS_OUT[0]) + ' , '+ str(PIXELS_OUT[1]))
plt.figure()
v = [1, 1024, 1, 1024]
plt.axis(v)
# maintaining camera coordinate system
plt.ylim(1024,1)
plt.scatter(objRowCol[1], objRowCol[0], color = 'b')
plt.scatter(PIXELS_OUT[1], PIXELS_OUT[0], color = 'r')
plt.legend(['Object t1', 'Object t2'])
plt.xlabel('COLUMN')
plt.ylabel('ROW')
plt.show()

# =====================================================================================
print('TEST 3: One more boresite test, nonzero lats and longs')

locModel = Object_Location_Model(1)
objRowCol = [512, 512]

# We will start in ECEF for distance and convert to LLE for function input.
ecef1 = np.array((3.9054825307866509e-10, 6378137.0, 0.0)) # meters
ecef2 = np.array((3.9054825307866509e-10+30, 6378137.0, 0.0)) # meters
LLE1 = CT.ECEF_to_LLE(ecef1)
LLE2 = CT.ECEF_to_LLE(ecef2)

cam1 = cameraData(LatLonEl = LLE1, heading = 270, pitch = 0)
cam2 = cameraData(LatLonEl = LLE2, heading = 270, pitch = 0)

PIXELS_OUT = locModel. objectLocationPredictor(objRowCol, cam1, cam2, degFlag = True)

unitTest(np.abs(PIXELS_OUT[0] - objRowCol[0]) < 1)
unitTest(np.abs(PIXELS_OUT[1] - objRowCol[1]) < 1)
print('Predicted Pixel: ' + str(PIXELS_OUT[0]) + ' , '+ str(PIXELS_OUT[1]))
plt.figure()
v = [1, 1024, 1, 1024]
plt.axis(v)
# maintaining camera coordinate system
plt.ylim(1024,1)
plt.scatter(objRowCol[1], objRowCol[0], color = 'b')
plt.scatter(PIXELS_OUT[1], PIXELS_OUT[0], color = 'r')
plt.legend(['Object t1', 'Object t2'])
plt.xlabel('COLUMN')
plt.ylabel('ROW')
plt.show()