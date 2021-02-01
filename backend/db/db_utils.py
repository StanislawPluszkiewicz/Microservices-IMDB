
from mongoengine import (
    connect, Document, 
    StringField, ReferenceField, DateTimeField, FloatField, IntField, ListField
)
import datetime
import log


_MONGO_DB_HOST = "mongodb+srv://admin:admin@imdb.ewvcu.mongodb.net/IMDB?retryWrites=true&w=majority"
_MONGO_DB_DATABASE_NAME = "IMDB"
_MONGO_CLIENT = connect(db=_MONGO_DB_DATABASE_NAME, host=_MONGO_DB_HOST)

class User(Document):
    login = StringField(max_length=255, required=True)
    password = StringField(max_length=255, required=True)
    salt = StringField(max_length=255, required=True)

# Replaced with Redis
# class Session_Token(Document):
#    id_user = ReferenceField(User)
#    token = StringField(required=True)
#    expiration = DateTimeField()


class Movie(Document):
    imdb_id = StringField(required=True)
    name = StringField(required=True, unique=True)
    description = ListField(StringField(), default=list)
    cover_url = StringField()
    
class Note(Document):
    id_user = ReferenceField(User)
    id_movie = ReferenceField(Movie)
    note = FloatField(min_value=0, max_value=10)
    date = DateTimeField(default=datetime.datetime.now)
    comment = StringField()

def example_usage():
    User .objects.delete()
    Movie.objects.delete()
    Note .objects.delete()

    def insert_user():
        user = User (
            login="Michel", 
            password="michemiche", 
            salt=""
        )
        user.save()
    def insert_movie():
        movie = Movie (
            imdb_id="0436992",
            name="The Matrix"
        )
        movie.save()
    def insert_note():
        user_michel = User.objects(login="Michel").first()
        movie_matrix = Movie.objects(name="The Matrix").first()

        note = Note (
            id_user=user_michel, 
            id_movie=movie_matrix,
            note=8.5,
            comment="Without a doubt one of the best and most influential movies of all time, the Matrix is the defining science fiction film of the 1990's and the biggest leap the genre has taken since Stanley Kubrick's 2001: A Space Odyssey and Ridley Scott's Blade Runner. The Matrix is a ground-breaking motion picture that not only raised the bar for all the science-fiction films to come after it but also redefined the action genre with its thrilling action sequences and revolutionary visual effects."
        )
        note.save()
    def count_note():
        note_count = Note.objects().count() 
        print(note_count)
        
    insert_user()
    insert_movie()
    insert_note()
    

if __name__ == '__main__':
    example_usage()
