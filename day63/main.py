# Virtual Bookshelf

from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# specify the database file to be used with SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///new-books-collection.db"
# disable the deprecation warning in the console
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # no need for the title to be UNIQUE
    title = db.Column(db.String(250), nullable=False)
    author = db.Column(db.String(250), nullable=False)
    # allow None as a value for the rating
    rating = db.Column(db.Float, nullable=True)

    # optional, set the string to return when using print() on the object
    def __repr__(self):
        return f"<Book: {self.title} by {self.author}>"


# used to create the initial database, no need to execute more than once
# db.create_all()


def check_rating(raw_rating):
    """Checks whether a STR is a number and returns a FLOAT or NONE."""
    try:
        rating = float(raw_rating)
    except ValueError:
        # set the value to null
        return None
    else:
        # to keep things simple, skip checking whether the value is within a certain range
        return round(rating, 1)


@app.route("/")
def home():
    # read all records
    all_books = db.session.query(Book).all()
    return render_template("index.html", books=all_books, count=len(all_books))


@app.route("/add", methods=["GET", "POST"])
def add_book():
    if request.method == "POST":
        # make sure "rating" is an acceptable value
        rating = check_rating(request.form["rating"])
        # add the book to the database through SQLAlchemy
        # not necessary to provide an id number, the PK gets auto-incremented
        new_book = Book(title=request.form["title"], author=request.form["author"], rating=rating)
        db.session.add(new_book)
        db.session.commit()
        # redirect to the main page
        return redirect("/")
    return render_template("add.html")


@app.route("/edit", methods=["GET", "POST"])
def edit_rating():
    # retrieve the id from the request
    book_id = request.args.get("id")
    # find the book in the DB
    book = Book.query.get(book_id)
    if book is not None and request.method == "POST":
        # check the input and update the rating
        book.rating = check_rating(request.form["new_rating"])
        db.session.commit()
        # redirect to the main page
        return redirect("/")
    return render_template("edit.html", book=book)


@app.route("/delete")
def delete_book():
    book_id = request.args.get("id")
    # find the book in the DB, and if it exists, delete it
    book = Book.query.get(book_id)
    if book is not None:
        db.session.delete(book)
        db.session.commit()
    # redirect to the main page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
