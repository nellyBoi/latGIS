# -*- coding: utf-8 -*-

"""
Created on Sun Dec 15 19:07:22 2018

@author: Max Marno
"""
from pandas import DataFrame
import numpy as np
from PIL import Image
from io import BytesIO

# Import from latGIS_containers, but for now easier to reference here
class CameraData:
    def __init__(self, LatLonEl: list, heading: float, pitch: float):
        # instance variable unique to each instance
        self.LatLonEl = LatLonEl   
        self.heading = heading
        self.pitch = pitch

class image_obj:
    oid = 0     
    __cols = ['oid', 'cameradata', 'pix_coords', 'imagearray']         
    def __init__(self):

        self.features = DataFrame(columns = image_obj.__cols)

    def add_feature(self, pixelcoords:list, cameradata, imagearray, **kwargs):

        
        # Create new feature
        newfeature = dict.fromkeys(image_obj.__cols, 0)
        newfeature['oid'] = self.oid
        newfeature['pix_coords'] = pixelcoords
        newfeature['cameradata'] = cameradata
        newfeature['imagearray'] = imagearray

        if 'ftype' in kwargs:
            newfeature['ftype'] = kwargs['ftype']
        if 'panoid' in kwargs:
            newfeature['panoid'] = kwargs['panoid']
        if 'date' in kwargs:
            newfeature['date'] = kwargs['date']
        if 'datasource' in kwargs:
            newfeature['datasource'] = kwargs['date']
        self.features = self.features.append(newfeature, ignore_index=True, sort=False)
        
        # Increment object ID
        image_obj.oid += 1
        self.oid = image_obj.oid

    def showimage(self, image_array):
        try:
            img = Image.fromarray(image_array, 'RGB')
            img.show()
        except AttributeError:
            print('Image Array does not exist')

            
            
         

