#! /public/home/ziqiangw/anaconda3/bin/python

#######
#This script is used to create discretely distributed Frenkel pairs in the ThO2 system
#The ratio of the number of the removed Th atoms to the number of the removed oxygen atoms is 1:2
#By Ziqiang Wang on Jilin university
######

import random
from read_lmp_dat import *
from distance import *
import numpy as np

system = Read_data('perfect_relaxed.dat')
tot_num = system.get_tot_num()
def check_distance(atom_id, id_list):
    return_value = 0
    for index in id_list:
        if get_distance(system.get_position(atom_id),system.get_position(index)) >8.0:
            pass
        else:
            return_value = 1
            break
    if return_value == 1:
        return False
    else:
        return True 

vac_O_list = []
oct_O_list = []
dict = {}

while len(vac_O_list) < 180: # define the total number of oxygen Frenkel pairs
    atom_id = random.randint(1,tot_num) # randomly select the Oxygen atom 
    while not (system.get_type(atom_id) == 1 and check_distance(atom_id,oct_O_list) and check_distance(atom_id,vac_O_list) and atom_id not in vac_O_list):
        atom_id = random.randint(1, tot_num)
    vac_O_list.append(atom_id)
    for id in range(1,tot_num+1):
        if system.get_type(id) == 3 or system.get_type(id) == 4: # randomly select an octahedral interstitial site
            if check_distance(id,vac_O_list) and check_distance(id,oct_O_list): # the minimum distance between the selected atom and any existed atom is greater 
                if id not in oct_O_list:
                    oct_O_list.append(id)    
                    dict[atom_id] = id
                    break
            else:
                pass
        else:
            pass

print('vac_O_list:', len(vac_O_list), np.array(vac_O_list))
print('oct_O_list:', len(oct_O_list), np.array(oct_O_list))
