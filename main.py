# -*- coding: utf-8 -*-
"""
Created on Mon Nov 22 18:46:11 2021

@author: via
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from sklearn.tree import DecisionTreeRegressor
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import confusion_matrix
from sklearn.neighbors import KNeighborsClassifier

'''
LEITURA DO DATASET
'''
# os.chdir('D:\OneDrive - Mestrado\OneDrive - Universidade do Minho\MEI\DAA\TP\daa') 
training = pd.read_csv('training_data.csv', encoding='latin')
test = pd.read_csv('test_data.csv', encoding='latin')

'''
ELIMINAR COLUNAS SEM INFORMACAO
'''
# AVERAGE_PRECIPITATION
training = training.drop('AVERAGE_PRECIPITATION',axis=1)
test = test.drop('AVERAGE_PRECIPITATION',axis=1)

'''
REMOVER LINHAS ERRADAS NO DATASET
(possivelmente nao aplicavel)
'''
training['record_date'] = pd.to_datetime(training['record_date'], errors='coerce')
training = training.dropna(subset=['record_date'])
test['record_date'] = pd.to_datetime(test['record_date'], errors='coerce')
test = test.dropna(subset=['record_date'])


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
training.loc[training.AVERAGE_CLOUDINESS == 'nuvens quebrados', 'AVERAGE_CLOUDINESS'] = 'céu pouco nublado'
training.loc[training.AVERAGE_CLOUDINESS == 'nuvens quebradas', 'AVERAGE_CLOUDINESS'] = 'céu pouco nublado'
training.loc[training.AVERAGE_CLOUDINESS == 'tempo nublado', 'AVERAGE_CLOUDINESS'] = 'céu nublado'
training.loc[training.AVERAGE_CLOUDINESS == 'nublado', 'AVERAGE_CLOUDINESS'] = 'céu nublado'

test.loc[training.AVERAGE_CLOUDINESS == 'céu claro', 'AVERAGE_CLOUDINESS'] = 'céu limpo'
test.loc[training.AVERAGE_CLOUDINESS == 'algumas nuvens', 'AVERAGE_CLOUDINESS'] = 'céu pouco nublado'
test.loc[training.AVERAGE_CLOUDINESS == 'nuvens dispersas', 'AVERAGE_CLOUDINESS'] = 'céu pouco nublado'
test.loc[training.AVERAGE_CLOUDINESS == 'nuvens quebrados', 'AVERAGE_CLOUDINESS'] = 'céu pouco nublado'
test.loc[training.AVERAGE_CLOUDINESS == 'nuvens quebradas', 'AVERAGE_CLOUDINESS'] = 'céu pouco nublado'
test.loc[training.AVERAGE_CLOUDINESS == 'tempo nublado', 'AVERAGE_CLOUDINESS'] = 'céu nublado'
test.loc[training.AVERAGE_CLOUDINESS == 'nublado', 'AVERAGE_CLOUDINESS'] = 'céu nublado'

# AVERAGE_RAIN
training.loc[training.AVERAGE_RAIN == 'chuva leve', 'AVERAGE_RAIN'] = 'chuva fraca' 
training.loc[training.AVERAGE_RAIN == 'chuvisco fraco', 'AVERAGE_RAIN'] = 'chuva fraca' 
training.loc[training.AVERAGE_RAIN == 'chuvisco e chuva fraca', 'AVERAGE_RAIN'] = 'chuva fraca' 
training.loc[training.AVERAGE_RAIN == 'chuva', 'AVERAGE_RAIN'] = 'chuva moderada' 
training.loc[training.AVERAGE_RAIN == 'chuva de intensidade pesada', 'AVERAGE_RAIN'] = 'chuva forte' 
training.loc[training.AVERAGE_RAIN == 'chuva de intensidade pesado', 'AVERAGE_RAIN'] = 'chuva forte' 
training.loc[training.AVERAGE_RAIN == 'céu limpo', 'AVERAGE_RAIN'] = 'sem chuva'

test.loc[training.AVERAGE_RAIN == 'chuva leve', 'AVERAGE_RAIN'] = 'chuva fraca' 
test.loc[training.AVERAGE_RAIN == 'chuvisco fraco', 'AVERAGE_RAIN'] = 'chuva fraca' 
test.loc[training.AVERAGE_RAIN == 'chuvisco e chuva fraca', 'AVERAGE_RAIN'] = 'chuva fraca' 
test.loc[training.AVERAGE_RAIN == 'chuva', 'AVERAGE_RAIN'] = 'chuva moderada' 
test.loc[training.AVERAGE_RAIN == 'chuva de intensidade pesada', 'AVERAGE_RAIN'] = 'chuva forte' 
test.loc[training.AVERAGE_RAIN == 'chuva de intensidade pesado', 'AVERAGE_RAIN'] = 'chuva forte' 
test.loc[training.AVERAGE_RAIN == 'céu limpo', 'AVERAGE_RAIN'] = 'sem chuva'


'''
FUNCOES DE TRANSFORMACAO EM VALORES NUMERICOS
'''
# AVERAGE_SPEED_DIFF
'''
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
'''
    
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
        return 0
    elif( tempo == 'céu pouco nublado' ):
        return 1/2
    elif( tempo == 'céu nublado' ):
        return 2/2

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
# acho que esta coluna não devia passar para numérica, porque são estes dados que temos que treinar 
# o modelo para prever, e na submissão tem que ir textual, então acho que faz sentido deixar textual
#training['AVERAGE_SPEED_DIFF'] = training['AVERAGE_SPEED_DIFF'].apply(speedType)

# LUMINOSITY
training['LUMINOSITY'] = training['LUMINOSITY'].apply(luminosityType)
test['LUMINOSITY'] = test['LUMINOSITY'].apply(luminosityType)

'''
# NAO FUNCIONA aqui mas no colab funciona
# enconded altera os valores textuais para numéricos (acaba por ser o mesmo que estamos a fazer,
# e a diferença no score é nenhum por isso tbem não interessa muito acho eu)
'''
#from sklearn.preprocessing import LabelEncoder
#label_encoder = LabelEncoder()
#encoded_luminosity = label_encoder.fit_transform(training[["LUMINOSITY"]])
#training[["LUMINOSITY"]] = encoded_luminosity
#encoded_luminosity = label_encoder.fit_transform(test[["LUMINOSITY"]])
#test[["LUMINOSITY"]] = encoded_luminosity


# AVERAGE_CLOUDINESS
training['AVERAGE_CLOUDINESS'] = training['AVERAGE_CLOUDINESS'].apply(weatherType)
test['AVERAGE_CLOUDINESS'] = test['AVERAGE_CLOUDINESS'].apply(weatherType)

# AVERAGE_RAIN
training['AVERAGE_RAIN'] = training['AVERAGE_RAIN'].apply(rainType)
test['AVERAGE_RAIN'] = test['AVERAGE_RAIN'].apply(rainType)


training = training.sort_values(by=['record_date'])
test = test.sort_values(by=['record_date'])

#######################################################################
# OS VALORES TEXTUAIS ESTAO TODOS EM NUMERICO NESTE PONTO



'''
INTERPOLACAO PARA PREENCHIMENTO DE CÉLULAS VAZIAS
'''
training['AVERAGE_CLOUDINESS'] = training['AVERAGE_CLOUDINESS'].interpolate(method = 'linear').fillna(method='bfill')
training['AVERAGE_RAIN'] = training['AVERAGE_RAIN'].interpolate(method = 'linear').fillna(method='bfill')
test['AVERAGE_CLOUDINESS'] = test['AVERAGE_CLOUDINESS'].interpolate(method = 'linear').fillna(method='bfill')
test['AVERAGE_RAIN'] = test['AVERAGE_RAIN'].interpolate(method = 'linear').fillna(method='bfill')

# não funciona
#training = training.interpolate(method ='linear', limit_direction ='forward')
# ha varias funcoes de interpolação
#training = training.interpolate(method = 'time') ver isto nao sei mexer nas datas


#plt.scatter( training['AVERAGE_SPEED_DIFF'], training['AVERAGE_FREE_FLOW_SPEED'] )

# matriz de correlação - ajuda a perceber se há colunas redundantes
corr_matrix = training.corr()
f,ax = plt.subplots(figsize=(8,6))
sns.heatmap(corr_matrix,vmin=-1,vmax=1,square=True,annot=True)

# FARÁ SENTIDO NORMALIZAR ESTES VALORES? 
#min_max_scaler = preprocessing.MinMaxScaler(feature_range=(0,1))
#training['AVERAGE_FREE_FLOW_SPEED'] = min_max_scaler.fit_transform(training[['AVERAGE_FREE_FLOW_SPEED']])
#test['AVERAGE_FREE_FLOW_SPEED'] = min_max_scaler.fit_transform(test[['AVERAGE_FREE_FLOW_SPEED']])

x = training.drop(['AVERAGE_SPEED_DIFF'], axis=1)
y = training['AVERAGE_SPEED_DIFF'].to_frame()
x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.2201)

# drop de colunas textuais e datetime não suportadas pelo DecisionTree
# also: outros métodos de treino/previsão?
x_train = x_train.drop(['city_name','record_date'],axis=1)
x_test = x_test.drop(['city_name','record_date'],axis=1)
x = x.drop(['city_name','record_date'],axis=1)
test = test.drop(['city_name','record_date'],axis=1)

# outro método de treino
#knn = KNeighborsClassifier(n_neighbors=3);
#knn.fit(x,y.values.ravel())
#print(knn.score(test, y_test))


# para dados contínuos
#clf = DecisionTreeRegressor(random_state=2021)

# para dados não contínuos
clf = DecisionTreeClassifier(random_state=2021)

clf.fit(x,y)

predictions = clf.predict(x_test)

predictionstest = clf.predict(test)

# métricas de qualidade e avaliação do modelo
# ------- dados contínuos -------
# mae - measures the average magnitude of the errors (express the error in units pf the variable of interest)
#mean_absolute_error(test,predictions)
# mse - measure the average of squared error (squaring the error, gives high wait to large errors)
#mean_squared_error(test,predictions)

# ------- apenas para dados não continuos -------
# accuracy
# SCORE QUE TEREMOS NA SUBMISSÃO (em principio)
pseudoScore = accuracy_score(y_test,predictionstest)
# precision aka sensitivity - measure of exactness (determines the fraction of relevant items aomg the retrieved)
#precision_score(y_test,predictions,average='macro')
# recall aka specificity - measure of completeness (determines the fraction of relevant items that were obtained)
#recall_score(y_test,predictions,average='macro')
# true and false positives and negatives        
#confusion_matrix(y_test,predictions)

predictions = pd.DataFrame(predictions, columns=['Speed_Diff'])
predictions.index.name='RowId'
predictions.index += 1 
predictions.to_csv("./predictions.csv")

predictionstest = pd.DataFrame(predictionstest, columns=['Speed_Diff'])
predictionstest.index.name='RowId'
predictionstest.index += 1 
predictionstest.to_csv("./predictionstest.csv")
