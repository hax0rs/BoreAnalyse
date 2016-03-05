#!/usr/bin/env python3
from flask import Flask
from flask import request

import utm

app = Flask(__name__)

from borealysis.dbprovider import database
db = database()
try:
    db.build_tables()
except:
    pass

# GET Views


@app.route('/')
def index():
    return 'Hello World!'


@app.route('/holes')
@app.route('/holes/')
def holes():
    """ Returns Hole ID, Latitude, and Longitude"""
    print(db.get_holes())
    return ('''
        {
    "1": {
        "location": {
            "latitude": 123.456,
            "longitude": 789.101
        }
    },
    "2": {
        "location": {
            "latitude": 123.456,
            "longitude": 789.101
        }
    }
}
        ''')


@app.route('/holes/<bore_id>')
@app.route('/holes/<bore_id>/')
def hole_id(bore_id):
    """Returns JSON data related to the specifichole.

    Arguments:
    borehole_id -- The ID of the borehole

    Returns:
    location --
        latitude -- coordinates
        longitude --
    seam_count --


    """
    return 'Bore_ID: %s' % bore_id


@app.route('/holes/<bore_id>/<seam_id>')
@app.route('/holes/<bore_id>/<seam_id>/')
def seam(bore_id, seam_id):
    """ """
    return ("seam")


@app.route('/summary/<bore_id>')
@app.route('/summary/<bore_id>/')
def summary(bore_id):
    return('''
{
    "coal_count": 54,
    "coal_percent": 73.5,
    "rare": [{
        "name": "ABBREVIATION",
        "percent": 1
    }, {
        "name": "ABBREVIATION",
        "percent": 2
    }]
}
        ''')


# POST Views
#curl --data "holeid=123&easting=2419970.28&northing=7535210.728" http://localhost:5000/post/hole
@app.route("/post/hole", methods=['GET','POST'])
def post_hole():
    try:
        holeid = int(request.form['holeid'])
        zone, zoneletter = 4, 'u'
        east, north = float(request.form['easting']), float(request.form['northing'])
        lat, lon = utm.to_latlon(east, north, zone, zoneletter)
        print(holeid, lat, lon)
        return "Inserted"
    except Exception as e:
        return "read the docs ({})".format(e)


