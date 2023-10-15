#! /public/home/ziqiangw/anaconda3/bin/python

import numpy as np
import matplotlib.pyplot as plt
import statistics

antisites_zero = [5.611,5.6252,5.6433,5.6629]
antisites_fourth = []
antisites_fourth_error = [] 
antisites_half = []
antisites_half_error = []
antisites_one = []
antisites_one_error = []
for i in [0.0025,0.005,0.01]:
    with open ('Frenkel_'+str(i)+'/lattice_constant.txt', 'r') as file:
        while True:
            line = file.readline()
            if len(line.split()) == 0:
                break
            else:
                if i == 0.0025:
                    antisites_fourth.append(float(line.split()[1]))
                    antisites_fourth_error.append(float(line.split()[-1]))
                elif i == 0.005:
                    antisites_half.append(float(line.split()[1]))
                    antisites_half_error.append(float(line.split()[-1]))
                elif i == 0.01:
                    antisites_one.append(float(line.split()[1]))
                    antisites_one_error.append(float(line.split()[-1]))

#print(*antisites_fourth)
#print(*antisites_half)
#print(*antisites_one_error)
#quit()

temp_list = [600, 900, 1200, 1500]

model = np.polyfit(temp_list, antisites_zero, 1)
x, y = model
print('The Slope: ', x)
print('The intercept: ', y)

reference = [x*value+y for value in temp_list]

c_fourth_list = []
c_half_list = []
c_one_list = []
for value, temp in zip(antisites_fourth,temp_list):
    coeff = (value-(x*temp+y))/0.0025
    c_fourth_list.append(coeff)
for value, temp in zip(antisites_half, temp_list):
    coeff = (value-(x*temp+y))/0.005
    c_half_list.append(coeff)
for value, temp in zip(antisites_one, temp_list):
    coeff = (value-(x*temp+y))/0.01
    c_one_list.append(coeff)
    
c = c_fourth_list+c_half_list+c_one_list
c_value = np.mean(c)
c_std = statistics.stdev(c) 
print('Mean value: ', c_value)
print('Standard deviation: ', c_std)

pred_fourth = [x*value+y+c_value*0.0025 for value in temp_list]
pred_half = [x*value+y+c_value*0.005 for value in temp_list]
pred_one = [x*value+y+c_value*0.01 for value in temp_list]

#plt.scatter(temp_list, antisites_fourth, s=60, color='red')
#plt.scatter(temp_list, antisites_half, s=60,color='red')
#plt.scatter(temp_list, antisites_one,  s=60, color='red')
plt.errorbar(temp_list, antisites_fourth, yerr=antisites_fourth_error, elinewidth = 3, capsize = 6, fmt='o', color='red', markersize = 10, label = '0.25%_Frenkel_pairs')
plt.errorbar(temp_list, antisites_half, yerr=antisites_half_error, elinewidth = 3, capsize = 6, fmt='o', color = 'green', markersize = 10, label = '0.5%_Frenkel_pairs')
plt.errorbar(temp_list, antisites_one, yerr=antisites_one_error, fmt='o', elinewidth = 3, capsize = 6, color = 'blue', markersize = 10, label = '1%_Frenkel_pairs')

plt.plot(temp_list, pred_fourth, linestyle='--', lw=4, color='red', label = '0.25%_Frenkel_pairs_Fit')
plt.plot(temp_list, pred_half, linestyle='--', lw=4, color='green', label = '0.5%_Frenkel_pairs_Fit')
plt.plot(temp_list, pred_one, linestyle='--', lw=4, color='blue', label = '1%_Frenkel_pairs_Fit')
plt.xticks([600,900,1200,1500])
plt.xlabel('Temperature(K)', font='Times New Roman', weight='bold')
plt.ylabel('Lattice constant(Å)', font='Times New Roman', weight= 'bold')
plt.tick_params(axis='x', direction='in', width=1)
plt.tick_params(axis='y', direction='in', width=1)
plt.tick_params(top=True, right=True)
plt.legend()
plt.savefig('Frenkel_pairs.tiff', dpi=300, bbox_inches='tight')
plt.show()


