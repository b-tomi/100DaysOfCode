# Flask Higher Lower Game

import random

from flask import Flask

NUM_FROM = 1
NUM_TO = 10

# set FLASK_APP environment variable
# e.g. "set FLASK_APP=main.py" (or the corresponding command on other systems)
app = Flask(__name__)


def get_number():
    """Returns a random INT within the defined range."""
    return random.randint(NUM_FROM, NUM_TO)


def reset_game():
    """Resets the game to initial state."""
    params["secret_number"] = get_number()
    params["guess_count"] = 0
    params["game_over"] = False


@app.route('/')
def start():
    # reset the game at the start and after it's over
    if params["game_over"]:
        reset_game()
    return f'<h1 style="color: #2C3A47">I\'m thinking of a number between {NUM_FROM} and {NUM_TO}.</h1>' \
           '<img src="https://media.giphy.com/media/l3nWhI38IWDofyDrW/giphy.gif" alt="Thinking animation">' \
           '<p>Enter your guess to the end of website address, e.g. /5 to guess "5".</p>'


@app.route('/reset')
def reset():
    # reset the game at any time
    reset_game()
    return '<h2 style="color: #2C3A47">The secret number has been reset.</h2>'


@app.route('/<int:guess>')
def evaluate_guess(guess):
    if params["game_over"]:
        # this will also get displayed if the user tries to guess before "initializing" the game
        # e.g. without visiting the main page (or /reset)
        return f'<h2 style="color: #B33771">The game is already over!</h2>' \
               f'<p>Access the main page or /reset to reset the game if you want to play again.</p>'
    else:
        params["guess_count"] += 1
        # exclude invalid guesses, but still count them as a "guess"
        # anything other than a number should return a "Not Found" page
        if guess < NUM_FROM or guess > NUM_TO:
            return f'<h2 style="color: #F97F51">Invalid guess!</h2>' \
                   f'<p>The secret number is between {NUM_FROM} and {NUM_TO}.</p>'
        elif guess == params["secret_number"]:
            params["game_over"] = True
            return f'<h2 style="color: #EAB543">Correct!</h2>' \
                   f'<img src="https://media.giphy.com/media/9xt1MUZqkneFiWrAAD/giphy.gif" alt="Winner animation">' \
                   f'<p>Congratulations! It took you {params["guess_count"]} guesses.</p>' \
                   f'<p>Access the main page or /reset to reset the game if you want to play again.</p>'
        elif guess < params["secret_number"]:
            return f'<h2 style="color: #58B19F">Too low!</h2>' \
                   f'<img src="https://media.giphy.com/media/jD4DwBtqPXRXa/giphy.gif" alt="Too low animation">'
        else:
            return f'<h2 style="color: #3B3B98">Too high!</h2>' \
                   f'<img src="https://media.giphy.com/media/73h3LBWraONTW/giphy.gif" alt="Too high animation">'


# start with a "game over" state, to force the user to initialize (or reset) the game before accepting guesses
params = {
    "secret_number": 0,
    "guess_count": 0,
    "game_over": True
}

if __name__ == "__main__":
    # enable debug mode (also enables auto-reload)
    app.run(debug=True)
