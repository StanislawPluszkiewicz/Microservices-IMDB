import flask
from flask import *
from modules.DB.db_utils import *
import modules.Utils.util as util
from flask_cors import CORS, cross_origin

app = flask.Flask(__name__)
CORS(app)

@app.route('/comments', methods=["GET","POST","PUT"])
def comments():

    #if util.is_timeout() :
    #    return util.timeout()

    data = {}
    #region GET
    if request.method == 'GET':
        
        movieID = request.args.get('movieID')
        userID = request.args.get('userID')

        if(userID == None and movieID == None) :
            return util.parameter_missing('userID or movieID')
        
        if(movieID != None and userID!=None):
            movie = Movie.objects.get(imdb_id=movieID)
            commentList = Note.objects(id_movie=movie.id, id_user=userID)
            message = "Comments of a User of a Movie"
            devMessage = 'list of comments of a user of a movie was successfully made'

        elif(movieID != None):
            movie = Movie.objects.get(imdb_id=movieID)
            commentList = Note.objects(id_movie=movie.id)
            message = "Comments of a Movie"
            devMessage = 'List of comments of a movie was successfully made'

        elif(userID != None):
            commentList = Note.objects(id_user=userID)
            message = "Comments of a User"
            devMessage = 'list of comments of a user was successfully made'
        
        else :
            return util.parameter_missing("userID/movieID")
            
        commentJsonList = {
            "comments": [{"userName":comment.id_user.login,"movieName":comment.id_movie.name,"date":comment.date,"note":comment.note,"review":comment.comment} for comment in commentList]
        } 
        data = commentJsonList
    #endregion

    #region POST
    elif request.method == 'POST':

        movieID, error = util.retrieve_var(flask.request.form,'movieID')
        if error:
            return error
        userID, error = util.retrieve_var(flask.request.form, 'userID')
        if error:
            return error
        note, error = util.retrieve_var(flask.request.form, 'note')
        if error:
            return error
        comment, error = util.retrieve_var(flask.request.form, 'comment')
        if error:
            return error      

        movie = Movie.objects.get(imdb_id=movieID)


        review = Note (
        id_user=userID, 
        id_movie=movie,
        note=note,
        comment=comment
        )
        review.save()

        message = "Insertion d'une nouvelle review"
        devMessage = "newReview movieId : " + str(movieID) + " userId : " + str(userID)

    #endregion
    
    #region PUT
    elif request.method == 'PUT' :


        commentID, error = util.retrieve_var(flask.request.form,'commentID')
        if error:
            return error

        note, error = util.retrieve_var(flask.request.form, 'note')
        if error:
            return error
            
        comment, error = util.retrieve_var(flask.request.form, 'comment')
        if error:
            return error


        Note.objects.get(id=commentID).update(note=note,comment=comment)

        message = "Update d'une  review"
        devMessage = "update review commentID : " + str(commentID)
    #endregion
    
    else :
        return util.cannot_call_with_this_method()

    return util.response(
        success = True,
        message = message,
        data = data,
        developerMessage = devMessage,
        code = util.ErrorCode.SUCCESS)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5005, debug=True)