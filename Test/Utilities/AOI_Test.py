# -*- coding: utf-8 -*-

import sys, os
sys.path.append(os.path.join(os.getcwd(),'..','..','Src','Utilities'))

from AOI import gridgen

xy1 = [-105.260432, 40.040073]
xy2 = [-105.253751, 40.036415]

mgrid= gridgen(xy1, xy2, stepsize=100)

#gg = gsvobject()
#
#[gg.getpanoid([[row['YY'], row['XX']]]) for ii, row in mgrid.iterrows()]
#
#imgobjs = [gsvobject().getpanoid(row['YY'], row['XX']) for ii, row in mgrid.iterrows()]
#
#img_data = []
#img_panos = []
#for ii, row in mgrid.iterrows():
#    g = gsvobject()
#    g.getpanoid(row['YY'], row['XX'])
#    if g.metadata['status']=='OK':
#        if g.metadata['pano_id'] not in img_panos:
#            img_panos.append(g.metadata['pano_id'])
#            g.getimage(heading = 0, pitch = 0)
#            img_data.append(g)