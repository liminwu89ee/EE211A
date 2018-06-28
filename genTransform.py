
import numpy as np
import math

def genTransform (viewpoint_degree, x_center, y_center, z_center, newsize = 500):
    
    viewpoint = math.radians(viewpoint_degree)
    #print("degree to radius :",viewpoint_degree,viewpoint)
    
    T1 = np.array([[ 1, 0, 0, -x_center], 
                   [ 0, 1, 0, -y_center],
                   [ 0, 0, 1, -z_center],
                   [ 0, 0, 0, 1]], 
                    np.float) 
    
    T2 = np.array([[ math.cos(viewpoint), 0, math.sin(viewpoint), 0], 
                    [ 0, 1, 0, 0],
                    [-math.sin(viewpoint), 0, math.cos(viewpoint), 0],
                    [ 0, 0, 0, 1]], 
                    np.float)
    
    T3 = np.array([[ 1, 0, 0, newsize/2], 
                   [ 0, 1, 0, newsize/2],
                   [ 0, 0, 1, newsize/2],
                   [ 0, 0, 0, 1]], 
                    np.float)
    
    T21 = np.dot(T2, T1)
    T321 = np.dot(T3,T21)
    
    return T321
    
    
    