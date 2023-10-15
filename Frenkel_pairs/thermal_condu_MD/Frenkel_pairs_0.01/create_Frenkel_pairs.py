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
        if get_distance(system.get_position(atom_id),system.get_position(index)) >10.0:
            pass
        else:
            return_value = 1
            break
    if return_value == 1:
        return False
    else:
        return True 

vac_Th_list = []
vac_oxygen_list = []
oct_Th_list = []
oct_oxygen_list = []
dict_Th = {}
dict_oxygen = {}
while len(vac_Th_list) < 60: # define the total number of Frenkel pairs
    atom_id = random.randint(1,tot_num) # randomly select the Th atom 
    while not (system.get_type(atom_id) == 2 and check_distance(atom_id,oct_Th_list) and check_distance(atom_id,oct_oxygen_list)):
        atom_id = random.randint(1, tot_num)
    vac_Th_list.append(atom_id)
    elem_num = 0
    value_list = []
    for id in range(1,tot_num+1):
        if system.get_type(id) == 4: # randomly select an octahedral interstitial site
            if check_distance(id,vac_Th_list) and check_distance(id,vac_oxygen_list): # the minimum distance between the selected atom and any existed atom is greater
                elem_num = elem_num + 1  # than 10 A
                if elem_num  >= 2:
                    break
                else:
                    if id not in oct_Th_list:
                        value_list.append(id)
                        oct_Th_list.append(id)
                        dict_Th[atom_id] = value_list
                    else:
                        elem_num = elem_num - 1 
            else:
                pass
        else:
            pass
    second_id = random.randint(1, tot_num) # randomly select an oxygen atom
    while not (system.get_type(second_id)==1 and check_distance(second_id,oct_Th_list) and check_distance(second_id, oct_oxygen_list)):
        second_id = random.randint(1, tot_num)
    vac_oxygen_list.append(second_id)
    elem_num = 0
    value_list = []
    for id in range(1,tot_num+1): 
        if system.get_type(id) == 3: # randomly select an octahedral interstitial site
            if check_distance(id,vac_oxygen_list) and check_distance(id,vac_Th_list):
                elem_num = elem_num + 1
                if elem_num >= 2:
                    break
                else:
                    if id not in oct_oxygen_list:
                        value_list.append(id)
                        oct_oxygen_list.append(id)
                        dict_oxygen[second_id] = value_list
                    else:
                        elem_num = elem_num - 1
            else:
                pass
        else:
            pass 
    third_id = random.randint(1, tot_num) # randomly select an oxygen atom and the ratio of the Th atoms to the O atoms 1:2
    while not (system.get_type(third_id)==1  and check_distance(third_id,oct_Th_list) and check_distance(third_id, oct_oxygen_list)):
        third_id = random.randint(1, tot_num)
    vac_oxygen_list.append(third_id)
    elem_num = 0
    value_list = []
    for id in range(1,tot_num+1):
        if system.get_type(id) == 3:
            if check_distance(id,vac_oxygen_list) and check_distance(id,vac_Th_list):
                elem_num = elem_num + 1
                if elem_num >= 2:
                    break
                else:
                    if id not in oct_oxygen_list:
                        value_list.append(id)
                        oct_oxygen_list.append(id)
                        dict_oxygen[second_id] = value_list
                    else:
                        elem_num = elem_num - 1
            else:
                pass
        else:
            pass 

print('vac_Th_list:', len(vac_Th_list), np.array(vac_Th_list))
print('oct_Th_list:', np.array(oct_Th_list))
print('vac_oxygen_list:', len(vac_oxygen_list), np.array(vac_oxygen_list))
print('oct_oxygen_list:', np.array(oct_oxygen_list))
