# Flask Name Card Website

from flask import Flask, render_template

# base template by @ajlkn from https://html5up.net/identity
# background image by Manuel Cosentino from https://unsplash.com/photos/n--CMLApjfI

# set FLASK_APP environment variable
# e.g. "set FLASK_APP=main.py" (or the corresponding command on other systems)
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


if __name__ == "__main__":
    # enable debug mode (also enables auto-reload)
    app.run(debug=True)
