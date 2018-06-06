# -*- coding: utf-8 -*-
"""
Created on Wed May 23 20:27:58 2018
s
@author: WLM-PC
"""
from get2Dfrom3D import get2Dfrom3D
import cv2
import numpy as np
import pickle

with open('config.pkl', 'rb') as f:  
    viewpoints, fileNames, part, version, resolution, windowSize, numTrainPerFile = pickle.load(f)

fileName = "BH0002"
viewpoints = [0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180,190,200,210,220,230,240,250,260,270,280,290,300,310,320,330,340,350]

matrix = np.load("matrix3D/matrix3D_" + fileName + '_' + part + '_' + str(resolution) + ".npy")
predictedmatrix = np.load("reconstruct_matrix3D/reconstruct_matrix3D_" + fileName + '_' + part + '_' + str(resolution) + ".npy")

viewsTruth = get2Dfrom3D( viewpoints, matrix, resolution)

for i in range( len(viewsTruth)):
    image = viewsTruth[i]
    viewpoint = viewpoints[i]
    cv2.imwrite( "360views/ground_truth/image_" + fileName + "_" + str(viewpoint) + '_' + part + '_' + str(resolution) + '.png', image)
    
viewsReconstructed = get2Dfrom3D( viewpoints, predictedmatrix, resolution)
for i in range( len(viewsTruth)):
    image = viewsReconstructed[i]
    viewpoint = viewpoints[i]
    cv2.imwrite( "360views/reconstructed/image_" + fileName + "_" + str(viewpoint) + '_' + part + '_' + str(resolution) + '.png', image)
    
    
for i in range( len(viewsTruth)):
    image = np.concatenate(( viewsTruth[i], viewsReconstructed[i]), axis=1)
    viewpoint = viewpoints[i]
    cv2.imwrite( "360views/concatenate/image_" + fileName + "_" + str(viewpoint) + '_' + part + '_' + str(resolution) + '.png', image)
  