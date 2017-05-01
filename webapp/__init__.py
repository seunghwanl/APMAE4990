from flask import Flask, render_template, request, url_for, flash, redirect
from flask_bootstrap import Bootstrap

from sqlalchemy import *
from haversine import haversine

from sklearn.ensemble import RandomForestRegressor
from sklearn.externals import joblib

from forms import LatLongForm

import os


app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY'] = os.environment.get('SECRET_KEY')

@app.route("/")
def main():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('index.html')


@app.route('/search', methods=['GET', 'POST'])
def search():
    form = LatLongForm()
    months = ['apr', 'may', 'jun', 'jul', 'aug', 'sep']
    days = ['Mon', 'Tues', 'Wed', 'Thurs', 'Fri', 'Sat', 'Sun']

    if form.validate_on_submit():
        month1 = form.month1.data
        day1 = form.day1.data
        hour1 = form.hour1.data
        minute1 = form.minute1.data
        am_pm1 = form.am_pm1.data
        latitude1 = form.latitude1.data
        longitude1 = form.longitude1.data

        month2 = form.month2.data
        day2 = form.day2.data
        hour2 =form.hour2.data
        minute2 = form.minute2.data
        am_pm2 = form.am_pm2.data
        latitude2 = form.latitude2.data
        longitude2 = form.longitude2.data
        print("month1: " + str(month1))
        print("day1: " + str(day1))
        print("latitide1: " + str(latitude1))
        print("longitude1: " + str(longitude1))

        username = os.environment.get('db_username')
        password = os.environment.get('db_password')
        host = os.environment.get('db_host')
        port = os.environment.get('db_port')
        database = os.environment.get('db_name')
        db_string = "postgresql+psycopg2://"+username+":"+password+"@"+host+":"+port+"/"+database

        engine = create_engine(db_string)

        result_set1 = engine.execute("SELECT label, latitude, longitude FROM centroids WHERE month = %s and day = %s" % (int(month1), int(day1)))
        result_set2 = engine.execute("SELECT label, latitude, longitude FROM centroids WHERE month = %s and day = %s" % (int(month2), int(day2)))

        result_set1_list = []
        result_set2_list = []

        for t in result_set1:
            result_set1_list.append(t)

        for t in result_set2:
            result_set2_list.append(t)

        rf1 = joblib.load("./Result/" + months[int(month1)]+days[int(day1)]+"2014.pkl")
        rf2 = joblib.load("./Result/" + months[int(month2)]+days[int(day2)]+"2014.pkl")

        X1 = [int(hour1) + 12 * int(am_pm1) + int(minute1) / 60]
        X2 = [int(hour2) + 12 * int(am_pm2) + int(minute2) / 60]

        optimalSet = 0


        if (rf1.predict(X1) > rf2.predict(X2)):
            optimalSet = 1
        else:
            optimalSet = 2

        print("set " + str(optimalSet))
        print("predict rate1 " + str(rf1.predict(X1)))
        print("predict rate2 " + str(rf2.predict(X2)))

        result_set_list = []
        latitude = 0
        longitude = 0
        month = 0
        day = 0
        hour = 0
        minute = 0
        am_pm = 0

        if (optimalSet == 1):
            result_set_list = result_set1_list
            latitude = latitude1
            longitude = longitude1
            month = month1
            day = day1
            hour= hour1
            minute = minute1
            am_pm = am_pm1
        else:
            result_set_list = result_set2_list
            latitude = latitude2
            longitude = longitude2
            month = month2
            day = day2
            hour = hour2
            minute = minute2
            am_pm = am_pm2

        if am_pm == '0':
            am_pm = 'AM'
        else:
            am_pm = 'PM'

        result_set_distance = []

        for t in result_set_list:
            loc1 = (t[1], t[2])
            loc2 = (latitude, longitude)

            result_set_distance.append((t[0], haversine(loc1, loc2)))

        result_set_distance.sort(key=lambda x: float(x[1]))
        result_set_distance = result_set_distance[:5]

        top_results = []

        rank = 1

        for t1 in result_set_distance:
            for t2 in result_set_list:

                if str(t1[0]) == str(t2[0]):
                    top_results.append((rank, float(t2[1]),float(t2[2])))
                    rank += 1
                    break

        days_eng = ['Mon', 'Tues', 'Wed', 'Thurs', 'Fri', 'Sat', 'Sun']
        months_eng = {}
        months_eng['4'] = 'April'
        months_eng['5'] = 'May'
        months_eng['6'] = 'June'
        months_eng['7'] = 'July'
        months_eng['8'] = 'August'
        months_eng['9'] = 'September'

        return render_template('map.html', month = months_eng[month], day = days_eng[int(day)], \
                               hour = hour, minute = minute, am_pm = am_pm, top_results = top_results)

    else:
        return render_template('search.html', form = form)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
