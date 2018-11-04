# -*- coding: utf-8 -*-
"""
Created on Wed Jun 20 17:04:20 2018

@author: Max
"""
import pandas as pd
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

from ggapikeydoc import GoogleAPIKey
from gsvapifuns import getpanoid

panogrid = mgrid.apply(lambda gridrow: getpanoid(inlat=gridrow.ylat, inlon=gridrow.xlon), axis=1)
panogrid = pd.DataFrame(list(panogrid))
panogrid = panogrid.drop_duplicates(['pano_id'])
panogrid.to_csv('panogrid20.csv')

# DOWNLOAD ALL IMAGES (NOTE THAT DEFAULT HEADING, PITCH AND SIZE VALUES EXIST)
from gsvapifuns import panodnld

panogrid.pano_id.apply(lambda x: panodnld(destinationpath='D:\Projects\GSV\downloads', panoID=x))
