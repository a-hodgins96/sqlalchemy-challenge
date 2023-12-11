from flask import Flask, json, jsonify
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import inspect

engine = create_engine("sqlite:///Resources/hawaii.sqlite", connect_args={'check_same_thread': False})

Base = automap_base()

Base.prepare(engine, reflect=True)


measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

app = Flask(__name__) 


@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"Welcome to the Climate API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/2016-01-01/<br/>"
        f"/api/v1.0/2016-01-01/2016-12-31/"
    )


@app.route('/api/v1.0/precipitation/')
def precipitation():
    print("In Precipitation section.")
    
    lastest_date = session.query(measurement.date).order_by(measurement.date.desc()).first().date
    lastest_year = dt.datetime.strptime(lastest_date, '%Y-%m-%d') - dt.timedelta(days=365)

    results = session.query(measurement.date, measurement.prcp).\
    filter(measurement.date >= lastest_year).\
    order_by(measurement.date).all()

    p_dict = dict(results)
    print(f"Results for Precipitation - {p_dict}")
    print("Out of Precipitation section.")
    return jsonify(p_dict) 


@app.route('/api/v1.0/stations/')
def stations():
    print("In station section.")
    
    station_list = session.query(Station.station)\
    .order_by(Station.station).all() 
    print()
    print("Station List:")   
    for row in station_list:
        print (row[0])
    print("Out of Station section.")
    return jsonify(station_list)


@app.route('/api/v1.0/tobs/')
def tobs():
    print("In TOBS section.")
    
    lastest_date = session.query(measurement.date).order_by(measurement.date.desc()).first().date
    lastest_year = dt.datetime.strptime(lastest_date, '%Y-%m-%d') - dt.timedelta(days=365)

    temp_obs = session.query(measurement.date, measurement.tobs)\
        .filter(measurement.date >= lastest_year)\
        .order_by(measurement.date).all()
    print()
    print("Temperature Results for All Stations")
    print(temp_obs)
    print("Out of TOBS section.")
    return jsonify(temp_obs)


@app.route('/api/v1.0/<start_date>/')
def calc_temps_start(start_date):
    print("In start date section.")
    print(start_date)
    
    select = [func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)]
    result_temp = session.query(*select).\
        filter(Measurement.date >= start_date).all()
    print()
    print(f"Calculated temp for start date {start_date}")
    print(result_temp)
    print("Out of start date section.")
    return jsonify(result_temp)


@app.route('/api/v1.0/<start_date>/<end_date>/')
def calc_temps_start_end(start_date, end_date):
    print("In start & end date section.")
    
    select = [func.min(Measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)]
    result_temp = session.query(*select).\
        filter(measurement.date >= start_date).filter(measurement.date <= end_date).all()
    print()
    print(f"Calculated temp for start date {start_date} & end date {end_date}")
    print(result_temp)
    print("Out of start & end date section.")
    return jsonify(result_temp)

if __name__ == "__main__":
    app.run(debug=True)