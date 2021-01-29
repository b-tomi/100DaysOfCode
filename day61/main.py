# Flask-WTF Forms

from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length
from flask_bootstrap import Bootstrap

# fake credentials for the form
SECRET_EMAIL = "myemail@mydomain.zyx"
SECRET_PASSWORD = "123123"

app = Flask(__name__)
# random string, needed for CSRF
app.secret_key = "ThisIsASecretKey"
# needed for flask_bootstrap
Bootstrap(app)


class LoginForm(FlaskForm):
    # parameters for the form, with specific requirements for each field
    email = StringField(label="Email", validators=[DataRequired(), Email()])
    password = PasswordField(label="Password", validators=[DataRequired(), Length(min=6)])
    submit = SubmitField(label="Submit")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    # evaluate the submitted credentials
    if form.validate_on_submit():
        if form.email.data == SECRET_EMAIL and form.password.data == SECRET_PASSWORD:
            return render_template("success.html")
        else:
            return render_template("denied.html")
    return render_template("login.html", login_form=form)


@app.route("/success")
def success():
    return render_template("success.html")


if __name__ == '__main__':
    app.run(debug=True)
