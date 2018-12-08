# -*- coding: utf-8 -*-

'''
Author: Nelly Kane
Originated: 12.03.2018

Repo: latGIS
File: latGIS_containers.py

The defined containers for the latGIS Python architecture.

'''
from pandas import DataFrame as df
import numpy as np

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
'''
        
class ObjectLocation:
    
    objID = 0 # object counter
    maxObsPerObj = 10 # maximum observations for each object
    
    
    def __init__(self, origCameraData: CameraData, origPixel: list):
        
        # incrementing object counter
        ObjectLocation.objID += 1 # NOTE how the accessor is the class, not the object
        self.objID = ObjectLocation.objID
        
        # start Pandas.DataFrame
        columns = ['objID', 'cameraData', 'pixel' ,'enuVec', 'ecefVec', 'triangulationResults',
                'triangulationError']
        self.objectDataArray = df(columns = columns, index = 
            np.linspace(1, ObjectLocation.maxObsPerObj, ObjectLocation.maxObsPerObj))
        
        self.objectDataArray['objID'][0] = self.objID
        self.objectDataArray['cameraData'][0] = origCameraData
        self.objectDataArray['pixel'][0] = origPixel
        
    
        
    def addNewObservation(cameraData, pixel):
        pass
    
    def ENU_2_ECEF(ENU: list, LatLonEl: list) -> list:
        pass
    
    def triagulation():
        pass
    
    def triangulationError():
        pass