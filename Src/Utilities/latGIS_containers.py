# -*- coding: utf-8 -*-

'''
Author: Nelly Kane
Originated: 12.03.2018

Repo: latGIS
File: latGIS_containers.py

The defined containers for the latGIS Python architecture.

'''
class CameraData:
    def __init__(self, LatLonEl: list, heading: float, pitch: float):
        # instance variable unique to each instance
        self.LatLonEl = LatLonEl   
        self.heading = heading
        self.pitch = pitch