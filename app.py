import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

# Flask Setup
app = Flask(__name__)




@app.route("/")
def welcome():
    
    return (
        f"Available Routes:<br/>"
        f"<a href='/api/v1.0/precipitation'>Precipitation</a></br>"
        f"<a href='/api/v1.0/stations'>Stations</a></br>" 
        f"<a href='/api/v1.0/tobs'>Total Observed</a></br>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():

    #results = session.query(Measurement.prcp).all()
    # .all() IS CRUCIAL!
    meass = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= "2016-06-23").all()
    # Convert list of tuples into normal list
    ravelx = list(np.ravel(meass))
    #lotta nonsense to get there.
    return jsonify(ravelx)


@app.route("/api/v1.0/stations")
def stations():
     # .all() IS CRUCIAL!
    statis = session.query(Station.station).all()
    # Convert list of tuples into normal list
    ravelx = list(np.ravel(statis))
    #lotta nonsense to get there.
    return jsonify(ravelx)


@app.route("/api/v1.0/tobs")
def tobs():

    #results = session.query(Measurement.prcp).all()
    # .all() IS CRUCIAL!
    last12topstat = session.query(Measurement.tobs).filter(Measurement.date >= "2016-06-23").filter(Measurement.station=="USC00519281").all()
    # Convert list of tuples into normal list
    ravelx = list(np.ravel(last12topstat))
    #lotta nonsense to get there.
    return jsonify(ravelx)


if __name__ == '__main__':
    app.run(debug=True)
