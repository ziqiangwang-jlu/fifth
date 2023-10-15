#! /public/home/ziqiangw/anaconda3/bin/python

import os
import statistics 
import numpy as np

dict = {}
for temp in [600,900,1200,1500]:
    os.chdir(str(temp)+'K')
    lattice_constant_list = []
    for i in range(1,6):
        os.chdir('seed_'+str(i))
        with open ('log.lammps', 'r') as file:
            while True:
                line = file.readline()
                if len(line.split()) == 10:
                    if line.split()[0] == '100000':
                        lattice_constant_list.append(float(line.split()[-1]))
                        break
                    else:
                        pass
                else:
                    pass
        os.chdir('../')
    dict[temp] = lattice_constant_list
    os.chdir('../')


for temp in [600,900,1200,1500]:
    with open ('lattice_constant.txt', 'a') as file:
        file.write(str(temp)+'K '+str(np.mean(dict[temp]))+' '+str(statistics.stdev(dict[temp]))+'\n')

print(*dict[600])
print(*dict[900])
