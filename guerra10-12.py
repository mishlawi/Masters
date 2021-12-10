
import pandas as pd
from sklearn.tree import DecisionTreeClassifier

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import mean_absolute_error
from sklearn.impute import SimpleImputer


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


fa.limpa_valores(training,test)

# AVERAGE_CLOUDINESS
training['AVERAGE_CLOUDINESS'] = training['AVERAGE_CLOUDINESS'].apply(fa.weatherType)
test['AVERAGE_CLOUDINESS'] = test['AVERAGE_CLOUDINESS'].apply(fa.weatherType)




training.drop('AVERAGE_RAIN',axis=1,inplace=True)
test.drop('AVERAGE_RAIN',axis=1,inplace=True)




print(training.shape)

valores_em_falta = (training.isnull().sum())
print(valores_em_falta[valores_em_falta > 0])




training["Day_Name"] = LabelEncoder().fit_transform(training[["Day_Name"]])
test["Day_Name"] = LabelEncoder().fit_transform(test[["Day_Name"]])

training["LUMINOSITY"]  = LabelEncoder().fit_transform(training[["LUMINOSITY"]])
test["LUMINOSITY"] = LabelEncoder().fit_transform(test[["LUMINOSITY"]])


y = training['AVERAGE_SPEED_DIFF'].to_frame()
x = training.drop('AVERAGE_SPEED_DIFF', axis=1)



my_imputer = SimpleImputer(strategy="most_frequent")

x = pd.DataFrame(my_imputer.fit_transform(x))
test = pd.DataFrame(my_imputer.transform(test))

# Fill in the lines below: imputation removed column names; put them back
x.columns = training.columns
test.columns = test.columns

print("\n\n\naqui sem erros2\n\n\n")


rf_model = RandomForestClassifier(random_state=95)
rf_model.fit(x, y)


rf_predictions = rf_model.predict(test)


rf_predictions = pd.DataFrame(rf_predictions, columns=['Speed_Diff'])
rf_predictions.index.name='RowId'
rf_predictions.index += 1 
rf_predictions.to_csv("./predictions/predictionsGuerra"+ str(datetime.now().strftime("%Y-%m-%d %H-%M"))+".csv")

























