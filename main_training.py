# -*- coding: utf-8 -*-
"""
Created on Sun May 20 23:53:52 2018
s
@author: WLM-PC
"""
import csv
import cv2
import numpy as np
import pickle
from getModel_ANN import getModel_ANN
from getModel_logistic import getModel_logistic

with open('config.pkl', 'rb') as f:  
    viewpoints, fileNames, part, version, resolution, windowSize, numTrainPerFile = pickle.load(f)

y = []
x = []
pixels = []

for fileName in fileNames:
    print("Processinf file:" + fileName )
    y_newfile = []
    x_newfile = []
    pixels_newfile = []
    with open("data/vessel/data_" + fileName + '_' + part + '_' + str(resolution) + ".csv", newline='') as csvfile:
        spamreader = csv.reader(csvfile)
        for index, row in enumerate(spamreader):
            if not index:
                continue
            
            y_newfile.append( int(row[1])>0)
            x_newfile.append( list(map(int,row[2:5])) + list(map(float,row[5:8])))
            pixelsString = ""
            for k in range(8,8+6):
                pixelsString +=  row[k] + '\t'
                
            temp = np.fromstring( pixelsString, dtype = np.uint8, sep='\t').tolist()
            pixels_newfile.append(temp)
            
    y.extend(y_newfile)        
    x.extend(x_newfile)
    pixels.extend(pixels_newfile)
    
    numDataVessel = len(y)
    
    y_newfile = []
    x_newfile = []
    pixels_newfile = []
    with open("data/nonvessel/data_" + fileName + '_' + part + '_' + str(resolution) + ".csv", newline='') as csvfile:
        spamreader = csv.reader(csvfile)
        for index, row in enumerate(spamreader):
            if not index:
                continue
            if index > numDataVessel:
                break
            
            y_newfile.append( int(row[1])>0)
            x_newfile.append( list(map(int,row[2:5])) + list(map(float,row[5:8])))
            pixelsString = ""
            for k in range(8,8+6):
                pixelsString +=  row[k] + '\t'
                
            temp = np.fromstring( pixelsString, dtype = np.uint8, sep='\t').tolist()
            pixels_newfile.append(temp)
            
    y.extend(y_newfile)        
    x.extend(x_newfile)
    pixels.extend(pixels_newfile)    

print("pixels size:")
print(len(pixels))
print(len(pixels[0]))
# value(True/False), X, Y, Z, radial, azimuthal(radius), polar(radius), Pixels(len = 6*windowSize^2)
#getModel_ANN(y, x, pixels)
model = getModel_logistic(y, x, pixels)

modelFilename = "Logistic_" + version
pickle.dump(model, open( 'model/' + modelFilename, 'wb'))






