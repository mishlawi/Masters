# -*- coding: utf-8 -*-
"""
Created on Mon Nov 22 18:46:11 2021

@author: via
"""

from scipy.sparse import data
import funcoes_auxiliares
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
from sklearn.preprocessing import LabelEncoder

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

#city_name
training = training.drop('city_name',axis=1)
test = test.drop('city_name',axis=1)

'''
REMOVER LINHAS ERRADAS NO DATASET
(possivelmente nao aplicavel)
'''
training['record_date'] = pd.to_datetime(training['record_date'], errors='coerce')
training['record_date'].dropna()
test['record_date'] = pd.to_datetime(test['record_date'], errors='coerce')
test['record_date'].dropna()


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
funcoes_auxiliares.limpa_valores(training,test)


'''
ALTERAR OS VALORES TEXTUAIS PARA NUMERICOS 
'''
label_encoder = LabelEncoder()

#encoded_speed_diff = label_encoder.fit_transform(training[["AVERAGE_SPEED_DIFF"]])
#training["AVERAGE_SPEED_DIFF"] = encoded_speed_diff

encoded_luminosity = label_encoder.fit_transform(training[["LUMINOSITY"]])
training["LUMINOSITY"] = encoded_luminosity
encoded_luminosity = label_encoder.fit_transform(test[["LUMINOSITY"]])
test["LUMINOSITY"] = encoded_luminosity

encoded_cloudiness = label_encoder.fit_transform(training[["AVERAGE_CLOUDINESS"]])
training["AVERAGE_CLOUDINESS"] = encoded_cloudiness
encoded_cloudiness = label_encoder.fit_transform(test[["AVERAGE_CLOUDINESS"]])
test["AVERAGE_CLOUDINESS"] = encoded_cloudiness

encoded_rain = label_encoder.fit_transform(training[["AVERAGE_RAIN"]])
training["AVERAGE_RAIN"] = encoded_rain
encoded_rain = label_encoder.fit_transform(test[["AVERAGE_RAIN"]])
test["AVERAGE_RAIN"] = encoded_rain


'''
# LUMINOSITY
training['LUMINOSITY'] = training['LUMINOSITY'].apply(funcoes_auxiliares.luminosityType)
test['LUMINOSITY'] = test['LUMINOSITY'].apply(funcoes_auxiliares.luminosityType)

# AVERAGE_CLOUDINESS
training['AVERAGE_CLOUDINESS'] = training['AVERAGE_CLOUDINESS'].apply(funcoes_auxiliares.weatherType)
test['AVERAGE_CLOUDINESS'] = test['AVERAGE_CLOUDINESS'].apply(funcoes_auxiliares.weatherType)

# AVERAGE_RAIN
training['AVERAGE_RAIN'] = training['AVERAGE_RAIN'].apply(funcoes_auxiliares.rainType)
test['AVERAGE_RAIN'] = test['AVERAGE_RAIN'].apply(funcoes_auxiliares.rainType)
'''


# O index (ordem) do dataSet passa a ser definido pela data 
training.index = training['record_date']
test.index = test['record_date']

#  OS VALORES TEXTUAIS ESTAO TODOS EM NUMERICO NESTE PONTO #

#..~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~..#
# DIFERENTES INTERPOLACOES PARA PREENCHIMENTO DE CÉLULAS VAZIAS 
#..~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~..#



# interpolação por meio da data
dataInterpolation = training
dataInterpolation['AVERAGE_CLOUDINESS'] = training['AVERAGE_CLOUDINESS'].interpolate(method = 'time').fillna(method='bfill')
dataInterpolation['AVERAGE_RAIN'] = training['AVERAGE_RAIN'].interpolate(method = 'time').fillna(method='bfill')

dataInterpolationTest = test
dataInterpolationTest['AVERAGE_CLOUDINESS'] = test['AVERAGE_CLOUDINESS'].interpolate(method = 'time').fillna(method='bfill')
dataInterpolationTest['AVERAGE_RAIN'] = test['AVERAGE_RAIN'].interpolate(method = 'time').fillna(method='bfill')


# interpolação pelo index
indexInterpolation = training
indexInterpolation['AVERAGE_RAIN'] = training['AVERAGE_RAIN'].interpolate(method='index').fillna(method='bfill')
indexInterpolation['AVERAGE_CLOUDINESS'] = training['AVERAGE_CLOUDINESS'].interpolate(method = 'index').fillna(method='bfill')

indexInterpolationTest = test
indexInterpolationTest['AVERAGE_RAIN'] = test['AVERAGE_RAIN'].interpolate(method='index').fillna(method='bfill')
indexInterpolationTest['AVERAGE_CLOUDINESS'] = test['AVERAGE_CLOUDINESS'].interpolate(method = 'index').fillna(method='bfill')



