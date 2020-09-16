#!/usr/bin/env python3
"""
Created on Sun Jun 24 20:06:30 2018

@author: johnnelsonkane

test_object_location_model.py

This unit test will check the 'Object_Location_Model' in which an objects 
movement from image to image is predicted.

"""
import numpy as np
import unittest
import matplotlib.pyplot as plt

from latgis.util.coord_transfers import CoordTransfers
from latgis.position_predict import ObjectLocationModel
from latgis.location import CameraData

CT = CoordTransfers()


########################################################################################################################
def plot_results(start_pixel: list, pixel_out: list) -> None:
    """
    :param start_pixel:
    :param pixel_out:
    :return:
    """
    plt.figure()
    v = [1, 1024, 1, 1024]
    plt.axis(v)
    # maintaining camera coordinate system
    plt.ylim(1024, 1)
    plt.scatter(start_pixel[1], start_pixel[0], color='b')
    plt.scatter(pixel_out[1], pixel_out[0], color='r')
    plt.legend(['Object t1', 'Object t2'])
    plt.xlabel('COLUMN')
    plt.ylabel('ROW')
    plt.show()


########################################################################################################################
class MyTestCase(unittest.TestCase):

    ####################################################################################################################
    def test_1(self):

        print('TEST 1: Object along direction of travel (prime meridian')

        objRowCol = [512, 512]

        locModel = ObjectLocationModel(2)
        # We will start in ECEF for distance and convert to LLE for function input.
        ecef1 = np.array((6378137, 0, 0))  # meters
        ecef2 = np.array((6378137, 0, 50))  # meters, due north by 5 meters
        LLE1 = CT.ECEF_to_LLE(ecef1)
        LLE2 = CT.ECEF_to_LLE(ecef2)

        cam1 = CameraData(LatLonEl=LLE1, heading=0, pitch=0)
        cam2 = CameraData(LatLonEl=LLE2, heading=0, pitch=0)

        PIXELS_OUT = locModel.objectLocationPredictor(objRowCol, cam1, cam2, degFlag=True)

        self.assertEqual(np.abs(PIXELS_OUT[0] - objRowCol[0]) < 1, True)
        self.assertEqual(np.abs(PIXELS_OUT[1] - objRowCol[1]) < 1, True)

        plot_results(start_pixel = objRowCol, pixel_out = PIXELS_OUT)

    def test_2(self):
        print('TEST 2: Hand calculated pixels for a regular step')

        locModel = ObjectLocationModel(1)
        objRowCol = [454, 454]

        # We will start in ECEF for distance and convert to LLE for function input.
        ecef1 = np.array((6378137, 0, 0))  # meters
        ecef2 = np.array((6378137, 0, 30))  # meters, due north by 5 meters
        LLE1 = CT.ECEF_to_LLE(ecef1)
        LLE2 = CT.ECEF_to_LLE(ecef2)

        cam1 = CameraData(LatLonEl=LLE1, heading=0, pitch=0)
        cam2 = CameraData(LatLonEl=LLE2, heading=0, pitch=0)

        PIXELS_OUT = locModel.objectLocationPredictor(objRowCol, cam1, cam2, degFlag=True)

        self.assertTrue(np.abs(PIXELS_OUT[0] - 66) < 1)
        self.assertTrue(np.abs(PIXELS_OUT[1] - 66) < 1)

        plot_results(start_pixel=objRowCol, pixel_out=PIXELS_OUT)

    def test_3(self):
        print('TEST 3: One more boresite test, nonzero lats and longs')

        locModel = ObjectLocationModel(1)
        objRowCol = [512, 512]

        # We will start in ECEF for distance and convert to LLE for function input.
        ecef1 = np.array((3.9054825307866509e-10, 6378137.0, 0.0))  # meters
        ecef2 = np.array((3.9054825307866509e-10 + 30, 6378137.0, 0.0))  # meters
        LLE1 = CT.ECEF_to_LLE(ecef1)
        LLE2 = CT.ECEF_to_LLE(ecef2)

        cam1 = CameraData(LatLonEl=LLE1, heading=270, pitch=0)
        cam2 = CameraData(LatLonEl=LLE2, heading=270, pitch=0)

        PIXELS_OUT = locModel.objectLocationPredictor(objRowCol, cam1, cam2, degFlag=True)

        self.assertTrue(np.abs(PIXELS_OUT[0] - objRowCol[0]) < 1)
        self.assertTrue(np.abs(PIXELS_OUT[1] - objRowCol[1]) < 1)

        plot_results(start_pixel=objRowCol, pixel_out=PIXELS_OUT)


########################################################################################################################
if __name__ == '__main__':
    unittest.main()

