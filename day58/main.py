# Flask TinDog

import datetime as dt
import random

from flask import Flask, render_template

import data

app = Flask(__name__)


def get_current_year():
    """Returns the current year as INT."""
    return dt.datetime.now().year


def get_testimonials():
    """Randomly selects two testimonials and returns them in a LIST."""
    # rather than having them hard-coded in the HTML, moved testimonials into a separate "database"
    # randomly select two to display
    return random.sample(data.testimonials_list, 2)


@app.route("/")
def home():
    return render_template("index.html", testimonials=get_testimonials(), year=get_current_year())


if __name__ == "__main__":
    app.run(debug=True)
