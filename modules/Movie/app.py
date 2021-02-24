from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
import json
from modules.DB.db_utils import Movie
import requests
import modules.Utils.util as util
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
#print(ia.get_movie_infoset())
#m = ia.get_movie('0133093', info=['main', 'video clips'])
#print(m.infoset2keys)
#print(m.get('video clips and trailers'))
#print(ia.get_person_infoset())

#m = ia.get_movie('0436992')
#m = ia.get_movie('0133093')
#getListFromCast(m['cast'], True)

HOMEPAGE = ['0436992', '0903747', '0266543', '1392190', '4477976',
'0411008', '3569230', '2802144', '0119698', '0288045']


def popBasicAndStringFromData(data):
    e = removekey(data, 'id')
    e = removekey(e, 'title')
    e = removekey(e, 'description')
    e = removekey(e, 'image')
    return json.dumps(e)

def removekey(d, key):
    r = dict(d)
    del r[key]
    return r

def merge_dicts(x, y):
    z = x.copy()
    z.update(y)
    return z
    
def getInfoMovieWithDB(id_movie, details=False):

    movie_db = Movie.objects(imdb_id=id_movie).first()
    txt = "http://parser:5013/parser/" + id_movie
    if(details):
        txt += "/details"
    if movie_db is None:
         # If not found in BDD or asked for details
        
        result = json.loads(util.convert_response(requests.get(txt)))
        if result and result['success'] and result['success'] == "True":
            
            if not details:
                movie_db = Movie (
                    imdb_id = result['data']['id'],
                    name= result['data']['title'],
                    description = result['data']['description'],
                    cover_url = result['data']['image'],
                    detailed = False
                )
                movie_db.save()
            else:
                dataOnly = popBasicAndStringFromData(result['data'])
                movie_db = Movie (
                    imdb_id = result['data']['id'],
                    name= result['data']['title'],
                    description = result['data']['description'],
                    cover_url = result['data']['image'],
                    detailed = True,
                    details = dataOnly
                )
                movie_db.save()

        return result['data']

    else:
        if details and movie_db.details:
            x = {
                "id" : movie_db.imdb_id,
                "title": movie_db.name,
                "description" : movie_db.description,
                "image": movie_db.cover_url,
            }

            y = json.loads(movie_db.details)
            x = merge_dicts(x, y)
            return x
        elif details and not movie_db.details:

            result = json.loads(util.convert_response(requests.get(txt)))
            if result and result['success'] and result['success'] == "True":
                dataOnly = popBasicAndStringFromData(result['data'])
                movie_db.detailed = True
                movie_db.details = dataOnly
                movie_db.save()
            
            return result['data']

        elif not details:
            x = {
                "id" : movie_db.imdb_id,
                "title": movie_db.name,
                "description" : movie_db.description,
                "image": movie_db.cover_url,
            }
            return x


       

def get10Movies():

    m = []
    for idM in HOMEPAGE:
        movie_db = Movie.objects(imdb_id=idM).first()
        if movie_db is not None:
            y = {
                "id" : movie_db.imdb_id,
                "title": movie_db.name,
                "description" : movie_db.description,
                "image": movie_db.cover_url,
            }
            m.append(y)
        else:
            txt = "http://parser:5013/parser/" + idM
            result = json.loads(util.convert_response(requests.get(txt)))
            print(result)
            if result and result['success'] and result['success'] == "True":
                movie_db = Movie (
                    imdb_id = result['data']['id'],
                    name= result['data']['title'],
                    description = result['data']['description'],
                    cover_url = result['data']['image']
                )
                movie_db.save()
                
            m.append(result['data'])

    return m



@app.route('/movie/<id_movie>')
def getInfoMovie(id_movie=None):
    if id_movie == None:
        return util.parameter_missing('id_movie')
    else:
        #Add here DBB content
        result = getInfoMovieWithDB(id_movie, False)
        if result == {}:
            return util.response(success=False, message="No movie/show found", code=util.ErrorCode.ERROR_404)
        else:
            return util.response(success=True, message='it worked', code=util.ErrorCode.SUCCESS, data=result)


@app.route('/movie/<id_movie>/details')
def getInfoMovieDetailed(id_movie=None):
    if id_movie == None:
        return util.parameter_missing('id_movie')
    else:
        result = getInfoMovieWithDB(id_movie, True)
        if result == {}:
            return util.response(success=False, message="No movie/show found", code=util.ErrorCode.ERROR_404)
        else:
            return util.response(success=True, message='it worked', code=util.ErrorCode.SUCCESS, data=result)

@app.route('/movie/homepage')
def getHomepage():
    result = get10Movies()
    return util.response(success=True, message='it worked', code=util.ErrorCode.SUCCESS, data=result)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5011, debug=True)


#print(json.dumps(getInfoMovieWithDB('0133093'), indent=4)) # Matrix 0133093
#print(json.dumps(getInfoMovieWithDB('4477976'), indent=4)) # Superstore 4477976
  
#print(json.dumps(getInfoMovieWithDB('0411008'), indent=4))  # Lost 0411008
#print(json.dumps(getInfoParsed('3569230', True), indent=4)) 3569230