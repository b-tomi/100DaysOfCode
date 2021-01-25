# Blog Capstone Project Part 1

import datetime as dt

from flask import Flask, render_template
import requests

from post import Post

# dummy blog post data
JSON_URL = "https://api.npoint.io/9b81097a622d688871fa"

app = Flask(__name__)


def get_current_year():
    """Returns the current year as INT."""
    # get the current year to display in the footer
    return dt.datetime.now().year


@app.route("/")
def home():
    return render_template("index.html", posts=all_posts, year=get_current_year())


@app.route("/blog/<int:blog_id>")
def get_blog(blog_id):
    # for now, just a crude, quick way to find the post to display
    current_post = None
    for post in all_posts:
        if post.id == blog_id:
            current_post = post
            break
    # when trying to access a non-existing blog_id, it will display the page without the post content elements
    return render_template("post.html", post=current_post, year=get_current_year())


# get the test blog posts
response = requests.get(JSON_URL)
response.raise_for_status()
blog_posts = response.json()
# store posts as objects in a list
all_posts = []
for blog_post in blog_posts:
    all_posts.append(Post(blog_post["id"], blog_post["title"], blog_post["subtitle"], blog_post["body"]))

if __name__ == "__main__":
    app.run(debug=True)
