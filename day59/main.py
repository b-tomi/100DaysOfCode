# Blog Capstone Project Part 2

import datetime as dt

from flask import Flask, render_template
import requests

from post import Post

# extended dummy blog post data
JSON_URL = "https://api.npoint.io/fce4df05100e25cfbc7f"

app = Flask(__name__)


def get_current_year():
    """Returns the current year as INT."""
    return dt.datetime.now().year


@app.route("/")
def home():
    return render_template("index.html", posts=all_posts, year=get_current_year())


@app.route("/about.html")
def about():
    return render_template("about.html", year=get_current_year())


@app.route("/contact.html")
def contact():
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
