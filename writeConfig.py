# -*- coding: utf-8 -*-
"""
Created on Fri May 18 20:39:52 2018

@author: WLM-PC
"""

import pickle

viewpoints = [ 150, 120, 90, 60, 30, 0]
#fileNames = ['BG001']

#fileNames = ['BH0002']
fileNames = ['BG0002','BG0003','BG04','BG05','BG06','BG07','BG08','BG09','BG10','BG11','BG12','BG13','BG0014','BG15','BG17','BG18','BG0019','BG0020','BG0021','BG0022']
part = 'Left' #'Full', 'Left', 'Right'
version = "v1"
resolution = 500
windowSize = 5
numTrainPerFile  = 20000

with open('config.pkl', 'wb') as f:  
    pickle.dump([viewpoints, fileNames, part, version, resolution, windowSize, numTrainPerFile], f)