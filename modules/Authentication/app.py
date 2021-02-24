import flask
from flask_cors import CORS, cross_origin
import requests
import json
import hashlib, uuid

import modules.DB.db_utils as db
import modules.Utils.util as util

app = flask.Flask(__name__)
CORS(app)


def wrong_credentials_error():
    return util.response(
        success = False,
        message = "Wrong credentials.",
        code = util.ErrorCode.AUTHENTICATION_ERROR
    )


def create_session_token(userId):
    return requests.post(
        "http://authorization:5003/auth", 
        data={
            "user": userId
        }
    )


@app.route('/login', methods=['POST'])
def login():
    if flask.request.method == 'POST':

        # Retrieve all data
        print('form: ' + str(flask.request.form))
        print('args: ' + str(flask.request.args))
        username, error = util.retrieve_var(flask.request.form, 'username')
        if error:
            return error
        password, error = util.retrieve_var(flask.request.form, 'password')
        if error:
            return error

        # Get user
        user = db.User.objects(login=username).first()

        # If user doesnt exist create error response
        if user is None or salt_password(password, user.salt) != user.password:
            return wrong_credentials_error()

        # Create session
        response_session_token = create_session_token(user.pk)
        token_response = json.loads(util.convert_response(response_session_token))

        # Create response
        login_response_data = {
            "id_user": str(user.pk),
            "username": user.login,
            "email": user.email,
            "firstname": user.firstname,
            "lastname": user.lastname
        }

        return util.response(
            success = True,
            message = "Successfully logged user",
            data = login_response_data,
            developerMessage = 'User is logged with a session cookie.',
            code = util.ErrorCode.SUCCESS,
            cookies = response_session_token.cookies
        )

    return util.cannot_call_with_this_method()


@app.route('/register', methods=['POST'])
def register():
    if flask.request.method == 'POST':

        # Retrieve all data
        username, error = util.retrieve_var(flask.request.form, 'username')
        if error:
            return error
        password, error = util.retrieve_var(flask.request.form, 'password')
        if error:
            return error
        email, error = util.retrieve_var(flask.request.form, 'email')
        if error:
            return error
        firstname, error = util.retrieve_var(flask.request.form, 'firstname')
        if error:
            return error
        lastname, error = util.retrieve_var(flask.request.form, 'lastname')
        if error:
            return error

        salt = generate_salt(username, password)
        # Insert new user into database
        user = db.User(
            login=username,
            password=salt_password(password, salt),
            email=email,
            firstname=firstname,
            lastname=lastname, 
            salt=salt
        )
        user.save()
        
        # Create response
        return util.response(
            success = True,
            message = "Successfully registered user",
            developerMessage = 'User is not logged in. Please call /login',
            code = util.ErrorCode.SUCCESS
        )

def generate_salt(username, password):
    return uuid.uuid4().hex

def salt_password(password, salt):
    return hashlib.sha512((password + salt).encode('utf-8')).hexdigest()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)