# -*- coding: utf-8 -*-
"""
Created on Sun Dec  9 18:37:43 2018

@author: Max Marno

Interface to Google Streetview API

Note: some methods are predicated on results from other methods, ie
'getimage' cannot be run until the panoid has been fetched, and 'showimage'
cannot be run until the image has been fetched
"""
import sys, os
sys.path.append(os.path.join(os.getcwd(),'..','..','Src','Utilities'))

from elevation import get_elevation
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
    oid=0
    __imagecols = ['oid', 'panoid', 'metadata', 'searchcoords', 'cameradata', 'imagearray']
    __searchcols = ['oid', 'panoid', 'metadata', 'searchcoords']
    def __init__(self):

        self.meta_url = 'https://maps.googleapis.com/maps/api/streetview/metadata'
        self.api_url = 'https://maps.googleapis.com/maps/api/streetview?'
        self.api_key = GoogleAPIKey
        self.search_results= DataFrame(columns=gsvobject.__searchcols)
        self.image_data = DataFrame(columns = gsvobject.__imagecols)
        
    def getpanoid(self, search_latlon:list):
        # TODO?: include search cases where no pano_id is returned??
        
        # returns the nearest panoid given a lat and lon within a 50 meter radius
        for coordpair in search_latlon:
            slat = coordpair[0]
            slon = coordpair[1]
            # Concatenate parameters for street view api
            metadata_query = self.meta_url+'?location={},{}&key={}'.format(str(slat),
                                                str(slon),
                                                GoogleAPIKey)
            # json results as dict
            results = requests.get(metadata_query, stream=True).json()
            # if unique:
            if 'pano_id' in results:
                if results['pano_id'] not in self.search_results['panoid']:
                    gsvobject.oid += 1
                    self.oid = gsvobject.oid
                    newfeature = dict.fromkeys(gsvobject.__searchcols, 0)
                    newfeature['oid'] = gsvobject.oid
                    newfeature['panoid'] = results['pano_id']
                    newfeature['metadata'] = results
                    newfeature['searchcoords'] = [slat,slon]
                    # Append to features dataframe
                    self.search_results = self.search_results.append(newfeature, ignore_index=True, sort=False)
        return self.search_results

    def getimage(self,
                 imagemetadata: DataFrame,
                 heading: int,
                 pitch: float,
                 fov = 180,
                 size = '640x640',
                 source = 'outdoor'):
        newimage = dict.fromkeys(gsvobject.__searchcols, 0)
        '''
        Need to use a left merge where the dup cols are panoid, heading, pitch
        '''
        
        try:
            for i, row in imagemetadata.iterrows():
                params = {}
                
                params['pano'] = row['panoid']
                params['size'] = size
                params['heading'] = heading
                params['pitch'] = pitch
                params['fov'] = fov
                params['source'] = source
                params['key'] = GoogleAPIKey
                params_text = '&'.join(['%s=%s' % (key, value) for (key, value) in self.params.items()])
                rurl = self.api_url+params_text
                self.rresponse = requests.get(rurl)
                if self.rresponse.status_code == 200:
                    newimage.image_array = np.array(Image.open(BytesIO(self.rresponse.content)))
                    elev = get_elevation(self.metadata['location']['lat'], self.metadata['location']['lng'])
                    newimage.cameradata = CameraData([self.metadata['location']['lat'],
                                                  self.metadata['location']['lng'],
                                                  elev], heading, pitch)
                    # HERE
                    # now left merge with image_data DF based on pano ID, heading, and pitch
                    # Print if new or duplicate with CameraData
        
        
        except AttributeError:
            print('No pano id ')
            
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
            