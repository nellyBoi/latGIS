#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 19 01:27:53 2018

@author: johnnelsonkane

CoordTransfers class

This class will contain tools for coordinate transfers in support of the 
tracking & object locating algorithms.

NOTES:
    Functions LLE_to_ECEF and ECEF_to_LLE are adopted from Planet Model Earth (WGS84).
    In this functions, elevation is referring to the standard elevation, i.e. - 
    the distance above sea level at the respective lat.lon. Total distance from
    the centroid of the earth is accounted for.

fcns:
    LLE_to_ECEF: This routine will ingest geodetic latitude, longitude, and elevation
    data and convert to ECEF data. 
        Inputs: LLE: (Latidude [deg], Longitude [deg], Elevation [m]): 1x3 list
        Outputs: ECEF: (X [m], Y [m], Z [m]): 1x3 list
        TESTED
        
    ECEF_to_LLE: This routine will ingest ECEF data and convert to geodetic latitude, 
    longitude, and elevationdata. 
        Inputs: ECEF: (X [m], Y [m], Z [m]): 1x3 list   
        Outputs: LLE: (Latidude [deg], Longitude [deg], Elevation [m]): 1x3 list
        TESTED
"""

from numpy import sqrt, cos, sin, pi, mod
from math import atan2

class CoordTransfers:
    """A Coordinate Transfer Class"""
    
    # The __init__ method will be executed when the classname CoordTransfers
    # is used to construct a new coord pair.
    def __init__(self):
        
        # WGS84 ellipsoid constants:
        self.a = 6378137 # meters
        self.E = 8.1819190842622e-2
        self.deg2Rad = pi/180
        self.rad2Deg = 180/pi
    
    def LLE_to_ECEF(self, LLE):
        
        # radians, radians, meters
        lat, lon, el = LLE[0]*self.deg2Rad , LLE[1]*self.deg2Rad , LLE[2]
        # intermediate calculation
        # (prime vertical radius of curvature)
        N = self.a/sqrt(1 - self.E**2 * (sin(lat))**2)
        
        x = (N + el) * cos(lat) * cos(lon) # meters
        y = (N + el) * cos(lat) * sin(lon) # meters
        z = ((1 - self.E**2)*N + el) * sin(lat) # meters
    
        ECEF = [x, y, z]
        
        return ECEF
    
    def ECEF_to_LLE(self, ECEF):
        
        # meters, meters, meters
        x, y, z = ECEF[0], ECEF[1], ECEF[2]
        
        # calculatons
        b = sqrt(self.a**2 * (1-self.E**2))
        ep = sqrt((self.a**2 - b**2)/(b**2))
        p = sqrt(x**2 + y**2)
        th = atan2(self.a * z, b * p)
        
        lon = atan2(y, x)
        lat = atan2((z + ep**2 * b * sin(th)**3),(p - self.E**2 * self.a * cos(th)**3))
        N = self.a/(sqrt( 1 - self.E**2 * sin(lat)**2))
        el = p/cos(lat) - N
        
        # return lon in range [0, 2*pi)
        lon = mod(lon, 2*pi)
        
        # correct for numerical instability in altitude near exact poles:
        # (after this correction, error is about 2 millimeters, whish is about 
        # the same as the numerical precision of the overall function)
        if abs(x) < 1 and abs(y) < 1:
            el = abs(z) - b
            
        LLE = [lat*self.rad2Deg, lon*self.rad2Deg, el]
        
        return LLE
    