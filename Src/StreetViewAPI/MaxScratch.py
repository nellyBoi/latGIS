# -*- coding: utf-8 -*-
"""
Created on Sun Nov 25 16:25:29 2018

@author: Max Marno
"""
#import sys
#
#sys.path.append(r'C:\Users\Max Marno\Documents\Projects\latGIS\Src\StreetViewAPI')

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
latpermeter = 1/111111
def longbasedonlat(inlat):
    # Returns the number of degrees of longitude per meter
    earth_radius = 6378 # In KM
    degrees_to_radians = math.pi/180.0
    #radians_to_degrees = 180.0/math.pi
    cc = math.pi*(earth_radius*2)
    eqdist = cc/360
    rr = inlat*degrees_to_radians
    return 1/((math.cos(rr)*eqdist)*1000)






import pandas as pd
from AOIfunctions import gridgen, projcoords
# INITIAL COORDS (TWO XY PAIRS AS OPPOSITE CORNERS OF AOI BOUNDING BOX)
# Format as Lon, Lat to mirror X,Y notation
xy1 = [-105.071049, 40.305424]
xy2 = [-105.071780, 40.309820]
minlat = min([abs(xy1[1]),abs(xy2[1])])

    # WGS84 = epsg 4326
    # World Equidistant Cylindrical = epsg 4087

mgrid= gridgen(xy1, xy2, stepsize=10)
mgrid['xxyy'] = mgrid.apply(lambda x: projcoords(4087, 4326, [x.XX, x.YY]), axis=1)
mgrid[['xlon', 'ylat']] = mgrid['xxyy'].apply(pd.Series)

mgrid.to_csv('mgridtest10.csv')




from GSV_API import gsvobject
xx = 41.341536
yy = -106.305714
g = gsvobject()
g.getpanoid(xx,yy)
g.getimage(heading=100, pitch=0)

ii = np.frombuffer(a.content, dtype = 'uint8')

from PIL import Image
from io import BytesIO
img = Image.open(BytesIO(ii))

#https://markhneedham.com/blog/2018/04/07/python-serialize-deserialize-numpy-2d-arrays/

uu = 'https://maps.googleapis.com/maps/api/streetview?size=600x300&location=46.414382,10.013988&heading=151.78&pitch=-0.76&key={}'.format(GoogleAPIKey)

import requests
r = requests.get(uu, stream=True)
type(r.content)

def download(url, out_dir, filename):
    if not os.path.isdir(out_dir):
        makedirs(out_dir)
    file_path = os.path.join(out_dir, filename)
    r = requests.get(url, stream=True)
    if r.status_code == 200: # if request is successful
        with open(file_path, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
            
# DOWNLOAD ALL IMAGES (NOTE THAT DEFAULT HEADING, PITCH AND SIZE VALUES EXIST)
from gsvapifuns import panodnld


import requests
r = requests.get(uu)
type(r.content)

def download(url, out_dir, filename):
    if not path.isdir(out_dir):
        makedirs(out_dir)
    file_path = os.path.join(out_dir, filename)
    r = requests.get(url, stream=True)
    if r.status_code == 200: # if request is successful
        with open(file_path, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
            
s = {'slat':'41.341536', 'slon':'-106.305714'}


#https://maps.googleapis.com/maps/api/streetview/metadata?location=78.648401,14.194336&key=YOUR_API_KEY
xx = 41.341536
yy = -106.305714
murl = 'https://maps.googleapis.com/maps/api/streetview/metadata'

qq = murl+'?location={},{}&key={}'.format(str(xx), str(yy), GoogleAPIKey)


metadata = requests.get(qq, stream=True).json()