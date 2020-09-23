#!/usr/bin/env python3
"""
Created on Sat May 19 01:48:38 2018

@author: johnnelsonkane

Test driver for running the coord_transfers class. This also serves as a unit tests.

"""
import pathlib
filepath = pathlib.Path(__file__).parent.absolute()

import os
import sys

sys.path.append(os.path.join(filepath, '..'))
from test_setup import setup
setup()

from util.coord_transfers import CoordTransfers

# instantiation of the class
d = CoordTransfers()


'''LLE to ECEF'''
LLE1 = [90, 0, 1.333]
ECEF1 = d.LLE_to_ECEF(LLE1)

print('X = ' + str(ECEF1[0]) + ' Y = ' + str(ECEF1[1]) + ' Z = ' + str(ECEF1[2]))

LLE2 = [30, 30, 10]
ECEF2 = d.LLE_to_ECEF(LLE2)

print('X = ' + str(ECEF2[0]) + ' Y = ' + str(ECEF2[1]) + ' Z = ' + str(ECEF2[2]))

LLE3 = [2, 80, 0.25]
ECEF3 = d.LLE_to_ECEF(LLE3)

print('X = ' + str(ECEF3[0]) + ' Y = ' + str(ECEF3[1]) + ' Z = ' + str(ECEF3[2]))

LLE4 = [-42, 10, 5]
ECEF4 = d.LLE_to_ECEF(LLE4)

print('X = ' + str(ECEF4[0]) + ' Y = ' + str(ECEF4[1]) + ' Z = ' + str(ECEF4[2]))

LLE5 = [3, 285, 15]
ECEF5 = d.LLE_to_ECEF(LLE5)

print('X = ' + str(ECEF5[0]) + ' Y = ' + str(ECEF5[1]) + ' Z = ' + str(ECEF5[2]))


'''ECEF to LLE'''
LL1_result = d.ECEF_to_LLE(ECEF1)
print ('Lat = ' + str(LL1_result[0]) + ' Lon = ' + str(LL1_result[1]) + ' El = ' + str(LL1_result[2]))

LL2_result = d.ECEF_to_LLE(ECEF2)
print ('Lat = ' + str(LL2_result[0]) + ' Lon = ' + str(LL2_result[1]) + ' El = ' + str(LL2_result[2]))

LL3_result = d.ECEF_to_LLE(ECEF3)
print ('Lat = ' + str(LL3_result[0]) + ' Lon = ' + str(LL3_result[1]) + ' El = ' + str(LL3_result[2]))

LL4_result = d.ECEF_to_LLE(ECEF4)
print ('Lat = ' + str(LL4_result[0]) + ' Lon = ' + str(LL4_result[1]) + ' El = ' + str(LL4_result[2]))

LL5_result = d.ECEF_to_LLE(ECEF5)
print ('Lat = ' + str(LL5_result[0]) + ' Lon = ' + str(LL5_result[1]) + ' El = ' + str(LL5_result[2]))

'''Difference Calculations'''
print('Test 1 Difference: Lat:' +str(LL1_result[0]-LLE1[0]) + ' Lon: '+ \
      str(LL1_result[1]-LLE1[1])+ ' El: ' + str(LL1_result[2]-LLE1[2]))

print('Test 2 Difference: Lat:' +str(LL2_result[0]-LLE2[0]) + ' Lon: '+ \
      str(LL2_result[1]-LLE2[1])+ ' El: ' + str(LL2_result[2]-LLE2[2]))

print('Test 3 Difference: Lat:' +str(LL3_result[0]-LLE3[0]) + ' Lon: '+ \
      str(LL3_result[1]-LLE3[1])+ ' El: ' + str(LL3_result[2]-LLE3[2]))

print('Test 4 Difference: Lat:' +str(LL4_result[0]-LLE4[0]) + ' Lon: '+ \
      str(LL4_result[1]-LLE4[1])+ ' El: ' + str(LL4_result[2]-LLE4[2]))

print('Test 5 Difference: Lat:' +str(LL5_result[0]-LLE5[0]) + ' Lon: '+ \
      str(LL5_result[1]-LLE5[1])+ ' El: ' + str(LL5_result[2]-LLE5[2]))

