# -*- coding: utf-8 -*-
"""
Created on 11/29/2018

@author: Nelly

This class will predict the probable location of an object in frame t2
from knowledge of the object location in frame t1, the direction of intra-frame
camera travel, the line-of-sight and various optical and sensor parameters. 
This model will be used in intraframe tracking of objects, by aiding in the 
association of object with previous tracks. 

MODIFIED: This version of the object location model differs from the original 
    in that it used the pitch and the heading to calculate the pixel associated 
    with the direction vector. 
    
heading: indicates the compass heading of the camera. Accepted values are from
 0 to 360 (both values indicating North, with 90 indicating East, and 180 South).
 
pitch: (default is 0) specifies the up or down angle of the camera relative to 
the Street View vehicle. This is often, but not always, flat horizontal. 
Positive values angle the camera up (with 90 degrees indicating straight up); 
negative values angle the camera down (with -90 indicating straight down).

CLASS DEFINATIONS:
    cameraData:
        LatLonEl: [Latitude (deg), Longitude (deg), Elevation(m)] -> List
        heading:  heading of image (deg or rad)
        pitch:    pitch of image (deg or rad)

INPUT:
    (TO CLASS) W: estimated closest point of desired target to direction vector
        in ECEF coordinates (meters). Each object must be instantiated with W
        from this class.
        
    objRowCol: object row and column from frame t+1
        ( 1x2 list )
        
    camData1: cameraData instance for frame 1.
    
    camData2: cameraData instance for frame 2.
    
    degFlag: True is camData heading and pitch in degrees.
        
OUTPUT:
    [ROW, COL] of the predicted position of an object in frame t+1
        (1x2 list)

ASSUMPTIONS: 
    - Constant Field-Of-View (FOV)
    - All objects detected with the same instance have same 'W' estimation. For
      applications with multiple 'W' applications, have multiple 'W's.

TODO: 
    - Currently using W (closest dist of obj. to D vector estimate) as a param
    that is held within the class. This may frequently change and will need to
    be variable once this class is used for more general targets. 
"""
import sys, os
sys.path.append(os.path.join(sys.path[0],'..','Utilities'))
import numpy as np
from enu_to_ecef import enu2ecef
from rotation import Rotate
from coord_transfers import CoordTransfers

class cameraData:
    def __init__(self, LatLonEl: list, heading: float, pitch: float):
        # instance variable unique to each instance
        self.LatLonEl = LatLonEl   
        self.heading = heading
        self.pitch = pitch
        
  
