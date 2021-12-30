    
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import classification_report
from numpy import unique
from numpy import where
from matplotlib import pyplot
from sklearn.preprocessing import LabelEncoder






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
        print(elem)
    return cols[index]



greater = []
for i in range(len(df)):
    row = df.iloc[i].to_list()
    greater.append(get_greater_index(row))
    
        
df['Most_Probably'] = greater

X=df.drop('User Id', axis=1)
X=X.drop('Sports', axis=1)
X=X.drop('Most_Probably', axis=1)




df.iloc[1].to_list()

'''
for column in df.columns[2:]:
    print(len(df[df.Sports > df[column]]))
'''
model = KMeans(n_clusters=5)

# fit the model
model.fit(X)

yhat = model.predict(X)

clusters = unique(yhat)

accum=0
for cluster in clusters:
    row_ix = where(yhat == cluster)
    print(len(row_ix[0]))
    accum += len(row_ix[0])
 

output = df.Most_Probably.value_counts()
   
classification_report(LabelEncoder().fit_transform(df[['Most_Probably']]), yhat)
# show the plot
pyplot.show()
