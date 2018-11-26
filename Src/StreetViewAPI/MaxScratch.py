# -*- coding: utf-8 -*-
"""
Created on Sun Nov 25 16:25:29 2018

@author: Max Marno
"""
import sys

sys.path.append(r'C:\Users\Max Marno\Documents\Projects\latGIS\Src\StreetViewAPI')

from ggapikeydoc import GoogleAPIKey
from gsvapifuns import getpanoid
'''
41.313999, -106.138349
'''
getpanoid()


'''
Elevation API
'''
'''
Test Coords - in front of my house:
    39.525858, -106.043589
'''

import json
import requests
coords = '39.525858,-106.043589'
openelevation = 'https://api.open-elevation.com/api/v1/lookup?locations='
oe = json.loads(requests.get(url=openelevation+coords).text)
oe_elev = oe['results'][0]['elevation']

# GOOGLE ELEVATION
ggelevation = 'https://maps.googleapis.com/maps/api/elevation/json?locations={}&key='.format(coords)+GoogleAPIKey

gg = json.loads(requests.get(ggelevation).text)
gg_elev = gg['results'][0]['elevation']




import math

# Distances are measured in miles.
# Longitudes and latitudes are measured in degrees.
# Earth is assumed to be perfectly spherical.

earth_radius = 6378 # In KM
degrees_to_radians = math.pi/180.0
radians_to_degrees = 180.0/math.pi

def change_in_latitude(miles):
    "Given a distance north, return the change in latitude."
    return (miles/earth_radius)*radians_to_degrees

def change_in_longitude(latitude, miles):
    "Given a latitude and a distance west, return the change in longitude."
    # Find the radius of a circle around the earth at given latitude.
    r = earth_radius*math.cos(latitude*degrees_to_radians)
    return (miles/r)*radians_to_degrees

def longbasedonlat(inlat):
    print(inlat*degrees_to_radians)
    cc = math.pi*(earth_radius*2)
    eqdist = cc/360
    rr = inlat*degrees_to_radians
    print(rr)
    return math.cos(rr)*eqdist 