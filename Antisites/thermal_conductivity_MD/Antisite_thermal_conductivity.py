#! /public/home/ziqiangw/anaconda3/bin/python

from irradiation_GB_Cu  import *
import os

data = []

for i in [0.0025,0.005,0.01]:
#    print(i)
    temp_list = []
    ther_condu_list = []
    Error_list = []
    os.chdir('antisite_'+str(i))
    with open ('mean_error.txt', 'r') as file:
        while True:
            line = file.readline()
            if len(line.split()) == 0:
                break
            else:
                temp_list.append(int(line.split()[0][:-2]))
                ther_condu_list.append(float(line.split()[1]))
                Error_list.append(float(line.split()[-1]))
    Turple = (temp_list, ther_condu_list, Error_list)
    data.append(Turple)
    os.chdir('../')
#print(data)

axislabel = ['Temperature(K)','Thermal conductivity(W/m/K)']
legend = ['0.25%_Antisites', '0.5%_Antisites', '1%_Antisites']  
MultipleTwoVariableErrorBar(data, saveto='antisites.png',labels=axislabel, legend=legend)


