from google.appengine.ext import ndb


class FilmskaBaza(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add=True)
    title = ndb.StringProperty()
    description = ndb.TextProperty()
    release = ndb.StringProperty()
    delete = ndb.BooleanProperty(default=False)
    picture = ndb.TextProperty()
    rating = ndb.StringProperty()
