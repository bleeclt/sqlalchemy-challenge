import numpy as np
import sqlalchemy
import datetime as dt

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


# DB engine
engine = create_engine("sqlite:///./Resources/hawaii.sqlite")


Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# establish measurement and station tables
measurement = Base.classes.measurement

station = Base.classes.station

# establish flask

app = Flask(__name__)

# flask routes

@app.route("/")
def index():
    print("Available Routes")
    return (
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"          
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # establish session link from Python to the DB
    session = Session(engine)

     # Query for the dates and precipitation values
    results = session.query(measurement.date, measurement.prcp).order_by(measurement.date).all()

    # Convert to list of dictionaries to jsonify
    rain_date_list = []

    for date, rain in results:
        rain_dict = {}
        rain_dict[date] = rain
        rain_date_list.append(new_dict)

    session.close()

    return jsonify(rain_date_list)

@app.route("/api/v1.0/stations")
def stations():
    # establish session link from Python to the DB
    session = Session(engine)

    stations = {}

    # Query all stations
    results = session.query(Station.station, Station.name).all()
    for s,name in results:
        stations[s] = name

    session.close()
 
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # establish session link from Python to the DB
    session = Session(engine)

    # Get the last date
    last_date = session.query(measurement.date).order_by(measurement.date.desc()).first()
    last_year_date = (dt.datetime.strptime(last_date[0],'%Y-%m-%d') - dt.timedelta(days=365)).strftime('%Y-%m-%d')

    # Query for dates and temps
    results = session.query(measurement.date, measurement.tobs).filter(measurement.date >= last_year_date).order_by(measurement.date).all()

    # Convert to list of dictionaries to jsonify
    tobs_list = []

    for date, tobs in results:
        tobs_dict = {}
        tobs_dict[date] = tobs
        tobs_list.append(new_dict)

    session.close()

    return jsonify(tobs_list)

@app.route("/api/v1.0/start")
def start(start):
    
    session = Session(engine)
    
    start_list = []
    
    results = session.query(measurement.date, func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).filter(measurement.date >= start).group_by(measurement.date).all()

    for date, min, avg, max in results:
        start_dict = {}
        start_dict["Date"] = date
        start_dict["TMIN"] = min
        start_dict["TAVG"] = avg
        start_dict["TMAX"] = max
        start_list.append(start_dict)

    session.close()    

    return jsonify(start_list)
    
@app.route("/api/v1.0/start/end")
def end(start, end):
   
    session = Session(engine)
         
    end_list = []
    
    results = session.query(measurement.date, func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).filter(measurement.date >= start).group_by(measurement.date).all()

    for date, min, avg, max in results:
        end_dict = {}
        end_dict["Date"] = date
        end_dict["TMIN"] = min
        end_dict["TAVG"] = avg
        end_dict["TMAX"] = max
        end_list.append(end_dict)

    session.close()    

    return jsonify(end_list)

if __name__ == '__main__':
    app.run(debug=True)