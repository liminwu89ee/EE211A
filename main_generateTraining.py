# -*- coding: utf-8 -*-
"""
Created on Sun May 20 11:39:58 2018
s
@author: WLM-PC
"""
import cv2
import numpy as np
import pickle
import pandas as pd
from getPatch import getPatch

with open('config.pkl', 'rb') as f:  
    viewpoints, fileNames, part, version, resolution, windowSize, numTrainPerFile = pickle.load(f)


for fileName in fileNames:
    print("Processinf file:" + fileName )
    matrix = np.load("matrix3D/matrix3D_" + fileName + '_' + part + '_' + str(resolution) + ".npy")
    metadataFileName = "metadata/meta_" + fileName + '_' + part + '_' + str(resolution) + ".pkl"
    
    with open(metadataFileName, 'rb') as f:
        metadata = pickle.load(f)
    
    images2D = []
    for viewpoint in viewpoints:
        image = cv2.imread("2Dimages/image_" + fileName + "_" + str(viewpoint) + '_' + part + '_' + str(resolution) + '.png',0)
        images2D.append(image)
    
    df_vessel, df_nonvessel= getPatch( matrix, images2D, metadata, viewpoints, part, resolution, windowSize, numTrainPerFile)

    df_vessel.to_csv( "data/vessel/data_" + fileName + '_' + part + '_' + str(resolution) + ".csv", sep=',', encoding='utf-8')
    df_nonvessel.to_csv( "data/nonvessel/data_" + fileName + '_' + part + '_' + str(resolution) + ".csv", sep=',', encoding='utf-8')
    
    