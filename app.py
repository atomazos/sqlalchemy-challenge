import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Welcome to the Hawaii Stations API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
        f"/api/v1.0/temp/<start>" 
        f"/api/v1.0/temp/<start>/<end>"
    )
query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
@app.route("/api/v1.0/stations")
def stations():
    """Return a json list of stations from the dataset."""
    print("Server recieved request for Stations...")
    results = session.query(Station.name).all()
    session.close()

    stations_list = []
    for name in results:
        stations_dict = {}
        stations_dict["name"] = name
        stations_list.append(stations_dict)

    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return a JSON list of Temperature Observations (tobs) for the previous year."""
    print("Server recieved request for Temperature Observations...")
    results = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date > query_date).\
    order_by(Measurement.date).all()
    session.close()

    tobs_data = []
    for tobs in results:
        tobs_dict = {}
        tobs_dict["Temperature Observations"] = tobs
        tobs_data.append(tobs_dict)
    
    return jsonify(tobs_data)

@app.route("/api/v1.0/temp/<start>")
def start_stats(start=None):
    """ Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range."""
    print("Server recieved request for finding out temperature data from a specific start date...")
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    session.close()
    temp_results = []
    for Tmin, Tmax, Tavg in results: 
        temp_dict = {}
        temp_dict["Minumum Temprature"] = Tmin
        temp_dict["Average Temprature"] = Tavg
        temp_dict["Maximum Temprature"] = Tmax
        temp_results.append(temp_dict)

    return jsonify(temp_results)

@app.route("/api/v1.0/temp/<start>/<end>")

def calc_temps(start = None, end=None):
    """ Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range."""
    print("Server recieved request for finding out temperature data from a specific start date to end date...")
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    session.close()
    temp2_results = []
    for Tmin, Tmax, Tavg in results: 
        temp_dict = {}
        temp_dict["Minumum Temprature"] = Tmin
        temp_dict["Average Temprature"] = Tavg
        temp_dict["Maximum Temprature"] = Tmax
        temp2_results.append(temp_dict)

    return jsonify(temp2_results)

if __name__ == '__main__':
    app.run(debug=True)
