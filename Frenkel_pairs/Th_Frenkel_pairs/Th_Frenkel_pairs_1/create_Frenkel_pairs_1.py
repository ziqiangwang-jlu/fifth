#! /public/home/ziqiangw/anaconda3/envs/atomman_env/bin/python


import atomman as am
from distance import *
import numpy as np

system = am.load('atom_data', 'perfect_relaxed.dat')
neighbors = am.NeighborList(system=system,cutoff=5.0)

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
Th_interstitials_ls = []
Th_vacancies_ls = []
dict = {}

for i, neighborlist in enumerate(neighbors):
    if len(Th_interstitials_ls) < 180:
        if system.atoms_prop('atype', i) == 2:
            vac_num = 0   
            inter_num = 0
            for index, j in enumerate(neighborlist):
                xi, yi, zi = system.atoms.pos[i]
                xj, yj, zj = system.atoms.pos[j]
                vector = ((xj-xi)/latt, (yj-yi)/latt, (zj-zi)/latt)
                if abs(vector[0]-0.5)<0.01 and abs(vector[1]-0.5)<0.01 and abs(vector[2]-0.5)<0.01:
                    if system.atoms.atype[j] == 4:
                        if j+1 not in Th_interstitials_ls:
                            Th_interstitials_ls.append(j+1)
                            inter_num = inter_num + 1
                if abs(vector[0]-(-0.5))<0.01 and abs(vector[1]-0.5)<0.01 and abs(vector[2]-0.0) < 0.01:
                    if system.atoms.atype[j] == 2:
                        if check_distance(j+1, Th_vacancies_ls):
                            Th_vacancies_ls.append(j+1)
                            vac_num = vac_num + 1
                        else:
                            pass
                    else:
                        pass
                
                if vac_num == 1 and inter_num == 1:
                    dict[Th_interstitials_ls[-1]] = Th_vacancies_ls[-1]
                    break
                if index == len(neighborlist)-1:
                    if vac_num == 1 and inter_num == 0:
                        Th_vacancies_ls.remove(Th_vacancies_ls[-1])
                    elif vac_num == 0 and inter_num == 1:
                        Th_interstitials_ls.remove(Th_interstitials_ls[-1])                       
    else:
        break

print('Th vacancy: ', len(Th_vacancies_ls), np.array(Th_vacancies_ls))
print('Th interstitial: ', len(Th_interstitials_ls), np.array(Th_interstitials_ls))
