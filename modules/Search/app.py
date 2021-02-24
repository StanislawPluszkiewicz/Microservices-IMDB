from flask import Flask
from flask import render_template
from flask import request
import json
import requests
import modules.Utils.util as util
from flask_cors import CORS
from flask import jsonify

app = Flask(__name__)
CORS(app)

MAX_SEARCH = 5

def getFromParser(text, movie_name = True):
    result = ""

    if movie_name:
        result = requests.get(
            "http://parser:5013/parser/search?movie=" + text
        )
    else:
        result = requests.get(
            "http://parser:5013/parser/search?keyword=" + text
        )
    result = json.loads((util.convert_response(result)))
    result = result['data']
    # I have result

    final = []
    i = 1
    for movie in result['movies']:
        if i > MAX_SEARCH:
            break
        rtr = requests.get("http://movie:5011/movie/" + movie['id'])
        rtr = json.loads((util.convert_response(rtr)))
        final.append(rtr["data"])
        i = i + 1

    return final


@app.route('/search/movie')
def getMoviesByName():
    name = request.args.get('name')
    if name == None:
        return util.parameter_missing('name')
    else:
        result = getFromParser(name, True) # dict
        return util.response(success=True, message='it worked', code=util.ErrorCode.SUCCESS, data=result)


@app.route('/search/keyword')
def getMoviesByKeyword(key=None):
    name = request.args.get('name')
    if name == None:
        return util.parameter_missing('name')
    else:
        result = getFromParser(name, False)
        return util.response(success=True, message='it worked', code=util.ErrorCode.SUCCESS, data=result)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5012, debug=True)

#print(getMoviesByName("matrix"))
#print(getMoviesByKeyword('robot'))
