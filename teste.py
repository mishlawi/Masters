
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
import funcoes_auxiliares as fa
from datetime import datetime
import random


training = pd.read_csv('training_data.csv', encoding='latin')
test = pd.read_csv('test_data.csv', encoding='latin')

# AVERAGE_PRECIPITATION
training.drop('AVERAGE_PRECIPITATION',axis=1, inplace=True)
test.drop('AVERAGE_PRECIPITATION',axis=1, inplace=True)

#city_name
training.drop('city_name',axis=1,inplace=True)
test.drop('city_name',axis=1,inplace=True)

'''
training.drop('AVERAGE_RAIN',axis=1,inplace=True)
test.drop('AVERAGE_RAIN',axis=1,inplace=True)

training.drop('AVERAGE_CLOUDINESS',axis=1,inplace=True)
test.drop('AVERAGE_CLOUDINESS',axis=1,inplace=True)
'''

training.record_date = pd.to_datetime(training.record_date)
training['Hour'] = training.record_date.dt.hour
training['Day'] = training.record_date.dt.day
training['Month'] = training.record_date.dt.month
training['Day_Name'] = training.record_date.dt.day_name(locale='pt')

test.record_date = pd.to_datetime(test.record_date)
test['Hour'] = test.record_date.dt.hour
test['Day'] = test.record_date.dt.day
test['Month'] = test.record_date.dt.month
test['Day_Name'] = test.record_date.dt.day_name(locale='pt')

training.drop('record_date',axis=1,inplace=True)
test.drop('record_date',axis=1,inplace=True)

fa.limpa_valores(training,test)

label_encoder = LabelEncoder()
training["AVERAGE_RAIN"] = label_encoder.fit_transform(training[["AVERAGE_RAIN"]])
test["AVERAGE_RAIN"] = label_encoder.fit_transform(test[["AVERAGE_RAIN"]])
training["AVERAGE_CLOUDINESS"] = label_encoder.fit_transform(training[["AVERAGE_CLOUDINESS"]])
test["AVERAGE_CLOUDINESS"] = label_encoder.fit_transform(test[["AVERAGE_CLOUDINESS"]])
training["Day_Name"] = label_encoder.fit_transform(training[["Day_Name"]])
test["Day_Name"] = label_encoder.fit_transform(test[["Day_Name"]])
training["LUMINOSITY"]  = label_encoder.fit_transform(training[["LUMINOSITY"]])
test["LUMINOSITY"] = label_encoder.fit_transform(test[["LUMINOSITY"]])

x = training.drop(['AVERAGE_SPEED_DIFF'], axis=1)
y = training['AVERAGE_SPEED_DIFF'].to_frame()

# 2**32 its the number max of int type
clf = DecisionTreeClassifier(random_state=random.randrange(2**32))

clf.fit(x,y)

predictions = clf.predict(test)

predictions = pd.DataFrame(predictions, columns=['Speed_Diff'])
predictions.index.name='RowId'
predictions.index += 1 
predictions.to_csv("./predictions"+ str(datetime.now().strftime("%Y-%m-%d %H-%M"))+".csv")

























