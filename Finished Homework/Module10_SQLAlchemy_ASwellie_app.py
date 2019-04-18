import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

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
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
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
        f"Available Routes:<br/>"
        f"<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"<br/>"
        f"<br/>"
        f"Get weather stats for a specific start date...enter date in this format:<br/>"
        f"/api/v1.0/yyyy-mm-dd/<br/>"
        f"<br/>"
        f"<br/>"
        f"Get weather stats for a specific start and end date...enter dates in this format:<br/>"
        f"/api/v1.0/yyyy-mm-dd/yyyy-mm-dd/<br/>"
    )

@app.route('/api/v1.0/precipitation')
def precipitation():
   most_recent = session.query(Measurement).order_by(Measurement.date.desc()).limit(1)
    
   for day in most_recent:
        most_recent_date = day.date

   most_recent_date = dt.datetime.strptime(most_recent_date, "%Y-%m-%d")  

  
   one_year_date = most_recent_date - dt.timedelta(days=366)

    
   rain_info = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= one_year_date).order_by(Measurement.date).all()
    
   precip_data = []
   for date, precip in rain_info:
        precip_dict = {}
        precip_dict["date"] = date
        precip_dict["prcp"] = precip
        precip_data.append(precip_dict)
        
   return jsonify(precip_data)

# @app.route("/api/v1.0/passengers")
# def passengers():
#     """Return a list of passenger data including the name, age, and sex of each passenger"""
#     # Query all passengers
#     results = session.query(Passenger.name, Passenger.age, Passenger.sex).all()

#     # Create a dictionary from the row data and append to a list of all_passengers
#     all_passengers = []
#     for name, age, sex in results:
#         passenger_dict = {}
#         passenger_dict["name"] = name
#         passenger_dict["age"] = age
#         passenger_dict["sex"] = sex
#         all_passengers.append(passenger_dict)

#     return jsonify(all_passengers)

@app.route('/api/v1.0/<date>/')
def one_date(date):
    
    result = session.query(Measurement.date, func.avg(Measurement.tobs), func.max(Measurement.tobs), func.min(Measurement.tobs)).\
        filter(Measurement.date == date).all()


    one_date_list = []
    for date in result:
        output = {}
        output['Date'] = date[0]
        output['Average Temperature'] = date[1]
        output['Highest Temperature'] = date[2]
        output['Lowest Temperature'] = date[3]
        one_date_list.append(output)

    return jsonify(one_date_list)

@app.route('/api/v1.0/<start_date>/<end_date>/')
def date_range(start_date, end_date):
    
    result = session.query(func.avg(Measurement.tobs), func.max(Measurement.tobs), func.min(Measurement.tobs)).\
        filter(Measurement.date >= start_date, Measurement.date <= end_date).all()

    range_date_list = []
    for date in result:
        output = {}
        output["Start Date"] = start_date
        output["End Date"] = end_date
        output["Average Temperature"] = date[0]
        output["Highest Temperature"] = date[1]
        output["Lowest Temperature"] = date[2]
        range_date_list.append(output)
    return jsonify(range_date_list)


if __name__ == '__main__':
    app.run(debug=True)
