#! /public/home/ziqiangw/anaconda3/bin/python


import sys
import math
import numpy as np

'''
if len(sys.argv) == 5:
    x_0 = float(sys.argv[1])
    y_0 = float(sys.argv[2])
    x_1 = float(sys.argv[3])
    y_1 = float(sys.argv[4])
    result = math.sqrt((x_0-x_1)**2+(y_0-y_1)**2)
elif len(sys.argv) == 7:
    x_0 = float(sys.argv[1])
    y_0 = float(sys.argv[2])
    z_0 = float(sys.argv[3])
    x_1 = float(sys.argv[4])
    y_1 = float(sys.argv[5])
    z_1 = float(sys.argv[6])
    result = math.sqrt((x_0-x_1)**2+(y_0-y_1)**2+(z_0-z_1)**2)
else:
    raise Exception('four or six arguments are excepted')
#print(result)'''

def get_distance(point_1,point_2):
    xlen = point_1[0]-point_2[0]
    ylen = point_1[1]-point_2[1]
    zlen = point_1[2]-point_2[2]
   
    distance = np.linalg.norm([xlen, ylen, zlen])
    return distance
