# -*- coding: utf-8 -*-

"""
Created on Sun Dec  15 19:07:22 2018

@author: Max Marno
"""
from pandas import DataFrame
from numpy import ndarray

class image_obj:
    oid = 0     
    cols = ['ylat', 'xlon', 'zelv', 'img_shape', 'heading', 'pitch', 'pix_coords','ftype']         
    def __init__(self, imagearray, latlonelv, heading:float, pitch:float, **kwargs):
        self.exif = {}
        # Increment object ID
        image_obj.oid += 1
        self.oid = image_obj.oid
        # Image Metadata
        if type(imagearray) == ndarray:
            self.imagedata = imagearray
            self.exif['shape'] = imagearray.shape
        self.exif['LLE'] = latlonelv
        self.exif['heading'] = heading
        self.exif['pitch'] = pitch
        if 'datasource' in kwargs:
            self.exif['source'] = kwargs['datasource']
        if 'date' in kwargs:
            self.exif['date'] = kwargs['date']
        # DataFrame to store observed features
        #cols = ['ylat', 'xlon', 'zelv', 'img_shape', 'heading', 'pitch', 'pix_coords','ftype']
        self.features = DataFrame(columns = image_obj.cols)
    def add_feature(self, pixelcoords:list, **kwargs):
        newfeature = dict.fromkeys(image_obj.cols, 0)
        if pixelcoords[0] < self.exif['shape'][0] and pixelcoords[1] < self.exif['shape'][1]:
            newfeature['pix_coords'] = pixelcoords
            newfeature['ylat'],newfeature['xlon'],newfeature['zelv'] = self.exif['LLE'][0],self.exif['LLE'][1], self.exif['LLE'][2]
            newfeature['img_shape'] = self.exif['shape']
            newfeature['heading'] = self.exif['heading']
            newfeature['pitch'] = self.exif['pitch']
            if 'ftype' in kwargs:
                newfeature['ftype'] = kwargs['ftype']
            self.features.append(newfeature)
            
            
            
NEED TO APPEND THE NEW FEATURE DICT DIFFERENTLY 
'TypeError: Can only append a Series if ignore_index = True or if the Series has a name'
                
#        
#    def addobject
        
