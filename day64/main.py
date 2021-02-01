# My Top 10 Movies

from flask import Flask, render_template, request, redirect
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, SubmitField
from wtforms.validators import DataRequired, URL
import requests

import config

# number of movies to display, by default 10
# limited by the actual number of rows in the DB though
TOP_LIMIT = 10
TMDB_SEARCH_URL = "https://api.themoviedb.org/3/search/movie"
TMDB_INFO_URL = "https://api.themoviedb.org/3/movie"
TMDB_IMAGE_URL = "https://image.tmdb.org/t/p/w500"

app = Flask(__name__)
app.secret_key = "ThisIsASecretKey"
Bootstrap(app)
# specify the database file to be used with SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///top_movies.db"
# disable the deprecation warning in the console
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    # allow NULL ranking when creating a new entry, since it will be generated automatically
    ranking = db.Column(db.Integer, nullable=True)
    review = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)

    # set the string to return when using print() on the object
    def __repr__(self):
        return f"<Movie: {self.title} ({self.year})>"


class AddForm(FlaskForm):
    title = StringField("Movie Title", validators=[DataRequired()])
    year = IntegerField("Year", validators=[DataRequired()])
    description = StringField("Description", validators=[DataRequired()])
    rating = FloatField("Rating", validators=[DataRequired()])
    review = StringField("Review", validators=[DataRequired()])
    img_url = StringField("Image URL", validators=[DataRequired(), URL()])
    submit = SubmitField('Submit')


class AddFromTMDBForm(FlaskForm):
    title = StringField("Add Movie From TMDB", validators=[DataRequired()])
    submit = SubmitField('Submit')


class EditForm(FlaskForm):
    rating = FloatField("Your Rating (out of 10, e.g. 8.5)", validators=[DataRequired()])
    review = StringField("Your Review", validators=[DataRequired()])
    submit = SubmitField('Submit')


# create the initial database
# db.create_all()


def check_rating(raw_rating):
    """Checks whether a STR is a number and returns a FLOAT or NONE."""
    try:
        print(raw_rating)
        rating = float(raw_rating)
    except ValueError:
        # to avoid using NULL, set the value to 0.0 instead
        return 0.0
    except TypeError:
        return 0.0
    else:
        return round(rating, 1)


@app.route("/")
def home():
    # query the DB and get the results ordered by rating
    all_movies = Movie.query.order_by(Movie.rating).limit(TOP_LIMIT).all()
    # generate the ranking based on rating
    for i in range(len(all_movies)):
        all_movies[i].ranking = len(all_movies) - i
    db.session.commit()
    return render_template("index.html", movies=all_movies)


@app.route("/edit", methods=["GET", "POST"])
def edit_rating():
    form = EditForm()
    movie_id = request.args.get("id")
    # find the movie in the DB, returns None in case it doesn't exist
    movie = Movie.query.get(movie_id)
    if movie is not None and request.method == "POST":
        # get the fields from the form and update the DB
        movie.rating = check_rating(form.rating.data)
        movie.review = form.review.data
        db.session.commit()
        # redirect to the main page
        return redirect("/")
    return render_template("edit.html", form=form)


@app.route("/add", methods=["GET", "POST"])
def add_movie():
    form = AddForm()
    if request.method == "POST":
        # retrieve the contents of the form an create a new movie object
        # just use None for the ranking
        new_movie = Movie(
            title=form.title.data,
            year=form.year.data,
            description=form.description.data,
            rating=check_rating(form.rating.data),
            ranking=None,
            review=form.review.data,
            img_url=form.img_url.data
        )
        db.session.add(new_movie)
        db.session.commit()
        # redirect to the main page
        return redirect("/")
    return render_template("add.html", form=form)


@app.route("/delete")
def delete_movie():
    movie_id = request.args.get("id")
    # find the book in the DB, and if it exists, delete it
    movie = Movie.query.get(movie_id)
    if movie is not None:
        db.session.delete(movie)
        db.session.commit()
    else:
        # just to have some feedback
        print(f"There is no movie matching the id {movie_id}.")
    return redirect("/")


@app.route("/find", methods=["GET", "POST"])
def find_movie():
    form = AddFromTMDBForm()
    if form.validate_on_submit():
        params = {
            "api_key": config.TMDB_API_KEY,
            "query": form.title.data
        }
        # look up the movie title on TMDB
        response = requests.get(url=TMDB_SEARCH_URL, params=params)
        response.raise_for_status()
        data = response.json()["results"]
        return render_template("select.html", options=data)
    return render_template("find.html", form=form)


@app.route("/tmdb")
def add_movie_from_tmdb():
    movie_api_id = request.args.get("id")
    if movie_api_id:
        url = f"{TMDB_INFO_URL}/{movie_api_id}"
        params = {
            "api_key": config.TMDB_API_KEY,
            "language": "en-US"
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        # use placeholder values for rating and review, they have to be manually edited
        new_movie = Movie(
            title=data["title"],
            year=data["release_date"].split("-")[0],
            description=data["overview"],
            rating=0,
            ranking=None,
            review="",
            img_url=f"{TMDB_IMAGE_URL}{data['poster_path']}"
        )
        db.session.add(new_movie)
        db.session.commit()
        return redirect("/")


if __name__ == '__main__':
    app.run(debug=True)
