# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 20:09:17 2019

@author: Max Marno
"""

coords = list()

import matplotlib.pyplot as plt

im = plt.imread(r"C:\Users\Max Marno\Documents\Projects\GSV\TESTIMAGE.png")
ax = plt.gca()
fig = plt.gcf()
implot = ax.imshow(im)

def onclick(event):
    if event.xdata != None and event.ydata != None:
        print(event.xdata, event.ydata)

cid = fig.canvas.mpl_connect('button_press_event', onclick)

plt.show()