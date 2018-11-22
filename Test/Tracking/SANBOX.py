#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 11 23:09:31 2018


@author: johnnelsonkane

SANDBOX


"""


'''import numpy as np

# instantiate the class
from Object_Location_Model import Object_Location_Model
locModel = Object_Location_Model()

coords = np.array((0 ,1, 0))
normal = np.array((0, 0, -1))
knownCoords = np.array((0, 0, np.linalg.norm(coords)))
outCoords1 = locModel.rotateCoordsToTilda(coords, normal)
print('Test 6: Coordinate Transformation Error: ' + \
      str(knownCoords - outCoords1))
'''
import numpy as np
import sys
sys.path.append('..//Utilities')
import matplotlib.pyplot as plt

from coord_transfers import CoordTransfers
CT = CoordTransfers()
# instantiate the class
from Object_Location_Model import Object_Location_Model
locModel = Object_Location_Model(8)

print('TEST 5: ')
objRowCol = [512, 512]
frame_t1_ecef = np.asarray([0, 0, 1000])
frame_t2_ecef = np.asarray([0, 10, 1000])
LOS = np.asarray([5, 10, 5])
LatLon = [90, 0]
PIXELS_OUT = locModel. objectLocationPredictor(objRowCol, frame_t1_ecef, frame_t2_ecef, LOS, LatLon)
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