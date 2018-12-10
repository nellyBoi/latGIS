# -*- coding: utf-8 -*-

'''
Author: Nelly Kane
Originated: 12.03.2018

Repo: latGIS
File: latGIS_containers.py

The defined containers for the latGIS Python architecture.

'''
import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)),'..','Triangulation'))

from pandas import DataFrame as df
import numpy as np
from typing import Tuple
from CONSTANTS import constants
from triangulate import minDistPoint_3D
from enu_to_ecef import enu2ecef
from coord_transfers import CoordTransfers


class CameraData:
    def __init__(self, LatLonEl: list, heading: float, pitch: float):
        # instance variable unique to each instance
        self.LatLonEl = LatLonEl   
        self.heading = heading
        self.pitch = pitch
        
'''
This class stores all information regarding an object searched in geo-coordinate
space. It will also, include functions to for coordinate transformations so those 
operations don't have to clutter up the algorithm.
Members:
    - object ID (generated from a static ID counter.)
    - Pandas.DataFrame of a list, size(capture points) of:
        - CameraData data per capture point
        - ENU vector per capture point
        - ECEF vector per capture point
        - triangulation results 
        - triangulation errors
    
Method:
    - new obseration
    - ENU to ECEF
    - triangulation
    - triangulation error
    
TODO:
    - change objectDataArray to __objectDataArray__ to signal privacy
    - write a results getter
    - adapt triangulation for all possible observation combinations
'''
        
