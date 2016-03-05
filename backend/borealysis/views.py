from borealysis import app

# GET Views


@app.route('/')
def index():
    return 'Hello World!'


@app.route('/holes/')
def holes():
    return ("these are the holes")


@app.route('/holes/<id>')
def hole_id():
    return ("h")


@app.route('/summary/<id>')
def summary():
    pass


# POST Views

