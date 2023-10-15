#! /public/home/ziqiangw/anaconda3/bin/python

import numpy as np
import matplotlib.pyplot as plt
import sys

# The total thermal energy due to the swap between the fastest atom in the cold 
# and the slowest atom in the hot region

num = sys.argv[1]
with open ('seed_'+num+'/log.lammps', 'r') as file:
    while True:
        line = file.readline()
        ls = line.split()
        if len(ls) == 5:
            if ls[0] == '1200000': # The system is excepted to reach the thermal equilibrium after 0.8 ns
                cumulative_energy = float(ls[1]) # The total energy due to the swap is similarly equal to the energy
            else:                          # which is transfered from the hot region to the cold by the system
                pass
        elif len(ls) == 4:
            if ls[1] == 'wall':
              #  print(ls)
                break
            else:
                pass
        elif len(ls) == 10:
            if ls[0] == 'orthogonal':
                xmin,ymin,zmin,xmax,ymax,zmax = float(ls[3][1:]), float(ls[4]), float(ls[5][:-1]), float(ls[7][1:]), float(ls[8]), float(ls[9][:-1])
                lenx = xmax-xmin
                leny = ymax-ymin
                lenz = zmax-zmin
            else:
                pass

temp_list = []
atom_num_list = []
bin_loc_list = []

binnum = 20
with open ('seed_'+num+'/profile_600K.mp', 'r') as file:
    for i in file.readlines()[-binnum:]:
        temp_list.append(float(i.split()[-1]))
        atom_num_list.append(float(i.split()[-2]))
        bin_loc_list.append(float(i.split()[-3]))

kb = 8.6173e-05 #unnits eV/K Boltzmann constant
heat_trans_len = leny  # The total length of the box in the direction of heat transfer
index = int(binnum/2)
temp_ls = [temp_list[i]/kb for i in range(2, index-1)]  # Filter the unstable data at the boundary
len_ls = [bin_loc_list[i]*heat_trans_len*1.0E-10 for i in range(2, index-1)]

xcoord_ls = [bin_loc_list[i]*heat_trans_len*1.0e-10 for i in range(index+2,binnum-2)]
ycoord_ls = [temp_list[i]/kb for i in range(index+2,binnum-2)]

# Fitting the discrete data points into a straight line
model = np.polyfit(len_ls, temp_ls, 1)
slope_value,intercept = model
model_1 = np.polyfit(xcoord_ls, ycoord_ls,1)
slope_1, intercept_1 = model_1
pred_value = [slope_value*i+intercept for i in len_ls]
pred_1 = [slope_1*i+intercept_1 for i in xcoord_ls]

#Determine the transfered thermal energy per second
deltatime = 1200.0 # unit of ps
deltatime = (float(deltatime))*1.0E-12 # time in second
heat_flux = ((cumulative_energy/deltatime)*1.60217E-19/2.0) #unit of Watt(1 eV/s = 1.60217E-19 Watts)
                                      # unit of Watt  The hot region is in the center so divided by 2

# Determine the area of the cross section through which the heat flux passes
 
crossarea = lenx*lenz*1.0E-20   #unit of square meter
delta_heat = heat_flux/crossarea  # the thermal energy per time(s) per area(m2)
slope = (slope_value+(-slope_1))/2.0
therm_condu = delta_heat/slope
print('The thermal conductivity is ' + str(therm_condu) + ' unit of W/m*K\n')
with open ('thermal_conductivity.txt', 'a+') as file:
    file.write(num+' : '+str(therm_condu)+'\n')

####
#----- Visualation --------
####
xcoord = [i*leny for i in bin_loc_list]
len_ls = [i*1.0E+10 for i in len_ls]
xcoord_ls = [i*1.0e+10 for i in xcoord_ls]
templist = [temp/kb for temp in temp_list]
plt.plot(xcoord, templist, color='green', linestyle='dashed', \
         linewidth = 2, marker = 'o', markersize=6)
plt.plot(len_ls, pred_value, color='red', linestyle='solid', \
         linewidth = 3)
plt.plot(xcoord_ls, pred_1, color='red', linestyle='solid', lw=3)
plt.xlabel('x-coordination(Å)', weight = 'bold')
plt.ylabel('Temperature(K)', weight = 'bold')
plt.title('Temperature gradient', weight = 'bold')
plt.savefig('results.tiff', dpi = 300.0, bbox_inches = 'tight')
plt.show()

'''
import os
if os.path.exists(file_directory):
    pass
else:
    os.makedirs(file_directory)
    print('The file has been made!')
    
with open (file_directory + '/therm_condu.txt', 'a+') as file:
    file.seek(0)
    data = file.read()
    ls = data.split()
    if len(ls) == 5 or len(ls) == 10 or len(ls) == 15 or len(ls) == 20:
        file.write('\n')
        file.write(' ' + str(therm_condu))
    else:
        file.write(' ' + str(therm_condu))'''
