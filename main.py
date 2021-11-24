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

training = pd.read_csv('training_data.csv', encoding='latin')


'''
# COMPUTADOR DO BARATA 
    
import os
# get current working directory
cwd = os.getcwd()
print(cwd)

os.chdir('D:\OneDrive - Mestrado\OneDrive - Universidade do Minho\MEI\DAA\TP\daa') # relative path: scripts dir is under Lab
os.getcwd()

#get files in directory
files = os.listdir(cwd) 

print(files)
'''


'''
ELIMINAR COLUNAS SEM INFORMACAO
'''
# AVERAGE_PRECIPITATION
training = training.drop('AVERAGE_PRECIPITATION',1)


'''
REMOVER LINHAS ERRADAS NO DATASET
'''
training['record_date'] = pd.to_datetime(training['record_date'], errors='coerce')
training = training.dropna(subset=['record_date'])


'''
VERIFICAR VALORES NUMA DETERMINADA COLUNA
'''
# AVERAGE_RAIN
training.AVERAGE_RAIN.unique() 

# AVERAGE_CLOUDINESS
training.AVERAGE_CLOUDINESS.unique() 

'''
LIMPEZA DE VALORES
'''
# AVERAGE_RAIN
training.loc[training.AVERAGE_RAIN == 'chuva leve'] = 'chuva fraca' 
training.loc[training.AVERAGE_RAIN == 'chuvisco fraco'] = 'chuva fraca' 
training.loc[training.AVERAGE_RAIN == 'chuvisco e chuva fraca'] = 'chuva fraca' 
training.loc[training.AVERAGE_RAIN == 'chuva'] = 'chuva moderada' 
training.loc[training.AVERAGE_RAIN == 'chuva de intensidade pesada'] = 'chuva forte' 
training.loc[training.AVERAGE_RAIN == 'chuva de intensidade pesado'] = 'chuva forte' 

# AVERAGE_CLOUDINESS
training.loc[training.AVERAGE_CLOUDINESS == 'céu claro'] = 'céu limpo'
training.loc[training.AVERAGE_CLOUDINESS == 'algumas nuvens'] = 'céu pouco nublado'
training.loc[training.AVERAGE_CLOUDINESS == 'nuvens dispersas'] = 'céu pouco nublado'
training.loc[training.AVERAGE_CLOUDINESS == 'nuvens quebrados'] = 'céu pouco nublado'
training.loc[training.AVERAGE_CLOUDINESS == 'nuvens quebradas'] = 'céu pouco nublado'
training.loc[training.AVERAGE_CLOUDINESS == 'tempo nublado'] = 'céu nublado'
training.loc[training.AVERAGE_CLOUDINESS == 'nublado'] = 'céu nublado'

training.loc[training.AVERAGE_CLOUDINESS == 'céu limpo', 'AVERAGE_RAIN'] = 0


'''
TRANSFORMACAO EM VALORES NUMERICOS
'''
# AVERAGE_RAIN
def rainType(chuva):
    if( chuva == 'aguaceiros fracos' ):
        return 1/7
    elif( chuva == 'aguaceiros' ):
        return 2/7
    elif( chuva == 'chuva fraca' ):
        return 3/7
    elif( chuva == 'chuva moderada' ):
        return 4/7
    elif( chuva == 'trovoada com chuva leve' ):
        return 5/7
    elif( chuva == 'chuva forte' ):
        return 6/7
    elif( chuva == 'trovoada com chuva' ):        
        return 7/7

'''
ALTERAR OS VALORES TEXTUAIS PARA NUMERICOS 
'''
training['AVERAGE_RAIN'] = training['AVERAGE_RAIN'].apply(rainType)


training.AVERAGE_CLOUDINESS.unique()



clean = training.drop('AVERAGE_PRECIPITATION',1)
clean = clean.fillna(method='bfill').fillna(method='ffill')




#plt.scatter( training['AVERAGE_SPEED_DIFF'], training['AVERAGE_FREE_FLOW_SPEED'] )


#to be used
"""
X = training[['AVERAGE_FREE_FLOW_SPEED','AVERAGE_TIME_DIFF','AVERAGE_FREE_FLOW_TIME','LUMINOSITY','AVERAGE_TEMPERATURE','AVERAGE_ATMOSP_PRESSURE','AVERAGE_HUMIDITY','AVERAGE_WIND_SPEED','AVERAGE_CLOUDINESS','AVERAGE_PRECIPITATION','AVERAGE_RAIN']] 
y= training['AVERAGE_SPEED_DIFF']
X_train,x_test,Y_train,y_test = train_test_split(X,y,test_size=0.2)
"""
