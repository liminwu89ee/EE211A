# -*- coding: utf-8 -*-
"""
Created on Fri May 18 22:22:26 2018
s
@author: WLM-PC
"""
import cv2
import numpy as np
import pickle
from get2Dfrom3D import get2Dfrom3D
from conv3Dto2D import get2DLeft

with open('config.pkl', 'rb') as f:  
    viewpoints, fileNames, testFileNames, part, version, resolution, windowSize, numTrainPerFile, method = pickle.load(f)

for fileName in (fileNames + testFileNames):
    print("Processing file:" + fileName )
    matrix = np.load("matrix3D/matrix3D_" + fileName + '_' + part + '_' + str(resolution) + ".npy")
    #leftView = get2DLeft(matrix)
    #cv2.imshow( "test " + fileName, leftView)
    
    images2D = get2Dfrom3D( viewpoints, matrix, resolution)

    for i in range( len(images2D)):
        image = images2D[i]
        viewpoint = viewpoints[i]
        #cv2.imshow( "2Dimages/image" + fileName + "_" + str(viewpoint) + '_' + part + '_' + str(resolution) + '.png', image)
        cv2.imwrite( "2Dimages/image_" + fileName + "_" + str(viewpoint) + '_' + part + '_' + str(resolution) + '.png', image)
        
cv2.waitKey(0)
cv2.destroyAllWindows()