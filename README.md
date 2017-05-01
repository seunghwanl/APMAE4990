# APMAE4990

<h1>Vehicle for Hire Data Analysis</h1>

<b>Team members</b>: Rahi Punjabi, Seung Hwan Lee

<b>Roles</b>: Web Development, Machine Learning

<b>Tools</b>: Python, Scikit, Flask + AWS (Backend), Flask-Bootstrap + Mapbox (UI Frontend)

<b>Data set: </b> https://github.com/fivethirtyeight/uber-tlc-foil-response

<b> Motivation: </b> Driving for a for-hire vehicle service like Uber or Lyft is often a side job for people looking for multiple streams of income. To increase the revenue potential of being a driver, you want to be sure that you wait near areas with high demand throughout your shifts. Obviously, these areas of optimal revenue potential vary during the day and by day of the week and could also be affected by customer preferences of the service you’re working for. We plan to develop a web app that recommends nearby locations for drivers to wait based on the time, day of the week, and current location. The app can also help a potential driver determine which service she or he would like to drive for and what days/times they will work to.

<b> Audience: </b> 
Current and potential drivers for for-hire vehicle services like Uber or Lyft

<b> Algorithm: </b> Clustering and Regression. 

* We will use clustering to find the high demand locations. We will also use regression to analyze and predict the peak hours during each day. We could also potentially analyze the peak demand days and months.

* We will also compare the ride demand for Uber vs Lyft.

<b> Challenges: </b> We will be dealiing with big data (14 million+ data points) so even if we our model may appear simple, it might be hard to train and fit the model.

<b> Interface: </b> A driver will input his/her two possible locations and times. Our app will output the optimal location and time (of those two inputs) for the driver to drive.

<b> Web App Link: </b> http://35.163.13.13

