# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 17:31:59 2018

@author: Max
"""

# google street view api functions

from ggapikeydoc import GoogleAPIKey
def getpanoid(inlat, inlon, apikey=GoogleAPIKey):
    from pandas import DataFrame
    import google_streetview.api
    # Define parameters for street view api
    params = [{
    'location': '{},{}'.format(str(inlat), str(inlon)),
    'key': apikey
    }]
    results = google_streetview.api.results(params).metadata[0]
    if results['status']=='OK':
        results['panoLAT']=results['location']['lat']
        results['panoLON']=results['location']['lng']
        results['searchLAT']=inlat
        results['searchLON']=inlon
    else:
        results['panoLAT']='NA'
        results['panoLON']='NA'
        results['searchLAT']=inlat
        results['searchLON']=inlon
        
    return results

def panodnld(destinationpath, panoID, size='640x640', heading='0', pitch='0'):
    import os
    import google_streetview.api
    destinationpath = os.path.abspath(destinationpath)
    from ggapikeydoc import GoogleAPIKey
    params = [{
            'size': size,
            'pano': panoID,
            'heading': heading,
            'pitch': pitch,
            'key': GoogleAPIKey
            }]
       
    results = google_streetview.api.results(params)
    dpath = os.path.join(destinationpath, panoID)
    results.download_links(dpath)
    

    
