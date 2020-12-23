# Hirst Painting

import turtle
import random

import colorgram


def paint(cols, rows):
    """Takes number of columns and rows as INT and paints a dot of random color at each position."""
    # extract the colors
    extracted_colors = colorgram.extract("image.jpg", 30)
    color_list = []
    for col in extracted_colors:
        color_list.append(col.rgb)

    # set up the brush
    brush = turtle.Turtle()
    brush.shape("circle")
    # from a range of 0-10, 7 seems reasonable
    brush.speed(7)
    brush.penup()
    brush.hideturtle()

    # initial position
    width = screen.window_width()
    height = screen.window_height()
    # offset between the dots
    x_offset = int(width / cols)
    y_offset = int(height / rows)
    # the coordinates go from -300 to +300 (i.e. half the height or width)
    # initial offset by half of the distance between each dot
    x_pos = int(width / -2 + x_offset / 2)
    y_pos = int(height / -2 + y_offset / 2)
    for _ in range(0, rows):
        for __ in range(0, cols):
            brush.setx(x_pos)
            brush.sety(y_pos)
            brush.dot(30, random.choice(color_list))
            x_pos += x_offset
        # reset the x position to the first column
        x_pos = int(width / -2 + x_offset / 2)
        y_pos += y_offset


# set the color mode to accept RGB values instead of color name strings
turtle.colormode(255)
# set up the screen
screen = turtle.Screen()
screen.title("Hirst-like art")
# possible to modify the canvas size
screen.setup(width=800, height=600)

# paint the image, the number of columns and rows can be any (reasonable) positive INT
paint(cols=6, rows=4)

# make the window wait for a click, rather than closing immediately after completion
screen.exitonclick()
