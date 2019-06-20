#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 24 20:06:30 2018

@author: johnnelsonkane

Object_Location_Model_unitTest.py

This unit test will check the 'Object_Location_Model' in which an objects 
movement from image to image is predicted.

"""

''' RETIRED '''
import sys
sys.exit()
''' RETIRED '''
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
from Object_Location_Model import Object_Location_Model
locModel = Object_Location_Model(8)

print('TEST 1: Object along direction of travel')
objRowCol = [512, 512]
frame_t1_ecef = np.asarray([0, 0, 1000])
frame_t2_ecef = np.asarray([0, 10, 1000])
LOS = np.asarray([0, 10, 0])
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

print('TEST 2: ')
objRowCol = [512, 512]
frame_t1_ecef = np.asarray([0, 0, 1000])
frame_t2_ecef = np.asarray([0, 10, 1000])
LOS = np.asarray([0, 10, -5])
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

print('TEST 3: ')
objRowCol = [512, 512]
frame_t1_ecef = np.asarray([0, 0, 1000])
frame_t2_ecef = np.asarray([0, 10, 1000])
LOS = np.asarray([0, 10, 5])
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

print('TEST 4: ')
objRowCol = [512, 512]
frame_t1_ecef = np.asarray([0, 0, 1000])
frame_t2_ecef = np.asarray([0, 10, 1000])
LOS = np.asarray([-5, 10, 5])
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