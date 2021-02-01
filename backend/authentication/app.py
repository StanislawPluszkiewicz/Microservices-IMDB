import flask


app = flask.Flask(__name__)

@app.route('/index')
def index():
    return 'Index Page'

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = flask.request.form['username']
        password = flask.request.form['password']

        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute('SELECT id FROM user WHERE username = ?', (username, )).fetchone() is not None:
            error = 'User {} is already registered'.format(username)
        
        if error is None:
            db.execute(
                'INSERT INTO user(username, password) VALUES(?, ?)',
                (username, generate_passsword_hash(password))
            )
            db.commit()
            return redirect(url_for('login'))
        flask.flash(error)

    return 'Register page'


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