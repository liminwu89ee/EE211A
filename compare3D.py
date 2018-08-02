
import numpy as np
from conv3Dto2D import get2Dlayer
from skimage.measure import compare_ssim as ssim

def rmse(x, y):
    return np.linalg.norm(x - y)

def flatten( matrix, sizeImage):
    
    flattened = layerImage = matrix[:,0,:]
    
    for idx in range(1,sizeImage):
        layerImage = matrix[:,idx,:]
        flattened = np.concatenate(( flattened, layerImage), axis=1)
    
    return flattened

def compare3D ( matrix1, matrix2, sizeImage):
    
    flattened_matrix1 = flatten( matrix1, sizeImage)
    flattened_matrix2 = flatten( matrix2, sizeImage)
    
    RMSE = rmse( flattened_matrix1, flattened_matrix2)
    SSIM = ssim( flattened_matrix1, flattened_matrix2, 255)
    
    m = np.sum(flattened_matrix1[flattened_matrix2>0])*2.0
    n = (np.sum(flattened_matrix1) + np.sum(flattened_matrix2)) 
    DICE = m/n
    
    result = {}
    result['RMSE'] = RMSE
    result['SSIM'] = SSIM
    result['DICE'] = DICE
    
    return result