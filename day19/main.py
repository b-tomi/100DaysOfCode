# Turtle Race

import turtle
import random


# initial setup, possible to modify (using reasonable) values
# dimensions of the window
FRAME_WIDTH = 600
FRAME_HEIGHT = 400
# the number of colors determines the number of racers
COLOR_LIST = ["red", "orange", "yellow", "green", "blue", "purple"]
# a positive INT to set the speed, between like 5 and 15 is a reasonable value
SPEED = 10

# screen setup
screen = turtle.Screen()
screen.setup(width=FRAME_WIDTH, height=FRAME_HEIGHT)
screen.title("Turtle Race")

# find the location of the first racer, count an extra one so there is some offset from the edge
offset = int(FRAME_HEIGHT / (len(COLOR_LIST) + 1))
# 12 should be enough offset from the vertical edge of the window
start_x = FRAME_WIDTH / -2 + 12
# the vertical position depends on window size and number of racers
start_y = int(FRAME_HEIGHT / -2 + offset)

# initialize all turtles, based on the number of colors
racers = len(COLOR_LIST)
racer_list = []
for i in range(racers):
    # just add a object to the list, no need to assign them to specific variables
    racer_list.append(turtle.Turtle(shape="turtle"))
    racer_list[i].hideturtle()
    racer_list[i].color(COLOR_LIST[i])
    racer_list[i].penup()
    racer_list[i].setx(start_x)
    racer_list[i].sety(start_y + offset * i)
    racer_list[i].showturtle()

# ask for input, for simplicity, accept whatever is entered
guess = screen.textinput(title="Make Your Bet", prompt="Which turtle will win the race? Enter a color:")

# the finish line, offset from the right edge
end_x = FRAME_WIDTH / 2 - 25
race_is_over = False
winner = ""
# the race loop
while not race_is_over:
    # could have just used "for racer in racer_list:", but this way is more consistent with the above
    # and makes retrieving the winner's color (a tiny bit) simpler
    for i in range(racers):
        # starting randint from 1, so they move at least a little every iteration
        racer_list[i].setx(racer_list[i].xcor() + random.randint(1, SPEED))
        # check for win condition
        if racer_list[i].xcor() >= end_x:
            race_is_over = True
            # retrieve the winner's color
            winner = COLOR_LIST[i]

print(f"The winner was {winner}.")
if guess.lower() == winner.lower():
    print("You won the bet!")
else:
    # lose even if they enter an invalid input, e.g. a color not in the list
    print("Sorry, you lost.")

# wait for a click once the race is over, rather than just closing the window
screen.exitonclick()
