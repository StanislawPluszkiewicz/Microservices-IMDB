import flask
from flask_cors import CORS, cross_origin
from flask import request
import sys
import modules.DB.db_utils as db
import modules.Utils.util as util
import session_manager as sm

app = flask.Flask(__name__)
CORS(app)
for key, value in sm.SessionManager.dumpAll():
    sm.SessionManager.remove(key)


_HEADERS_SESSION_TOKEN_NAME = 'token'

def check_session_token_is_valid(session_token):
    return False

# Example POST request
# {
#     "route": "",
#     "data": {}
# }
# cookies.token -> session_token

def authorization_error_response():
    return util.response(
        success = False,
        message = "Session token does not exist. Please log in or register",
        data = {},
        code = util.ErrorCode.AUTHORIZATION_ERROR
    )

def verify_session_token_is_set():
    session_token = None

    if _HEADERS_SESSION_TOKEN_NAME in request.cookies:
        session_token = request.cookies[_HEADERS_SESSION_TOKEN_NAME]
    else:
        return authorization_error_response()

    userId = sm.SessionManager.get(session_token)
    if userId is not None:
        sm.SessionManager.update(session_token, userId)
        return util.response(
            success = True,
            message = "Authorized.",
            code = util.ErrorCode.SUCCESS,
            cookies = {
                _HEADERS_SESSION_TOKEN_NAME: session_token
            },
            developerMessage="Session token is refreshed"
        )
    else:
        return authorization_error_response()

def create_session_token(userID):
    if not userID:
        return util.parameter_missing('user')
    session_token = sm.SessionManager.create(userID)
    return util.response(
        success = True,
        message = "Created session.",
        code = util.ErrorCode.SUCCESS,
        cookies = {
            _HEADERS_SESSION_TOKEN_NAME: session_token
        },
        developerMessage="Session token is created"
    )



@app.route('/auth', methods=['POST', 'GET'])
def authorize():
    if request.method == 'GET':
        return verify_session_token_is_set()
    elif request.method == 'POST':
        return create_session_token(request.form['user'])
    return util.cannot_call_with_this_method()

@app.route('/authCreateSession', methods=['POST'])
def createFakeToken():
    parameter_user_id_name = 'user'
    if request.method == 'POST':
        if not parameter_user_id_name in request.form:
            return util.parameter_missing(parameter_user_id_name)
        userId =  request.form.get(parameter_user_id_name)

        sessionId = sm.SessionManager.create(userId)
        return util.response(
            success = True,
            message = "Added user",
            data = {
                userId: sessionId.decode("utf-8")
            },
            code = util.ErrorCode.SUCCESS,
            cookies = {
                _HEADERS_SESSION_TOKEN_NAME: sessionId.decode("utf-8")
            }
        )
    return util.cannot_call_with_this_method()

@app.route('/authDumpAll', methods=['POST'])
def authorizeDumpAll():  
    if request.method == 'POST':
        data = sm.SessionManager.dumpAll()
        for key, value in data:
            sm.SessionManager.remove(key)
        return util.response(
            success = True,
            message = "Dumped all REDIS keys",
            data = data,
            code = util.ErrorCode.SUCCESS
        )
    return util.cannot_call_with_this_method()


    
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5003, debug=True)