# Blog Capstone Project for Heroku

# Note: login credentials for user #1
# myemail@mydomain.zyx
# mypassword

import datetime as dt
import smtplib
from functools import wraps

from flask import Flask, render_template, request, redirect, flash, abort
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_ckeditor import CKEditor
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_gravatar import Gravatar

import config
import forms

# notification settings, unchanged from Day 60
SMTP_SERVER = "smtp.mailtrap.io"
SMTP_PORT = "2525"
SUBJECT_TEXT = "A Message from the Blog Capstone Project"
RECEIVER_NAME = "Anita Bath"
RECEIVER_ADDRESS = "myemail@mydomain.zyx"

app = Flask(__name__)
app.config["SECRET_KEY"] = config.SECRET_KEY
ckeditor = CKEditor(app)
Bootstrap(app)

# Gravatar setup
gravatar = Gravatar(app, size=100, rating='g', default='retro', force_default=False, force_lower=False,
                    use_ssl=False, base_url=None)

# DB setup
app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Flask login manager
login_manager = LoginManager()
login_manager.init_app(app)


class BlogPost(db.Model):
    __tablename__ = "blog_posts"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    # set a foreign key for this field, id from the users table
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    # define the relationship with the users table
    author = relationship("User", back_populates="posts")
    img_url = db.Column(db.String(250), nullable=False)
    # define the relationship with the comments table
    comments = relationship("Comment", back_populates="parent_post")


class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    # set foreign keys
    post_id = db.Column(db.Integer, db.ForeignKey("blog_posts.id"))
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    # define the relationships with the other tables
    parent_post = relationship("BlogPost", back_populates="comments")
    comment_author = relationship("User", back_populates="comments")
    text = db.Column(db.Text, nullable=False)


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    # define the relationship with the blog_posts table
    posts = relationship("BlogPost", back_populates="author")
    # define the relationship with the comments table
    comments = relationship("Comment", back_populates="comment_author")


# create the tables in the DB
db.create_all()


def get_current_year():
    """Returns the current year as INT."""
    return dt.datetime.now().year


def get_current_date():
    """Returns the current date as a STR."""
    return dt.datetime.now().strftime("%B %d, %Y")


def send_email(message):
    """Takes a DICT with the details and sends an email to the defined address."""
    # format the email
    sender = f"{message['name']} <{message['email']}>"
    receiver = f"{RECEIVER_NAME} <{RECEIVER_ADDRESS}>"
    body = f"Subject: {SUBJECT_TEXT}\nTo: {receiver}\nFrom: {sender}\n\n" \
           f"{message['message']}\n\n" \
           f"From:\nName: {message['name']}\nEmail: {message['email']}\nPhone: {message['phone']}"
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(config.SMTP_LOGIN, config.SMTP_PASS)
            server.sendmail(sender, receiver, body)
    except smtplib.SMTPServerDisconnected as ex:
        print(ex)
        print("Make sure the SMTP_LOGIN and SMTP_PASS credentials have been set correctly in config.py.")
        return False
    else:
        # just to have some feedback
        print(f"A message was sent to {RECEIVER_ADDRESS}.")
        return True


