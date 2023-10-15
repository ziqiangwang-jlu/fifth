#! /public/home/ziqiangw/anaconda3/bin/python


import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.datasets import load_boston
import pandas as pd
from statistics import mean, pstdev
from scipy.interpolate import make_interp_spline

'''boston = load_boston()
print(boston.data.shape)
print(boston.feature_names)
data = pd.DataFrame(boston.data)
data.columns = boston.feature_names
print(data.head(10))
print('The shape of the target: ', boston.target.shape)
data['price'] = boston.target
print(data.head())

print(data.describe())
print(data.info())
x = boston.data
y = boston.target
from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state = 0)
print('xtrain shape :', x_train.shape)
print('xtest shape:', x_test.shape)
print('ytrain shape:', y_train.shape)
print('ytest shape:', y_test.shape)

regressor = LinearRegression()
regressor.fit(x_train, y_train)
y_pred = regressor.predict(x_test)
plt.scatter(y_test, y_pred, c = 'red')
plt.xlabel('price')
plt.ylabel('pred')
plt.show()
quit()'''


#therm_condu_list = [8.994, 5.991, 4.364, 3.551]  # The thermal conductivities of the pure ThO2 at different temperatures
therm_condu_list = [7.193, 4.91, 3.69, 3.06]  # The thermal conductivities of the pure ThO2 
                                                
inverse_list = [1.0/value for value in therm_condu_list]
temp_list = [600.0, 900.0, 1200.0, 1500.0]      # temperature list
temp_array = np.array(temp_list)
inverse_array = np.array(inverse_list)
temp_array = temp_array.reshape(-1, 1)  # The feature array only has one feature so the shape is one dimension 
                                        # with the length of n-samples
inverse_array = inverse_array.reshape(-1, 1) # The target array 

# adopt the linear regression algorithm in the sk-learn module
regressor = LinearRegression()
regressor.fit(temp_array, inverse_array)

# output the slope and intercept of the fitted line
coeff, intercept = regressor.coef_[0][0], regressor.intercept_[0]
print('coeff: ', coeff, 'intercept: ', intercept)

# Calculate the value of C in the the equation 1/k = A+BT+Cx 

one_antisites = [5.16, 4.11, 3.26, 2.74] # the thermal conductivities of the system with 1% antisites 
                                         # at different temperatures
one_error = [0.196,0.097,0.089,0.057]
five_antisites = [3.643, 3.102,2.729,2.259]
five_error = [0.114,0.0739,0.046,0.0149]
two_antisites = [4.592,3.631,3.019,2.597]
two_error = [0.14,0.062,0.077,0.029]

inverse_1_antisite = [1.0/value for value in one_antisites]
c_value_1 = [(value-(coeff*temp+intercept))/0.0025 for value, temp in zip(inverse_1_antisite, temp_list)]
inverse_2_antisite = [1.0/value for value in two_antisites]
c_value_2 = [(value-(coeff*temp+intercept))/0.005 for value, temp in zip(inverse_2_antisite, temp_list)]
inverse_5_antisite = [1.0/value for value in five_antisites]
c_value_5 = [(value-(coeff*temp+intercept))/0.01 for value, temp in zip(inverse_5_antisite, temp_list)]

c_value = c_value_1 + c_value_2 + c_value_5   # merge all three lists
mean_value, stdev = mean(c_value), pstdev(c_value)
print('mean: ', mean_value, 'standard deviation: ', stdev)


figure, ax = plt.subplots()
pred_0 = [1.0/(coeff*temp+intercept+mean_value*0.0) for temp in temp_list]
#plt.scatter(temp_list, therm_condu_list, color = 'blue', s=45, label = 'MD simulation')

#predict the thermal conductivity of the system with 0.25% Frenkel defects based on the analytical model
pred_1 = [1.0/(coeff*temp+intercept+mean_value*0.0025) for temp in temp_list]
plt.scatter(temp_list, one_antisites)
plt.errorbar(temp_list, one_antisites, yerr=one_error, fmt='o', color='blue', markersize=8,label='0.25%_Frenkel_pairs', elinewidth=3, capsize=5)

# predict the thermal conductivity of the system with 0.5% Frenkel defects based on the analytical model
pred_2 = [1.0/(coeff*temp+intercept+mean_value*0.005) for temp in temp_list]
plt.scatter(temp_list, two_antisites)
plt.errorbar(temp_list, two_antisites, yerr=two_error, color = 'red', fmt='o', markersize=8,label='0.5%_Frenkel_pairs', elinewidth=3, capsize=5)

# predict the thermal conductivity of the system with 1% Frenkel defects based on the analytical model
pred_5 = [1.0/(coeff*temp+intercept+mean_value*0.01) for temp in temp_list]
plt.scatter(temp_list, five_antisites)
plt.errorbar(temp_list, five_antisites,yerr=five_error,color='green', fmt='o', markersize=8,label = '1%_Frenkel_pairs', elinewidth=3, capsize=5)


# Make a spline curve among discrete data points
x_smooth = np.linspace(min(temp_list), max(temp_list), 300)
spline_func_2 = make_interp_spline(temp_list, pred_2)
y_smooth_2 = spline_func_2(x_smooth)
spline_func_1 = make_interp_spline(temp_list, pred_1)
y_smooth_1 = spline_func_1(x_smooth)
spline_func_5 = make_interp_spline(temp_list, pred_5)
y_smooth_5 = spline_func_5(x_smooth)
spline_func_0 = make_interp_spline(temp_list, pred_0)
y_smooth_0 = spline_func_0(x_smooth)

#plt.plot(x_smooth, y_smooth_0, linestyle = ':', color = 'red', lw = 3, label = 'Analytical model')
plt.plot(x_smooth, y_smooth_1, linestyle = '--', color = 'blue', lw = 3, label = '0.25%_Frenkel_pairs_Fit')
plt.plot(x_smooth, y_smooth_2, linestyle = '-', color = 'red', lw = 3, label = '0.5%_Frenkel_pairs_Fit')
plt.plot(x_smooth, y_smooth_5, linestyle = 'dotted', color = 'green', lw = 3, label = '1%_Frenkel_pairs_Fit')
plt.xlabel('Temperature(K)', font='Times New Roman', weight='bold')
plt.ylabel('Thermal conductivity(W/m/K)', font='Times new roman', weight='bold')
plt.xticks([600,900,1200,1500])
plt.tick_params(axis = 'x',direction='in', width=1)
plt.tick_params(axis = 'y', direction='in',width=1)
plt.tick_params(top=True, right=True)
ax.spines['left'].set_linewidth(1.0)
ax.spines['right'].set_linewidth(1.0)
ax.spines['top'].set_linewidth(1.0)
ax.spines['bottom'].set_linewidth(1.0)
plt.legend()
plt.savefig('results.png', bbox_inches = 'tight', dpi=300)
plt.show()

