# -*- coding: utf-8 -*-
"""
Created on Wed Jun 20 17:03:24 2018

@author: Max
"""


#   THIS FUNCTION GENERATES A MESHGRID GIVEN TWO COORDINATE PAIRS AS DIAGONAL CORNERS, AND A STEP SIZE
def gridgen(coordpair1, coordpair2, stepsize=1):
    # COORDINATES SHOULD BE SUPPLIED IN PROJECTED COORDINATE SYSTEM
    from numpy import meshgrid, arange
    from pandas import DataFrame as dataf
    xx = arange(min([coordpair1[0], coordpair2[0]]), max([coordpair1[0], coordpair2[0]]), stepsize)
    yy = arange(min([coordpair1[1], coordpair2[1]]), max([coordpair1[1], coordpair2[1]]), stepsize)
    xxg, yyg = meshgrid(xx, yy, indexing = 'ij')
    
    columnNames = ['XX', 'YY']
    df = dataf(columns = columnNames)
    df['XX'] = xxg.ravel()
    df['YY'] = yyg.ravel()
    return df


#   PROJECTS AN XY COORDINATE PAIR GIVEN AN INPUT AND OUTPUT ESPG
def projcoords(inepsg, outepsg, xycoords):
    from pyproj import transform, Proj
    # WGS84 = epsg 4326
    # World Equidistant Cylindrical = epsg 4087
    incoordsys = Proj(init='epsg:{}'.format(inepsg))
    outcoordsys = Proj(init='epsg:{}'.format(outepsg))
    return transform(p1=incoordsys, p2=outcoordsys, x=xycoords[0], y=xycoords[1])

