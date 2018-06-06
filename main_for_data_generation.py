
# VERSION : 6 IMAGES
import numpy as np
from importSWC import importSWC
import cv2
from conv3Dto2D import get2DLeft
from conv3Dto2D import get2DFront
from conv3Dto2D import get2DTop
from conv3Dto2D import get2Dlayer

from build3D import build3D
from noiseFilter import noiseFilter
from plot3Dmatrix import plot3Dmatrix
import math
from skimage.morphology import erosion, dilation, opening, closing, white_tophat
from genData import genData
from genData import genData_9pixels

plot = True
newsize = 500
filepath = 'BG0020.CNG.swc'
filenameItems = filepath.split(".")
filename = filenameItems[0]
numWhite = 10000
numBlack = 10000
partName = 'leftOnly' #'fullImage', 'leftOnly', 'rightOnly'

viewpoints = [ 150, 120, 90, 60, 30, 0]
images2D = []
metadatas = []

for viewpoint in viewpoints:
    
    tag = str(viewpoint) + ".png"
    metadata, matrix = importSWC( "input/" + filepath, newsize, viewpoint, False, partName) #'fullImage', 'leftOnly', 'rightOnly'
    print("3D matrix created!")
    leftView = get2DLeft(matrix)
    frontView = get2DFront(matrix)
    topView = get2DTop(matrix)
    #cv2.imshow("leftView"+ tag, leftView)
    #cv2.imshow("frontView"+ tag, frontView)
    #cv2.imshow("topView"+ tag, topView)

    #leftView_blur = cv2.GaussianBlur(leftView,(3,3),0)
    cv2.imwrite( "output/leftView_" + filename + "_" + tag, leftView)
    #reconstruction is based on leftviews of different viewpoint
    images2D.append(leftView)
    metadatas.append(metadata)
    print("2D images created!")
    
#genData( viewpoints, images2D, newsize, matrix, metadata, filename + '-' + partName, numWhite, numBlack)     
genData_9pixels( viewpoints, images2D, newsize, matrix, metadata, filename + '-' + partName, numWhite, numBlack)     
matrix = None #clear matrix to save memory

cv2.waitKey(0)
cv2.destroyAllWindows()