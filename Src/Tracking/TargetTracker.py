# -*- coding: utf-8 -*-
import numpy as np
class TargetTracker:
    
    # static variables
    maxObservations = 25
    
    def __init__(self, gateSize: int):
        
        self.gateSize = gateSize # size of gate in pixels
        
        
    def gate(self, prediction: list, observation: list) -> float:
        
        rowPred = prediction[0]
        colPred = prediction[1]
        rowObs = observation[0]
        colObs = observation[1]
        
        # calculate distance from prediction to observation
        dist = np.sqrt((rowPred - rowObs)**2 + (colPred - colObs)**2)
        
        # equation taken from 'http://mathworld.wolfram.com/Circle-CircleIntersection.html'
        R = self.gateSize
        A = 2*R**2*np.arccos(dist/(2*R)) - (1.0/2.0)* np.sqrt((dist**2)*(2*R - dist)*(2*R + dist))
        return A
    