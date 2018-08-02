# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 11:33:22 2018

@author: WLM-PCs
"""
import numpy as np

def noiseFilter ( matrix, newsize, threshold):
    
    resMatrix  = np.empty(shape=[newsize, newsize, newsize]).astype(np.uint32)
    uint8Matrix = np.empty(shape=[newsize, newsize, newsize]).astype(np.uint8)
    
    branchIdx = 1
    branchCount = [0]
    branchLabel = [False]
    
    print("Check start")
    for x in range(newsize):
        for y in range(newsize):
            for z in range(newsize):
                if ( resMatrix[x][y][z] == 0 and matrix[x][y][z] == 255):
                    #print("Check " + str(x) + str(y) + str(z))
                    branchCount.append(0)
                    cord = (x,y,z)
                    countDFS( matrix, resMatrix, newsize, cord, branchIdx, branchCount)
                    if ( branchCount[branchIdx] > threshold):
                        branchLabel.append(True)
                    else:
                        branchLabel.append(False)
                    branchIdx += 1
    
#    print(branchLabel)
#    return resMatrix

    for x in range(newsize):
        for y in range(newsize):
            for z in range(newsize):
                if ( branchLabel[resMatrix[x][y][z]] == True):
                    uint8Matrix[x][y][z] = np.uint8(255)
                else:
                    uint8Matrix[x][y][z] = np.uint8(0)
    
    return uint8Matrix

def countDFS ( matrix, resMatrix, newsize, start, branchIdx, branchCount):
    
    mystack = []
    mystack.append(start)
        
    while ( len(mystack) != 0):
        curcord = mystack.pop()
        x = curcord[0]
        y = curcord[1]
        z = curcord[2]
        if ( x<0 or x>=newsize or y<0 or y>=newsize or z<0 or z>=newsize or matrix[x][y][z] != 255 or resMatrix[x][y][z] != 0):   
            continue
        branchCount[branchIdx] += 1
        resMatrix[x][y][z] = branchIdx
        mystack.append((x+1,y,z))
        mystack.append((x-1,y,z))
        mystack.append((x,y+1,z))
        mystack.append((x,y-1,z))
        mystack.append((x,y,z-1))
        mystack.append((x,y,z+1))
        
        mystack.append((x+1,y+1,z+1))
        mystack.append((x+1,y+1,z-1))
        mystack.append((x+1,y-1,z+1))
        mystack.append((x+1,y-1,z-1))        
        mystack.append((x-1,y+1,z+1))
        mystack.append((x-1,y+1,z-1))
        mystack.append((x-1,y-1,z+1))
        mystack.append((x-1,y-1,z-1))         
    return