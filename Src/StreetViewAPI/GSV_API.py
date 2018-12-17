# -*- coding: utf-8 -*-
"""
Created on Sun Dec  9 18:37:43 2018

@author: Max Marno
"""

from ggapikeydoc import GoogleAPIKey
from pandas import DataFrame
import requests
import os
class gsvobject:
    def __init__(self):
        self.meta_url = 'https://maps.googleapis.com/maps/api/streetview/metadata'
        self.api_url = 'https://maps.googleapis.com/maps/api/streetview'
        self.api_key = GoogleAPIKey
        self.search_coords = {}
    def getpanoid(self, search_lat, search_lon):
        self.search_coords['slat'] = search_lat
        self.search_coords['slon'] = search_lon
        # Define parameters for street view api
        metadata_query = self.meta_url+'?location={},{}&key={}'.format(str(search_lat),
                                            str(search_lon),
                                            GoogleAPIKey)
        self.metadata = requests.get(metadata_query, stream=True).json()
#    def getimage(self,
#                 panoid=self.metadata['pano_id'],
#                 heading:int,
#                 pitch:float,
#                 fov = 180,
#                 size = list,
#                 source = 'outdoor'):
#        params = [s]
#        pass
        


uu = 'https://maps.googleapis.com/maps/api/streetview?size=600x300&location=46.414382,10.013988&heading=151.78&pitch=-0.76&key={}'.format(GoogleAPIKey)

import requests
r = requests.get(uu)
type(r.content)

def download(url, out_dir, filename):
    if not path.isdir(out_dir):
        makedirs(out_dir)
    file_path = os.path.join(out_dir, filename)
    r = requests.get(url, stream=True)
    if r.status_code == 200: # if request is successful
        with open(file_path, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)