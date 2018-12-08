# -*- coding: utf-8 -*-

import sys, os
import pandas as pd

sys.path.append(os.path.join(sys.path[0],'..','..','Src','Tracking'))
sys.path.append(os.path.join(sys.path[0],'..','..','Src','Utilities'))


from latGIS_containers import CameraData, ObjectLocation

camData = CameraData([0, 0, 10], 0, 0)

objObj = ObjectLocation(origCameraData = camData, origPixel = [512, 512])

# add a couple of objections 
camData1 = CameraData([21, 51, 171], 0, 90)
objObj.addNewObservation(cameraData = camData1, pixel = [712,512])


# print back data
dataFrame = objObj.objectDataArray

with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print(dataFrame)

camDataBack = dataFrame['cameraData'][0]
print(('LatLonEl: ' + str(camDataBack.LatLonEl)))
print(('heading: ' + str(camDataBack.heading)))
print(('pitch: ' + str(camDataBack.pitch)))

enuBack = dataFrame['enuVec'][0]
print(('ENU Vector: ' + str(enuBack)))
ecefBack = dataFrame['ecefVec'][0]
print(('ECEF Vector: ' + str(ecefBack)))

camDataBack = dataFrame['cameraData'][1]
print(('LatLonEl: ' + str(camDataBack.LatLonEl)))
print(('heading: ' + str(camDataBack.heading)))
print(('pitch: ' + str(camDataBack.pitch)))

enuBack = dataFrame['enuVec'][1]
print(('ENU Vector: ' + str(enuBack)))
ecefBack = dataFrame['ecefVec'][1]
print(('ECEF Vector: ' + str(ecefBack)))