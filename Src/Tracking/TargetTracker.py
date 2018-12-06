# -*- coding: utf-8 -*-
import numpy as np
from munkres import Munkres


class TargetTracker:
    
    # static variables
    maxObservations = 25
    LARGE_VAL = 10000000
    
    def __init__(self, gateSize: int):
        
        self.gateSize = gateSize # size of gate in pixels
        self.assignmentAlgorithm = Munkres()
        # TODO deal with track ID's, data storage, and do we do triangulation 
        # here or do we save that for somewhere else?
        
    def generateTracks(self, observations: list, currentTracks: list) -> list:
        # this function ingests a list of observations in pixel (row, col) 
        # coordinates and a list of current track predictions in (row, col) 
        # coordinates and using a list of TODO, answer this.
        costMatrix = self.buildCostMatrix(observations, currentTracks)
        indexes = self.assignmentAlgorithm.compute(costMatrix) 
        
        
    def buildCostMatrix(self, observations: list, currentTracks: list) -> np.array:
        
        numObservations = len(observations)
        numTracks = len(currentTracks)
        
        # value of perfect overlap, zero distance between obs and track
        bestMatch = np.pi*self.gateSize**2
        
        # TODO if no current tracks than each obs starts it's own
        
        #TODO figure out best way to pass obs and trks and do type checking
        costMatrix = np.zeros((numObservations, numObservations + numTracks), dtype = float)
        
        # input will both be two dimensional lists
        for obsIdx in np.arange(numObservations):
            for trkIdx in np.arange( numTracks):
                curObs = observations[obsIdx] # should be a len 2 list here
                curTrk = currentTracks[trkIdx] # should be a len 2 list here
                
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
    