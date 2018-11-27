# -*- coding: utf-8 -*-
"""
Created on Wed Jun 20 17:03:24 2018

@author: Max

Test Comment for Commit and Push 11/22/2018

"""

def longbasedonlat(inlat):
    import math
    # Returns the number of degrees of longitude per meter at a given latitude
    earth_radius = 6378 # In KM
    degrees_to_radians = math.pi/180.0
    #radians_to_degrees = 180.0/math.pi
    cc = math.pi*(earth_radius*2)
    eqdist = cc/360
    rr = inlat*degrees_to_radians
    return 1/((math.cos(rr)*eqdist)*1000)


def gridgen(coordpair1, coordpair2, stepsize=1):
    #GENERATES A MESHGRID GIVEN TWO COORDINATE PAIRS AS DIAGONAL CORNERS, AND A STEP SIZE IN METERS
    # COORD PAIRS MUST BE SUPPLIED IN LON,LAT FORMAT TO MIRROR X,Y NOTATION
    minlat = min([abs(coordpair1[1]),abs(coordpair2[1])])
    lonstep = longbasedonlat(minlat)*stepsize
    latstep = (1/111111)*stepsize
    # COORDINATES SHOULD BE SUPPLIED IN PROJECTED COORDINATE SYSTEM
    from numpy import meshgrid, arange
    from pandas import DataFrame as dataf
    xx = arange(min([coordpair1[0], coordpair2[0]]), max([coordpair1[0], coordpair2[0]]), lonstep)
    yy = arange(min([coordpair1[1], coordpair2[1]]), max([coordpair1[1], coordpair2[1]]), latstep)
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

