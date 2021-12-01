
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
# import os


training = pd.read_csv('training_data.csv', encoding='latin')
test = pd.read_csv('test_data.csv', encoding='latin')

# AVERAGE_PRECIPITATION
training.drop('AVERAGE_PRECIPITATION',axis=1, inplace=True)
test.drop('AVERAGE_PRECIPITATION',axis=1, inplace=True)

#city_name
training.drop('city_name',axis=1,inplace=True)
test.drop('city_name',axis=1,inplace=True)

training.drop('AVERAGE_RAIN',axis=1,inplace=True)
test.drop('AVERAGE_RAIN',axis=1,inplace=True)

training.drop('AVERAGE_CLOUDINESS',axis=1,inplace=True)
test.drop('AVERAGE_CLOUDINESS',axis=1,inplace=True)

training.record_date = pd.to_datetime(training.record_date)
training['Hour'] = training.record_date.dt.hour

test.record_date = pd.to_datetime(test.record_date)
test['Hour'] = test.record_date.dt.hour

training.drop('record_date',axis=1,inplace=True)
test.drop('record_date',axis=1,inplace=True)

label_encoder = LabelEncoder()
encoded_luminosity = label_encoder.fit_transform(training[["LUMINOSITY"]])
training["LUMINOSITY"] = encoded_luminosity
encoded_luminosity = label_encoder.fit_transform(test[["LUMINOSITY"]])
test["LUMINOSITY"] = encoded_luminosity


x = training.drop(['AVERAGE_SPEED_DIFF'], axis=1)
y = training['AVERAGE_SPEED_DIFF'].to_frame()


clf = DecisionTreeClassifier(random_state=2021)

clf.fit(x,y)

predictions = clf.predict(test)

predictions = pd.DataFrame(predictions, columns=['Speed_Diff'])
predictions.index.name='RowId'
predictions.index += 1 
predictions.to_csv("./predictionsTest.csv")

























