import turtle
import math
import random

BALL_MOVEMENT = 20


class Ball(turtle.Turtle):
    def __init__(self):
        super().__init__()
        # "move speed", actually just used as the wait time
        self.move_speed = 0.1
        self.shape("circle")
        self.color("white")
        self.penup()
        self.speed(0)
        # calculate the initial angle based on the sides in a right triangle
        a = self.getscreen().window_height() / 2
        b = self.getscreen().window_width() / 2
        c = math.sqrt(a*a + b*b)
        # convert radians to whole degrees
        self.initial_angle = int(math.degrees(math.asin(a / c)))
        # on second thought, it's probably better to offset it by a little, rather than aiming straight for the corner
        self.setheading(self.initial_angle + random.randint(15, 30))
        self.setpos(0, 0)

    def move(self):
        """Moves the ball in its current heading."""
        self.forward(BALL_MOVEMENT)

    def wall_bounce(self):
        """Bounces the ball from the top or bottom edge of the screen."""
        self.setheading(360 - self.heading())

    def paddle_bounce(self):
        """Bounces the ball from the top or bottom edge of the screen."""
        # decrease the wait time with each bounce
        self.move_speed *= 0.9
        self.setheading(180 - self.heading())

    def reset_position(self, side=""):
        """Resets the ball. Defaults to start moving right, unless "left" is specified."""
        self.move_speed = 0.1
        if side == "left":
            self.setheading(180 + self.initial_angle + random.randint(15, 30))
        else:
            self.setheading(self.initial_angle + random.randint(15, 30))
        self.setpos(0, 0)
