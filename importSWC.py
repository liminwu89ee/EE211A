
import numpy as np
from math import floor
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
from genTransform import genTransform 

filename = 'BG001.CNG.swc'
LIMIT = 1000

SIZE = 200
NUM_SEG = 200

def importSWC( filename, newsize, viewpoint = 0, plot=False , option = 'fullImage'):
    
    nodecountLimit = 5000
    
    #Segment Number, Segment Color/Type, X Coordinate, Y Coordinate, Z Coordinate, Segment Radius, Parent Segment Number
    data = []
    
    count_seg = 0
    x_cord_min = LIMIT
    x_cord_max = -LIMIT
    y_cord_min = LIMIT
    y_cord_max = -LIMIT
    z_cord_min = LIMIT
    z_cord_max = -LIMIT
    x_sum = 0
    y_sum = 0
    z_sum = 0
    
    with open(filename, 'r') as file:
        for row in file:
            seg_num, seg_color, x_cord, y_cord, z_cord, seg_rad, parent_seg = row.split()
            count_seg += 1
            
            seg_num = int(seg_num)
            seg_color = int(seg_color)
            x_cord = float(x_cord)
            x_sum += x_cord
            y_cord = float(y_cord)
            y_sum += y_cord
            z_cord = float(z_cord)
            z_sum += z_cord
            seg_rad = float(seg_rad)
            parent_seg = int(parent_seg)
            tempdata = [seg_num,seg_color,x_cord,y_cord,z_cord,seg_rad,parent_seg]
            data.append(tempdata)
            x_cord_min = min( x_cord_min, x_cord)
            x_cord_max = max( x_cord_max, x_cord)
            y_cord_min = min( y_cord_min, y_cord)
            y_cord_max = max( y_cord_max, y_cord)
            z_cord_min = min( z_cord_min, z_cord)
            z_cord_max = max( z_cord_max, z_cord)        
            
            if (count_seg == nodecountLimit):
                break;
            
    matrix = np.empty(shape=[newsize, newsize, newsize]).astype(np.uint8) * 0
    
    print("viewpoint (degree) = ", viewpoint)
    #print("x range = ", x_cord_min, ',', x_cord_max)
    #print("y range = ", y_cord_min, ',', y_cord_max)
    #print("z range = ", z_cord_min, ',', z_cord_max)
    
    x_center = (x_cord_min + x_cord_max)/2
    y_center = (y_cord_min + y_cord_max)/2
    z_center = (z_cord_min + z_cord_max)/2
    
    x_center_new_scale = x_center * 1.0 * newsize / SIZE
    y_center_new_scale = y_center * 1.0 * newsize / SIZE
    z_center_new_scale = z_center * 1.0 * newsize / SIZE
    
    #generate transform T such that object will be rotated 90 degree about Y axis, and moved to the center of new scale
    T = genTransform( viewpoint, x_center_new_scale, y_center_new_scale, z_center_new_scale, newsize)
    #print("center x,y,z = ",x_center,',',y_center,',', z_center)
    #print("Viewpoint is :", viewpoint)
    #print("Transform matrix is：")
    #print(T)

    idx_x = []
    idx_y = []
    idx_z = []
    
    metadata = {}
    metadata['max_x'] = x_cord_max * newsize / SIZE
    metadata['min_x'] = x_cord_min * newsize / SIZE
    metadata['max_y'] = y_cord_max * newsize / SIZE
    metadata['min_y'] = y_cord_min * newsize / SIZE
    metadata['max_z'] = z_cord_max * newsize / SIZE
    metadata['min_z'] = z_cord_min * newsize / SIZE    
    
    metadata['center_x'] = newsize/2 #x_center_new_scale
    metadata['center_y'] = newsize/2 #y_center_new_scale
    metadata['center_z'] = newsize/2 #z_center_new_scale
    
    metadata['range_x'] = metadata['max_x'] - metadata['min_x']
    metadata['range_y'] = metadata['max_y'] - metadata['min_y']
    metadata['range_z'] = metadata['max_z'] - metadata['min_z']
    
       
    if (option == 'rightOnly'):
        valid_x_range_lowerbound = 0
        valid_x_range_upperbound = x_center_new_scale
        metadata['max_x'] = metadata['center_x']
    elif ( option == 'leftOnly'):
        valid_x_range_lowerbound = x_center_new_scale
        valid_x_range_upperbound = newsize
        metadata['min_x'] =  metadata['center_x']
    else:
        valid_x_range_lowerbound = 0
        valid_x_range_upperbound = newsize
     

    for line in data:
        if (line[6] == -1):
            continue
        start_x = line[2]
        start_y = line[3]
        start_z = line[4]
        
        end_point = line[6] - 1
        end_x = data[end_point][2]
        end_y = data[end_point][3]
        end_z = data[end_point][4]
        
        #print("From point: ", start_x, start_y, start_z)
        #print("To point: ", end_x, end_y, end_z)
        
        start_x_newcord = start_x * 1.0 * newsize / SIZE
        start_y_newcord = start_y * 1.0 * newsize / SIZE
        start_z_newcord = start_z * 1.0 * newsize / SIZE
        end_x_newcord = end_x * 1.0 * newsize / SIZE
        end_y_newcord = end_y * 1.0 * newsize / SIZE
        end_z_newcord = end_z * 1.0 * newsize / SIZE
        
        dist_x = end_x_newcord - start_x_newcord
        dist_y = end_y_newcord - start_y_newcord
        dist_z = end_z_newcord - start_z_newcord
        
        seg_x = dist_x / NUM_SEG
        seg_y = dist_y / NUM_SEG
        seg_z = dist_z / NUM_SEG

        for i in range(NUM_SEG+1):
            if ( matrix[floor(start_x_newcord+i*seg_x)][floor(start_y_newcord+i*seg_y)][floor(start_z_newcord+i*seg_z)] != 255):
                x = floor(start_x_newcord+i*seg_x)
                y = floor(start_y_newcord+i*seg_y)
                z = floor(start_z_newcord+i*seg_z)
                
                if ( valid_x_range_lowerbound<= x < valid_x_range_upperbound):
                
                    cord_org = np.array([x,y,z,1], np.float)
                    cord_new = np.dot(T, cord_org)
                    
                    new_x = floor(cord_new[0])
                    new_y = floor(cord_new[1])
                    new_z = floor(cord_new[2])
                
                    matrix[new_x][new_y][new_z] = 255
                    idx_x.append(new_x)
                    idx_y.append(new_y)
                    idx_z.append(new_z)
        
    return metadata, matrix
    