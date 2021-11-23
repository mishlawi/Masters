# -*- coding: utf-8 -*-
"""
Created on Mon Nov 22 18:46:11 2021

@author: via
"""
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

# avg_speed_diff diz nos o nivel de transito (nenhum, medio, alto, mt alto)
# AVG_CLOUDINESS tem dados em falta
# AVG_RAIN tem dados em falta



#print(training.head())

training = pd.read_csv('training_data.csv' ,sep=',', encoding='gbk')

  #estes prints so sao dados, depois remove-se
   #print(training.isna().any())
   #print(training.isna().sum()) # nr de elementos em falta
   
   # o parametro avg_rain ou está a NULL ou está em falta, em cada row
   # por isso vou cortá-lo
   # o parametro avg_precipitation esta sempre a 0, corto? up of debate porque pode nao ter chovido xD

clean = training.drop('AVERAGE_RAIN',1)
clean = clean.drop('AVERAGE_PRECIPITATION',1)
clean = clean.fillna(method='bfill').fillna(method='ffill')


#plt.scatter( training['AVERAGE_SPEED_DIFF'], training['AVERAGE_FREE_FLOW_SPEED'] )


#to be used
"""
X = training[['AVERAGE_FREE_FLOW_SPEED','AVERAGE_TIME_DIFF','AVERAGE_FREE_FLOW_TIME','LUMINOSITY','AVERAGE_TEMPERATURE','AVERAGE_ATMOSP_PRESSURE','AVERAGE_HUMIDITY','AVERAGE_WIND_SPEED','AVERAGE_CLOUDINESS','AVERAGE_PRECIPITATION','AVERAGE_RAIN']] 
y= training['AVERAGE_SPEED_DIFF']
X_train,x_test,Y_train,y_test = train_test_split(X,y,test_size=0.2)
"""
