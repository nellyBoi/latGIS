# -*- coding: utf-8 -*-

'''
Nelly Kane
Dec.08.2018

This script will hold constants used by multiple routines in latGIS.

'''
import numpy as np

# camera/sensor parameters
class constants:
    FOV = 30 # degrees
    sensorSize = [1024, 1024]
    rad2deg = 180/np.pi
    deg2rad = np.pi/180