from borealysis import app

# GET Views


@app.route('/')
def index():
    return 'Hello World!'


@app.route('/holes')
@app.route('/holes/')
def holes():
    """ Returns Hole ID, Latitude, and Longitude"""
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

