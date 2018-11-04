#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  9 22:20:38 2018

@author: johnnelsonkane
"""

from  PIL import Image
from os import listdir

filePath = 'imageFolder'
DIRS = listdir(filePath)

for imDir in DIRS:
    
    curDir = filePath + "/" +  imDir
    print(type(curDir))
    image = Image.open(curDir +'/gsv_0.jpg')
    image.show()
    
    