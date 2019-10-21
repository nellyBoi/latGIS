# -*- coding: utf-8 -*-
from latgis.util import enu_to_ecef

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

xECEF, yECEF, zECEF = enu_to_ecef.enu2ecef(e0, n0, u0, lat0, lon0, h0, deg0)
