# -*- coding: utf-8 -*-
"""
Created on Fri May 18 20:39:52 2018

@author: WLM-PC
"""

import pickle

viewpoints = [ 150, 120, 90, 60, 30, 0]

#training set
fileNames = ['BG0002','BG0003','BG04','BG05','BG06','BG07','BG08','BG09','BG10','BG11','BG12','BG13','BG0014','BG15','BG17','BG18','BG0019','BG0020','BG0021','BG0022']

#testing set
testFileNames = ['BH0002','BH0030','BH0031','BH0032']

part = 'Left' #'Full', 'Left', 'Right'
version = "v1"
resolution = 500
windowSize = 3
numTrainPerFile  = 20000
method = 'Logistic' #Logistic, ANN

with open('config.pkl', 'wb') as f:  
    pickle.dump([viewpoints, fileNames, testFileNames, part, version, resolution, windowSize, numTrainPerFile, method], f)