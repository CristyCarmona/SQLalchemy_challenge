import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import distinct

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
measurement = Base.classes.measurement
station = Base.classes.station

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
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/2016-08-23<br/>"
        f"/api/v1.0/2016-08-23/2017-08-23"
    )


@app.route("/api/v1.0/precipitation")
def precip():
# Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of precipitation"""
    # Query all passengers
    precipition_data = session.query(measurement.date,measurement.prcp).filter(measurement.date >= "2016-08-23").all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_precipitation = []
    for date,prcp in precipition_data:
        precipitation_dict = {}
        precipitation_dict[date] = prcp
        all_precipitation.append(precipitation_dict)

    return jsonify(all_precipitation)


@app.route("/api/v1.0/stations")
def stat():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of weather stations"""
    # Query all passengers
    station_data = session.query(distinct(measurement.station)).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_stations = []
    for station in station_data:
        all_stations.append(station)

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of temperatures"""
    # Query all passengers
    temp_data = session.query(measurement.tobs,measurement.date).filter(measurement.station == 'USC00519281').all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_tobs = []
    for tobs,date in temp_data:
        temp_dict = {}
        temp_dict['temp'] = tobs
        temp_dict['date'] = date
        all_tobs.append(temp_dict)

    return jsonify(all_tobs)
    

@app.route("/api/v1.0/<start>")
def start_d(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of passenger data including the name, age, and sex of each passenger"""
    # Query all passengers
    results_start = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_start = []
    for min_value,avg_value,max_value in results_start:
        start_dict = {}
        start_dict['min'] = min_value
        start_dict['avg'] = avg_value
        start_dict['max'] = max_value
        all_start.append(start_dict)

    return jsonify(all_start)

@app.route("/api/v1.0/<start>/<end>")
def start_end_d(start,end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return temperature min, max and avg """
    # Query all passengers
    results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start).filter(measurement.date <= end).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_start_end = []
    for min_value,avg_value,max_value in results:
        start_end_dict = {}
        start_end_dict['min'] = min_value
        start_end_dict['avg'] = avg_value
        start_end_dict['max'] = max_value
        all_start_end.append(start_end_dict)

    return jsonify(all_start_end)


if __name__ == '__main__':
    app.run(debug=True)
