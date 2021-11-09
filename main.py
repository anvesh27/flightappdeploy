import joblib
import warnings
import pandas as pd
from flask import Flask, render_template, request
from flask_cors import cross_origin
import logging
import timeit


logging.basicConfig(filename='record.log', level=logging.DEBUG, format='%(asctime)s_%(levelname)s-%(message)s')

app = Flask(__name__)
model = joblib.load('best.pkl')
warnings.filterwarnings('ignore')


@app.route("/")
@app.route("/home")
@cross_origin()
def home():
    app.logger.info('Home')
    return render_template('home.html')


@app.route("/enter", methods=['POST', 'GET'])
@cross_origin()
def enter():
    app.logger.info('Entering the details')
    return render_template('enter.html')


airlines = {"IndiGo": 3, "Air India": 1, "Jet Airways": 4, "SpiceJet": 8, "Multiple carriers": 6, "GoAir": 2,
            "Vistara": 10, "Air Asia": 0, "Vistara Premium economy": 11, "Jet Airways Business": 5,
            "Multiple carriers Premium economy": 7, "Trujet": 9}

source = {'Bangalore': 0, 'Kolkata': 3, 'Delhi': 2, 'Chennai': 1, 'Mumbai': 4}
destination = {'New Delhi': 5, 'Bangalore': 0, 'Cochin': 1, 'Kolkata': 4, 'Delhi': 2, 'Hyderabad': 3}

additional = {'No info': 8, 'In-flight meal not included': 5, 'No check-in baggage included': 7,
              '1 Short layover': 1, 'No Info': 6, '1 Long layover': 0, 'Change airports': 4,
              'Business class': 3, 'Red-eye flight': 9, '2 Long layover': 2}


@app.route("/predict", methods=['GET', 'POST'])
@cross_origin()
def predict():
    app.logger.info('predicting the fare')
    start = timeit.timeit()
    if request.method == "POST":
        airline_name = request.form["airline"]
        Airline = airlines[airline_name]

        Date_of_Journey = request.form["Dep_time"]
        Journey_day = int(pd.to_datetime(Date_of_Journey, format="%Y-%m-%dT%H:%M").day)
        Journey_month = int(pd.to_datetime(Date_of_Journey, format="%Y-%m-%dT%H:%M").month)

        date_dep = request.form["Dep_time"]
        Dep_hour = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").hour)
        Dep_minute = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").minute)

        date_arr = request.form["Arrival_time"]
        Arrival_hour = int(pd.to_datetime(date_arr, format="%Y-%m-%dT%H:%M").hour)
        Arrival_minute = int(pd.to_datetime(date_arr, format="%Y-%m-%dT%H:%M").minute)

        Sou = request.form["Source"]
        Source = source[Sou]

        Des = request.form["Destination"]
        Destination = destination[Des]

        Total_stops = request.form["Total_stops"]

        Du_hours = abs(Arrival_hour - Dep_hour)
        Du_minutes = abs(Arrival_minute - Dep_minute)

        add = request.form['add']
        Additional_Info = additional[add]


        prediction = model.predict([[
                                     Airline,
                                     Source,
                                     Destination,
                                     Total_stops,
                                     Additional_Info,
                                     Journey_day,
                                     Journey_month,
                                     Dep_hour,
                                     Dep_minute,
                                     Arrival_hour,
                                     Arrival_minute,
                                     Du_hours,
                                     Du_minutes
                                 ]])
        output = round(prediction[0], 2)
        app.logger.info('finished predicting')
        end = timeit.timeit()
        time_taken = (start - end)
        source_file = open('time_taken.txt', 'a')
        print(time_taken, file=source_file)
        source_file.close()
        return render_template('output.html', prediction_text="Your Flight fare is Rs. {}".format(output))
    return render_template("home.html")

