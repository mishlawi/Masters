# -*- coding: utf-8 -*-
"""
Created on Mon Nov 22 18:46:11 2021

@author: via
"""
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

# avg_speed_diff diz nos o nivel de transito (nenhum, medio, alto, mt alto)

training = pd.read_csv('training_data.csv' ,sep=',', encoding='gbk')

#print(training.head())


plt.scatter( training['AVERAGE_SPEED_DIFF'], training['AVERAGE_FREE_FLOW_SPEED'] )

X = training[['AVERAGE_FREE_FLOW_SPEED','AVERAGE_TIME_DIFF','AVERAGE_FREE_FLOW_TIME','LUMINOSITY','AVERAGE_TEMPERATURE','AVERAGE_ATMOSP_PRESSURE','AVERAGE_HUMIDITY','AVERAGE_WIND_SPEED','AVERAGE_CLOUDINESS','AVERAGE_PRECIPITATION','AVERAGE_RAIN']] 
y= training['AVERAGE_SPEED_DIFF']
X_train,x_test,Y_train,y_test = train_test_split(X,y,test_size=0.2)

