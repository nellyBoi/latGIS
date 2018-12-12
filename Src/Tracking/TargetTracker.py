# -*- coding: utf-8 -*-
import numpy as np
from munkres import Munkres, DISALLOWED_OBJ
from latGIS_containers import ObjectLocation, CameraData
from pandas import DataFrame as df
from Object_Location_Model import Object_Location_Model

# Do we need this or does the other file pull it in?
DISALLOWED = DISALLOWED_OBJ()
DISALLOWED_PRINTVAL = "D"

class TargetTracker:
    
    # static variables
    maxObservations = 25
    maxTracks = 50
    LARGE_VAL = 10000000
    SMALL_VAL = 1/1000000
    
    # instantiate the assignment algorithm
    assignmentAlgorithm = Munkres()
    
    # instantiate the object motion model
    objectMotion = Object_Location_Model()
    
    def __init__(self, gateSize: int):
        
        self.gateSize = gateSize # size of gate in pixels
        self.assignmentAlgorithm = Munkres()
        
        # start Pandas.DataFrame
        columns = ['trackID', 'ObjectLocation_instance']
        self.__trackDataArray = df(columns = columns, index = 
            np.linspace(0, TargetTracker.maxTracks - 1, TargetTracker.maxTracks))
        
        # This function passes in a list of 'observations' as pixels [row, col]
        # and a current CameraData instance associated with them. It attempts to associate
        # the new observations with tracks. For those observations that an association is
        # not made, new object instances will begin.
    def generateTracks(self, observations: list, curCameraData: CameraData) -> list:
        
        # grab size of current __trackDataArray
        curTrks = self.__trackDataArray['trackID'].count()
        
        # TODO:: Get all track ID's here
        
        # make a prediction for each current track, NOTE: the loop doesn't execute if curTrks = 0
        predictions = []
        for idx in np.arange(curTrks):
            
            trkObject = self.__trackDataArray['ObjectLocation_instance'][idx]
            trkCameraData = trkObject.getRecentCameraData()
            trkPixel = trkObject.getRecentPixel()
            
            predictedPixel = TargetTracker.objectMotion.objectLocationPredictor(objRowCol = trkPixel,
                camData1 = trkCameraData, camData2 = curCameraData)
            
            predictions.append(predictedPixel)
            
        # build cost matrix with observations and predictions
        costMatrix = TargetTracker.buildCostMatrix(self, observations, predictions)
        
        # run the association algorithm on the cost matrix
        indices = TargetTracker.assignmentAlgorithm.compute(costMatrix)
        
        # loop over indexes, if an index matches a track than add to that tracks ObjectLocation instance,
        # if an index is out of the track columns of the cost matrix than instantiate a new track and a 
        # new object. Finally, eliminate old tracks and add their ObjectLocation instances
        # to the list for output. ALSO can output result from each track as it is updated, output all tracks here!!
        # YOU ARE HERE
        
    def buildCostMatrix(self, observations: list, predictions: list) -> np.array:
        
        numObservations = len(observations)
        numTracks = len(predictions)
        
        # value of perfect overlap, zero distance between obs and track
        bestMatch = np.pi*self.gateSize**2
        
        # TODO if no current tracks than each obs starts it's own
        
        #TODO figure out best way to pass obs and trks and do type checking
        costMatrix = np.zeros((numObservations, numObservations + numTracks), dtype = float)
        
        # input will both be two dimensional lists
        for obsIdx in np.arange(numObservations):
            for trkIdx in np.arange( numTracks):
                curObs = observations[obsIdx] # should be a len 2 list here
                curTrk = predictions[trkIdx] # should be a len 2 list here
                
                # value of overlapping gates
                matchVal = self.gate(prediction = curTrk, observation = curObs)

                costVal = bestMatch - matchVal # note: if match = best, cost = 0
                costMatrix[obsIdx, trkIdx] = costVal
                
        # build right side of array
        for obsIdx in np.arange(numObservations):
             for obsIdx2 in np.arange(numTracks, numTracks + numObservations):
                 if (obsIdx == (obsIdx2 - numTracks)):
                     costMatrix[obsIdx, obsIdx2] = bestMatch
                 else:
                     costMatrix[obsIdx, obsIdx2] = TargetTracker.LARGE_VAL
    
        return costMatrix
    
    def gate(self, prediction: list, observation: list) -> float:
        
        rowPred = prediction[0]
        colPred = prediction[1]
        rowObs = observation[0]
        colObs = observation[1]
        
        # calculate distance from prediction to observation
        dist = np.sqrt((rowPred - rowObs)**2 + (colPred - colObs)**2)
        
        if (dist >= 2*self.gateSize):
            return 0
        else:
            # equation taken from 'http://mathworld.wolfram.com/Circle-CircleIntersection.html'
            R = self.gateSize
            A = 2*R**2*np.arccos(dist/(2*R)) - (1.0/2.0)* np.sqrt((dist**2)*(2*R - dist)*(2*R + dist))
            return A
    