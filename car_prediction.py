# -*- coding: utf-8 -*-
"""Car Prediction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/191XVCLj_2zREQ_6zc8oCxppuu6CNkaqT

class 24

**Problem definition**

This is the first step of machine learning life cycle.Here we analyse what kind of problem is, how to solve it. So for this project we are using a car dataset, where we want to predict the selling price of car based on its certain features. Since we need to find the real value, with real calculation, therefore this problem is regression problem. We will be using regression machine learning algorithms to solve this problem.
"""

# import libraries
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

"""**Data Gathering**"""

df = pd.read_csv('/content/car data.csv')
df.head()

"""**Data Preparation**"""

df.columns

df.isnull().sum()

df.describe()

df['Car_Name'].unique()

df['Car_Name'].nunique()

df['Fuel_Type'].unique()

df['Seller_Type'].unique()

df['Transmission'].unique()

"""**Feature Engineering**"""

#drop/remove car name
df = df.drop('Car_Name', axis=1)

df

#add another column 
df['Current_year'] = 2021
df.head()

df['No_of_year'] = df['Current_year']-df['Year']
df.head()

df = df.drop('Year',axis=1)
df = df.drop('Current_year',axis=1)
df.head()

# for Fuel_Type,	Seller_Type,	Transmission we have to convert string to numbers
# Fuel_Type(3),	Seller_Type(2),	Transmission(2)

#Creating dummy variables
# dummies = pd.get_dummies(df.Fuel_Type)
# dummies

#adding those dummies to df
# merge = pd.concat([df,dummies],axis='columns')
# merge

#drop the original column -'Fuel_Type'
# final = merge.drop(['Fuel_Type'],axis='columns')
# final.head()

#Drop the unnessary column- dummy variable trap
# final = final.drop(['CNG'],axis=columns)    #drop last column of 'Fuel_type'
# final.head()

# we can do this in other way , 
# all columns-> Creating dummies, adding dummies to df, drop original column, drop one unnessesary column-dummy variable trap, at once by doing this
final_df = pd.get_dummies(df, drop_first=True) #drop_first= True - drop one unnessesary column-dummy variable trap
final_df.head()

final_df.corr()

"""**Heatmap**"""

import seaborn as sns
corr = final_df.corr()
sns.heatmap(corr,annot=True)
#negative correlation is inversely proportional 
# Fuel_Type_Petrol vs Fuel_Type_Diesel =-0.98, when Fuel_Type_Petrol increases Fuel_Type_Diesel decreases and vice-versa.

"""**Features and target variable**"""

# taking all the features except "selling price"
x = final_df.iloc[:,1:]
# taking "selling price" as y , as it is our target variable
y = final_df.iloc[:,0]

x.head()

y.head()

"""**Feature importance**"""

#Find out which feature is more important
#checking and comparing the importance of features
from sklearn.ensemble import ExtraTreesRegressor
#creating object
model = ExtraTreesRegressor()
#fit the model
model.fit(x,y)  

print(model.feature_importances_)

#plot graph of feature importances for better visualization
feat_importances = pd.Series(model.feature_importances_, index=x.columns) #index=x.columns->to put column names
# considering top 8 important features
feat_importances.nlargest(8).plot(kind='barh')  #nlargest(8)--> 8 most imp features, barh--> horizontal bar grph 
plt.show()

"""**Splitting data into training and testing**"""

import sklearn
from sklearn.model_selection import train_test_split
xtrain,xtest,ytrain,ytest = train_test_split(x,y,test_size=0.25,random_state=5)

#to store the final dataset in a csv file
final_df.to_csv('final_dataset.csv')

"""#Fitting and evaluating different models
Here I am using three models :


1. Linear Regression
2. Decision Tree
3. Random forest Regressor

I will fit these models and then choose one with the better accuracy. You can use any regression model as per your choice.

**1. Linear Regression**
"""

from sklearn.linear_model import LinearRegression
#creating object for linear regression
reg=LinearRegression()
#fitting the linear regression model
reg.fit(xtrain,ytrain)

# Predict on the test data: y_pred
ytest_pred = reg.predict(xtest)


#metrics
from sklearn import metrics
#print mean absolute error
print('MAE:', metrics.mean_absolute_error(ytest, ytest_pred))
#print mean squared error
print('MSE:', metrics.mean_squared_error(ytest, ytest_pred))
#print the root mean squared error
print('RMSE:', np.sqrt(metrics.mean_squared_error(ytest, ytest_pred)))
#print R2 metrics score
R2 = metrics.r2_score(ytest,ytest_pred)
print('R2:',R2)

"""**2. Decision tree Model**"""

from sklearn.tree import DecisionTreeRegressor

#creating object for Decision tree
tree = DecisionTreeRegressor()