# interpolaçao linear
linearInterpolation = training
linearInterpolation['AVERAGE_CLOUDINESS'] = training['AVERAGE_CLOUDINESS'].interpolate(method = 'linear').fillna(method='bfill')
linearInterpolation['AVERAGE_RAIN'] = training['AVERAGE_RAIN'].interpolate(method = 'linear').fillna(method='bfill')

linearInterpolationTest = test
linearInterpolationTest['AVERAGE_CLOUDINESS'] = test['AVERAGE_CLOUDINESS'].interpolate(method = 'linear').fillna(method='bfill')
linearInterpolationTest['AVERAGE_RAIN'] = test['AVERAGE_RAIN'].interpolate(method = 'linear').fillna(method='bfill')



'''
training['AVERAGE_CLOUDINESS'] = training['AVERAGE_CLOUDINESS'].interpolate(method = 'linear').fillna(method='bfill')
training['AVERAGE_RAIN'] = training['AVERAGE_RAIN'].interpolate(method = 'linear').fillna(method='bfill')

test['AVERAGE_CLOUDINESS'] = test['AVERAGE_CLOUDINESS'].interpolate(method = 'linear').fillna(method='bfill')
test['AVERAGE_RAIN'] = test['AVERAGE_RAIN'].interpolate(method = 'linear').fillna(method='bfill')
'''



# matriz de correlação - ajuda a perceber se há colunas redundantes
#corr_matrix = training.corr()
#f,ax = plt.subplots(figsize=(8,6))
#sns.heatmap(corr_matrix,vmin=-1,vmax=1,square=True,annot=True)

x = linearInterpolation.drop(['AVERAGE_SPEED_DIFF'], axis=1)
y = linearInterpolation['AVERAGE_SPEED_DIFF'].to_frame()
x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.2201)

# drop de colunas textuais e datetime não suportadas pelo DecisionTree
# also: outros métodos de treino/previsão?
x_train = x_train.drop('record_date',axis=1)
x_test = x_test.drop('record_date',axis=1)
x = x.drop('record_date',axis=1)
test = test.drop('record_date',axis=1)
dataInterpolationTest = dataInterpolationTest.drop('record_date',axis=1)
indexInterpolationTest = indexInterpolationTest.drop('record_date',axis=1)
linearInterpolationTest = linearInterpolationTest.drop('record_date',axis=1)


clf = DecisionTreeClassifier(random_state=2021)

clf.fit(x,y)

predictions = clf.predict(x_test)

predictionstest = clf.predict(test)


# SCORE QUE TEREMOS NA SUBMISSÃO (em principio)
pseudoScore = accuracy_score(y_test,predictionstest)
print(pseudoScore)

funcoes_auxiliares.predictions_to_csv(pred=predictions,filename="predictions")

funcoes_auxiliares.predictions_to_csv(pred=predictionstest,filename="predictionstest")



# -.-.-.-.-.-.-.-.-.
# KNN
# -.-.-.-.-.-.-.-.-.


from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report


X = dataInterpolation.drop(['AVERAGE_SPEED_DIFF'], axis=1).drop(['record_date'],axis=1)
y = dataInterpolation['AVERAGE_SPEED_DIFF'].to_frame()   

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2201)



scaler = StandardScaler()
scaler.fit(X_train)
X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)
test = scaler.transform(test)



classifier = KNeighborsClassifier(n_neighbors = 8)
classifier.fit(X_train, y_train)

y_pred = classifier.predict(test)

funcoes_auxiliares.predictions_to_csv(y_pred,"knnpredictions")


result = confusion_matrix(y_test, y_pred)
print("Confusion Matrix:")
print(result)
result1 = classification_report(y_test, y_pred)
print("Classification Report:",)
print (result1)
result2 = accuracy_score(y_test,y_pred)
print("Accuracy:",result2)



'''

# NAO FUNCIONA aqui mas no colab funciona
# enconded altera os valores textuais para numéricos
#from sklearn.preprocessing import LabelEncoder
#label_encoder = LabelEncoder()
#encoded_luminosity = label_encoder.fit_transform(training[["LUMINOSITY"]])
#training[["LUMINOSITY"]] = encoded_luminosity
#encoded_luminosity = label_encoder.fit_transform(test[["LUMINOSITY"]])
#test[["LUMINOSITY"]] = encoded_luminosity



 métricas de qualidade e avaliação do modelo
 
 ------- dados contínuos -------
 mae - measures the average magnitude of the errors (express the error in units pf the variable of interest)
 mean_absolute_error(test,predictions)
 mse - measure the average of squared error (squaring the error, gives high wait to large errors)
 mean_squared_error(test,predictions)
 
 ------- apenas para dados não continuos -------
 accuracy
 
 ...............................................
 precision aka sensitivity -> measure of exactness (determines the fraction of relevant items aomg the retrieved)

 precision_score(y_test,predictions,average='macro')
 
 recall aka specificity -> measure of completeness (determines the fraction of relevant items that were obtained)
  
 recall_score(y_test,predictions,average='macro')
 
 true and false positives and negatives        
 
 confusion_matrix(y_test,predictions)

'''

