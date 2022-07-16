import pandas as pd
from sklearn.tree import DecisionTreeClassifier

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import mean_absolute_error
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split


from sklearn.preprocessing import LabelEncoder
from datetime import datetime
import random


from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import StratifiedKFold


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

x_test = test


model = XGBClassifier(n_estimators = 120, learning_rate=0.1, criterion='friedman_mse',max_depth=5)


model.fit(x, y)

y_test = model.predict(x_test)


'''
n_estimators = [120,150,180]
learning_rate = [0.1]
criterion = ['friedman_mse']
max_depth = [5]
param_grid = dict(n_estimators=n_estimators,learning_rate=learning_rate,criterion=criterion,max_depth=max_depth)
kfold = StratifiedKFold(n_splits=10, shuffle=True, random_state=7)
grid_search = GridSearchCV(model, param_grid, scoring="neg_log_loss", n_jobs=-1, cv=kfold)
grid_result = grid_search.fit(x, y)
# summarize results
print("Best: %f using %s" % (grid_result.best_score_, grid_result.best_params_))
means = grid_result.cv_results_['mean_test_score']
stds = grid_result.cv_results_['std_test_score']
params = grid_result.cv_results_['params']
'''


y_test = pd.DataFrame(y_test, columns=['Speed_Diff'])
y_test.index.name='RowId'
y_test.index += 1 
y_test.to_csv("./predictions/predictionsXGB"+ str(datetime.now().strftime("%Y-%m-%d %H-%M"))+".csv")





