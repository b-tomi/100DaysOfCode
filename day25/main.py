# U.S. States Game

import turtle

import pandas as pd

BG_IMAGE = "blank_states_img.gif"
INPUT_CSV_FILE = "50_states.csv"
OUTPUT_CSV_FILE = "states_to_learn.csv"
FONT = ("Arial", 10, "normal")


def add_label(entry):
    """Creates a new label matching the provided text and position."""
    new_turtle = turtle.Turtle()
    new_turtle.hideturtle()
    new_turtle.penup()
    new_turtle.speed(0)
    new_turtle.setx(entry.x.item())
    new_turtle.sety(entry.y.item())
    new_turtle.write(entry.state.item(), align="left", font=FONT)


# screen setup
screen = turtle.Screen()
# matching the size of the image to avoid white borders
screen.setup(width=725, height=491)
screen.title("U.S. States Game")
screen.bgpic(BG_IMAGE)

# load the dataframe
df = pd.read_csv(INPUT_CSV_FILE)
all_states = df.state.tolist()
# to avoid hard-coding the total count
states_count = len(all_states)
revealed_states = []

# set initial texts for the prompt
title_text = "Guess the state"
prompt_text = "Enter a state name"

game_is_over = False
while not game_is_over:
    answer = screen.textinput(title=title_text, prompt=prompt_text).title()
    # include a way to exit at any time
    if answer == "Exit":
        game_is_over = True
    elif answer in all_states and answer not in revealed_states:
        # using a function to improve readability
        add_label(df[df.state == answer])
        revealed_states.append(answer)

    # update the prompt labels
    revealed_count = len(revealed_states)
    if revealed_count > 0:
        title_text = f"{revealed_count}/{states_count} states correct"
        # not really necessary to update this more than once, but to keep things simple...
        prompt_text = "Enter another state name"

    # "win" condition
    if revealed_count == states_count:
        game_is_over = True

# evaluate the final "score"
if len(revealed_states) == 0:
    # for simplicity, just a message in the console
    print("You didn't guess a single state.")
elif len(revealed_states) == states_count:
    print("Well done, you've entered all states.")
else:
    # if there were any missing states, save them into a new csv
    missed_states = []
    for state in all_states:
        if state not in revealed_states:
            missed_states.append(state)
    pd.DataFrame(missed_states).to_csv(OUTPUT_CSV_FILE)
    print(f"The {len(missed_states)} missing states have been saved to {OUTPUT_CSV_FILE}.")
