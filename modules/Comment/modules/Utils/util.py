import flask
import json 
import requests
class ErrorCode:
    SUCCESS = 200
    AUTHORIZATION_ERROR = 401
    WRONG_METHOD = 402
    PARAMETER_MISSING = 403
    ERROR_404 = 404
    TIMEOUT = 405
    AUTHENTICATION_ERROR = 406


def parameter_missing(paramter):
    return response(
        success = False,
        message = "Paramter missing: " + str(paramter),
        code = ErrorCode.PARAMETER_MISSING,
        developerMessage="Consider adding this paramter to the body and/or consulting the doc."
    )

# Typical usage: 
# username, error = retrieve_var(flask.request.form, 'username')
# if error != None:
#   return error
def retrieve_var(_from, name):
    if name in _from:
        return _from[name], None
    else:
        return None, parameter_missing(name)

def check_timeout():
    r = requests.post("http://127.0.0.1:5000/auth")
    return r.status_code == ErrorCode.SUCCESS

def timeout():
    return response(
        success = False,
        message = "Timeout",
        code = ErrorCode.TIMEOUT
    )
    
def _timeout_usage_example():
    if (check_timeout()):
        return timeout()
    return None


def cannot_call_with_this_method():
    return response(
        success = False,
        message = "Cannot call with this method.",
        code = ErrorCode.WRONG_METHOD
    )

def convert_response(response):
    return response.text


def response(
    success, 
    message, 
    data = {}, 
    code='', 
    developerMessage='', 
    cookies = {}, 
    headers = {}
    ):
    
    innerData = data
    if data is dict:
        innerData = flask.jsonify(data)

    res = flask.make_response(
        {
            "success": str(success),
            "message": str(message),
            "developerMessage": str(developerMessage),
            "data": innerData
        }, 
        code
    )
    for cookie_name, cookie_value in cookies.items():
        res.set_cookie(cookie_name, value=cookie_value)

    for header_name, header_value in headers.items():
        res.headers[header_name] = header_value

    # Enable CORS
    res.headers.add("Access-Control-Allow-Origin", "*")

    res.status_code = code
    return res