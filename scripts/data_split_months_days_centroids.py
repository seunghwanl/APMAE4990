import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

from sklearn import metrics
from scipy.cluster.vq import kmeans, kmeans2, whiten

import time
import datetime


months_data= ['uber-raw-data-apr14.csv', 'uber-raw-data-may14.csv', 'uber-raw-data-jun14.csv', 'uber-raw-data-jul14.csv', 'uber-raw-data-aug14.csv', 'uber-raw-data-sep14.csv']
months = [4, 5, 6, 7, 8, 9]
months_eng = ['Apr', 'May', 'June', 'Jul', 'Aug', 'Sep']
i = 0


for idx, data in enumerate(months_data):

    df = pd.read_csv(data)
    datetimedf = df['Date/Time']

    t=pd.to_datetime(datetimedf, format="%m/%d/%Y %H:%M:%S")
    df['Dayofweek']=t.dt.dayofweek
    df["Hour"] = t.dt.hour
    df['Month'] = t.dt.month


    # restricting lat and long as data as we tried to focuse near Manhattan.
    df = df.loc[df.Lat <= 40.87]
    df = df.loc[df.Lat >= 40.6]

    df = df.loc[df.Lon <= -73.9]
    df = df.loc[df.Lon >= -74.05]

    df = df.drop('Base', 1)

    # define the number of kilometers in one radian
    kms_per_radian = 6371.0088

    # 7 days per week
    days = [x for x in range(0, 7)]

    days_eng = ["Mon", "Tues", "Wed", "Thurs", "Fri", "Sat", "Sun"]
    hours = [x for x in range(24)]



    for day in days:
        df1 = df.loc[df.Dayofweek == day]

        coordinates = df1.as_matrix(columns=['Lon', 'Lat'])

        N = len(coordinates)

        # normalize the coordinate data with the whiten function
        # each feature is divided by its standard deviation across all observations to give it unit variance.
        w = whiten(coordinates)

        print(str(day))
        print(np.array([w[:, 0]]).T)

        # # number of cluster centroids
        k = 50

        # i is the number of iterations to perform for kmeans
        i = 300

        # plot the final reduced set of coordinate points vs the original full set
        cluster_centroids2, closest_centroids = kmeans2(w, k, iter=i, minit='points')

        df1["centroids"] = closest_centroids
        df1["normalized_Longitude"] = pd.DataFrame(np.array([w[:, 0]]).T)
        df1["normalized_Latitude"] = pd.DataFrame(np.array([w[:, 1]]).T)

        filename = data[-9:-6] + days_eng[day] + "2014.csv"

        with open(filename, 'w') as f:
            df1.to_csv(f, sep = ",")

        df_centroidinfo = pd.DataFrame()
        df_centroidinfo["Longitude"] = cluster_centroids2[:, 0]
        df_centroidinfo["Latitude"] = cluster_centroids2[:, 1]
        df_centroidinfo["Month"] = df1.head(len(df_centroidinfo))["Month"]
        df_centroidinfo["Dayofweek"] = df1.head(len(df_centroidinfo))["Dayofweek"]

        print(df1.head(len(df_centroidinfo))["Month"])
        print(df1.head(len(df_centroidinfo))["Dayofweek"])

        filename = data[-9:-6] + days_eng[day] + "info.csv"

        with open(filename, 'a') as f:
            df_centroidinfo.to_csv(f, sep = ",", header=False)

        filename = "centroidinfo.csv"
        centroid_info = []

        for i in range(50):
            df2 = df1.loc[df1.centroids == i]

            lat_mean = df2["Lat"].mean()
            lon_mean = df2["Lon"].mean()

            centroid_info.append([lat_mean, lon_mean, int(months[idx]) ,int(day)])

        centroid_info = np.asarray(centroid_info)

        df_centroid = pd.DataFrame()
        df_centroid["Latitude"] = centroid_info[:, 0]
        df_centroid["Longitude"] = centroid_info[:, 1]
        df_centroid["Month"] = centroid_info[:, 2].astype(int)
        df_centroid["Day"] = centroid_info[:, 3].astype(int)

        with open(filename, 'a') as f:
            df_centroid.to_csv(f, sep = ",", header=False)

        # plot the cluster centroids
        # fig = plt.figure(figsize=(15, 10), dpi=100)
        # plt.scatter(coordinates[:,0], coordinates[:,1], c=closest_centroids, s=.05)
        # fig.suptitle(months_eng[idx] + " " + days_eng[day] + " 2014" )
        # plt.show()

