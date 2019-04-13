# -*- coding: utf-8 -*-
"""
Created on Wed Jun 20 17:04:20 2018

@author: Max Marno


"""

import sys, os
sys.path.append(os.path.join(os.getcwd(),'..','..','Src','Utilities'))
sys.path.append(os.path.join(os.getcwd(),'..','..','Src','StreetViewAPI'))


from GSV_API import gsvobject
from image_object import image_obj
from image_object import CameraData
import numpy as np
from AOI import gridgen

# Bounding coords (around Nelson's)
xy1 = [-105.260432, 40.040073]
xy2 = [-105.253751, 40.036415]

#Generate mesh grid w/in area of interest
mgrid = gridgen(xy1, xy2, stepsize=100)
# Instantiate gsv dataset object
gg = gsvobject()
# Get all unique panoid's (capture points) 
[gg.getpanoid([[row['YY'], row['XX']]]) for ii, row in mgrid.iterrows()]
# Get Images
gg.getimage(imagemetadata=gg.search_results, heading=90, pitch=0)

# show image:
gg.showimage(gg.image_data.imagearray[3])