class ObjectLocation:
    
    objID = 0 # object counter
    maxObsPerObj = 10 # maximum observations for each object
    deg2rad = np.pi/180 # degrees to radians
    focalLength = float
    
    coordTransfers = CoordTransfers() 
    
    
    def __init__(self, origCameraData: CameraData, origPixel: list):
        
        # calculate virtual focal length
        ObjectLocation.focalLength = ObjectLocation.calcVirtualFocalLength()
        
        # incrementing object counter
        ObjectLocation.objID += 1 # NOTE how the accessor is the class, not the object
        self.objID = ObjectLocation.objID
        
        # start Pandas.DataFrame
        columns = ['objID', 'cameraData', 'pixel', 'ecefPt','enuVec', 'ecefVec', 'objectLocationECEF',
                'objectLocationLLE', 'triangulationError']
        self.objectDataArray = df(columns = columns, index = 
            np.linspace(0, ObjectLocation.maxObsPerObj - 1, ObjectLocation.maxObsPerObj))
        
        self.objectDataArray['objID'][0] = self.objID
        self.objectDataArray['cameraData'][0] = origCameraData
        self.objectDataArray['pixel'][0] = origPixel
        
        # convert to ENU
        ObjectLocation.sensor_2_ENU(self, 0)
        
        # get ECEF vector of object location (NOTE: Object can be anywhere on this vector)
        ObjectLocation.ENU_2_ECEF(self, 0)
        
    
    def addNewObservation(self, cameraData: CameraData, pixel: list):
        
        curObs = self.objectDataArray['objID'].count() # current observation number for indexing
        
        if (curObs == ObjectLocation.maxObsPerObj):
            print('WARNING: Object list full, increase maximum observations')
            return
        
        self.objectDataArray['objID'][curObs] = self.objID
        self.objectDataArray['cameraData'][curObs] = cameraData
        self.objectDataArray['pixel'][curObs] = pixel
        
        # convert to ENU
        ObjectLocation.sensor_2_ENU(self,curObs)
        
        # get ECEF vector of object location (NOTE: Object can be anywhere on this vector)
        ObjectLocation.ENU_2_ECEF(self, curObs)
        
        # perform triangulation and get error
        ObjectLocation.triagulation(self, curObs)
        
        # compute object location Latitude, Longitude, Elevation
        ObjectLocation.getObjectLLE(self, curObs)
        
        return
    
    
    def sensor_2_ENU(self, curObs:int, degFlag : bool = True ):
        
        cameraData = self.objectDataArray['cameraData'][curObs]
        heading = cameraData.heading
        pitch = cameraData.pitch
        pixel = self.objectDataArray['pixel'][curObs]
        
        # degrees to radians, if (degFlag == True)
        if (degFlag == 1):    
            heading = heading*constants.deg2rad
            pitch = pitch*constants.deg2rad
            
        # calculate angle-to-target from north contributions from object pixel location
        pitchAdjust, headingAdjust = ObjectLocation.calcAngleOffsets(pixel)
        
        headingForRot = heading + headingAdjust
        pitchForRot = pitch + pitchAdjust
        
        # start from definition, ENU = <0, 1, 0>
        enuDef = np.array((0, 1, 0))
        
        # rotate about east by the pitch
        Rx = np.array([[1, 0, 0], 
                       [0, np.cos(pitchForRot), -np.sin(pitchForRot)], 
                       [0, np.sin(pitchForRot), np.cos(pitchForRot)]])
            
        ENU = np.matmul(Rx, enuDef)
            
        # rotate about north by the heading (NOTE: sign change since heading defined in CW)
        headingForRot = -headingForRot
        Rz = np.array([[np.cos(headingForRot), -np.sin(headingForRot), 0],
                        [np.sin(headingForRot), np.cos(headingForRot), 0], 
                        [0, 0, 1]])
        
        objENU = np.matmul(Rz, ENU) # NOTE: This should now be the object direction in ENU coords.
        self.objectDataArray['enuVec'][curObs] = objENU
        
        return 
    
    
    def calcAngleOffsets(pixel: list) -> Tuple[float, float]:
        
        # positive col offset pairs with an INCREASE in heading-to-target
        colPixelOffset = pixel[1] - float(constants.sensorSize[1]/2)
        colAngle = np.arctan(np.abs(colPixelOffset/ObjectLocation.focalLength))
        if (colPixelOffset < 0):
            colAngle = -colAngle
            
        # positive row offset pairs with a DECREASE in pitch-to-target
        rowPixelOffset = pixel[0] - float(constants.sensorSize[0]/2)
        rowAngle = np.arctan(np.abs(rowPixelOffset/ObjectLocation.focalLength))
        if (rowPixelOffset > 0):
            rowAngle = -rowAngle
            
        return rowAngle, colAngle 
    
    
    # This function will compute the ecef capture point and the ecef direction vector.
    def ENU_2_ECEF(self, curObs: int):
        
        cameraData = self.objectDataArray['cameraData'][curObs]
        LLE = cameraData.LatLonEl
        
        enuVec = self.objectDataArray['enuVec'][curObs] 
        
        # To create the ECEF vector there has to be two points in ECEF. The first one will
        # be at the ENU origin, the second one will be on the ENU vector. 
        xECEF1, yECEF1, zECEF1 = enu2ecef(0, 0, 0, LLE[0], LLE[1], LLE[2], deg = True)
        ptEcef = np.array((xECEF1, yECEF1, zECEF1))
        
        LARGE_NUMBER = 100000000
        xECEF2, yECEF2, zECEF2 = enu2ecef(LARGE_NUMBER*enuVec[0], LARGE_NUMBER*enuVec[1], LARGE_NUMBER*enuVec[2], 
                                          LLE[0], LLE[1], LLE[2], deg = True)
        
        xECEF = xECEF2 - xECEF1
        yECEF = yECEF2 - yECEF1
        zECEF = zECEF2 - zECEF1
        
        vecEcef = np.array((xECEF, yECEF, zECEF))
        vecEcef = vecEcef/np.linalg.norm(vecEcef)
        
        self.objectDataArray['ecefPt'][curObs] = ptEcef
        self.objectDataArray['ecefVec'][curObs] = vecEcef
        
        return
    
    def triagulation(self, curObs: int):
        
        # grabbing ECEF data from previous observation for triangulation
        # NOTE: TODO:: For now the triangulation will only be computed with data from the 
        # current observation and the previous observation. Adapt this to do triangulation
        # on all possible combinations in the list of observations and use the results 
        # of all of them to compute one final result.
        ecefPt1 = self.objectDataArray['ecefPt'][curObs-1]
        ecefVec1 = self.objectDataArray['ecefVec'][curObs-1]
        ecefPt2 = self.objectDataArray['ecefPt'][curObs]
        ecefVec2 = self.objectDataArray['ecefVec'][curObs]
        [objectLocationECEF, minDist] = minDistPoint_3D(ecefVec1, ecefPt1, ecefVec2, ecefPt2)
        
        self.objectDataArray['objectLocationECEF'][curObs] = objectLocationECEF
        
        # computing triangulation error
        ObjectLocation.triangulationError(self, curObs, ecefVec1, ecefVec2, minDist)
    
        return
    
    
    def triangulationError(self, curObs, vec1: np.array, vec2: np.array, distance: float):
        
        # TODO: Adapt this function when more than one triangulation can occur per observation
        
        if (distance == []):
            return
        # the error is currently (1/2)*minimumDistance/sin(angle between vectors)
        angle = np.arccos((np.dot(vec1,vec2))/(np.linalg.norm(vec1)*np.linalg.norm(vec2)))
    
        SMALL_NUMBER = 1e-8
        if (angle < SMALL_NUMBER):
            calcError = np.inf
        else:
            calcError = (1.0/2.0)*distance/np.sin(angle)
        
        self.objectDataArray['triangulationError'][curObs] = calcError
        
        return
    
    
    def getObjectLLE(self, curObs):
        
        objectLocationECEF = self.objectDataArray['objectLocationECEF'][curObs]
        
        if(objectLocationECEF != []):
            LLE = ObjectLocation.coordTransfers.ECEF_to_LLE([objectLocationECEF[0], objectLocationECEF[1], objectLocationECEF[2]])
        else:
            LLE = []
            
        self.objectDataArray['objectLocationLLE'][curObs] = LLE
        
        
    def calcVirtualFocalLength() -> float:
        '''Pixel units'''
        FOV = constants.FOV
        # focal length calculation is based off 2nd sensor size value, numCols
        numCols = constants.sensorSize[1]
        focalLength = numCols/(2*np.arctan(constants.deg2rad*FOV/2))
        return focalLength
        