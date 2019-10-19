# -*- coding: utf-8 -*-
"""
Nelly Kane
10.18.2019

TargetTracker.py
"""
import numpy as np
from munkres import Munkres
from lat_gis import ObjectLocation, CameraData
from pandas import DataFrame as df
from ObjectLocationModel import ObjectLocationModel

########################################################################################################################
class TargetTracker:
    """
    A class to compute object-to-object associations between frames with knowledge of sensor location/orientation 
    metadata and a predictive model approximating where an object might appear in a future frame given a current frame.
    """
    # static variables
    maxObservations = 25
    maxTracks = 50
    LARGE_VAL = np.inf
    SMALL_VAL = 1/LARGE_VAL
    
    # instantiate the assignment algorithm
    assignmentAlgorithm = Munkres()
    
    ####################################################################################################################
    def __init__(self, gateSize: int, distToDVec: float):
        """
        Constructor
            gateSize: circular gate size used by the cost matrix to compute possible associations
            distToDVec: shortest distance from object to direction vector (vector in 3D space from camera pos t to t+1) 
        """
        self.gateSize = gateSize # size of gate in pixels
        
        # instantiate the object motion model
        self.objectMotion = ObjectLocationModel(W = distToDVec) 
        
        # start Pandas.DataFrame
        columns = ['trackID', 'ObjectLocation_instance']
        self.__trackDataArray = df(columns = columns, index = 
            np.linspace(0, TargetTracker.maxTracks - 1, TargetTracker.maxTracks))
        
    ####################################################################################################################
    def generateTracks(self, observations: list, curCameraData: CameraData) -> list:
        """
        This function passes in a list of 'observations' as pixels [row, col] and a current CameraData instance 
        associated with them. It attempts to associate the new observations with tracks. For those observations that an 
        association is not made, new object instances will begin.
            observations: list of [row, col]  lists representing objects
            curCameraData: CameraData instance associated with observations
        """
        # for output
        results = []
        
        # grab size of current __trackDataArray
        curTrks = self.__trackDataArray['trackID'].count()
        
        # Get track ID's. NOTE: This is a list. trackIDs
        trackIDs = np.array(self.__trackDataArray[self.__trackDataArray['trackID'].notnull()]['trackID']).tolist()
        
        # NOTE: This will be used to remove unused tracks at the end. As tracks are used they will be
        # removed from this list, and the remaining list will be removed from self.__trackDataArray
        trackIDsUnused = trackIDs.copy()
        
        # make a prediction for each current track, NOTE: the loop doesn't execute if curTrks = 0
        predictions = []
        for idx in np.arange(curTrks):
            
            trkObject = self.__trackDataArray['ObjectLocation_instance'][idx]
            trkCameraData = trkObject.getRecentCameraData()
            trkPixel = trkObject.getRecentPixel()
            
            predictedPixel = self.objectMotion.objectLocationPredictor(objRowCol = trkPixel,
                camData1 = trkCameraData, camData2 = curCameraData)
            
            predictions.append(predictedPixel)
            
        # build cost matrix with observations and predictions
        costMatrix = self.buildCostMatrix(observations, predictions)
        
        # run the association algorithm on the cost matrix
        indices = TargetTracker.assignmentAlgorithm.compute(costMatrix)
        
        # loop over indexes, if an index matches a track than add to that tracks ObjectLocation instance,
        # if an index is out of the track columns of the cost matrix than instantiate a new track and a 
        # new object. Finally, eliminate old tracks and add their ObjectLocation instances
        # to the list for output. ALSO can output result from each track as it is updated, output all tracks here!!
        # YOU ARE HERE
        for idx in indices:
            
            obsIdx = idx[0]
            predIdx = idx[1]
            
            if (predIdx) < len(trackIDs):
                # match trackID to observation, update ObjectLocation object with camera data and pixel
                trackID = self.__trackDataArray['trackID'][predIdx]
                trackIDidx = int(np.where(self.__trackDataArray['trackID'] == trackID)[0])
                
                # TODO: PASS BY REFERENCE
                self.__trackDataArray['ObjectLocation_instance'][trackIDidx].addNewObservation(
                        cameraData = curCameraData, pixel = observations[obsIdx])
                
                # remove used track from unused list
                trackIDsUnused.remove(trackID)
                
                # add object ID and location and error updates to the list of results for end of generateTracks call
                curResults = self.__trackDataArray['ObjectLocation_instance'][trackIDidx].getResults()
                results.append(curResults)
                
            else:
                # instantiate new Object, let object create track ID, once it instantiates a new ObjectLocation object
                newObj = ObjectLocation(origCameraData = curCameraData, origPixel = observations[obsIdx])
                newID = newObj.objID
                
                # TODO: PASS BY REFERENCE
                self.__trackDataArray['trackID'] = newID
                self.__trackDataArray['ObjectLocation_instance'][curTrks  + idx] = newObj
                
        # remove tracks that were NOT updated from the track list
        for dropID in trackIDsUnused:
            dropIDidx = int(np.where(self.__trackDataArray['trackID'] == dropID)[0])
            self.__trackDataArray = self.__trackDataArray.drop(dropIDidx)
            
        return results

    ####################################################################################################################         
    def buildCostMatrix(self, observations: list, predictions: list, printMatrix: bool = False) -> np.array:
        """
        construction of the cost matrix as a numpy array. Size: [number obs, number obs + num current tracks]
        """
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

                # TODO revisit this
                if (matchVal == 0):
                    costVal = np.inf
                else:
                    costVal = bestMatch - matchVal # note: if match = best, cost = 0
                costMatrix[obsIdx, trkIdx] = costVal
                
        # build right side of array
        for obsIdx in np.arange(numObservations):
             for obsIdx2 in np.arange(numTracks, numTracks + numObservations):
                 if (obsIdx == (obsIdx2 - numTracks)):
                     costMatrix[obsIdx, obsIdx2] = bestMatch
                 else:
                     costMatrix[obsIdx, obsIdx2] = TargetTracker.LARGE_VAL
    
        if (printMatrix is True):
            TargetTracker.printArray(costMatrix)
        
        return costMatrix
    
    ####################################################################################################################
    def gate(self, prediction: list, observation: list) -> float:
        """
        compute gate for given prediction and observation. A gate is considered to be the overlap of two circles of
        radius 'gateSize' centered at prediction and observation respectively. The more accurate the model used for 
        predictions the tighter the game size can be. If there is no overlap then no association can be made and this
        returns a 0 (meaning a new track has to start itself)
            prediction: [row, col] list
            observation: [row, col] list
        """
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
    
    ####################################################################################################################
    def printArray(array: np.array):
        """
        Static method to print cost matrix.
        """
        np.set_printoptions(precision=3)
        print(array)
            
        return
        