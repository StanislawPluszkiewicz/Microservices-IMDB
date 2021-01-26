import flask
from flask_mongoengine import MongoEngine
from flask import *


app = flask.Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'IMDB',
    'host': 'mongodb+srv://admin:admin@imdb.ewvcu.mongodb.net/IMDB?retryWrites=true&w=majority'
}
db = MongoEngine(app)

@app.route('/')
def test():
    return 'test'

@app.route('/index')
def index():
    return 'Index Page'

@app.route('/comments', methods=["GET","POST"])
def comments():
    if request.method == 'POST':
        return 'non'
    return '''
        <form method="post">
            <p><input type=text name=comments>
            <p><input type=submit value=Send>
        </form>
    '''
    
