[![Build Status](https://travis-ci.com/kokadva/Tbilisi-Traffic-Routing-App-Backend.svg?branch=master)](https://travis-ci.com/kokadva/Tbilisi-Traffic-Routing-App-Backend)

### Tbilisi Traffic and Routing Based On Public Tranport

### URL: [tbilisi-traffic-routing-front.herokuapp.com](https://tbilisi-traffic-routing-front.herokuapp.com/)

#### Backend Project

### Project Description:
This project provides traffic data for Tbilisi Georgia on the roads
where public transport (Busses) work. Tbilisi Transport Company(TTC) has
public data to which bus stop will the certain bus arrive and when in
two forms, first is static schedule for the whole week and the second
is a live data which tells how many minutes are left till the certain
bus will arrive to a certain bus stop, but in case of traffics in the
city busses do not get on bus stops on time and live data is sometimes
mistaken cause they don't take into considaration the traffic in front,
but when they arrive at the bus stop then the sensor shows that 0
minutes are left till the arrival so if we look at the sensors which
show 0 (we scrape all the bus stops sensors in tbilisi in every 30
seconds) then we know when the bus actually arrived and also we have
schedule which tells us when it should have arrived so we can determine
the deley so we have an info on traffic. We also though a little ahead
of just gathering traffic data and found out that google uses TTC
information on public transport routing, as we already know that TTC
is in fact in case of traffic mistaken in bus arrival times then google
is too so we've built a routing engine using A Start algorithm based on
traffic data which we gather just to have more fun. +_+

### Technologies used:
* Pyhon/Flask
* SQLAlchemy
* PostgreSQL
* Docker/Docker-Compose
* Geojson
* Docker/Docker-Compose
* Heroku
* Travis CI

### How to run the app locally:
1. Install Docker/Docker-Compose
2. Run `docker-compose up` to start the database
3. Install python 3.6+
4. Create python virtual environment
5. Install requirements by running `pip install -r requirements`
6. Run the app `python app.py`

### How to run the app in the Docker:
1. Install Docker/Docker-Compose
2. Build docker image `docker build -t flask-app:latest .`
3. Run `docker-compose up` to start the app and the database

### Frontend Repository:
https://github.com/kokadva/Tbilisi-Traffic-Routing-App-Frontend

### Authors:
* Konstantine Dvalishvili konstantine.dvalishvil@gmail.com
* Kakhaber Margalitadze kaxax95@gmail.com
* Alexandr Azizian