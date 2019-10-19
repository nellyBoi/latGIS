# -*- coding: utf-8 -*-

'''
Nelly Kane
Dec.08.2018

This script will hold constants used by multiple routines in latGIS.

TODO: Change to python config file

'''
import numpy as np

# camera/sensor parameters
class Constants:
    FOV = 30 # degrees
    SENSOR_SIZE = [1024, 1024] # TODO Change
    RAD2DEG = 180/np.pi
    DEG2RAD = np.pi/180