class Object_Location_Model:
    
    def __init__(self, W: float):
        
        # constants
        self.FOV = 30 # degrees
        self.sensorSize = [1024, 1024]
        self.rad2deg = 180/np.pi
        self.deg2rad = np.pi/180
        
        # calculated values
        self.focalLength = self.calcVirtualFocalLength()
        
        # variables to be moved out of _init__
        self.W_est = W # (m) : estimated closest dist. to obj. from D vector.
        
    
    def objectLocationPredictor(self, objRowCol: list, camData1: cameraData, camData2: cameraData, degFlag : bool = False )-> list:
        
        '''This function will be used to predict the objects location in frame t+1 
        from from knowledge of frame t, various camera parameters and the necessary
        geometrical arguments.
        INPUT: 
            - objRowCol ( in frame 1 )
            - camData1 ( degrees )
            - camData2 ( degrees )
            - degFlag ( degrees )

        '''
        # TODO: this should be moved
        coordTransfers = CoordTransfers() 
        # transfer Latitude, Longitude to ECEF, converted to arrays
        frame_t1_ecef = np.asarray(coordTransfers.LLE_to_ECEF(LLE = camData1.LatLonEl))
        frame_t2_ecef = np.asarray(coordTransfers.LLE_to_ECEF(LLE = camData2.LatLonEl))
        
        # degrees to radians, if (degFlag == True)
        if (degFlag == 1):    
            heading_t1 = camData1.heading*self.deg2rad
            pitch_t1 = camData1.pitch*self.deg2rad
            heading_t2 = camData2.heading*self.deg2rad
            pitch_t2 = camData2.pitch*self.deg2rad
        else:
            heading_t1 = camData1.heading
            pitch_t1 = camData1.pitch
            heading_t2 = camData2.heading
            pitch_t2 = camData2.pitch
        
        # distance moved along direction vector
        deltaL = np.sqrt((frame_t2_ecef[0] - frame_t1_ecef[0])**2 + \
                         (frame_t2_ecef[1] - frame_t1_ecef[1])**2 + \
                         (frame_t2_ecef[2] - frame_t1_ecef[2])**2)
        
        # if the camera has not moved place the direction pixel in the center of the image
        if (deltaL == 0):
            directionPixel = [self.sensorSize[0]/2, self.sensorSize[1]/2]
        else:
            # get direction of movement in camera coordinates
            directionPixel = self.getDirectionPixel(frame_t1_ecef, frame_t2_ecef, heading_t1,
                                                    pitch_t1, camData1.LatLonEl)

        # TODO: solve issue if heading is close to 360 degrees
    
        
        PIXEL_t2 = [[],[]]
        for sensorDir in [0,1]:
        
            objOffset = np.abs(objRowCol[sensorDir] - directionPixel[sensorDir]) # object pixels from dir. pixel
            objAngle = np.arctan(objOffset/self.focalLength) # angle from direction vec
            
            # get direction of offset
            if (objRowCol[sensorDir] - directionPixel[sensorDir]) < 0:
                sign = -1.0
            else:
                sign = 1.0
            # calc estimated length, NOTE: This is not dist. to target, but dist
            # on D vector's closest point to target.
            SMALL_NUMBER = 0.00001
            if np.abs(objAngle) > SMALL_NUMBER:
                L_est = self.W_est/(np.tan(objAngle))
            else:
                L_est = 1/SMALL_NUMBER
            # since direction vector is within the FOV, the new length must be 
            # shorter than the previous length.
            L_t2 = L_est - deltaL
            # if we have passed to object and the new L is negative, the angle
            # may be nagative and will need to be adjusted by PI.
            if (L_t2 < 0):
                objAngle_t2 = np.pi - np.abs(np.arctan(self.W_est/L_t2))
            else:
                objAngle_t2 = np.abs(np.arctan(self.W_est/L_t2))
            
            # correct for heading and pitch
            if (sensorDir == 0):
                # add to obj angle before computing pixel offset
                # NOTE: The sign of this value represents object pixel > direction pixel
                sensorOrientCorrectAng = sign*objAngle_t2 + (pitch_t2 - pitch_t1)
            
                
            else:
                sensorOrientCorrectAng = sign*objAngle_t2 + (heading_t1 - heading_t2)
            
            # if angle from LOS to object if greater than pi/2 object cannot even
            # project onto the same plane as the focal plane.
            if (sensorOrientCorrectAng > np.pi/2):
                sensorOrientCorrect = np.nan
            else:
                #calculate final position ob object in pixel values
                sensorOrientCorrectAngSign = np.sign(sensorOrientCorrectAng)
                sensorOrientCorrect = (sensorOrientCorrectAngSign*self.focalLength*
                                       np.tan(np.abs(sensorOrientCorrectAng)))
                
            PIXEL_t2[sensorDir] = directionPixel[sensorDir] + sensorOrientCorrect
              
        return PIXEL_t2
    

    def getDirectionPixel(self, frame_t1_ecef: np.ndarray, frame_t2_ecef: np.ndarray,
                          heading: float, pitch: float, LatLonEl: list)-> list:
        
        '''This function will calculate to direction of the camera movement in
        pixel coordinates.
        INPUT:
            - frame_t1_ecef
            - frame_t2_ecef
            - heading
            - pitch
            - LatLonEl
        OUTPUT:
            - direction pixel [ row , col ]
            '''
        
        # get normal of earth at current frame t
        Normal = self.calculateNormal(LatLonEl[0:2])
        
        # get North vector at current frame t in ECEF
        North = self.getNorthECEF(LatLonEl)
        
        # rotate North about Normal by heading degrees to get LOS, zero pitch
        # NOTE: Since the current rotation routine uses two points rather than a
        # vector to define the rotation axes we will solve for two points on
        # Normal, p0: ECEF coord of camera, and p1: ECEF coord of camera + some 
        # distance along the Normal. p0 is frame_t1_ecef
        p1x = frame_t1_ecef[0] + 1000*Normal[0]
        p1y = frame_t1_ecef[1] + 1000*Normal[1]
        p1z = frame_t1_ecef[2] + 1000*Normal[2]
        # TODO: There is an error here with certain rotations
        LOS_noPitch = Rotate(North, frame_t1_ecef, [p1x, p1y, p1z], heading) 
        LOS_noPitch = LOS_noPitch/np.linalg.norm(LOS_noPitch)
        
        # calculation direction vector in ECEF
        Dvec = frame_t2_ecef - frame_t1_ecef
        Dvec = Dvec/np.linalg.norm(Dvec)
        
        # find angle between LOS (no pitch) and Direction vector
        D_LOS_angle = self.angleBetweenVectors(LOS_noPitch, Dvec)

        # find column offset in pixel values (direction of offset unknown at this time)
        columnOffset = self.calcPixelOffset(D_LOS_angle)

        # calculate direction of offset with angle comparison against the normal
        vecTemp = np.cross(Dvec, LOS_noPitch)
        angleTemp = self.angleBetweenVectors(vecTemp, Normal)
        
        if (angleTemp > np.pi/2):
            COL = np.floor(self.sensorSize[1])/2 - columnOffset
        else:
            COL = np.floor(self.sensorSize[1])/2 + columnOffset
         
        # use pitch directly to get ROW
        if (pitch != 0): 
            rowOffset = self.calcPixelOffset(np.abs(pitch))
            if (pitch > 0):
                ROW = np.floor(self.sensorSize[0])/2 + rowOffset
            else:
                ROW = np.floor(self.sensorSize[0])/2 - rowOffset
            
        else:
            ROW = np.floor(self.sensorSize[0])/2
            
        return [ROW, COL]
    
    
    def calculateNormal(self, LatLonEl):
        
        # LatLon should be 1x2 list
        Lat = self.deg2rad*LatLonEl[0]
        Lon = self.deg2rad*LatLonEl[1]
        
        normal = np.zeros((3,))
        normal[0] = np.cos(Lat)*np.cos(Lon)
        normal[1] = np.cos(Lat)*np.sin(Lon)
        normal[2] = np.sin(Lat)
        
        return normal
    
    '''angle returned in radians'''
    def angleBetweenVectors(self, vec1, vec2):
        
        angle = np.arccos((np.dot(vec1,vec2))/(np.linalg.norm(vec1)*np.linalg.norm(vec2)))
        return angle
    
    
    def calcVirtualFocalLength(self):
        '''Pixel units'''
        FOV = self.FOV
        # focal length calculation is based off 2nd sensor size value, numCols
        numCols = self.sensorSize[1]
        focalLength = numCols/(2*np.arctan(self.deg2rad*FOV/2))
        return focalLength
    
    
    def calcPixelOffset(self, angle):
        
        # NOTE: angle must be positive
        angle = np.absolute(angle)
        offset = (self.focalLength)*np.tan(angle)
        return offset
    
    
    def getNorthECEF(self, LatLonEl: list) -> np.ndarray:
        
        # create p0, origin of ENU in ECEF
        p0x, p0y, p0z = enu2ecef(0, 0, 0, LatLonEl[0], LatLonEl[1], LatLonEl[2])
        # create p1, point on North axis of ENU in ECEF
        p1x, p1y, p1z = enu2ecef(0, 1000, 0, LatLonEl[0], LatLonEl[1], LatLonEl[2])
        
        northECEF = np.array([(p1x - p0x), (p1y - p0y), (p1z - p0z)])
        #normalize
        return northECEF # turn on to normalize / np.linalg.norm(northECEF)
        
