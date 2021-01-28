# Flask HTML Forms

import datetime as dt
import smtplib

from flask import Flask, render_template, request
import requests

import config
from post import Post

# extended dummy blog post data
JSON_URL = "https://api.npoint.io/fce4df05100e25cfbc7f"
# default Mailtrap server settings
SMTP_SERVER = "smtp.mailtrap.io"
SMTP_PORT = "2525"
# not really necessary, but might as well format the email properly
SUBJECT_TEXT = "A Message from the Blog Capstone Project"
# fake contact info from Day 47
RECEIVER_NAME = "Anita Bath"
RECEIVER_ADDRESS = "myemail@mydomain.zyx"

app = Flask(__name__)


def get_current_year():
    """Returns the current year as INT."""
    return dt.datetime.now().year


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


@app.route("/")
def home():
    return render_template("index.html", posts=all_posts, year=get_current_year())


@app.route("/about.html")
def about():
    return render_template("about.html", year=get_current_year())


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
        return render_template("message.html", status=status, text=text)
    # display the regular contact page
    else:
        return render_template("contact.html", year=get_current_year())


@app.route("/post/<int:blog_id>")
def get_post(blog_id):
    id_exists = False
    current_post = None
    for post in all_posts:
        if post.id == blog_id:
            current_post = post
            id_exists = True
            # no need to check the rest
            break
    # just show the main page for non-existing blog_id's, rather than a semi-broken post.html
    if id_exists:
        return render_template("post.html", post=current_post, year=get_current_year())
    else:
        return render_template("index.html", posts=all_posts, year=get_current_year())


# get the test blog posts
response = requests.get(JSON_URL)
response.raise_for_status()
blog_posts = response.json()
# store posts as objects in a list
all_posts = []
for blog_post in blog_posts:
    all_posts.append(Post(blog_post["id"], blog_post["author"], blog_post["date"], blog_post["title"],
                          blog_post["subtitle"], blog_post["image_url"], blog_post["body"]))

if __name__ == "__main__":
    app.run(debug=True)
