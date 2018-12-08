# -*- coding: utf-8 -*-

import sys, os
import pandas as pd

sys.path.append(os.path.join(sys.path[0],'..','..','Src','Tracking'))
sys.path.append(os.path.join(sys.path[0],'..','..','Src','Utilities'))

from latGIS_containers import CameraData, ObjectLocation

camData = CameraData([12, 15, 17], 23, 56)

objObj = ObjectLocation(origCameraData = camData, origPixel = [21, 32])

# add a couple of objections 
camData1 = CameraData([121, 151, 171], 231, 561)
objObj.addNewObservation(cameraData = camData1, pixel = [455,544])

# print back data
dataFrame = objObj.objectDataArray

with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print(dataFrame)

camDataBack = dataFrame['cameraData'][0]
print(('LatLonEl: ' + str(camDataBack.LatLonEl)))
print(('heading: ' + str(camDataBack.heading)))
print(('pitch: ' + str(camDataBack.pitch)))

camDataBack = dataFrame['cameraData'][1]
print(('LatLonEl: ' + str(camDataBack.LatLonEl)))
print(('heading: ' + str(camDataBack.heading)))
print(('pitch: ' + str(camDataBack.pitch)))


