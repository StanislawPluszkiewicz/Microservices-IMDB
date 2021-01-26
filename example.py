from flask import Flask
from flask import render_template
from flask import request


app = Flask(__name__)

@app.route('/')
def index():
    return 'Index Page'

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

def valid_login(username, password):
    return username == 'root'

def log_the_user_in(username):
    print(log_the_user_in + ' is logged in')

@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['username'], request.form['password']):
            return log_the_user_in(request.form['username'])
        else:
            error = 'Invalid credentials'
    return render_template('login.html', error=error)