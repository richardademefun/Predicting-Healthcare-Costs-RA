# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 09:03:35 2019

@author: Richard Ademefun
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 08:55:00 2019

@author: Richard Ademefun
"""

# Multiple Linear Regression

# Importing the libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.api as sm

# Importing the dataset
""" This Datase was found at
 https://www.kaggle.com/mirichoi0218/insurance#insurance.csv
Content
Columns - age: age of primary beneficiary

sex: insurance contractor gender, female, male

bmi: Body mass index, providing an understanding of body,
 weights that are relatively high or low relative to height,
 objective index of body weight (kg / m ^ 2) using the ratio
 of height to weight, ideally 18.5 to 24.9

children: Number of children covered by health insurance / Number of dependents

smoker: Smoking

region: the beneficiary's residential area in the US, northeast,
 southeast, southwest, northwest.

charges: Individual medical costs billed by health insurance """
dataset = pd.read_csv('insurance.csv')
X = dataset.iloc[:, :-1].values
y = dataset.iloc[:, 6].values

""" Separating the numerical and categorical variable so I can
 onehotencode the categorical data """
#numerical variables
numerical_data = dataset[['age','bmi',]].to_numpy()

""" The variables sex,children,smoker and region are all chategorical
 variables that need to be encoded """
#all categoriacl variables
to_be_encoded = dataset[['sex','children','smoker','region']]

# Encoding categorical data
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
enc = OneHotEncoder(handle_unknown='ignore')
enc.fit(to_be_encoded)
enc.transform(to_be_encoded)
enc.get_feature_names()
drop_enc = OneHotEncoder(drop='first').fit(to_be_encoded)
drop_enc.categories_
encoded_data = drop_enc.transform(to_be_encoded).toarray()

# Feature Scaling
from sklearn import preprocessing 
""" MIN MAX SCALER """
min_max_scaler = preprocessing.MinMaxScaler(feature_range =(0, 1)) 
  
# Scaled feature 
x_after_min_max_scaler = min_max_scaler.fit_transform(numerical_data) 

#Combine numerical and categorical data
newX = np.concatenate((encoded_data,x_after_min_max_scaler),axis=1)
# Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(newX,
                                                    y, test_size = 0.2,
                                                    random_state = 0)

# Fitting Multiple Linear Regression to the Training set
from sklearn.linear_model import LinearRegression
regressor = LinearRegression()
regressor.fit(X_train, y_train)

# Predicting the Test set results
y_pred = regressor.predict(X_test)
from sklearn.metrics import r2_score 
r2_score = r2_score(y_test, y_pred)

# Visualising the Test set results
plt.scatter(y_test,y_pred, color = 'red')
plt.title('cost of medical inssurance vs predicted cost')
plt.xlabel('cost of medical inssurance ')
plt.ylabel('predicted cost')
plt.show()

#multilinear regression summary
a = 0
b = 0
a, b = X.shape
X = np.append(arr = np.ones((a, 1)).astype(int), values = newX, axis = 1)

sigLevel = 0.05

X_opt = X[:,[0,1,2,3,4,5,6,7,8,9,10,11,12]]
regressor_OLS = sm.OLS(endog = y, exog = X_opt).fit()
regressor_OLS.summary()
pVals = regressor_OLS.pvalues
rerun_newX = newX
#Reducing the dimentions of the multilinear model by deleting columns 
#where the P values are greater than 0.05
while pVals[np.argmax(pVals)] > sigLevel:
     X_opt = np.delete(X_opt, np.argmax(pVals), axis = 1)
     rerun_newX = np.delete(newX, np.argmax(pVals-1), axis = 1)
     print("pval of dim removed: " + str(np.argmax(pVals)))
     print(str(X_opt.shape[1]) + " dimensions remaining...")
     regressor_OLS = sm.OLS(endog = y, exog = X_opt).fit()
     pVals = regressor_OLS.pvalues

regressor_OLS.summary()

# rerun model with optimised variables

# Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split
rX_train, rX_test, ry_train, ry_test = train_test_split(rerun_newX,
                                                    y, test_size = 0.2,
                                                    random_state = 0)

# Fitting Multiple Linear Regression to the Training set
from sklearn.linear_model import LinearRegression
regressor = LinearRegression()
regressor.fit(rX_train, ry_train)

# MLR Predicting the Test set results
ry_pred = regressor.predict(rX_test)

from sklearn.metrics import r2_score 
MRLr2_score = r2_score(ry_test, ry_pred)#79.8%

#forest model
from sklearn.ensemble import RandomForestRegressor
# Instantiate model with 1000 decision trees
rf = RandomForestRegressor(n_estimators = 1000, random_state = 42, verbose = 1)
# Train the model on training data
rf.fit(rX_train, ry_train)
# Predicting a new result
rfy_pred = rf.predict(rX_test)

fmr2_score = r2_score(ry_test, rfy_pred)#87.4%


# Visualising the Test set results
plt.scatter(ry_test,ry_pred, color = 'red')
plt.scatter(ry_test,rfy_pred, color = 'black')
plt.plot(np.unique(ry_test), np.poly1d(np.polyfit(ry_test,
         ry_pred, 1))(np.unique(ry_test)),'red')

plt.plot(np.unique(ry_test), np.poly1d(np.polyfit(y_test,
         rfy_pred, 1))(np.unique(y_test)),'blue',dashes=[6, 2])
plt.title('cost of medical inssurance vs predicted cost')
plt.xlabel('cost of medical inssurance ')
plt.ylabel('predicted cost')
plt.show()



