import turtle


STARTING_POSITION = (0, -280)
MOVE_DISTANCE = 10
FINISH_LINE_Y = 280


class Player(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.shape("turtle")
        self.color("saddlebrown")
        self.penup()
        self.speed(0)
        # set heading toward top of the screen, so it's possible to use .forward()
        self.setheading(90)
        self.reset_position()

    def reset_position(self):
        """Resets the player's position."""
        self.setpos(STARTING_POSITION)

    def move_up(self):
        """Moves the player forward by the defined distance."""
        self.forward(MOVE_DISTANCE)

    def reached_finish(self):
        """Returns TRUE if the player has reached the finish line."""
        if self.ycor() > FINISH_LINE_Y:
            return True
        return False
