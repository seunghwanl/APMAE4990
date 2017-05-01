import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import matplotlib

from sklearn.cluster import DBSCAN
from sklearn import metrics
from geopy.distance import great_circle
from shapely.geometry import MultiPoint

import time
import datetime

df = pd.read_csv('uber-raw-data-apr14.csv')
datetimedf = df['Date/Time']

t=pd.to_datetime(datetimedf, format="%m/%d/%Y %H:%M:%S")


df['dayofweek']=t.dt.dayofweek

df = df.loc[df.dayofweek == 0]

df = df.loc[df.Lat <= 40.87]
df = df.loc[df.Lat >= 40.6]

df = df.loc[df.Lon <= -73.9]
df = df.loc[df.Lon >= -74.05]

fig, ax = plt.subplots(figsize=[15, 10])

df_scatter = ax.scatter(df['Lon'], df['Lat'], c='k', alpha=0.9, s=0.05)
ax.set_title('Uber April 2014')
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
ax.legend([df_scatter], ['full set'], loc='upper right')
plt.show()