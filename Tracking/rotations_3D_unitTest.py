#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 10 21:50:38 2018

@author: johnnelsonkane

Unit Test sandbox for the coordinate rotations in 3d.
 

NOTE: If coords and normal are in same direction than final coords should also
be in the same direction as normal.

ALL 8 QUADRANTS TESTED. 

"""
import numpy as np

# instantiate the class
from Object_Location_Model import Object_Location_Model
locModel = Object_Location_Model(8)

'''Testing the coordinate rotations'''
# Test 1
coords = np.array((3,4,5))
normal = np.array((0,0,1))

# since the normal is already (1,0,0) coordinates should not rotate
knownCoords = coords.copy()
outCoords1 = locModel.rotateCoordsToTilda(coords, normal)
print('Test 1: Coordinate Transformation Error: ' + \
      str(knownCoords - outCoords1))

# Test 2
coords = np.array((3,0,0))
normal = np.array((1,0,0))
knownCoords = np.array((0, 0, np.linalg.norm(coords)))
outCoords1 = locModel.rotateCoordsToTilda(coords, normal)
print('Test 2: Coordinate Transformation Error: ' + \
      str(knownCoords - outCoords1))

# Test 3
coords = np.array((0,4,0))
normal = np.array((0,1,0))
knownCoords = np.array((0, 0, np.linalg.norm(coords)))
outCoords1 = locModel.rotateCoordsToTilda(coords, normal)
print('Test 3: Coordinate Transformation Error: ' + \
      str(knownCoords - outCoords1))

# Test 4
coords = np.array((-3,0,0))
normal = np.array((-1,0,0))
knownCoords = np.array((0, 0, np.linalg.norm(coords)))
outCoords1 = locModel.rotateCoordsToTilda(coords, normal)
print('Test 4: Coordinate Transformation Error: ' + \
      str(knownCoords - outCoords1))


# Test 5
coords = np.array((1,-3,-4))
normal = np.array((1,-3,-4))
knownCoords = np.array((0, 0, np.linalg.norm(coords)))
outCoords1 = locModel.rotateCoordsToTilda(coords, normal)
print('Test 5: Coordinate Transformation Error: ' + \
      str(knownCoords - outCoords1))

# Test 6
coords = np.array((1.5,-3,1))
normal = np.array((1.5,-3,1))
knownCoords = np.array((0, 0, np.linalg.norm(coords)))
outCoords1 = locModel.rotateCoordsToTilda(coords, normal)
print('Test 6: Coordinate Transformation Error: ' + \
      str(knownCoords - outCoords1))

# Test 7
coords = np.array((-0.3,3,-1))
normal = np.array((-0.3,3,-1))
knownCoords = np.array((0, 0, np.linalg.norm(coords)))
outCoords1 = locModel.rotateCoordsToTilda(coords, normal)
print('Test 7: Coordinate Transformation Error: ' + \
      str(knownCoords - outCoords1))

# Test 8
coords = np.array((-7,8,4))
normal = np.array((-7,8,4))
knownCoords = np.array((0, 0, np.linalg.norm(coords)))
outCoords1 = locModel.rotateCoordsToTilda(coords, normal)
print('Test 8: Coordinate Transformation Error: ' + \
      str(knownCoords - outCoords1))

# Test 9
coords = np.array((4,6,8))
normal = np.array((2,3,4))
knownCoords = np.array((0, 0, np.linalg.norm(coords)))
outCoords1 = locModel.rotateCoordsToTilda(coords, normal)
print('Test 9: Coordinate Transformation Error: ' + \
      str(knownCoords - outCoords1))

# Test 10 (tests where normal.u != coords.u)
coords = np.array((1,0,0))
normal = np.array((0,1,0))
knownCoords = np.array((1, 0, 0))
outCoords1 = locModel.rotateCoordsToTilda(coords, normal)
print('Test 10: Coordinate Transformation Error: ' + \
      str(knownCoords - outCoords1))

# Test 11 (tests where normal.u != coords.u)
coords = np.array((0,1,0))
normal = np.array((1,0,0))
knownCoords = np.array((0, 1, 0))
outCoords1 = locModel.rotateCoordsToTilda(coords, normal)
print('Test 11: Coordinate Transformation Error: ' + \
      str(knownCoords - outCoords1))

# Test 12 (tests where normal.u != coords.u)
coords = np.array((0 ,1, 0))
normal = np.array((0, 0, -1))
knownCoords = np.array((0, -1, 0))
outCoords1 = locModel.rotateCoordsToTilda(coords, normal)
print('Test 12: Coordinate Transformation Error: ' + \
      str(knownCoords - outCoords1))

# Test 13
coords = np.array((-1,-2,4))
normal = np.array((-1,-2,4))
knownCoords = np.array((0, 0, np.linalg.norm(coords)))
outCoords1 = locModel.rotateCoordsToTilda(coords, normal)
print('Test 13: Coordinate Transformation Error: ' + \
      str(knownCoords - outCoords1))

# Test 14
coords = np.array((-3,-5,-7))
normal = np.array((-3,-5,-7))
knownCoords = np.array((0, 0, np.linalg.norm(coords)))
outCoords1 = locModel.rotateCoordsToTilda(coords, normal)
print('Test 14: Coordinate Transformation Error: ' + \
      str(knownCoords - outCoords1))

# Test 15
coords = np.array((1,2,-5))
normal = np.array((1,2,-5))
knownCoords = np.array((0, 0, np.linalg.norm(coords)))
outCoords1 = locModel.rotateCoordsToTilda(coords, normal)
print('Test 15: Coordinate Transformation Error: ' + \
      str(knownCoords - outCoords1))
