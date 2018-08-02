# -*- coding: utf-8 -*-
"""
Created on Mon Jul 30 10:42:05 2018

@author: WLM-PC
"""
import cv2
import numpy as np
import pickle

from compare3D import compare3D
from scipy.ndimage.filters import gaussian_filter

with open('config.pkl', 'rb') as f:  
    viewpoints, fileNames, testFileNames, part, version, resolution, windowSize, numTrainPerFile, method = pickle.load(f)

for testFileName in testFileNames:
    
    orgMatrix = np.load("matrix3D/matrix3D_" + testFileName + '_' + part + '_' + str(resolution) + ".npy")
    resMatrix = np.load("reconstruct_matrix3D/reconstruct_matrix3D_" + testFileName + '_' + part + '_' + str(resolution) + ".npy")
    
    
    orgMatrix = gaussian_filter( orgMatrix,1)
    resMatrix = gaussian_filter( resMatrix,1)
    
    print("Scores of reconstructed " + testFileName)
    result = compare3D( orgMatrix, resMatrix, resolution)
    print(result)


for testFileName in testFileNames:
    
    orgMatrix = np.load("matrix3D/matrix3D_" + testFileName + '_' + part + '_' + str(resolution) + ".npy")
    resMatrix = np.load("postprocessed_matrix3D/postprocessed_matrix3D_" + testFileName + '_' + part + '_' + str(resolution) + ".npy")
    
    
    orgMatrix = gaussian_filter( orgMatrix,1)
    resMatrix = gaussian_filter( resMatrix,1)
    
    print("Scores of postprocessed " + testFileName)
    result = compare3D( orgMatrix, resMatrix, resolution)
    print(result)