# -*- coding: utf-8 -*-
"""
Created on Mon Nov 22 18:46:11 2021

@author: via
"""
import os
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

'''
LEITURA DO DATASET
'''
# os.chdir('D:\OneDrive - Mestrado\OneDrive - Universidade do Minho\MEI\DAA\TP\daa') 
training = pd.read_csv('training_data.csv', encoding='latin')


'''
ELIMINAR COLUNAS SEM INFORMACAO
'''
# AVERAGE_PRECIPITATION
training = training.drop('AVERAGE_PRECIPITATION',1)


'''
REMOVER LINHAS ERRADAS NO DATASET
(possivelmente nao aplicavel)
'''
training['record_date'] = pd.to_datetime(training['record_date'], errors='coerce')
training = training.dropna(subset=['record_date'])


'''
VERIFICAR VALORES NUMA DETERMINADA COLUNA
'''
# AVERAGE_SPEED_DIFF
training.AVERAGE_SPEED_DIFF.unique()

# LUMINOSITY
training.LUMINOSITY.unique()

# AVERAGE_CLOUDINESS
training.AVERAGE_CLOUDINESS.unique()

# AVERAGE_RAIN
training.AVERAGE_RAIN.unique() 


'''
LIMPEZA DE VALORES
'''
# AVERAGE_CLOUDINESS
training.loc[training.AVERAGE_CLOUDINESS == 'céu claro', 'AVERAGE_CLOUDINESS'] = 'céu limpo'
training.loc[training.AVERAGE_CLOUDINESS == 'algumas nuvens', 'AVERAGE_CLOUDINESS'] = 'céu pouco nublado'
training.loc[training.AVERAGE_CLOUDINESS == 'nuvens dispersas', 'AVERAGE_CLOUDINESS'] = 'céu pouco nublado'
training.loc[training.AVERAGE_CLOUDINESS == 'nuvens quebrados', 'AVERAGE_CLOUDINESS'] = 'céu pouco nublado'
training.loc[training.AVERAGE_CLOUDINESS == 'nuvens quebradas', 'AVERAGE_CLOUDINESS'] = 'céu pouco nublado'
training.loc[training.AVERAGE_CLOUDINESS == 'tempo nublado', 'AVERAGE_CLOUDINESS'] = 'céu nublado'
training.loc[training.AVERAGE_CLOUDINESS == 'nublado', 'AVERAGE_CLOUDINESS'] = 'céu nublado'

# AVERAGE_RAIN
training.loc[training.AVERAGE_RAIN == 'chuva leve', 'AVERAGE_RAIN'] = 'chuva fraca' 
training.loc[training.AVERAGE_RAIN == 'chuvisco fraco', 'AVERAGE_RAIN'] = 'chuva fraca' 
training.loc[training.AVERAGE_RAIN == 'chuvisco e chuva fraca', 'AVERAGE_RAIN'] = 'chuva fraca' 
training.loc[training.AVERAGE_RAIN == 'chuva', 'AVERAGE_RAIN'] = 'chuva moderada' 
training.loc[training.AVERAGE_RAIN == 'chuva de intensidade pesada', 'AVERAGE_RAIN'] = 'chuva forte' 
training.loc[training.AVERAGE_RAIN == 'chuva de intensidade pesado', 'AVERAGE_RAIN'] = 'chuva forte' 
training.loc[training.AVERAGE_CLOUDINESS == 'céu limpo', 'AVERAGE_RAIN'] = 'sem chuva'


'''
FUNCOES DE TRANSFORMACAO EM VALORES NUMERICOS
'''
# AVERAGE_SPEED_DIFF
def speedType(vel):
    if( vel == 'None'):
        return 0
    elif( vel == 'Low' ):
        return 1/4
    elif( vel == 'Medium'):
        return 2/4
    elif( vel == 'High' ):
        return 3/4
    elif( vel == 'Very_High'):
        return 4/4
    
# LUMINOSITY
def luminosityType(lux):
    if( lux == 'DARK' ):
        return 0
    elif( lux == 'LOW_LIGHT' ):
        return 1/2
    elif( lux == 'LIGHT' ):
        return 2/2
    
# AVERAGE_CLOUDINESS
def weatherType(tempo):
    if( tempo == 'céu limpo' ):
        return 0.0
    elif( tempo == 'céu pouco nublado' ):
        return 0.5
    elif( tempo == 'céu nublado' ):
        return 1

# AVERAGE_RAIN
def rainType(chuva):
    if( chuva == 'sem chuva'):
        return 0.0
    elif( chuva == 'aguaceiros fracos' ):
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
# AVERAGE_SPEED_DIFF
training['AVERAGE_SPEED_DIFF'] = training['AVERAGE_SPEED_DIFF'].apply(speedType)

# LUMINOSITY
training['LUMINOSITY'] = training['LUMINOSITY'].apply(luminosityType)

# AVERAGE_CLOUDINESS
training['AVERAGE_CLOUDINESS'] = training['AVERAGE_CLOUDINESS'].apply(weatherType)

# AVERAGE_RAIN
training['AVERAGE_RAIN'] = training['AVERAGE_RAIN'].apply(rainType)



#######################################################################
# OS VALORES TEXTUAIS ESTAO TODOS EM NUMERICO NESTE PONTO. E NECESSARIO VER COMO FAZER AS INTERPOLACOES


# clean = training.drop('AVERAGE_PRECIPITATION',1)
# clean = clean.fillna(method='bfill').fillna(method='ffill')


training = training.interpolate(method = 'linear').fillna(method='bfill')
# ha varias funcoes de interpolação
# training = training.interpolate(method = 'time') ver isto nao sei mexer nas datas



#plt.scatter( training['AVERAGE_SPEED_DIFF'], training['AVERAGE_FREE_FLOW_SPEED'] )


#to be used
"""
X = training[['AVERAGE_FREE_FLOW_SPEED','AVERAGE_TIME_DIFF','AVERAGE_FREE_FLOW_TIME','LUMINOSITY','AVERAGE_TEMPERATURE','AVERAGE_ATMOSP_PRESSURE','AVERAGE_HUMIDITY','AVERAGE_WIND_SPEED','AVERAGE_CLOUDINESS','AVERAGE_PRECIPITATION','AVERAGE_RAIN']] 
y= training['AVERAGE_SPEED_DIFF']
X_train,x_test,Y_train,y_test = train_test_split(X,y,test_size=0.2)
"""
