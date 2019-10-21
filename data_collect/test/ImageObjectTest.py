# -*- coding: utf-8 -*-

import sys, os
sys.path.append(os.path.join(os.getcwd(),'..','..','Src','Utilities'))
sys.path.append(os.path.join(os.getcwd(),'..','..','Src','StreetViewAPI'))


from GSV_API import gsvobject
from image_object import image_obj
from image_object import CameraData
import numpy as np
#from latGIS_containers import CameraData

g = gsvobject()

g.getpanoid([[39.513231, -106.052872]])
g.getimage(g.heading=0, pitch=0)

ii = image_obj()
ii.add_feature(pixelcoords=[222, 333], cameradata=g.image_data.cameradata[0]
    , imagearray=g.image_data.imagearray[0], panoid = g.image_data.panoid[0])


#import pickle
#with open('dataset1.pkl', 'wb') as f:
#    pickle.dump(img_metadata, f)
#    
#pids = [x.metadata['pano_id'] for x in imgs]


    