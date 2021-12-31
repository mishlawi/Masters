    
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import classification_report
from numpy import unique
from numpy import where
from matplotlib import pyplot
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier


df = pd.read_csv("Clus_BuddyMove.csv")

cols = df.columns

def get_greater_index(row):
    index = 1
    j = 1
    bigger = 0
    for elem in row[1:]:
        if bigger < elem:
            bigger = elem
            index = j
        j += 1
        #print(elem)
    return cols[index]


greater = []
for i in range(len(df)):
    row = df.iloc[i].to_list()
    greater.append(get_greater_index(row))
        
df['Most_Probably'] = greater



X=df.drop('User Id', axis=1)
X=X.drop('Most_Probably', axis=1)

scaler = MinMaxScaler()
scaler.fit(X)
X=scaler.transform(X)


df.iloc[1].to_list()

'''
for column in df.columns[2:]:
    print(len(df[df.Sports > df[column]]))
'''

model = KMeans(n_clusters=3)
model.fit(X)
model.labels_
y_clusters = model.predict(X)

x = X
y = y_clusters
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.65, random_state=2022)

rf = RandomForestClassifier()
rf.fit(x_train,y_train)
y_pred = rf.predict(x_test)

print(f'accuracy: {accuracy_score(y_test, y_pred)}')


'''
clusters = unique(yhat)

accum=0
for cluster in clusters:
    row_ix = where(yhat == cluster)
    #print(len(row_ix[0]))
    accum += len(row_ix[0])

output = df.Most_Probably.value_counts()

classification_report(LabelEncoder().fit_transform(df[['Most_Probably']]), yhat)
# show the plot
pyplot.show()
'''