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
g.getpanoid(39.513231, -106.052872)
g.getimage(heading=0, pitch=0)

ii = image_obj()
ii.add_feature([222,338], g.CameraData, g.image_array, panoid = g.metadata['pano_id'])

#
#ii = image_obj(g.image_array, g.CameraData)
#ii = image_obj(g.image_array,  heading = 0, pitch=0, ftype='t1')  
#  
        
#ii.add_feature([444,333], ftype='type1')   



from AOIfunctions import gridgen

xy1 = [-105.260432, 40.040073]
xy2 = [-105.253751, 40.036415]

mgrid= gridgen(xy1, xy2, stepsize=100)

gg = gsvobject()

[gg.getpanoid([[row['YY'], row['XX']]]) for ii, row in mgrid.iterrows()]

imgobjs = [gsvobject().getpanoid(row['YY'], row['XX']) for ii, row in mgrid.iterrows()]

img_data = []
img_panos = []
for ii, row in mgrid.iterrows():
    g = gsvobject()
    g.getpanoid(row['YY'], row['XX'])
    if g.metadata['status']=='OK':
        if g.metadata['pano_id'] not in img_panos:
            img_panos.append(g.metadata['pano_id'])
            g.getimage(heading = 0, pitch = 0)
            img_data.append(g)
            

#    
#
#
#    
#
#import pickle
#with open('dataset1.pkl', 'wb') as f:
#    pickle.dump(img_metadata, f)
#    
#pids = [x.metadata['pano_id'] for x in imgs]


    