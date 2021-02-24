from imdb import IMDb
from flask import Flask
from flask import render_template
from flask import request
from imdb import IMDb
import json
from flask_cors import CORS
import modules.Utils.util as util
import time

ia = IMDb()

MAIN_CAST_AMOUNT = 6

app = Flask(__name__)
CORS(app)

def merge_dicts(x, y):
    z = x.copy()
    z.update(y)
    return z

def getInfoParsed(id_movie, details):
    movie = ia.get_movie(id_movie)
    if 'kind' not in movie:
        return 'not_found'
    kind = movie['kind']
    img = ""
    if 'full-size cover url' in movie:
        img = movie['full-size cover url']
    elif 'cover url' in movie:
        img = movie['cover url']

    plot = [""]
    if 'plot' in movie:
        plot = getDescFromPlot(movie['plot'])
    x = {
        "id" : movie['imdbID'],
        "title": movie['title'],
        "image": img,
        "description" : plot
    }

    if details:
        cast = movie['cast']
        y = {
            "genres": movie['genres'],
            "runtime" : movie['runtimes'][0]
        }
        
        if(kind == 'tv series'):
            creators = movie['creator']
            serieStuff = {
                "type" : "tv-show",
                "cast" : getListFromCast(cast, True),
                "directors": [p['name'] for p in creators],
                "seasons" : movie['number of seasons'],
                "date" : movie['series years']
            }
            y = merge_dicts(y, serieStuff)
        if(kind == 'movie'):
            directors = movie['directors']
            date = ""
            if 'original air date' in movie:
                date = movie['original air date']
            movieStuff = {
                "type" : "movie",
                "cast" : getListFromCast(cast, False),
                "directors" : [p['name'] for p in directors],
                "date" : date,
            }
            y = merge_dicts(y, movieStuff)


        x = merge_dicts(x, y)

    return x

def getListFromCast(cast, isSerie):
    r = []
    for i in range(min(MAIN_CAST_AMOUNT, len(cast))):
        currentCast = cast[i]
        ia.update(currentCast, info=['main'])
        roles = []
        
        #if hasattr(currentCast.currentRole, '__iter__'):
        #    for c in currentCast.currentRole:
        #        roles.append(c['name'])
        #else:

            #print(currentCast.currentRole.infoset2keys)
        roles = str(currentCast.currentRole).split("/")


        char = {
            "name" : currentCast['name'],
            "role" : roles,
        }

        if 'headshot' in currentCast :
            char = merge_dicts(char, {"image" : currentCast['headshot']})
            
        
        if isSerie and ((currentCast.currentRole.notes is not None and currentCast.currentRole.notes != "") or isinstance(currentCast.currentRole, list)):

            note = ""
            eps = ""
            date = ""
            if isinstance(currentCast.currentRole, list):
                note = currentCast.currentRole[0].notes.replace('(', '').replace(')', '')
            else:
                note = currentCast.currentRole.notes.replace('(', '').replace(')', '')

            if(len(note.split(',')) > 1):
                eps = note.split(',')[0]
                date = note.split(',')[1]
            else:
                date = note

            x = {
                "nb_episodes": eps.split(' ')[0],
                "date": date
            }
            char = merge_dicts(char, x)
        
        r.append(char)
    return r


def getDescFromPlot(plot):
    desc = []
    for p in plot:
        newText = p.replace("--", " ").replace("::", " - ")
        for t in newText.split("\n"):
            desc.append(t)
    return desc

@app.route('/parser/<id_movie>/')
def getParserMovie(id_movie=None):
    if id_movie == None:
        return util.parameter_missing('id_movie')
    else:
        result = getInfoParsed(id_movie, False)
        if result == 'not_found':
            return util.response(success=False, message="No movie/show found", code=util.ErrorCode.ERROR_404)
        else:
            return util.response(success=True, message='it worked', code=util.ErrorCode.SUCCESS, data=result)

@app.route('/parser/<id_movie>/details')
def getParserMovieDetailed(id_movie=None):
    if id_movie == None:
        return util.parameter_missing('id_movie')
    else:
        result = getInfoParsed(id_movie, True)
        if result == 'not_found':
            return util.response(success=False, message="No movie/show found", code=util.ErrorCode.ERROR_404)
        else:
            return util.response(success=True, message='it worked', code=util.ErrorCode.SUCCESS, data=result)

def updateSearchInfos(movieList):
    newList = []
    i = 1
    for movie in movieList:
        if i > 10:
            break
        ia.update(movie, info=['plot', 'main'])
        p = [""]
        if 'plot' in movie:
            p = getDescFromPlot(movie['plot'])


        y = {
            "id" : movie.movieID,
            "title": movie['title'],
            "image": movie['full-size cover url'],
            "description" : p
        }
        newList.append(y)
        i = i + 1
    return newList


@app.route('/parser/search')
def getSearchParser():
    name = request.args.get('movie')
    keyword = request.args.get('keyword')
    if name == None:
        if keyword == None:
            return util.parameter_missing('keyword')
        else:
            keyword = ia.search_keyword(keyword)
            movies = ia.get_keyword(keyword[0])
            x = {
                "movies": [{"id" : m.movieID, "title" : m['title']} for m in movies]
            }
            return util.response(success=True, message='it worked', code=util.ErrorCode.SUCCESS, data=x)
        return util.parameter_missing('movie')
    else:
        movies = ia.search_movie(name)
        x = {
            "movies": [{"id" : m.movieID, "title" : m['title']} for m in movies]
        }
        return util.response(success=True, message='it worked', code=util.ErrorCode.SUCCESS, data=x)
        


#movies = ia.search_movie("Superstore")
#tic = time.time()
#result = updateSearchInfos(movies)
#toc = time.time()
#print(toc-tic)
#x = {
#    "movies" : result
#}
#print(json.dumps(x, indent=4))
#exit()


#getInfoParsed('0436992', True)
        
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5013, debug=True)