# Cafe & Wifi API

import random

from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# API key for authentication used for the ADD and DELETE requests
SECRET_API_KEY = {"api-key": "ThisIsASecretKey"}

app = Flask(__name__)
# specify the database file to be used with SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_dict(self):
        # using dictionary comprehension, return key-value pairs
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


def to_bool(raw_str):
    """Takes a STR and returns a BOOL."""
    if raw_str.lower() == "true":
        return True
    elif raw_str.lower() == "false":
        return False
    # in case 0 or 1 were provided
    else:
        try:
            num = int(raw_str)
        # return False for anything that's not "1", just to be safe
        except ValueError:
            return False
        else:
            return bool(num)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/random")
def get_random():
    all_cafes = Cafe.query.all()
    random_cafe = random.choice(all_cafes)
    # return as JSON
    return jsonify(cafe=random_cafe.to_dict())


@app.route("/all")
def get_all():
    all_cafes = Cafe.query.all()
    # using list comprehension
    return jsonify(cafes=[cafe.to_dict() for cafe in all_cafes])


@app.route("/search")
def search():
    # check if location data was provided
    if "loc" in request.args:
        location = request.args.get("loc").capitalize()
        matches = Cafe.query.filter_by(location=location).all()
        if matches:
            return jsonify(cafes=[cafe.to_dict() for cafe in matches])
        else:
            return jsonify(error={"Not Found": "Sorry, we don't have a cafe at that location."})
    return jsonify(error={"Invalid query": "No location was specified."})


@app.route("/add", methods=["POST"])
def add_cafe():
    # skipping checking whether the name is already in the DB
    # verify the authorization, it should be sent in the header
    if request.headers.get("api-key") == SECRET_API_KEY["api-key"]:
        new_cafe = Cafe(
            name=request.form.get("name"),
            map_url=request.form.get("map_url"),
            img_url=request.form.get("img_url"),
            location=request.form.get("loc"),
            seats=request.form.get("seats"),
            has_toilet=to_bool(request.form.get("toilet")),
            has_wifi=to_bool(request.form.get("wifi")),
            has_sockets=to_bool(request.form.get("sockets")),
            can_take_calls=to_bool(request.form.get("calls")),
            coffee_price=request.form.get("coffee_price")
        )
        db.session.add(new_cafe)
        db.session.commit()
        # return a confirmation
        return jsonify(response={"Success": "Successfully added the new cafe."})
    # return status code: 401 Unauthorized
    return jsonify(error={"Unauthorized": "You are not authorized to perform this operation."}), 401


@app.route("/update-price/<int:cafe_id>", methods=["PATCH"])
def update_cafe(cafe_id):
    # find the cafe in the DB, returns None in case it doesn't exist
    cafe = Cafe.query.get(cafe_id)
    # should evaluate as "truthy", unless None
    if cafe:
        # get the fields from the form and update the DB
        cafe.coffee_price = request.args.get("new_price")
        db.session.commit()
        # return HTTP response status code: 200 OK
        return jsonify(response={"Success": "Successfully updated the price."}), 200
    # return status code: 404 Not Found
    return jsonify(error={"Not Found": "There is no cafe with the provided id."}), 404


@app.route("/report-closed/<int:cafe_id>", methods=["DELETE"])
def remove_cafe(cafe_id):
    # verify the authorization, it should be sent in the header
    if request.headers.get("api-key") == SECRET_API_KEY["api-key"]:
        cafe = Cafe.query.get(cafe_id)
        if cafe:
            db.session.delete(cafe)
            db.session.commit()
            return jsonify(response={"Success": "Successfully removed the cafe."}), 200
        else:
            return jsonify(error={"Not Found": "There is no cafe with the provided id."}), 404
    # return status code: 401 Unauthorized
    return jsonify(error={"Unauthorized": "You are not authorized to perform this operation."}), 401


if __name__ == "__main__":
    app.run(debug=True)
