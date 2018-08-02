# -*- coding: utf-8 -*-
"""
Created on Tue Jul 24 18:01:13 2018

@author: WLM-PC
"""


import cv2
import numpy as np
import pickle
import pandas as pd
from getPatch import getPatch
from noiseFilter import noiseFilter
from skimage.morphology import erosion, dilation, opening, closing, white_tophat


with open('config.pkl', 'rb') as f:  
    viewpoints, fileNames, testFileNames, part, version, resolution, windowSize, numTrainPerFile, method = pickle.load(f)


for testFileName in testFileNames:
    matrix = np.load("reconstruct_matrix3D/reconstruct_matrix3D_" + testFileName + '_' + part + '_' + str(resolution) + ".npy")
    
    minNeighborThreshold = 20
    result = noiseFilter( matrix, resolution, minNeighborThreshold)
    #result = erosion(result,np.ones([3,3,3]))
    np.save("postprocessed_matrix3D/postprocessed_matrix3D_" + testFileName + '_' + part + '_' + str(resolution), result)
