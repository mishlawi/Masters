
import pandas as pd
from sklearn.tree import DecisionTreeClassifier

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import mean_absolute_error

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

training.drop('record_date',axis=1, inplace=True)
test.drop('record_date',axis=1, inplace=True)

fa.limpa_valores(training,test)

# AVERAGE_CLOUDINESS
training['AVERAGE_CLOUDINESS'] = training['AVERAGE_CLOUDINESS'].apply(fa.weatherType)
test['AVERAGE_CLOUDINESS'] = test['AVERAGE_CLOUDINESS'].apply(fa.weatherType)

# AVERAGE_RAIN
training['AVERAGE_RAIN'] = training['AVERAGE_RAIN'].apply(fa.rainType)
test['AVERAGE_RAIN'] = test['AVERAGE_RAIN'].apply(fa.rainType)


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

# 2**32 its the number max of int type
#clf = DecisionTreeClassifier(random_state=random.randrange(2**32))
rf_model = RandomForestClassifier(random_state=95)
rf_model.fit(x, y)

#clf.fit(x,y)

#predictions = clf.predict(test)
rf_predictions = rf_model.predict(test)


rf_predictions = pd.DataFrame(rf_predictions, columns=['Speed_Diff'])
rf_predictions.index.name='RowId'
rf_predictions.index += 1 
rf_predictions.to_csv("./predictions"+ str(datetime.now().strftime("%Y-%m-%d %H-%M"))+".csv")

























