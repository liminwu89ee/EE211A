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
    viewpoints, fileNames, testFileNames, part, version, resolution, windowSize, numTrainPerFile, method = pickle.load(f)

font = cv2.FONT_HERSHEY_SIMPLEX

viewpoints = [0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180,190,200,210,220,230,240,250,260,270,280,290,300,310,320,330,340,350]

for testFileName in testFileNames:
    matrix = np.load("matrix3D/matrix3D_" + testFileName + '_' + part + '_' + str(resolution) + ".npy")
    predictedmatrix = np.load("reconstruct_matrix3D/reconstruct_matrix3D_" + testFileName + '_' + part + '_' + str(resolution) + ".npy")
    postprocessedmatrix = np.load("postprocessed_matrix3D/postprocessed_matrix3D_" + testFileName + '_' + part + '_' + str(resolution) + ".npy")
    
    print("Generating ground truth images:")
    viewsTruth = get2Dfrom3D( viewpoints, matrix, resolution)
    for i in range( len(viewsTruth)):
        print("Processing view ", i)
        image = viewsTruth[i]
        viewpoint = viewpoints[i]
        cv2.imwrite( "360views/ground_truth/image_" + testFileName + "_" + str(viewpoint) + '_' + part + '_' + str(resolution) + '.png', image)
    
    print("Generating reconstructed images:")    
    viewsReconstructed = get2Dfrom3D( viewpoints, predictedmatrix, resolution)
    for i in range( len(viewsTruth)):
        print("Processing view ", i)
        image = viewsReconstructed[i]
        viewpoint = viewpoints[i]
        cv2.imwrite( "360views/reconstructed/image_" + testFileName + "_" + str(viewpoint) + '_' + part + '_' + str(resolution) + '.png', image)
       
    print("Generating postprocessed images:")
    viewsPostprocessed = get2Dfrom3D( viewpoints, postprocessedmatrix, resolution)
    for i in range( len(viewsTruth)):
        print("Processing view ", i)
        image = viewsPostprocessed[i]
        viewpoint = viewpoints[i]
        cv2.imwrite( "360views/postprocessed/image_" + testFileName + "_" + str(viewpoint) + '_' + part + '_' + str(resolution) + '.png', image)
    
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    writer = cv2.VideoWriter("video/" + testFileName + "_" + str(viewpoint) + '_' + part + '_' + str(resolution) + '.avi', fourcc, 5, (1500,500), isColor=False)
    print("Generating concatenated images:")
    for i in range( len(viewsTruth)):
        print("Processing view ", i)
        imgTruth = viewsTruth[i]
        imgTruth = cv2.putText(imgTruth, "Ground Truth", (30, 30), font, 0.8, (255, 255, 255), 1, cv2.LINE_AA)
        
        imgReconstructed = viewsReconstructed[i]
        imgReconstructed = cv2.putText(imgReconstructed, "Reconstructed", (30, 30), font, 0.8, (255, 255, 255), 1, cv2.LINE_AA)

        imgPostprocessed = viewsPostprocessed[i]
        imgPostprocessed = cv2.putText(imgPostprocessed, "Postprocessed", (30, 30), font, 0.8, (255, 255, 255), 1, cv2.LINE_AA)
        
        image = np.concatenate(( imgTruth, imgReconstructed, imgPostprocessed), axis=1)
        writer.write(image)
        viewpoint = viewpoints[i]
        cv2.imwrite( "360views/concatenate/image_" + testFileName + "_" + str(viewpoint) + '_' + part + '_' + str(resolution) + '.png', image)
      
    writer.release()