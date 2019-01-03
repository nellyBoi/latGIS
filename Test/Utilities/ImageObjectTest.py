# -*- coding: utf-8 -*-

import sys, os
sys.path.append(os.path.join(os.getcwd(),'..','..','Src','Utilities'))
sys.path.append(os.path.join(os.getcwd(),'..','..','Src','StreetViewAPI'))


from GSV_API import gsvobject
from image_object import image_obj
from image_object import CameraDatas

g = gsvobject()
g.getpanoid(39.513231, -106.052872)
g.getimage(heading=0, pitch=0)


ii = image_obj(g.image_array, CameraData( )
ii = image_obj(g.image_array,  heading = 0, pitch=0, ftype='t1')  
          
ii.add_feature([444,333], ftype='type1')   