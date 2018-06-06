# -*- coding: utf-8 -*-
"""
Created on Fri May 18 20:11:58 2018

@author: WLM-PC
"""
import numpy as np
import pickle
from SWCto3D import SWCto3D

with open('config.pkl', 'rb') as f:  
    viewpoints, fileNames, part, version, resolution, windowSize, numTrainPerFile = pickle.load(f)

for fileName in fileNames:
    print("Processinf file:" + fileName )
    metadata, matrix = SWCto3D( "input/" + fileName + ".CNG.swc", resolution, part) #'full', 'left', 'right'
    np.save("matrix3D/matrix3D_" + fileName + '_' + part + '_' + str(resolution), matrix)
    
    metadataFileName = "metadata/meta_" + fileName + '_' + part + '_' + str(resolution) + ".pkl"
    with open( metadataFileName, 'wb') as f:  
        pickle.dump( metadata, f,protocol=pickle.HIGHEST_PROTOCOL)
    