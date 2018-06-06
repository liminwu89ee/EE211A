# -*- coding: utf-8 -*-
"""
Created on Fri May 18 22:43:16 2018
s
@author: WLM-PC
"""
import numpy as np
import math
from conv3Dto2D import get2DLeft
import cv2
from genTransform import genTransform 

def get2Dfrom3D (viewpoints, matrix, resolution):
    
    images = []
    Ts = []
    
    for viewpoint in viewpoints:
        
        T = genTransform( viewpoint, resolution/2, resolution/2, resolution/2, resolution)
        Ts.append(T)
        image = np.empty(shape=[ resolution, resolution]).astype(np.uint8) * 0
        images.append(image)
    
    
    for x in range(resolution):
        for y in range(resolution):
            for z in range(resolution):
                if ( matrix[x][y][z] == 255):
                    for k in range(len(images)):
                        

                        cord_org = np.array([x,y,z,1], np.float)
                        cord_new = np.dot(Ts[k], cord_org)
                        new_x = math.floor(cord_new[0])
                        new_y = math.floor(cord_new[1])
                        new_z = math.floor(cord_new[2]) 
                        if ( 0 <= new_y < resolution and 0 <= new_z < resolution):    
                            images[k][new_y][new_z] = 255
                        
    
    return images