#! /public/home/ziqiangw/anaconda3/bin/python

#Calculating the thermal conductivities of perfect ThO2 systems with five different lengths 
#determine the linear relationship between 1/k and 1/ly 
#determine the thermal conductivity of the infinitely large system based on the fitted line,
# which is defined as the bulk thermal conductivity
# By Ziqiang Wang on Jilin university

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator


y_inverse_1500 = [2.9215,3.065,3.12,3.172,3.279] # 1500K
y_inverse_1200 = [3.655,3.69,3.888,3.989,4.00]  # k of the supercells with 5 different lengths at 1200K
y_inverse_900 = [4.6418,4.9089,5.0963,5.142,5.376] # k of the supercells with 5 different lengths at 900K
y_inverse_600 = [6.57,7.193,7.391,7.514,7.7878] # the k of the supercells with 5 different lengths at 600K
y_1500 = [1.0/value for value in y_inverse_1500] 
y_1200 = [1.0/value for value in y_inverse_1200]
y_900 = [1.0/value for value in y_inverse_900]
y_600 = [1.0/value for value in y_inverse_600]
#err_600 = [0.351,0.06,0.203,0.231,0.178]
#err_900 = [0.257,0.09,0.107,0.091,0.123]
#err_1200 = [0.137,0.059,0.0265,0.04,0.0866]
#err_1500 = [0.077,0.074,0.0744,0.041,0.0659]
x = [252.4851,336.7352,420.7689,505.045,560.92] # 5 different lengths
inverse_x = [1.0/value for value in x]
model_600 = np.polyfit(inverse_x, y_600, 1)
slope_600, intercept_600 = model_600
model_900 = np.polyfit(inverse_x, y_900, 1)
slope_900, intercept_900 = model_900
model_1200 = np.polyfit(inverse_x, y_1200, 1)
slope_1200, intercept_1200 = model_1200
model_1500 = np.polyfit(inverse_x, y_1500, 1)
slope_1500, intercept_1500 = model_1500

pred_600 = [slope_600*value+intercept_600 for value in inverse_x]
pred_900 = [slope_900*value+intercept_900 for value in inverse_x]
pred_1200 = [slope_1200*value+intercept_1200 for value in inverse_x]
pred_1500 = [slope_1500*value+intercept_1500 for value in inverse_x]
bulk_thermal_condu_600 = 1.0/intercept_600
bulk_thermal_condu_900 = 1.0/intercept_900
bulk_thermal_condu_1200 = 1.0/intercept_1200
bulk_thermal_condu_1500 = 1.0/intercept_1500

print('Bulk thermal conductivity: ', bulk_thermal_condu_600)
print('Bulk thermal conductivity: ', bulk_thermal_condu_900)
print('Bulk thermal conductivity: ', bulk_thermal_condu_1200)
print('Bulk thermal conductivity: ', bulk_thermal_condu_1500)

fig, ax = plt.subplots()
ax.scatter(inverse_x, y_600, marker = 'o', c = 'blue', s=80)
ax.scatter(inverse_x, y_900, marker = 's', c = 'orange', s=80)
ax.scatter(inverse_x, y_1200, marker = 'd', c='red', s=80)
ax.scatter(inverse_x, y_1500, marker='*', c='green', s=80)
#plt.errorbar(inverse_x, y_600, yerr=err_600, fmt='o')
#plt.errorbar(inverse_x, y_900, yerr=err_900, fmt='o')
#plt.errorbar(inverse_x, y_1200, yerr=err_1200, fmt='o')
#plt.errorbar(inverse_x, y_1500, yerr=err_1500, fmt='o')
ax.plot(inverse_x, pred_600, linestyle = '-', color = 'blue', lw=3, label = '600K')
ax.plot(inverse_x, pred_900, linestyle = '-.', color='orange', lw=3, label = '900K')
ax.plot(inverse_x, pred_1200, linestyle='dotted', color='red', lw=3, label = '1200K')
ax.plot(inverse_x, pred_1500, linestyle='dashed', color='green', lw=3, label = '1500K')
ax.set_xlabel('$1/L_{y}(1/Å)$', font='Times new roman', weight='bold')
ax.set_ylabel('$1/k(W^{-1}mK)$', font='Times new roman', weight='bold')
ax.set_xlim([0.0015,0.00475])
ax.tick_params(axis='x', direction='in', width=1)
ax.tick_params(axis='y', direction='in', width=1)
ax.tick_params(top=True, right=True)
ax.xaxis.set_minor_locator(plt.MaxNLocator(3))
ax.legend(loc='upper right')
fig.savefig('results.tiff',dpi=300, bbox_inches='tight')
plt.show()