#fitting the decision tree model
tree.fit(xtrain,ytrain)

# Predict on the test data: ytest_pred
ytest_pred = tree.predict(xtest)

#print errors
from sklearn import metrics
print('MAE:', metrics.mean_absolute_error(ytest, ytest_pred))
print('MSE:', metrics.mean_squared_error(ytest, ytest_pred))
print('RMSE:', np.sqrt(metrics.mean_squared_error(ytest, ytest_pred)))
R2 = metrics.r2_score(ytest,ytest_pred)
print('R2:',R2)

"""**3. Random Forest**"""

from sklearn.ensemble import RandomForestRegressor    #RandomForestRegressor - bcuz it is predicting selling price (continuous val)

regressor = RandomForestRegressor(n_estimators = 100, random_state = 42)

regressor.fit(xtrain,ytrain)

# Predict on the test data: ytest_pred
ytest_pred = regressor.predict(xtest)

#print errors
from sklearn import metrics
print('MAE(mean_absolute_error):', metrics.mean_absolute_error(ytest, ytest_pred))
print('MSE(mean_squared_error):', metrics.mean_squared_error(ytest, ytest_pred))
print('RMSE:', np.sqrt(metrics.mean_squared_error(ytest, ytest_pred)))
R2 = metrics.r2_score(ytest,ytest_pred)
print('R2(r2_score):',R2)

# n_estimators - This parameter defines the number of trees in the random forest. 
# criterion gini - We have already discuss it in decision tree. 
# To make a split in tree we need to calculate impurities that can be entropy and gini. 
# In python sklearn by default gini is calculated. 
#  (In short to make a decision in decision tree we have to calculate gini index 
# and then join together these trees form random forest).

# Random State- Random state can be any integer. 
# The reason behind defining random state parameters is to initialize a random number generator 
# which ensures that the splits that you generate are reproducible. 

# What if you don't define a random state-  If we don't define a random state,
#  every time when we run(execute) code a new random value is generated and the train 
# and test datasets would have different values each time.

# Bootstrap = True , Bagging (Bootstrap Aggregation)

# This is done to create several subsets of data from training sample, chosen randomly.
#  Then form decision trees for each subsets of data and then ensemble them together to form random forest. 

# Bagging is done to reduce variance of decision tree.  (Bias and variance).

"""**We want our R2 score to be maximum and other errors to be minimum for better results**

**Random forest regressor is giving better results. therefore we will hypertune this model and then fit, predict.**

**Hyperparamter tuning**
"""

#n_estimators = The number of trees in the forest.
n_estimators = [int(x) for x in np.linspace(start = 100, stop = 1200, num = 12)]
print(n_estimators)

from sklearn.model_selection import RandomizedSearchCV

#Randomized Search CV

# Number of trees in random forest
n_estimators = [int(x) for x in np.linspace(start = 100, stop = 1200, num = 12)]
# Number of features to consider at every split
max_features = ['auto', 'sqrt']
# Maximum number of levels in tree
max_depth = [int(x) for x in np.linspace(5, 30, num = 6)]
# max_depth.append(None)
# Minimum number of samples required to split a node
min_samples_split = [2, 5, 10, 15, 100]
# Minimum number of samples required at each leaf node
min_samples_leaf = [1, 2, 5, 10]

# Create the random grid
random_grid = {'n_estimators': n_estimators,
               'max_features': max_features,
               'max_depth': max_depth,
               'min_samples_split': min_samples_split,
               'min_samples_leaf': min_samples_leaf}

print(random_grid)

# Use the random grid to search for best hyperparameters
# First create the base model to tune
rf = RandomForestRegressor()

# Random search of parameters, using 3 fold cross validation, 
# search across 100 different combinations
rf_random = RandomizedSearchCV(estimator = rf, param_distributions = random_grid,
                               scoring='neg_mean_squared_error', n_iter = 100, cv = 5, verbose=2, random_state=42, n_jobs = 1)

#fit the random forest model
rf_random.fit(xtrain,ytrain)

#displaying the best parameters
rf_random.best_params_

rf_random.best_score_

"""#Final Predictions"""

#predicting against test data
ytest_pred=rf_random.predict(xtest)
#print the erros
print('MAE:', metrics.mean_absolute_error(ytest, ytest_pred))
print('MSE:', metrics.mean_squared_error(ytest, ytest_pred))
print('RMSE:', np.sqrt(metrics.mean_squared_error(ytest, ytest_pred)))
R2 = metrics.r2_score(ytest,ytest_pred)
print('R2:',R2)

"""#Save the model"""

import pickle
# open a file, where you ant to store the data
file = open('car_price_model.pkl', 'wb')

# dump information to that file
pickle.dump(rf_random, file)

