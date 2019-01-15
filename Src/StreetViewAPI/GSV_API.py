# -*- coding: utf-8 -*-
"""
Created on Sun Dec  9 18:37:43 2018

@author: Max Marno

Interface to Google Streetview API

Note: some methods are predicated on results from other methods, ie
'getimage' cannot be run until the panoid has been fetched, and 'showimage'
cannot be run until the image has been fetched
"""

from ggapikeydoc import GoogleAPIKey
from pandas import DataFrame
import requests
import os
import numpy as np
from PIL import Image
from io import BytesIO


def searchpanoid(inlat, inlon, *kwargs):
    meta_url = 'https://maps.googleapis.com/maps/api/streetview/metadata'
    metadata_query = meta_url+'?location={},{}&key={}'.format(str(inlat),
                                            str(inlon),
                                            GoogleAPIKey)
    sresults = requests.get(metadata_query, stream=True).json()
    return sresults
    

# Import from latGIS_containers, but for now easier to reference here
class CameraData:
    def __init__(self, LatLonEl: list, heading: float, pitch: float):
        # instance variable unique to each instance
        self.LatLonEl = LatLonEl   
        self.heading = heading
        self.pitch = pitch

class gsvobject:
    '''
    Instantiates an object to hold Google Streetview data
    '''
    def __init__(self):
        # Remove this below
       # self.CameraData = CameraData()
        self.meta_url = 'https://maps.googleapis.com/maps/api/streetview/metadata'
        self.api_url = 'https://maps.googleapis.com/maps/api/streetview?'
        self.api_key = GoogleAPIKey
        self.search_coords = {}
        self.params = {}
        self.metadata = {}
    def getpanoid(self, search_lat, search_lon):
        self.search_coords['slat'] = search_lat
        self.search_coords['slon'] = search_lon
        # Concatenate parameters for street view api
        metadata_query = self.meta_url+'?location={},{}&key={}'.format(str(search_lat),
                                            str(search_lon),
                                            GoogleAPIKey)
        self.metadata = requests.get(metadata_query, stream=True).json()
    def getimage(self,
                 heading:int,
                 pitch:float,
                 fov = 180,
                 size = '640x640',
                 source = 'outdoor'):
        try:
            self.params['pano'] = self.metadata['pano_id']
            self.params['size'] = size
            self.params['heading'] = heading
            self.params['pitch'] = pitch
            self.params['fov'] = fov
            self.params['source'] = source
            self.params['key'] = GoogleAPIKey
            params_text = '&'.join(['%s=%s' % (key, value) for (key, value) in self.params.items()])
            rurl = self.api_url+params_text
            self.rresponse = requests.get(rurl)
            if self.rresponse.status_code == 200:
                self.image_array = np.array(Image.open(BytesIO(self.rresponse.content)))
                elev = get_elevation(self.metadata['location']['lat'], self.metadata['location']['lng'])
                self.CameraData = CameraData([self.metadata['location']['lat'],
                                              self.metadata['location']['lng'],
                                              elev], heading, pitch)
        except AttributeError:
            print('Run "getpanoid" first')
            
    def showimage(self):
        '''
        Show image in default image viewer
        '''
        
        try:
            img = Image.fromarray(self.image_array, 'RGB')
            img.show()
        except AttributeError:
            print('Image Array does not exist! - Run "getimage" first.')
    
    
    def saveimage(self, outpath, filename, imgformat='png'):
        '''
        Save image to specified path
        '''
        
        try:
            img = Image.fromarray(self.image_array, 'RGB')
            fullpath = os.path.join(outpath, filename+'.'+imgformat)
            print(fullpath)
            img.save(fullpath)
        except AttributeError:
            print('Could not save image')
def get_elevation(Lat, Lon):
    '''
    Returns elevation in meters given Lat, Lon input
    '''
    Lat = str(Lat)
    Lon = str(Lon)
    baseurl = 'https://maps.googleapis.com/maps/api/elevation/json?locations={},{}&key={}'.format(Lat, Lon, GoogleAPIKey)
    rr = requests.get(baseurl).json()
    if rr['status']=='OK':
        #print(rr['results'])
        return rr['results'][0]['elevation']
        
    else:
        return 'Invalid Request, status: '+rr['status']
            