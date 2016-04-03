#!/usr/bin/env python3
from flask import Flask
from flask import request
from flask import json

import utm
import csv
import urllib
import datetime

from multiprocessing import Process, Pool

app = Flask(__name__)

from borealysis.dbprovider import database
db = database()
try:
    db.build_tables()
except:
    pass

# GET Views
@app.route('/holes')
@app.route('/holes/')
def holes():
    """ Returns Hole ID, Latitude, and Longitude"""
    working = db.get_holes()
    final = {}
    for hole in db.get_holes():
        final[hole[0]] = {'location':{'latitude': hole[1], 'longitude': hole[2]}}
    return json.jsonify(final)

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
    info = db.get_hole(bore_id)[0]
    segments = db.get_segments(bore_id)
    segments_dic = {}
    for seg in segments:
        segdic = {}
        segdic['range'] = {'start': seg[3], 'end': seg[4]}
        if seg[1] == 1:
            segdic['type'] = seg[2]
        segments_dic[seg[0]] = segdic

    final = {'bore_id': bore_id, 'location':{'latitude': info[1], 'longitude': info[2]}, 'segment_count': len(segments), 'segment': segments_dic}
    return json.jsonify(final)


@app.route('/holes/<bore_id>/<seam_id>')
@app.route('/holes/<bore_id>/<seam_id>/')
def seam(bore_id, seam_id):
    #info = db.get_segment(bore_id, seam_id)[0]
    plys = db.get_plys(bore_id, seam_id)
    plys_dic = {}
    for ply in plys:
        plys_dic[ply[0]] = {'type': ply[1], 'range': {'start': ply[2], 'end': ply[3]}}

    final = {'bore_id': bore_id, 'seg_id': seam_id , 'ply_count': len(plys), 'ply': plys_dic}
    return json.jsonify(final)


@app.route('/summary/<bore_id>')
@app.route('/summary/<bore_id>/')
def summary(bore_id):
    coal = "CO"
    depth = db.get_hole_depth(bore_id)[0][0] or 0
    stats = db.get_hole_stats(bore_id, coal)
    if stats == []:
        stats = [(0,0)]
    coals, coaldepth = stats[0]
    pcoal = coaldepth/depth *100
    rares = []
    for element in db.get_hole_breakdown(bore_id):
        if element[0] not in (None, "", coal):
            rares.append({"name": element[0], "percent": element[2]/depth*100, "count": element[1]})

    final = {'depth': depth, 'coal_count': coals, 'coal_percent': pcoal, 'rare': rares}
    return json.jsonify(final)

@app.route('/generate')
@app.route('/generate/')
def generate_all():
    with open('full_data.csv') as f:
        full_data = list(csv.reader(f))
        holes = [x[0] for x in full_data]

        for hole in set(holes):
            generate(hole)

@app.route('/generate/<bore_id>')
@app.route('/generate/<bore_id>/')
def generate(bore_id):
    with open('full_data.csv') as csvfile:
        reader = csv.reader(csvfile)
        array = list(reader)
        array = list(filter(lambda x: x[0] == bore_id, array))
        
        db_segments = db.get_segments(bore_id)
        def check_redundant(row):
            for segment in db_segments:
                if segment[-2] <= float(row[1]) < segment[-1]:
                    return False
            return True

        print(len(array))
        array = list(filter(lambda x: check_redundant(x), array))
        print(len(array))

        pool = Pool(processes=10)
        results = pool.map(get_azure, array)
        print(len(results))
        results = list(filter(lambda x: x is not None, results))
        print(len(results))
        depths = [float(x[0]) for x in results]
        data = [(row[0], 1, result[1], float(result[0]), min(filter(lambda x: x > float(result[0]), depths))) 
            for row in array for result in results if float(result[0]) == float(row[1]) if float(result[0]) != max(depths)]
        
        for row in data:
            db.put_segment(*row)

        return str(data)

def get_azure(row):
    try:
        data =  {

        "Inputs": {
                "input1":
                {
                    "ColumnNames": ["Col1", "Col2", "Col3", "Col4", "Col5", "Col6", "Col7", "Col8", "Col9"],
                    "Values": [row]
                    },        
            },
            "GlobalParameters": {}
        }

        body = str.encode(json.dumps(data))

        url = 'https://ussouthcentral.services.azureml.net/workspaces/b39c93660f1b4f91b7c7578fdbb4747d/services/e81f93528e1949279c793679d7400965/execute?api-version=2.0&details=true'
        api_key = 'JvSUvSc4vV6VYIPlOCS+cNfF8fHSAaMWfD+6lELTywCko19eO6mE9w6L6DJHLkkYiJ7g8e7XpxprXD6ytJtXOw=='
        headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

        req = urllib.request.Request(url, body, headers) 
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read())['Results']['output1']['value']['Values'][0]
            return result[0], result[-1]
    except urllib.error.HTTPError as e:
        # Keep retrying iff 503 error
        if e.code == 503:
            return get_azure(row)
        else:
            print(e)
    return None

# POST Views
#OLD curl --data "holeid=123&lat=-20.244972&lon=143.743137" http://localhost:5000/post/hole
#curl --data "holeid=1235&easting=2419970.28&northing=7535210.728" http://localhost:5000/post/hole
@app.route("/post/hole", methods=['GET','POST'])
def post_hole():
    try:
        holeid = int(request.form['holeid'])
        zone, zoneletter = 55, 'K'                # \/ It just works tm
        east, north = float(request.form['easting'])/10, float(request.form['northing'])
        #lat, lon = float(request.form['lat']), float(request.form['lon'])
        lat, lon = utm.to_latlon(east, north, zone, zoneletter)
        db.put_hole(holeid, lat, lon)
        return "Inserted"
    except Exception as e:
        return "read the docs ({})".format(e)

#            Can be null       CM
#curl --data "seamtype=GOP&start=0&end=100" http://localhost:5000/post/hole/123/segment
#curl --data "start=150&end=200" http://localhost:5000/post/hole/456/segment
@app.route("/post/hole/<bore_id>/segment", methods=['GET','POST'])
def post_segement(bore_id):
    try:
        holeid = int(bore_id)
        seam = 'seamtype' in request.form and request.form['seamtype'] not in ("",None)
        if seam:
            seamtype = request.form['seamtype']
        else:
            seamtype = ""
        seam = int(seam)
        startrange, endrange = int(request.form['start']), int(request.form['end'])
        db.put_segment(holeid, seam, seamtype, startrange, endrange)
        return "Inserted"
    except Exception as e:
        return "read the docs ({})".format(e)

#                           CM
#curl --data "seamtype=GOP&start=0&end=100" http://localhost:5000/post/hole/123/segment/1/ply
@app.route("/post/hole/<bore_id>/segment/<seg_id>/ply", methods=['GET','POST'])
def post_ply(bore_id, seg_id):
    try:
        holeid, segid = int(bore_id), int(seg_id)
        seamtype = request.form['seamtype']
        startrange, endrange = int(request.form['start']), int(request.form['end'])
        db.put_ply(holeid, segid, seamtype, startrange, endrange)
        return "Inserted"
    except Exception as e:
        return "read the docs ({})".format(e)
