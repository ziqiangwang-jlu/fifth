#! /public/home/ziqiangw/anaconda3/envs/atomman_env/bin/python

#This script is used to generate the Oxygen Frenkel pairs with the specified type in ThO2 systems
#By Ziqiang Wang on Jilin university 

import atomman as am
from distance import *
import numpy as np

system = am.load('atom_data', 'perfect_relaxed.dat') # load the configuration
neighbors = am.NeighborList(system=system,cutoff=5.0) # generate the list of all neighbors within the cut-off distance for each atom

#The atom id(i) in the neighbor list corresponds to (i+1) in the configuration. For example, 0 -> 1 
def check_distance(atom_id, id_list):
    return_value = 0
    for index in id_list:
        if get_distance(system.atoms_prop('pos', atom_id), system.atoms_prop('pos', index)) >10.0:
            pass
        else:
            return_value = 1
            break
    if return_value == 1:
        return False
    else:
        return True

latt = 5.5788
O_interstitials_ls = []
O_vacancies_ls = []
dict = {}

for i, neighborlist in enumerate(neighbors):
    if len(O_interstitials_ls) < 180:
        if system.atoms_prop('atype', i) == 2:
            vac_num = 0   
            inter_num = 0
            for index, j in enumerate(neighborlist):
                xi, yi, zi = system.atoms.pos[i]
                xj, yj, zj = system.atoms.pos[j]
                vector = ((xj-xi)/latt, (yj-yi)/latt, (zj-zi)/latt)
                if abs(vector[0]-0.5)<0.01 and abs(vector[1]-0.5)<0.01 and abs(vector[2]-0.5)<0.01:
                    if system.atoms.atype[j] == 3:
                        if j+1 not in O_interstitials_ls:
                            O_interstitials_ls.append(j+1)
                            inter_num = inter_num + 1
                if abs(vector[0]-(-0.25))<0.01 and abs(vector[1]-(-0.25))<0.01 and abs(vector[2]-(-0.25)) < 0.01:
                    if system.atoms.atype[j] == 1:
                        if check_distance(j+1, O_vacancies_ls):
                            O_vacancies_ls.append(j+1)
                            vac_num = vac_num + 1
                        else:
                            pass
                    else:
                        pass
                
                if vac_num == 1 and inter_num == 1:
                    dict[O_interstitials_ls[-1]] = O_vacancies_ls[-1]
                    break
                if index == len(neighborlist)-1:
                    if vac_num == 1 and inter_num == 0:
                        O_vacancies_ls.remove(O_vacancies_ls[-1])
                    elif vac_num == 0 and inter_num == 1:
                        O_interstitials_ls.remove(O_interstitials_ls[-1])                       
    else:
        break

print('O vacancy: ', len(O_vacancies_ls), np.array(O_vacancies_ls))
print('O interstitial: ', len(O_interstitials_ls), np.array(O_interstitials_ls))
