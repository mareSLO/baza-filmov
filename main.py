#!/usr/bin/env python
import os
import jinja2
import webapp2

from models import FilmskaBaza


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        movies = FilmskaBaza.query(FilmskaBaza.delete == False).order(FilmskaBaza.title).fetch()

        params = {"movies": movies}

        self.render_template("hello.html", params)


class AddMovie(BaseHandler):
    def get(self):
        self.render_template("add_movie.html")


class MovieAdded(BaseHandler):
    def post(self):
        title = self.request.get("title")
        description = self.request.get("description")
        release = self.request.get("release")
        picture = self.request.get("picture")
        rating = self.request.get("rating")

        if release == "":
            release = "Not provided"
        else:
            release = ("%s.%s.%s") % (release.split("-", 3)[2], release.split("-", 3)[1], release.split("-", 3)[0])

        if rating == "":
            rating = "Not provided"

        if picture == "":
            picture = "/assets/images/no_picture.jpg"

        movie = FilmskaBaza(title=title, description=description, release=release, picture=picture, rating=rating)
        movie.put()

        self.render_template("movie_added.html")


class MovieHandler(BaseHandler):
    def get(self, movie_id):
        movie = FilmskaBaza.get_by_id(int(movie_id))

        params = {"movie": movie}

        self.render_template("movie.html", params)


class MovieEdit(BaseHandler):
    def get(self, movie_id):
        movie = FilmskaBaza.get_by_id(int(movie_id))

        params = {"movie": movie}

        self.render_template("edit_movie.html", params)

    def post(self, movie_id):
        edit_title = self.request.get("title2")
        edit_description = self.request.get("description2")
        edit_release = self.request.get("release2")
        edit_picture = self.request.get("picture2")
        edit_rating = self.request.get("rating2")

        if edit_release == "":
            edit_release = "Not provided"

        if edit_rating == "":
            edit_rating = "Not provided"

        if edit_picture == "":
            edit_picture = "/assets/images/no_picture.jpg"

        movie = FilmskaBaza.get_by_id(int(movie_id))

        movie.title = edit_title
        movie.description = edit_description
        movie.release = edit_release
        movie.picture = edit_picture
        movie.rating = edit_rating
        movie.put()

        return self.redirect_to("home")


class MovieDelete(BaseHandler):
    def get(self, movie_id):
        movie = FilmskaBaza.get_by_id(int(movie_id))

        params = {"movie": movie}

        self.render_template("delete_movie.html", params)

    def post(self, movie_id):
        movie = FilmskaBaza.get_by_id(int(movie_id))

        movie.delete = True
        movie.put()

        return self.redirect_to("home")

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler, name="home"),
    webapp2.Route('/add', AddMovie),
    webapp2.Route('/movieadded', MovieAdded),
    webapp2.Route('/movie/<movie_id:\d+>', MovieHandler),
    webapp2.Route('/movie/<movie_id:\d+>/edit', MovieEdit),
    webapp2.Route('/movie/<movie_id:\d+>/delete', MovieDelete),
], debug=True)