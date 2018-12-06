# -*- coding: utf-8 -*-
"""
Created on Tue May 22 01:25:39 2018

@author: Nelly 

This routine will find the closest point between two skew lines in 3D space. The
closest point will be defined as the average of the closest point on line 1 and 
the closest point on line 2. The closest points will then be tested to ensure 
that they are not located in the direction opposite of the direction LOS vectors.

NOTES: Single line-pair inputs for now, can generalize to n pairs if needed.

Inputs:
    vec1: 1x3 or 3x1 array representing cartesian line vector of line 1.
    pt1: A point on line 1.
    vec2: 1x3 or 3x1 array representing cartesian line vector of line 2. 
    pt2: A point on line 2.
        
Outputs:
    list[minDistPt, minDist]
    minDistPt: The point between the two lines in 3D space that lies closest to 
        each line. Defined as the average between the respective closest point
        in each line. (Inf if input lines are parallel)
    minDist: The minimum distance between the two input lines, crossing through
        minDistPt.
"""
from numpy import cross, dot, array
from numpy.linalg import norm
from math import sqrt

def minDistPoint_3D(vec1, pt1, vec2, pt2):
    
    # ensure inputs are correct size
    if (vec1.shape[0] != 3):
        print('ERROR: Input 1 to minDistPoint_3D must be size (3,)')
        return [[], []]
    if (pt1.shape[0] != 3):
        print('ERROR: Input 2 to minDistPoint_3D must be size (3,)')
        return [[], []]
    if (vec2.shape[0] != 3):
        print('ERROR: Input 3 to minDistPoint_3D must be size (3,)')
        return [[], []]
    if (pt2.shape[0] != 3):
        print('ERROR: Input 4 to minDistPoint_3D must be size (3,)')
        return [[], []]
        
    # force each vector to be a unit vector
    vec1 = vec1/(sqrt(vec1[0]**2 + vec1[1]**2 + vec1[2]**2))
    vec2 = vec2/(sqrt(vec2[0]**2 + vec2[1]**2 + vec2[2]**2))
    
    # check for parallel lines
    if (norm(cross(vec1, vec2)) == 0):
        print('Vectors ' + str(vec1) + ' and ' + str(vec2) + ' are parallel')
        # calculate min dist of parallel lines
        minDist = norm(cross(vec1, pt2 - pt1))
        return [array([0,0,0]),minDist]
    
    # compute skew line's closest point
    '''Computation notes'''
    # vec1: direction 1, pt1: initial point 1
    # vec2: direction 2, pt2: initial point 2
    # first, the points at which each vector is at closest proximity is found
    # D: point from line 1, E: point frokmm line 2
    c = pt2 - pt1
    numerator1 = -(dot(vec1,vec2)*dot(vec2,c)) + (dot(vec1,c)*dot(vec2, vec2))
    numerator2 = (dot(vec1,vec2)*dot(vec1,c)) - (dot(vec2,c)*dot(vec1, vec1))
    
    denominator = (dot(vec1,vec1)*dot(vec2,vec2)) - (dot(vec1,vec2)*dot(vec1, vec2))
    D = pt1 + vec1*(numerator1/denominator)
    E = pt2 + vec2*(numerator2/denominator)
    
    minDistPt = (D + E)/2
    minDist =  norm(E - D)
    
    # test that the closest points are not located behind the input points 
    # (i.e. - behind the cameras)
    if (dot((minDistPt - pt1), vec1)) < 0 or (dot((minDistPt - pt2), vec2) < 0):
        print('ERROR: Cartesian Coord. Evaluated To Behind Camera')
        return [[],[]]
    
    
    return minDistPt, minDist


