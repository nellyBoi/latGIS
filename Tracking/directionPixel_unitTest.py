#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 17 21:13:56 2018

@author: johnnelsonkane

direction pixel prediction - unit test

"""

import numpy as np
import sys
sys.path.append('..//Utilities')
from coord_transfers import CoordTransfers
CT = CoordTransfers()
# instantiate the class
from Object_Location_Model import Object_Location_Model
locModel = Object_Location_Model(8)

'''Testing boresight'''
# Denver
print('Test: 1 (Boresight check)')
LAT1, LON1, EL1 = 39.7392, 104.9903, 1609.3
LAT2, LON2, EL2 = 39.7392+0.1, 104.9903, 1609.3
frame_t1_ecef = CT.LLE_to_ECEF = np.asarray([LAT1,LON1,EL1])
frame_t2_ecef = CT.LLE_to_ECEF = np.asarray([LAT2,LON2,EL2])
LOS = frame_t2_ecef - frame_t1_ecef
[row1, col1] = locModel.getDirectionPixel(frame_t1_ecef, frame_t2_ecef, LOS, [LAT1, LON1])
print('Row: ' + str(row1)  + '   Col:' + str(col1),'\n')

'''IMPORTANT NOTE:: Tests 2-5 are only Lat/Long checks and will not have a 
reasonable row, col output value. This is because one can not specify LAT/LON
and frame ECEF, or the camera will be off rotation. For the correct camera 
rotation, one must use the coordinate transformations instead of over-defining
the system. This affects test 6-9 as well but not as much because those values
are reasonable.'''

print('Test: 2 (Lat/Long check)')
frame_t1_ecef = np.asarray([1000, 0, 0])
frame_t2_ecef = np.asarray([1000, 10, 0])
LOS = np.asarray([1, 10, 1])
[row1, col1] = locModel.getDirectionPixel(frame_t1_ecef, frame_t2_ecef, LOS, [0, 0])
print('Row: ' + str(row1)  + '   Col:' + str(col1),'\n')

print('Test: 3 (Lat/Long check)')
frame_t1_ecef = np.asarray([1000, 0, 0])
frame_t2_ecef = np.asarray([1000, 10, 0])
LOS = np.asarray([1, 10, 1])
[row1, col1] = locModel.getDirectionPixel(frame_t1_ecef, frame_t2_ecef, LOS, [-45, 45])
print('Row: ' + str(row1)  + '   Col:' + str(col1),'\n')

print('Test: 4 (Lat/Long check)')
frame_t1_ecef = np.asarray([1000, 0, 0])
frame_t2_ecef = np.asarray([1000, 10, 0])
LOS = np.asarray([1, 10, 1])
[row1, col1] = locModel.getDirectionPixel(frame_t1_ecef, frame_t2_ecef, LOS, [45, -45])
print('Row: ' + str(row1)  + '   Col:' + str(col1),'\n')

print('Test: 5 (Lat/Long check)')
frame_t1_ecef = np.asarray([1000, 0, 0])
frame_t2_ecef = np.asarray([1000, 10, 0])
LOS = np.asarray([1, 10, 1])
[row1, col1] = locModel.getDirectionPixel(frame_t1_ecef, frame_t2_ecef, LOS, [-45, -45])
print('Row: ' + str(row1)  + '   Col:' + str(col1),'\n')

print('Test: 6 (Sensor position (row greater than boresight) check)')
# Lat, Lon = 90, 0
frame_t1_ecef = np.asarray([0, 0, 1000])
frame_t2_ecef = np.asarray([0, 10, 1000])
LOS = np.asarray([0, 10, 1])
[row1, col1] = locModel.getDirectionPixel(frame_t1_ecef, frame_t2_ecef, LOS, [90, 0])
print('Row: ' + str(row1)  + '   Col:' + str(col1),'\n')

print('Test: 7 (Sensor position (row less than boresight) check)')
# Lat, Lon = 90, 0
frame_t1_ecef = np.asarray([0, 0, 1000])
frame_t2_ecef = np.asarray([0, 10, 1000])
LOS = np.asarray([0, 10, -1])
[row1, col1] = locModel.getDirectionPixel(frame_t1_ecef, frame_t2_ecef, LOS, [90, 0])
print('Row: ' + str(row1)  + '   Col:' + str(col1),'\n')

print('Test: 8 (Sensor position (col greater than boresight) check)')
# Lat, Lon = 90, 0
frame_t1_ecef = np.asarray([0, 0, 1000])
frame_t2_ecef = np.asarray([0, 10, 1000])
LOS = np.asarray([-1, 10, 0])
[row1, col1] = locModel.getDirectionPixel(frame_t1_ecef, frame_t2_ecef, LOS, [90, 0])
print('Row: ' + str(row1)  + '   Col:' + str(col1),'\n')

print('Test: 9 (Sensor position (col less than boresight) check)')
# Lat, Lon = 90, 0
frame_t1_ecef = np.asarray([0, 0, 1000])
frame_t2_ecef = np.asarray([-1, 10, 1000])
LOS = np.asarray([0, 10, 0])
[row1, col1] = locModel.getDirectionPixel(frame_t1_ecef, frame_t2_ecef, LOS, [90, 0])
print('Row: ' + str(row1)  + '   Col:' + str(col1),'\n')