# -*- coding: utf-8 -*-
"""
Created on Sun May 20 15:10:39 2018
s
@author: WLM-PC
"""
import numpy as np
import pandas as pd
from genTransform import genTransform
from math import floor
import random
import csv

def getPatch ( matrix, images2D, metadata, viewpoints, part, resolution, windowSize, numTrainPerFile):
    metadata
    
    np.random.seed(10)
    numViewpoint = len(viewpoints)
    
    min_x = floor(metadata['min_x'])
    max_x = floor(metadata['max_x'])
    min_y = floor(metadata['min_y'])
    max_y = floor(metadata['max_y'])
    min_z = floor(metadata['min_z'])
    max_z = floor(metadata['max_z'])  
    center_x = floor(metadata['center_x'])
    center_y = floor(metadata['center_y'])
    center_z = floor(metadata['center_z']) 
    
    colnames = []
    Ts = []
    
    for viewpoint in viewpoints:
        T =  genTransform( viewpoint, resolution/2, resolution/2, resolution/2, resolution)
        Ts.append(T)
    
    colnames.append('value')
    colnames.append('X')
    colnames.append('Y')
    colnames.append('Z')
    colnames.append('radial')
    colnames.append('azimuthal (radius)')
    colnames.append('polar (radius)')
    
    listWhiteVoxel = []
    listBlackVoxel = []

    rampling_rate_BlackXslice = 0.001
    rampling_rate_WhiteXslice = 1
    
    for x in range( min_x, max_x + 1):
        #print("In progress x = ", x)
        listWhiteVoxel_perXslice = []
        listBlackVoxel_perXslice = []        
        
        for y in range( min_y, max_y + 1):
            for z in range( min_z, max_z + 1):
                
                newrow = []
                
                newrow.append(matrix[x][y][z])    
                newrow.append(x)
                newrow.append(y)
                newrow.append(z)
                
                xy = (x-center_x)**2 + (y-center_y)**2
                radial = np.sqrt(xy + (z-center_z)**2)
                polar = np.arctan2(np.sqrt(xy), (z-center_z)) # for elevation angle defined from Z-axis down
                azimuthal = np.arctan2((y-center_y), (x-center_x))
                
                newrow.append(radial)
                newrow.append(azimuthal)
                newrow.append(polar)               
                
                if (matrix[x][y][z] == 255):
                    listWhiteVoxel_perXslice.append(newrow)
                else:
                    listBlackVoxel_perXslice.append(newrow)
                
        if (len(listWhiteVoxel_perXslice) > 0):
            sampleNumberWhite = floor(len(listWhiteVoxel_perXslice) * rampling_rate_WhiteXslice)
            sampledWhiteVoxel = random.sample(listWhiteVoxel_perXslice, sampleNumberWhite)
            listWhiteVoxel = listWhiteVoxel + sampledWhiteVoxel
            
        if (len(listBlackVoxel_perXslice) > 0):   
            sampleNumberBlack = floor(len(listBlackVoxel_perXslice) * rampling_rate_BlackXslice)
            sampledBlackVoxel = random.sample(listBlackVoxel_perXslice,sampleNumberBlack)
            listBlackVoxel = listBlackVoxel + sampledBlackVoxel
    
    dfWhite = pd.DataFrame(listWhiteVoxel, columns=colnames).sample(n=min( int(numTrainPerFile/2), len(listWhiteVoxel)))
    dfBlack = pd.DataFrame(listBlackVoxel, columns=colnames).sample(n=min( int(numTrainPerFile/2), len(listBlackVoxel)))
    dfWhite = dfWhite.reset_index(drop=True)
    dfBlack = dfBlack.reset_index(drop=True)
    
    halfWindowSize = int((windowSize-1)/2)
    
    patches_vessel = []
    for index, row in dfWhite.iterrows():
        value = row['value']

        cord_org = np.array([row['X'],row['Y'],row['Z'],1], np.float)
        
        new_patches = []
        for i in range(len(viewpoints)):
            T = Ts[i]
            image = images2D[i]
            cord_new = np.dot(T, cord_org)
            y_new = int(round(cord_new[1]))
            z_new = int(round(cord_new[2]))
            #print(y_new-halfWindowSize,y_new+halfWindowSize+1,z_new-halfWindowSize,z_new+halfWindowSize+1)
            patch = np.empty(shape=[ windowSize, windowSize]).astype(np.uint8) * 0
            if ( y_new-halfWindowSize >= 0 and y_new+halfWindowSize < resolution and z_new-halfWindowSize >= 0 and z_new+halfWindowSize < resolution):   
                patch = image[ y_new-halfWindowSize:y_new+halfWindowSize+1 , z_new-halfWindowSize:z_new+halfWindowSize+1 ]
            patchstring = '\t'.join('\t'.join('%d' %x for x in y) for y in patch)
            #print(patchstring)
            #patchstring += "   " +  np.array_str(cord_org) + "    " +  np.array_str(cord_new) + "   "
            new_patches.append(patchstring)
        patches_vessel.append(new_patches)

            
    patches_nonvessel = []
    for index, row in dfBlack.iterrows():
        value = row['value']

        cord_org = np.array([row['X'],row['Y'],row['Z'],1], np.float)
        
        new_patches = []
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
            #print(patchstring)
            #patchstring += "   " +  np.array_str(cord_org) + "    " +  np.array_str(cord_new) + "   "
            new_patches.append(patchstring)
        patches_nonvessel.append(new_patches)

        
    dfPatches_vessel = pd.DataFrame(patches_vessel)
    dfPatches_nonvessel = pd.DataFrame(patches_nonvessel)
    
    result_vessel = pd.concat([dfWhite, dfPatches_vessel], axis=1)
    result_nonvessel = pd.concat([dfBlack, dfPatches_nonvessel], axis=1)
    
    return result_vessel, result_nonvessel









