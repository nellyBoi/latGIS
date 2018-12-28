# -*- coding: utf-8 -*-

import sys, os
sys.path.append(os.path.join(sys.path[0],'..','..','Src','Utilities'))
sys.path.append(os.path.join(sys.path[0],'..','..','Src','StreetViewAPI'))

from GSV_API import gsvobject
from image_object import image_obj

g = gsvobject()
g.getpanoid(39.513231, -106.052872)
g.getimage(heading=0, pitch=0)



ii = image_obj(g.image_array, latlonelv=[3,4,5], heading = 0, pitch=0, ftype='t1')  
          
ii.add_feature([444,333], ftype='type1')   