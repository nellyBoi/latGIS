# -*- coding: utf-8 -*-
"""
Created on Wed Jun 20 17:04:20 2018

@author: Max Marno


"""
import pandas as pd
import os
from AOIfunctions import *
# INITIAL COORDS (TWO XY PAIRS AS OPPOSITE CORNERS OF AOI BOUNDING BOX)
xy1 = [-105.071049, 40.305424]
xy2 = [-105.071780, 40.309820]

    # WGS84 = epsg 4326
    # World Equidistant Cylindrical = epsg 4087

mgrid= gridgen(projcoords(inepsg=4326, outepsg=4087, xycoords=xy1), projcoords(inepsg=4326, outepsg=4087, xycoords=xy2), stepsize=20)
mgrid['xxyy'] = mgrid.apply(lambda x: projcoords(4087, 4326, [x.XX, x.YY]), axis=1)
mgrid[['xlon', 'ylat']] = mgrid['xxyy'].apply(pd.Series)

mgrid.to_csv('mgridtest20.csv')

import ggapikeydoc

from ggapikeydoc import GoogleAPIKey
from gsvapifuns import getpanoid

panogrid = mgrid.apply(lambda gridrow: getpanoid(inlat=gridrow.ylat, inlon=gridrow.xlon), axis=1)
panogrid = pd.DataFrame(list(panogrid))
panogrid = panogrid.drop_duplicates(['pano_id'])
panogrid.to_csv('panogrid20.csv')

# DOWNLOAD ALL IMAGES (NOTE THAT DEFAULT HEADING, PITCH AND SIZE VALUES EXIST)
from gsvapifuns import panodnld

panogrid.pano_id.apply(lambda x: panodnld(destinationpath='D:\Projects\GSV\downloads', panoID=x))


uu = 'https://maps.googleapis.com/maps/api/streetview?size=600x300&location=46.414382,10.013988&heading=151.78&pitch=-0.76&key={}'.format(GoogleAPIKey)

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