# admin_only decorator
def admin_only(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # the admin is the first entry in the users table
        # if not admin, abort the request
        if not current_user.is_authenticated or current_user.id != 1:
            return abort(403)
        # if admin, continue to the requested route
        return func(*args, **kwargs)
    return wrapper


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/")
def home():
    all_posts = BlogPost.query.all()
    return render_template("index.html", posts=all_posts, year=get_current_year(),
                           logged_in=current_user.is_authenticated)


@app.route("/post/<int:blog_id>", methods=["GET", "POST"])
def show_post(blog_id):
    comment_form = forms.CommentForm()
    blog_post = BlogPost.query.get(blog_id)
    if comment_form.validate_on_submit():
        if not current_user.is_authenticated:
            flash("You need to login or register to comment.")
            return redirect("/login")
        new_comment = Comment(
            text=comment_form.comment.data,
            comment_author=current_user,
            parent_post=blog_post
        )
        db.session.add(new_comment)
        db.session.commit()
        # clear the comment field
        comment_form.comment.data = ""
    if blog_post:
        return render_template("post.html", post=blog_post, form=comment_form, year=get_current_year(),
                               logged_in=current_user.is_authenticated)
    # if such post id doesn't exist
    return redirect("/")


@app.route("/about")
def about():
    return render_template("about.html", year=get_current_year(), logged_in=current_user.is_authenticated)


@app.route("/contact.html", methods=["GET", "POST"])
def contact():
    # display a different page after a message was submitted
    if request.method == "POST":
        message = {
            "name": request.form["name"],
            "email": request.form["email"],
            "phone": request.form["phone"],
            "message": request.form["message"]
        }
        # try to send the message
        if send_email(message):
            status = "Success!"
            text = "Your message has been sent."
        else:
            status = "Something went wrong."
            text = "The message could not be sent."
        # display the status page
        return render_template("message.html", status=status, text=text, year=get_current_year(),
                               logged_in=current_user.is_authenticated)
    return render_template("contact.html", year=get_current_year(), logged_in=current_user.is_authenticated)


# using the new decorator
@app.route("/new-post", methods=["GET", "POST"])
@admin_only
def add_post():
    post_form = forms.CreatePostForm()
    if post_form.validate_on_submit():
        new_post = BlogPost(
            title=post_form.title.data,
            subtitle=post_form.subtitle.data,
            date=get_current_date(),
            body=post_form.body.data,
            author=current_user,
            img_url=post_form.img_url.data
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect("/")
    return render_template("make-post.html", heading="New Post", form=post_form, year=get_current_year(),
                           logged_in=current_user.is_authenticated)


@app.route("/edit/<int:blog_id>", methods=["GET", "POST"])
@admin_only
def edit_post(blog_id):
    # find the blog in the DB
    post = BlogPost.query.get(blog_id)
    if post:
        # if the post exists, fill in the fields in the form
        post_form = forms.CreatePostForm(
            title=post.title,
            subtitle=post.subtitle,
            img_url=post.img_url,
            author=current_user,
            body=post.body
        )
        # update the DB
        if post_form.validate_on_submit():
            post.title = post_form.title.data
            post.subtitle = post_form.subtitle.data
            post.img_url = post_form.img_url.data
            post.body = post_form.body.data
            db.session.commit()
            # redirect to the post page
            return redirect(f"/post/{post.id}")
        return render_template("make-post.html", heading="Edit Post", form=post_form, year=get_current_year(),
                               logged_in=current_user.is_authenticated)
    # if no such post exists, just redirect to the main page
    return redirect("/")


@app.route("/delete/<int:blog_id>", methods=["GET", "POST"])
@admin_only
def delete_post(blog_id):
    post = BlogPost.query.get(blog_id)
    # if such posts exists, delete it
    if post:
        db.session.delete(post)
        db.session.commit()
    # redirect to the main page
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    register_form = forms.RegisterForm()
    if register_form.validate_on_submit():
        # check if email already if DB
        found_user = User.query.filter_by(email=register_form.email.data).first()
        if found_user:
            # set message to display and redirect to the login page
            flash("You've already signed up with that email, log in instead!")
            return redirect("/login")
        else:
            # generate password hash
            password_hash = generate_password_hash(password=register_form.password.data,
                                                   method="pbkdf2:sha256", salt_length=8)
            new_user = User(
                email=register_form.email.data,
                password=password_hash,
                name=register_form.name.data
            )
            db.session.add(new_user)
            db.session.commit()
            # log in as the new user
            login_user(new_user)
            return redirect("/")
    return render_template("register.html", form=register_form, year=get_current_year(),
                           logged_in=current_user.is_authenticated)


@app.route("/login", methods=["GET", "POST"])
def login():
    login_form = forms.LoginForm()
    if login_form.validate_on_submit():
        # try to find the email in the DB
        found_user = User.query.filter_by(email=login_form.email.data).first()
        if found_user:
            # verify the password
            verified = check_password_hash(pwhash=found_user.password, password=login_form.password.data)
            if verified:
                # use the Flask login manager
                login_user(found_user)
                return redirect("/")
            # incorrect password
            else:
                flash("Password incorrect, please try again.")
                return redirect("/login")
        # if email does not exist in the DB
        else:
            flash("Email not found, please try again.")
            return redirect("/login")
    return render_template("login.html", form=login_form, year=get_current_year(),
                           logged_in=current_user.is_authenticated)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


if __name__ == "__main__":
    app.run()
