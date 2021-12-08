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
%matplotlib inline

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, BatchNormalization
from tensorflow.keras.wrappers.scikit_learn import KerasRegressor
from sklearn.model_selection import GridSearchCV, KFold, train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import LabelEncoder

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


# Let's scale the features between [0-1]
scaler_X = MinMaxScaler(feature_range=(0, 1)).fit(x)
scaler_Y = MinMaxScaler(feature_range=(0, 1)).fit(y)
x_scaled = pd.DataFrame(scaler_X.transform(x[x.columns]), columns=x.columns)
y_scaled = pd.DataFrame(scaler_Y.transform(y[y.columns]), columns=y.columns)

def build_model( activation='relu', learning_rate=0.01 ):
    # Create a sequential model (with three layers - last one is the output)
    model = Sequential()
    model.add( Dense( 16, input_dim=14, activation=activation ) )
    model.add( Dense( 8, activation=activation ) )
    model.add( Dense( 1, activation=activation ) )
    
    # Compile the model
    # Define the loss function, the otimizer and metrics to be used
    model.compile(
        loss = 'mae',
        optimizer = tf.optimizers.Adam( learning_rate ),
        metrics = ['mae', 'mse'])
    
    return model

X_train, X_test, y_train, y_test = train_test_split(x_scaled, y_scaled,
                                                    test_size=0.2,
                                                    random_state=RANDOM_SEED)



