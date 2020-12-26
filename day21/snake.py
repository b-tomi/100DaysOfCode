import turtle

START_POSITIONS = [(0, 0), (-20, 0), (-40, 0)]
MOVE_DISTANCE = 20
UP = 90
DOWN = 270
LEFT = 180
RIGHT = 0


class Snake:
    def __init__(self):
        self.segments = []
        self.create_snake()
        # to make the "head" easier to access
        self.head = self.segments[0]
        self.length = len(self.segments)

    def create_snake(self):
        """Creates a new snake made up by squares at locations set in the START_POSITIONS list."""
        for i in range(len(START_POSITIONS)):
            self.add_segment(i)
            # set the positions as defined
            self.segments[i].setpos(START_POSITIONS[i])

    def add_segment(self, i):
        # a simple append works for at beginning too, since we're starting with an empty list
        self.segments.append(turtle.Turtle(shape="square"))
        self.segments[i].color("white")
        self.segments[i].penup()

    def extend(self):
        # the index of the new segment is equal to the current number of segments
        self.add_segment(self.length)
        # set the position of the new segment to the position of the previous one
        self.segments[self.length].setpos(self.segments[self.length - 1].pos())
        self.length += 1

    def move(self):
        """Moves the snake forward by the distance set in MOVE_DISTANCE."""
        # start from the end, go backwards by 1 with each step, up to the second segment (i.e. i = 1)
        for i in range(self.length - 1, 0, -1):
            # set the new location to the position of the previous segment
            self.segments[i].setx(self.segments[i - 1].xcor())
            self.segments[i].sety(self.segments[i - 1].ycor())
        # move the first segment in whatever direction it's facing
        self.head.forward(MOVE_DISTANCE)

    def up(self):
        """Turn the snake towards the top of the screen."""
        # to avoid turning backwards
        if self.head.heading() != DOWN:
            self.head.setheading(UP)

    def down(self):
        """Turn the snake towards the bottom of the screen."""
        if self.head.heading() != UP:
            self.head.setheading(DOWN)

    def left(self):
        """Turn the snake towards the left side of the screen."""
        if self.head.heading() != RIGHT:
            self.head.setheading(LEFT)

    def right(self):
        """Turn the snake towards the right side of the screen."""
        if self.head.heading() != LEFT:
            self.head.setheading(RIGHT)
