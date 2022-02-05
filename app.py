import sqlalchemy 
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import numpy as np
from flask import Flask, jsonify


# Database Setup
engine = create_engine("sqlite:///Resources//hawaii.sqlite")


# reflect an existing database into a new model
conn = engine.connect()
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# View all of the classes that automap found
Base.classes.keys()

# Save references to each table
mes = Base.classes.measurement
station = Base.classes.station

# # Create our session (link) from Python to the DB
# session = Session(conn)



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
def measurement():
 
    """Convert the query results to a dictionary using date as the key and prcp as the value.
        Return the JSON representation of your dictionary. """
    session = Session(engine)

    # Query all measurements
    results = session.query(mes.date , mes.prcp).all()
    session.close()
    all_measurements = []
    for d, p in results:
        measurements_dict = {}
        measurements_dict["date"] = d
        measurements_dict["prcp"] = p
        all_measurements.append(measurements_dict)
    
    return jsonify(all_measurements)

@app.route("/api/v1.0/stations")
def stations():
    """Return a JSON list of stations from the dataset."""
    session = Session(engine)
    # Query all Stations
    result2 = session.query(station.station).all()
    session.close()
    # Convert list of tuples into normal list
    all_stat = list(np.ravel(result2))

    return jsonify(all_stat)

@app.route("/api/v1.0/tobs")
def tob():
    """Return a JSON list of stations from the dataset."""
    session = Session(engine)
    # Query all Stations
    result3 = session.query(mes.date, mes.tobs).filter(mes.date >= '2016-08-23').filter(mes.station == 'USC00519281')
    session.close()
   
    tobs_365 = []
    for d, t in result3:
        tobs_dict = {}
        tobs_dict["date"] = d
        tobs_dict["prcp"] = t
        tobs_365.append(tobs_dict)
    
    return jsonify(tobs_365)

    
if __name__ == "__main__":
    app.run(debug=True)
