
        
import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


# Database Setup
engine = create_engine("sqlite:///Resources//hawaii.sqlite")
engine

# reflect an existing database into a new model
conn = engine.connect()
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# View all of the classes that automap found
Base.classes.keys()

# Save references to each table
measurements = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(conn)



# Flask Setup
app = Flask(__name__)


# Flask Routes
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs"
    )


@app.route("/api/v1.0/precipitation")
def names():

    session = Session(conn)

    """Return a list of all passenger names"""
    # Query all passengers
    results = session.query(measurements.date, measurements.prcp).all()
    session.close()
    all_passenger = []
    for date , prcp in results:
        measurements = {}
        measurements_dict["date"] = measurements.date
        measurements_dict["prcp"] = measurements.prcp
        all_passengers.append(measurements_dict)

    return jsonify(all_passengers)

# @app.route("/api/v1.0/stations")
# def stations():
#     """Return a list of passenger data including the name, age, and sex of each passenger"""
#     # Query all passengers
#     results = session.query(measurements.station).all()

#     # Convert list of tuples into normal list
#    # all_stations = list(np.ravel(results))

#     return jsonify(results)


if __name__ == "__main__":
    app.run(debug=True)
