import turtle

MOVE_DISTANCE = 20


class Paddle(turtle.Turtle):
    def __init__(self, side=""):
        """Creates a paddle. Defaults to the right side, unless "left" is specified."""
        super().__init__()
        # calculate from the screen size, offset by 5% from the edge
        self.x_pos = int(self.getscreen().window_width() * 45 / 100)
        # multiply by -1 to get the left paddle
        if side == "left":
            self.x_pos *= -1
        self.shape("square")
        self.color("white")
        # default size is 20x20, this will make it 20x100
        self.shapesize(stretch_len=5)
        self.penup()
        self.speed(0)
        # face to the to the top of the screen, so we can use .forward() and .backward()
        self.setheading(90)
        # start in the middle, so y_pos=0
        self.setpos(self.x_pos, 0)

    def move_up(self):
        """Moves the paddle up."""
        # simpler to just make use of the inherited methods
        self.forward(MOVE_DISTANCE)

    def move_down(self):
        """Moves the paddle down."""
        self.backward(MOVE_DISTANCE)
