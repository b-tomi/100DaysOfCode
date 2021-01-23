# Flask Quickstart

from flask import Flask

# set FLASK_APP environment variable
# e.g. "set FLASK_APP=main.py" (or the corresponding command on other systems)
app = Flask(__name__)


# using decorators
# displayed when accessing http://127.0.0.1:5000
@app.route("/")
def hello():
    return "Hello, World!"


# displayed when accessing http://127.0.0.1:5000/bye
@app.route("/bye")
def say_bye():
    return "Bye!"


if __name__ == "__main__":
    app.run()
