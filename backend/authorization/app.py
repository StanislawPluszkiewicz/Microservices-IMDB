import flask

app = flask.Flask(__name__)

@app.route('/index')
def index():
    return 'Index Page'

@app.route('/token', methods = ['GET'])
def login():
    username = flask.request.form['username']
    password = flask.request.form['password']

    response = flask.make_response()
    # response.headers['SetCookie'] = 'session_token=42'
    response.set_cookie('session_token', '42')
    response.set_cookie('coucou', str(username + ' ' + password))
    # flask.redirect(flask.url_for('index'))
    return response

