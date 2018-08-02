# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 15:31:06 2018

@author: WLM-PCs
"""
import numpy as np
from math import floor


def get2DLeft (matrix):
    matrix_2D_x = np.amax(matrix, axis = 0) #left view
    return matrix_2D_x

def get2DFront (matrix):
    matrix_2D_z = np.amax(matrix, axis = 2)
    matrix_2D_z_rotated = np.rot90(matrix_2D_z,3)
    return matrix_2D_z_rotated
    
def get2DTop (matrix):
    matrix_2D_y = np.amax(matrix, axis = 1)
    matrix_2D_y_rotated = np.rot90(matrix_2D_y,3)
    return matrix_2D_y_rotated

def get2Dlayer (matrix, y):
    #return a x-z plane which is a slice of matrix cut at y
    layerImage = matrix[:,floor(y),:]
    return layerImage
    
    
    
    
    
    