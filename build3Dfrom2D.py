# -*- coding: utf-8 -*-
"""
Created on Wed May 23 14:34:22 2018
s
@author: WLM-PC
"""
import numpy as np
from genTransform import genTransform
from math import floor

def build3Dfrom2D (viewpoints, images2D, model, resolution, part, windowSize):
    print("Start reconstructing, please wait!")
    predictedMatrix = np.empty(shape=[resolution, resolution, resolution]).astype(np.uint8)
    Ts = []
    halfWindowSize = int((windowSize-1)/2)
    
    for viewpoint in viewpoints:
        T =  genTransform( viewpoint, resolution/2, resolution/2, resolution/2, resolution)
        Ts.append(T)
        
    min_x = 0
    max_x = resolution
    
    #'full', 'Left', 'Right'
    if ( part == "Right"):
        max_x = int(resolution/2)
    elif ( part == "Left"):
        min_x = int(resolution/2)
        
    for x in range( min_x, max_x):
        print("In progress x = ", x)
        for y in range( 0, resolution):
            for z in range( 0, resolution):
                
                features = []
                features.append(x)
                features.append(y)
                features.append(z)                
                xy = (x-resolution/2)**2 + (y-resolution/2)**2
                radial = np.sqrt(xy + (z-resolution/2)**2)
                polar = np.arctan2(np.sqrt(xy), (z-resolution/2)) # for elevation angle defined from Z-axis down
                azimuthal = np.arctan2((y-resolution/2), (x-resolution/2))
                
                features.append(radial)
                features.append(azimuthal)
                features.append(polar)          
                
                cord_org = np.array([x,y,z,1], np.float)
                pixelsString = ""
                for i in range(len(viewpoints)):
                    T = Ts[i]
                    image = images2D[i]
                    cord_new = np.dot(T, cord_org)
                    y_new = int(round(cord_new[1]))
                    z_new = int(round(cord_new[2]))
                    patch = np.empty(shape=[ windowSize, windowSize]).astype(np.uint8) * 0
                    if ( y_new-halfWindowSize >= 0 and y_new+halfWindowSize < resolution and z_new-halfWindowSize >= 0 and z_new+halfWindowSize < resolution):   
                        patch = image[ y_new-halfWindowSize:y_new+halfWindowSize+1 , z_new-halfWindowSize:z_new+halfWindowSize+1 ]
                    patchstring = '\t'.join('\t'.join('%d' %x for x in y) for y in patch)
                    pixelsString += patchstring + '\t'
                
                temp = np.fromstring( pixelsString, dtype = np.uint8, sep='\t').tolist()
                #print(len(temp))
                
                if ( np.sum(temp) == 0):
                    continue
                
                
                features += temp
                features = np.asarray(features).reshape(1, -1)
                #print(features.shape)
                
                predictResult = model.predict(features)
                if (predictResult):
                    predictedMatrix[x][y][z] = 255
                else:
                    predictedMatrix[x][y][z] = 0
                
    return predictedMatrix
                
                
                
                
                
                
                
                
                