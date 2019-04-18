# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 20:31:14 2019

@author: Max Marno
"""

import matplotlib.pyplot as plt
import numpy as np

imsp0 = np.random.rand(10,10)
imsp1 = np.random.rand(10,10)

fig = plt.figure()

ax  = fig.add_subplot(121)
ax.imshow(imsp0)

ax2 = fig.add_subplot(122)
ax2.imshow(imsp1)

def onclick_select(event):
    if event.inaxes == ax:
        print ("event in ax")
    elif event.inaxes == ax2:
        print ("event in ax2")

fig.canvas.mpl_connect("button_press_event",onclick_select)

plt.show()