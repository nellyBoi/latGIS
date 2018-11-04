# -*- coding: utf-8 -*-
"""
Created on Sun Jun  20 13:52:39 2018

@author: Nelly

This class will predict the probable location of an object in frame t+1
from knowledge of the object location in frame t, the direction of intra-frame
camera travel, the line-of-sight and various optical and sensor parameters. 
This model will be used in intraframe tracking of objects, by aiding in the 
association of object with previous tracks. 

INPUT:
    (TO CLASS) W: estimated closest point of desired target to direction vector
        in ECEF coordinates (meters). Each object must be instantiated with W
        from this class.
    objRowCol: object row and column from frame t+1
        (1x2 list)
    frame_t1_ecef: camera coordinates for frame t in the rotated cartesian
        coordinate system
        (1x3 array)
    frame_t2_ecef: camera coordinates for frame t+1 in the rotated cartesian
        coordinate system
        (1x3 array)
    LOS: line-of-sight-vector in ECEF coordinates
        (1x3 array)
    LatLon: Lattitude and longitude of camera for frame_t1, used to orient 
        camera rotation in 3D space.
        (1x2 list)
        
OUTPUT:
    [ROW, COL] of the predicted position of an object in frame t+1
        (1x2 list)
    
ASSUMPTIONS:
    - LOS vector is constant from frame to frame. 
    - Direction vector must be within the field of view.

TO DO's: 
    - move the estimated 'closest dist. to object' from defined constant to
    a class input. Also, determine how this can be a variable, not const.
    
"""
import numpy as np
class Object_Location_Model:
    
    def __init__(self, W):
        
        # constants
        self.FOV = 30 # degrees
        self.sensorSize = [1024, 1024]
        self.rad2deg = 180/np.pi
        self.deg2rad = np.pi/180
        
        # calculated values
        self.focalLength = self.calcVirtualFocalLength()
        
        # variables to be moved out of _init__
        self.W_est = W # (m) : estimated closest dist. to obj. from D vector.
        
    
    def objectLocationPredictor(self, objRowCol, frame_t1_ecef, frame_t2_ecef, LOS, LatLon):
        
        '''This function will be used to predict the objects location in frame t+1 
        from from knowledge of frame t, various camera parameters and the necessary
        geometrical arguments.
        INPUT: 
            - objRowCol
            - frame_t1_ecef
            - frame_t2_ecef
            - LOS
            - LatLon
        '''
        
        # distance moved along direction vector
        deltaL = np.sqrt((frame_t2_ecef[0] - frame_t1_ecef[0])**2 + \
                         (frame_t2_ecef[1] - frame_t1_ecef[1])**2 + \
                         (frame_t2_ecef[2] - frame_t1_ecef[2])**2)
        # get direction of movement in camera coordinates
        [dirRow, dirCol] = self.getDirectionPixel(frame_t1_ecef, frame_t2_ecef, LOS, LatLon)
        directionPixel = [dirRow, dirCol]
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
            objAngle_t2 = np.arctan(self.W_est/L_t2)
            pixelsFromD = self.focalLength*np.tan(objAngle_t2)
            #calculate final position ob object in pixel values
            PIXEL_t2[sensorDir] = directionPixel[sensorDir] + sign*pixelsFromD
            
       
        return PIXEL_t2
    

    def getDirectionPixel(self, frame_t1_ecef, frame_t2_ecef, LOS, LatLon):
        
        '''This function will calculate to direction of the camera movement in
        pixel coordinates.
        INPUT:
            - frame_t1_ecef
            - frame_t2_ecef
            - LOS
            - LatLon
            '''
        # calculating virtual focal length, only if not calculated yet
        self.focalLength = self.calcVirtualFocalLength()
        # calculation direction vector in ECEF
        Dvec = frame_t2_ecef - frame_t1_ecef
        Dvec = Dvec/np.linalg.norm(Dvec)
        # find angle between LOS and D
        D_LOS_angle = self.angleBetweenVectors(LOS, Dvec)
        # find total offset in pixel values (direction of offset unknown at this time)
        totalOffset = self.calcPixelOffset(D_LOS_angle)
        # calculate normal of earth at current frame t
        normal = self.calculateNormal(LatLon)
        # rotate LOS and Dvec to coord system whose normal to earth would be 
        # N_tilda = <0,0,1>
        Dvec_tilda = self.rotateCoordsToTilda(Dvec, normal)
        LOS_tilda = self.rotateCoordsToTilda(LOS, normal)
        
        # find angle between D and (X_tilda, Y_tilda) plane
        # NOTE: to find, we measure from N_tilda = <0,0,1>
        D_xy_angle = np.pi/2 - self.angleBetweenVectors(Dvec_tilda, np.array((0,0,1)))
        
        # find angle between LOS and (X_tilda, Y_tilda) plane
        # NOTE: to find, we measure from N_tilda = <0,0,1>
        LOS_xy_angle = np.pi/2 - self.angleBetweenVectors(LOS_tilda, np.array((0,0,1)))
        
        # find difference from angles above to get row offset
        D_LOS_angleRow = D_xy_angle - LOS_xy_angle
        
        # this value is absolute, direction of offset is not determined here
        D_rowOffset = self.calcPixelOffset(D_LOS_angleRow)
        # calculate direction of offset with angle comparison against the normal
        if (D_LOS_angleRow > 0):
            ROW = np.floor(self.sensorSize[0])/2 - D_rowOffset
        else:
            ROW = np.floor(self.sensorSize[0])/2 + D_rowOffset
         
        SMALL_NUMBER = 0.00001   
        if (D_rowOffset - totalOffset > SMALL_NUMBER):
            print('ERROR: Sensor Model: Row offset calculated as greater than total offset')   
            return[[],[]]
            
        # use Pythagorean's theorem to get column offset 
        if (totalOffset > SMALL_NUMBER) and ((totalOffset - D_rowOffset)>0):
            D_colOffset = np.sqrt(totalOffset**2 - D_rowOffset**2)
        else:
            D_colOffset = 0
            
        # calculate direction of offset with cross product
        vecTemp = np.cross(Dvec_tilda, LOS_tilda)
        if (vecTemp[2] > 0):
            COL = np.floor(self.sensorSize[1])/2 + D_colOffset
        else:
            COL = np.floor(self.sensorSize[1])/2 - D_colOffset
            
        if (ROW < 0 or ROW > self.sensorSize[0]):
            print('WARNING: Sensor Model: Row prediction off sensor')
            
        if (COL < 0 or COL > self.sensorSize[1]):
            print('WARNING: Sensor Model: Col prediction off sensor')
            
        return [ROW, COL]
    
    def calculateNormal(self, LatLon):
        
        # LatLon should be 1x2 list
        Lat = self.deg2rad*LatLon[0]
        Lon = self.deg2rad*LatLon[1]
        
        normal = np.zeros((3,))
        normal[0] = np.cos(Lat)*np.cos(Lon)
        normal[1] = np.cos(Lat)*np.sin(Lon)
        normal[2] = np.sin(Lat)
        
        return normal
    
    '''angle returned in radians'''
    def angleBetweenVectors(self, vec1, vec2):
        
        angle = np.arccos((np.dot(vec1,vec2))/(np.linalg.norm(vec1)*np.linalg.norm(vec2)))
        return angle
    
    '''normal should rotate to <0, 0, 1>'''
    def rotateCoordsToTilda(self, coordsForRot, normal):
        
        ''' This function will rotate a coordinate vector to a system such that 
        the normal of the earth in the new system is <0,0,1>. This is used to 
        orient the camera in 3D space, since the assumption must be made that
        rows of the sensor are parallel to the earth while columns are orthogonal.
        
        '''
        
        # force normal to be unit vector 
        normal = normal/np.linalg.norm(normal)
        # force coordsForRot to be 3x1 for matrix multiplcations
        if coordsForRot.shape[0] != 3:
            print('Coordinates must be passed as a 3x1 or 3x0 array in Sensor Model')
            return []
        
        # force normal to be 3x1 for matrix multiplcations
        if normal.shape[0] != 3:
            print('Normal vector must be passed as a 3x1 or 3x0 array in Sensor Model')
            return []
        
        # if normal is already (1,0,0) then pass back the input coords
        if (normal[0] == 0 and normal[1] == 0 and normal[2]>0):
            return coordsForRot
        
        # find rotation angle about X
        angleX = np.arctan2(normal[1],normal[2])
        
        # rotation matrix about X
        Rx = np.array([[1, 0, 0], [0, np.cos(angleX), -np.sin(angleX)], \
                       [0, np.sin(angleX), np.cos(angleX)]])
        
        # temporary coords
        coordsTemp = np.matmul(Rx, coordsForRot)
        normalTemp = np.matmul(Rx, normal)
        
        # find rotation angle about Y
        angleY = -np.arctan2(normalTemp[0],normalTemp[2])
    
        Ry = np.array([[np.cos(angleY), 0, np.sin(angleY)], [0, 1, 0], \
                        [-np.sin(angleY), 0, np.cos(angleY)]])
    
        # rotations    
        coordsRotated = np.matmul(Ry, coordsTemp)
        normalRotated = np.matmul(Ry, normalTemp)
        
        # check to make sure that new normal is within error to <0, 0, 1>
        if (abs(normalRotated[0])>0.01 or abs(normalRotated[1])>0.01 or \
            abs(normalRotated[2] - 1)>0.01):
            print('WARNING: Normal = ' + str(normalRotated) + \
                  ', Normal should be [0, 0, 1]')
        
        return coordsRotated
    
    def calcVirtualFocalLength(self):
        '''Pixel units'''
        FOV = self.FOV
        # focal length calculation is based off 2nd sensor size value, numCols
        numCols = self.sensorSize[1]
        focalLength = numCols/(2*np.arctan(FOV/2))
        return focalLength
    
    def calcPixelOffset(self, angle):
        
        # NOTE: angle must be positive
        angle = np.absolute(angle)
        offset = (self.focalLength)*np.tan(angle)
        return offset
    
        
        
        
    
    
        
          
    
    
        
    
