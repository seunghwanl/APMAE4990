import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.grid_search import GridSearchCV
from sklearn.externals import joblib

import time
import datetime
import math

months = ["apr", "may", "jun", "jul", "aug", "sep"]
days_eng = ["Mon", "Tues", "Wed", "Thurs", "Fri", "Sat", "Sun"]

for month in months:
    for day in days_eng:

        filename = month+day+"2014.csv"
        df = pd.read_csv(filename)
        X = []
        y = []


        datetimedf=df.loc[:,'Date/Time']
        t=pd.to_datetime(datetimedf, format="%m/%d/%Y %H:%M:%S")

        df["Hour"] = t.dt.hour
        df["Week"] = t.dt.week

        dataframes = []

        for i in range(24):
            # doing this to get each hour for each week. So if there are 5 weeks
            # we need to get 5 data points for each of 24 hour intervals
            # df.Hour % 24 is done by using groupby('Hour').count() few lines below.
            df_new = df.loc[df.Week % 24 == i]
            dataframes.append(df_new)


        for dframe in dataframes:
            dframe = dframe.groupby("Hour").count()
            dframe = dframe[dframe.columns[0]]

            for idx, i in enumerate(dframe.as_matrix()):
                y.append([i])
                X.append([idx])


            # one week scatter plot
            # if month == 'jul' and day == 'Sun':
            #     plt.scatter(X, y, s = 1)
            #     plt.legend(loc="lower right")
            #     plt.title("RandomForest Regression " + month + " " + day)
            #     plt.xlabel("Hours")
            #     plt.ylabel("Number of Pickups")
            #     plt.show()



        y = np.asarray(y)
        X = np.asarray(X)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.4, random_state = 42)


        # perform gridsearch with cv = 5
        rf = RandomForestRegressor()
        params = {'n_estimators': [x for x in range(10, 40, 2)], 'max_depth': [x for x in range(1, 7)]}
        reg = GridSearchCV(estimator = rf, param_grid = params, cv = 5)
        reg.fit(X_train, y_train)
        print("best params: ", reg.best_params_)

        rf = RandomForestRegressor(n_estimators = reg.best_params_['n_estimators'], max_depth = reg.best_params_['max_depth'])
        rf.fit(X_train, y_train)

        r2_train = r2_score(y_train, rf.predict(X_train))
        r2_test = r2_score(y_test, rf.predict(X_test))

        # filename = "./Result/" + month+day+"2014.pkl"
        # joblib.dump(rf, filename, compress=9)

        filename = "./Result/rep.txt"

        with open(filename, 'a') as f:
            f.write("year: 2014 month: " + month + " day: " + day + " train r2: "
                + str(r2_train) + " test r2: " + str(r2_test) + "\n")

        print("train r2", r2_train)
        print("test r2",r2_test)

        scatter plot (all weeks cumulative)

        # if month == 'jul' and day == 'Fri':
        #     plt.scatter(X, y, s = 1)
        #     plt.legend(loc="lower right")
        #     plt.title("RandomForest Regression " + month + " " + day)
        #     plt.xlabel("Hours")
        #     plt.ylabel("Number of Pickups")
        #     plt.show()









