#! /public/home/ziqiangw/anaconda3/bin/python

from irradiation_GB_Cu import *

data = []
for i in [0.5, 1, 1.5, 2]:
    with open (str(i)+'%_porosity/mean_error.txt', 'r') as file:
        x=[]
        y=[]
        e=[]
        while True:
            line = file.readline()
            if len(line.split()) == 0:
                break
            else:
                ls = line.split()
                x.append(int(ls[0].split('_')[0]))
                y.append(float(ls[1]))
                e.append(float(ls[-1]))
    data.append((x,y,e))
MultipleTwoVariableErrorBar(data, labels=['Cluster size','Thermal conductivity(W/m/K)'])
