#! /public/home/ziqiangw/anaconda3/bin/python

import random
from read_lmp_dat import *
from distance import *
import numpy as np
import math

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

def calculate_angle(id_1, id_2, id_3):
    pos_1 = system.get_position(id_1)
    pos_2 = system.get_position(id_2)
    pos_3 = system.get_position(id_3)
    vect_1 = [pos_2[0]-pos_1[0],pos_2[1]-pos_1[1], pos_2[2]-pos_1[2]]
    vect_2 = [pos_3[0]-pos_1[0],pos_3[1]-pos_1[1], pos_3[2]-pos_1[2]]
    cos = np.dot(vect_1,vect_2)/(np.linalg.norm(vect_1)*np.linalg.norm(vect_2))
    
    if cos<-1.0 or cos > 1.0 :
        if abs(cos-(-1.0))<0.1:
            cos = -1.0
        #if abs(cos-1.0)<0.1:
        #    cos = 1.0
    angle = math.acos(cos)
    return angle

selected_list = []
occupied_list = []
oxygen_id_list = []
dict = {}
while len(selected_list) < 60:
    atom_id = random.randint(1,tot_num)
    while not (system.get_type(atom_id) == 2 and check_distance(atom_id, selected_list)):
        atom_id = random.randint(1, tot_num)
    selected_list.append(atom_id)
    status = 0
    for id in range(1, tot_num+1):
        if system.get_type(id) == 1:
            if get_distance(system.get_position(atom_id),system.get_position(id)) < 2.5:
                second_id = id
                occupied_list.append(second_id)
                break
            else:
                pass
        else:
            pass

    for id in range(1,tot_num+1):
        if system.get_type(id) == 1:
            if get_distance(system.get_position(atom_id), system.get_position(id)) < 2.5:
                if id not in occupied_list:
                    angle = calculate_angle(atom_id,second_id,id)*(180.0/math.pi)
                    print(angle)
                    if abs(angle-109.49)<=1.0:
                            print('**')
                            third_id = id

                            status = 1
                            occupied_list.append(third_id)
                            break
                    else:
                        pass
                else:
                    pass
            else:
                pass
    if status == 1:
        dict[atom_id] = [second_id, third_id]
    else:
        selected_list.remove(atom_id)    

key_list = []
for key, value in dict.items():
    key_list.append(key)
    oxygen_id_list.extend(value)
Th_id_array = np.array(key_list)
Oxygen_id_array = np.array(oxygen_id_list)

print(Th_id_array)
print(Oxygen_id_array)
