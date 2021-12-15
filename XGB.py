import pandas as pd
from sklearn.tree import DecisionTreeClassifier

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import mean_absolute_error
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split


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


training.drop('AVERAGE_CLOUDINESS',axis=1, inplace=True)
test.drop('AVERAGE_CLOUDINESS',axis=1, inplace=True)

training.drop('AVERAGE_RAIN',axis=1,inplace=True)
test.drop('AVERAGE_RAIN',axis=1,inplace=True)


training["Day_Name"] = LabelEncoder().fit_transform(training[["Day_Name"]])
test["Day_Name"] = LabelEncoder().fit_transform(test[["Day_Name"]])

training["LUMINOSITY"]  = LabelEncoder().fit_transform(training[["LUMINOSITY"]])
test["LUMINOSITY"] = LabelEncoder().fit_transform(test[["LUMINOSITY"]])


y = training.AVERAGE_SPEED_DIFF.to_frame()
x = training.drop(['AVERAGE_SPEED_DIFF'], axis=1)



xgbr_model = XGBClassifier(n_estimators = 10, max_depth = 20, verbosity = 2)
xgbr_model.fit(x, y)


xgbr_predictions = xgbr_model.predict(test)


xgbr_predictions = pd.DataFrame(xgbr_predictions, columns=['Speed_Diff'])
xgbr_predictions.index.name='RowId'
xgbr_predictions.index += 1 
xgbr_predictions.to_csv("./predictions/predictionsXGB"+ str(datetime.now().strftime("%Y-%m-%d %H-%M"))+".csv")