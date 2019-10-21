# -*- coding: utf-8 -*-
import sys, os
sys.path.append(os.path.join(sys.path[0],'..','..','Src','Utilities'))
from util.enu_to_ecef import enu2ecef

'''
enu2ecef(e1: float, n1: float, u1: float,
             lat0: float, lon0: float, h0: float,
             deg: bool = True) -> Tuple[float, float, float]:
'''

e0 = 0
n0 = 0
u0 = 0
lat0 = 0
lon0 = 0
h0 = 0
deg0 = True

xECEF, yECEF, zECEF = enu2ecef(e0, n0, u0, lat0, lon0, h0, deg0)
