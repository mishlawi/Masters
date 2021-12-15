# -*- coding: utf-8 -*-
"""
Created on Mon Dec  6 19:54:55 2021

@author: tiago
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import funcoes_auxiliares as fa

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, BatchNormalization
from tensorflow.keras.wrappers.scikit_learn import KerasRegressor
from sklearn.model_selection import GridSearchCV, KFold, train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import LabelEncoder
import datetime


RANDOM_SEED = 2021

training = pd.read_csv('training_data.csv', encoding='latin')
test = pd.read_csv('test_data.csv', encoding='latin')

# AVERAGE_PRECIPITATION
training.drop('AVERAGE_PRECIPITATION',axis=1, inplace=True)
test.drop('AVERAGE_PRECIPITATION',axis=1, inplace=True)

#city_name
training.drop('city_name',axis=1,inplace=True)
test.drop('city_name',axis=1,inplace=True)

training.record_date = pd.to_datetime(training.record_date)
training['Hour'] = training.record_date.dt.hour
training['Day'] = training.record_date.dt.day
training['Month'] = training.record_date.dt.month
training['Day_Name'] = training.record_date.dt.dayofweek

test.record_date = pd.to_datetime(test.record_date)
test['Hour'] = test.record_date.dt.hour
test['Day'] = test.record_date.dt.day
test['Month'] = test.record_date.dt.month
test['Day_Name'] = test.record_date.dt.dayofweek


training.drop('record_date',axis=1, inplace=True)
test.drop('record_date',axis=1, inplace=True)

fa.limpa_valores(training,test)

training["AVERAGE_RAIN"] = LabelEncoder().fit_transform(training[["AVERAGE_RAIN"]])
test["AVERAGE_RAIN"] = LabelEncoder().fit_transform(test[["AVERAGE_RAIN"]])

training["AVERAGE_CLOUDINESS"] = LabelEncoder().fit_transform(training[["AVERAGE_CLOUDINESS"]])
test["AVERAGE_CLOUDINESS"] = LabelEncoder().fit_transform(test[["AVERAGE_CLOUDINESS"]])

training["Day_Name"] = LabelEncoder().fit_transform(training[["Day_Name"]])
test["Day_Name"] = LabelEncoder().fit_transform(test[["Day_Name"]])

training["LUMINOSITY"]  = LabelEncoder().fit_transform(training[["LUMINOSITY"]])
test["LUMINOSITY"] = LabelEncoder().fit_transform(test[["LUMINOSITY"]])


x = training.drop(['AVERAGE_SPEED_DIFF'], axis=1)
y = training['AVERAGE_SPEED_DIFF'].to_frame()

y.AVERAGE_SPEED_DIFF = LabelEncoder().fit_transform(y[["AVERAGE_SPEED_DIFF"]])


# Let's scale the features between [0-1]
scaler_X = MinMaxScaler(feature_range=(0, 1)).fit(x)
scaler_Y = MinMaxScaler(feature_range=(0, 1)).fit(y)
scaler_test = MinMaxScaler(feature_range=(0, 1)).fit(test)

# não ficam todas enter [0,1]
x = pd.DataFrame(scaler_X.transform(x[x.columns]), columns=x.columns)
y = pd.DataFrame(scaler_Y.transform(y[y.columns]), columns=y.columns) # Como voltar ao origina?
test = pd.DataFrame(scaler_test.transform(test[test.columns]), columns=test.columns)


def create_model(activation1='relu', activation2='relu', activation3='sigmoid'):
    model = Sequential()
    model.add(Dense(64, input_dim=14, activation=activation1))
    model.add(Dense(32, activation=activation2))
    model.add(Dense(16, activation=activation2)) 
    model.add(Dense(1, activation=activation3))
    model.compile(loss='categorical_crossentropy', optimizer='Adam', metrics=["accuracy"])
	
    return model


model = KerasRegressor(build_fn=create_model, verbose=1)




# optimizer = ['SGD', 'RMSprop', 'Adagrad', 'Adadelta', 'Adam', 'Adamax', 'Nadam']
activation = ['softmax', 'softplus', 'softsign', 'relu', 'tanh', 'sigmoid', 'hard_sigmoid', 'linear']
# startNodes = [60+i*10 for i in range(0,10)]
# middle = [0,1,2,3,4]


param_grid = dict(activation1=activation, activation2=activation, activation3=activation)

grid = GridSearchCV(estimator=model, param_grid=param_grid, n_jobs=-1, cv=3)
grid_result = grid.fit(x,y)

print("Best: %f using %s" % (grid_result.best_score_, grid_result.best_params_))
means = grid_result.cv_results_['mean_test_score']
stds = grid_result.cv_results_['std_test_score']
params = grid_result.cv_results_['params']
for mean, stdev, param in zip(means, stds, params):
    print("%f (%f) with: %r" % (mean, stdev, param))


training.groupby(by=['AVERAGE_SPEED_DIFF']).count()



model.fit(x, y)

predictions = model.predict(test)



'''
OUTPUT
'''

predictions = pd.DataFrame(predictions, columns=['Speed_Diff'])
predictions.index.name='RowId'
predictions.index += 1 
predictions.to_csv("./predictions/predictionsKeras"+ str(datetime.now().strftime("%Y-%m-%d %H-%M"))+".csv")






