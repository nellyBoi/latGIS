# -*- coding: utf-8 -*-
"""
Created on Sun May 27 14:21:37 2018

@author: Nelly

unit tests for triangulation backend

This unit tests will ensure that the triangulation routine executes correctly.
There will be a total of 6 tests. 

1) Will tests parallel lines
2,3,4) Will tests lines in all 3 2D planes (XY, XZ, YZ). This is to tests all
axes independently. It is important to note that any non-parallel lines 
restricted to the same 2D planes will directly intersect, thus resulting in a 
closest distance of zero.
5) Skew lines in 3D space
6) Skey lines in 3D space such that the 'closest' points are located 'behind'
the input points (i.e. behind the cameras)

All outputs are hand-checked. A vaerification source should be used at a 
later point. 

"""
import unittest

from numpy import array, ndarray, abs
import pathlib
filepath = pathlib.Path(__file__).parent.absolute()

import os
import sys

sys.path.append(os.path.join(filepath, '..'))
from test_setup import setup
setup()
from util.triangulate import minDistPoint_3D

DOUBLE_TOL = 1e-5


########################################################################################################################

########################################################################################################################
class TriangulateTestCase(unittest.TestCase):

    def assertEqualsOnVector(self, vector: ndarray):
        """
        :param vector: input vector
        :return: pass if all components are smaller than DOUBLE_TOL.
        """
        self.assertTrue(abs(vector[0]) < DOUBLE_TOL)

    def test_parallel_lines(self):
        print('Triangulation: Unit Test 1')
        lineDir1 = array([0, 2, 0])
        linePt1 = array([1, 0, 0])
        lineDir2 = array([0, 1, 0])
        linePt2 = array([5, 0, 0])
        [minPt, minDist] = minDistPoint_3D(lineDir1, linePt1, lineDir2, linePt2)
        minDistCalc = 4
        minPtCalc = array([0, 0, 0])
        self.assertTrue(abs(minDist - minDistCalc) < DOUBLE_TOL)
        self.assertEqualsOnVector(minPt - minPtCalc)

    def test_2(self):
        # skew lines separated by a distance (in  XY-plane)
        print('Triangulation: Unit Test 2')
        lineDir1 = array([2, 1, 0])
        linePt1 = array([0, 0, 0])
        lineDir2 = array([-1, 1, 0])
        linePt2 = array([3, 0, 0])
        [minPt, minDist] = minDistPoint_3D(lineDir1, linePt1, lineDir2, linePt2)
        minDistCalc = 0
        minPtCalc = array([2, 1, 0])
        self.assertTrue(abs(minDist - minDistCalc) < DOUBLE_TOL)
        self.assertEqualsOnVector(minPt - minPtCalc)

    def test_3(self):
        # skew lines separated by a distance (in XZ-plane)
        print('Triangulation: Unit Test 3')
        lineDir1 = array([1, 0, 2])
        linePt1 = array([-4, 0, -2])
        lineDir2 = array([-1, 0, 0])
        linePt2 = array([5, 0, 2])
        [minPt, minDist] = minDistPoint_3D(lineDir1, linePt1, lineDir2, linePt2)
        minDistCalc = 0
        minPtCalc = array([-2, 0, 2])
        self.assertTrue(abs(minDist - minDistCalc) < DOUBLE_TOL)
        self.assertEqualsOnVector(minPt - minPtCalc)

    def test_4(self):
        # skew lines separated by a distance (in YZ-plane)
        print('Triangulation: Unit Test 4')
        lineDir1 = array([0, 1, -1])
        linePt1 = array([0, -2, 3])
        lineDir2 = array([0, -1, -1])
        linePt2 = array([0, 2, 3])
        [minPt, minDist] = minDistPoint_3D(lineDir1, linePt1, lineDir2, linePt2)
        minDistCalc = 0
        minPtCalc = array([0, 0, 1])
        self.assertTrue(abs(minDist - minDistCalc) < DOUBLE_TOL)
        self.assertEqualsOnVector(minPt - minPtCalc)

    def test_5(self):
        # skew lines separated by a distance (in 3D space)
        print('Triangulation: Unit Test 5')
        lineDir1 = array([-2, 0, 1])
        linePt1 = array([3, 2, 0])
        lineDir2 = array([5, 0, 1])
        linePt2 = array([-4, 0, 0])
        [minPt, minDist] = minDistPoint_3D(lineDir1, linePt1, lineDir2, linePt2)
        minDistCalc = 2
        minPtCalc = array([1, 1, 1])
        self.assertTrue(abs(minDist - minDistCalc) < DOUBLE_TOL)
        self.assertEqualsOnVector(minPt - minPtCalc)

    def test_6(self):
        # skew lines in 2D, intersect opposite of line of travel (intersection found
        # to be behind camera)
        print('Triangulation: Unit Test 6')
        lineDir1 = array([1, 1, 0])
        linePt1 = array([3, 0, 0])
        lineDir2 = array([-1, 1, 1])
        linePt2 = array([1, 0, 0])
        [minPt, minDist] = minDistPoint_3D(lineDir1, linePt1, lineDir2, linePt2)
        print('should be nan : ' + str(minPt) + ' ,    ' + str(minDist))

if __name__ == '__main__':
    unittest.main()