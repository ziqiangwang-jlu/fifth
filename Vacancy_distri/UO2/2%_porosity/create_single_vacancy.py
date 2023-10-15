#! /public/home/ziqiangw/anaconda3/bin/python

#######
#This script is used to create discretely distributed vacancies in the perfect ThO2 system, where the distance 
#between any two vacancies is greater than 10 A
#To preserve the charge neutral,the ratio between Th vacancies and O vacancies is 1:2
#By Ziqiang Wang on Jilin university
#######

import random
from read_lmp_dat import *
from distance import *
import numpy as np

system = Read_data('perfect_relaxed.dat')
tot_num = system.get_tot_num()
def check_distance(atom_id, id_list): #check if the distance between any two defect atoms is greater than 10A
    return_value = 0
    for index in id_list:
        if get_distance(system.get_position(atom_id),system.get_position(index)) >6.0:
            pass
        else:
            return_value = 1
            break
    if return_value == 1:
        return False
    else:
        return True 

selected_list = []
oxygen_id_list = []
dict = {}
while len(selected_list) < 120: # set the total number of Th vacancies
    atom_id = random.randint(1,tot_num)
    while not (system.get_type(atom_id) == 2 and check_distance(atom_id, selected_list) and check_distance(atom_id, oxygen_id_list)): # check the type of the selected atom and the distance between it and all existed atoms
        atom_id = random.randint(1, tot_num)
    selected_list.append(atom_id)
    elem_num = 0
    value_list = []
    for id in range(1,tot_num+1):
        if system.get_type(id) == 1: # check the atom type
            if check_distance(id, selected_list) and check_distance(id, oxygen_id_list): # check the distance 
                elem_num = elem_num + 1
                if elem_num  >= 3: # One Th vacancy corresponds to two O vacancies
                    break
                else:
                    if id not in oxygen_id_list:
                        value_list.append(id)
                        oxygen_id_list.append(id)
                        dict[atom_id] = value_list
                    else:
                        elem_num = elem_num - 1 
            else:
                pass
        else:
            pass

key_list = []
for key, value in dict.items():
    key_list.append(key)
Th_id_array = np.array(key_list)
Oxygen_id_array = np.array(oxygen_id_list)

print(Th_id_array)
print(Oxygen_id_array)


