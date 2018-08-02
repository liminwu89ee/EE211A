# -*- coding: utf-8 -*-
"""
Created on Wed May 23 13:55:22 2018
s
@author: WLM-PC
"""

import cv2
import numpy as np
import pickle
from build3Dfrom2D import build3Dfrom2D


with open('config.pkl', 'rb') as f:  
    viewpoints, fileNames, testFileNames, part, version, resolution, windowSize, numTrainPerFile, method = pickle.load(f)


modelName = method + "_" + version

model = pickle.load(open("model/" + modelName , 'rb'))


for testFileName in testFileNames:
    
    images2D = []
    for viewpoint in viewpoints:
        image = cv2.imread("2Dimages/image_" + testFileName + "_" + str(viewpoint) + '_' + part + '_' + str(resolution) + '.png',0)
        images2D.append(image)
            
    predictedMatrix = build3Dfrom2D( viewpoints, images2D, model, resolution, part, windowSize)
    np.save("reconstruct_matrix3D/reconstruct_matrix3D_" + testFileName + '_' + part + '_' + str(resolution), predictedMatrix)

