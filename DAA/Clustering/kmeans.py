    
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
import plotly.express as px


df = pd.read_csv("Clus_BuddyMove.csv")

X=df.drop('User Id', axis=1)

scaler = MinMaxScaler()
scaler.fit(X)
X=scaler.transform(X)


model = KMeans(n_clusters=3)
model.fit(X)
model.labels_
y_clusters = model.predict(X)


clusters=pd.DataFrame(X,columns=df.drop("User Id",axis=1).columns)
clusters['label']=model.labels_
polar=clusters.groupby("label").mean().reset_index()
polar=pd.melt(polar,id_vars=["label"])
fig4 = px.line_polar(polar, r="value", theta="variable", color="label", line_close=True,height=800,width=1400)
fig4.show()

pie=clusters.groupby('label').size().reset_index()
pie.columns=['label','value']
px.pie(pie,values='value',names='label',color=['blue','red','green'])

x = X
y = y_clusters
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.65, random_state=2022)

rf = RandomForestClassifier()
rf.fit(x_train,y_train)
y_pred = rf.predict(x_test)

print(f'accuracy: {accuracy_score(y_test, y_pred)}')
