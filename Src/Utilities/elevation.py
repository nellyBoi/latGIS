# -*- coding: utf-8 -*-

import requests
import sys, os
sys.path.append(os.path.join(sys.path[0],'..','..','Src','StreetViewAPI'))
from ggapikeydoc import GoogleAPIKey
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
    
    
    

