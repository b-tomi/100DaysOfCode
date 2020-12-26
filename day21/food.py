import turtle
import random


class Food(turtle.Turtle):
    def __init__(self):
        """Creates a new fruit and places it to a random location in the screen."""
        super().__init__()
        # save the screen dimensions into variables for simpler access
        self.screen_width = self.getscreen().window_width()
        self.screen_height = self.getscreen().window_height()
        self.shape("circle")
        # this should result in a 10x10
        self.shapesize(stretch_len=0.5, stretch_wid=0.5)
        self.color("violet")
        # speed 0 is equal to "fastest"
        self.speed(0)
        self.penup()
        self.respawn()

    def respawn(self):
        """Moves the fruit to a random location on the screen."""
        # assumes sensible dimensions, makes the coordinates multiplies of the snake's width (i.e. 20)
        # so the object is always centered in a particular grid position
        x_range = int((self.screen_width - 10) / 40)
        y_range = int((self.screen_height - 10) / 40)
        self.setpos(random.randint(-x_range, x_range) * 20, random.randint(-y_range, y_range) * 20)
