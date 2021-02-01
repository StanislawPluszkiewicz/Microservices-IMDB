import flask
from flask import request
import sys
import util


app = flask.Flask(__name__)

@app.route('/index')
def index():
    return 'Index Page'

_HEADERS_SESSION_TOKEN_NAME = 'token'

def check_session_token_is_valid(session_token):
    pass

# Example POST request
# {
#     "route": "",
#     "data": {}
# }
# cookies.token -> session_token
@app.route('/auth', methods=['GET', 'POST'])
def authorize():
    error = None
    if request.method == 'POST':
        session_token = None
        if _HEADERS_SESSION_TOKEN_NAME in request.cookies:
            session_token = request.cookies
        check_session_token_is_valid(session_token)

    flask.flash(error)    
    return util.response(error == None, '', {})

