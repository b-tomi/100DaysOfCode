import turtle

FONT = ("Arial", 60, "normal")


class Scoreboard(turtle.Turtle):
    def __init__(self):
        """Creates a scoreboard and places it on the screen."""
        super().__init__()
        self.color("silver")
        self.hideturtle()
        self.speed(0)
        self.penup()
        # find the y coordinate, the x will be static
        self.y_pos = int(self.getscreen().window_height() / 2 - 100)
        # set the initial scores
        self.left_score = 0
        self.right_score = 0
        self.update()

    def update(self):
        """Updates the scoreboard."""
        self.clear()
        self.setpos(-80, self.y_pos)
        self.write(self.left_score, align="center", font=FONT)
        self.setpos(80, self.y_pos)
        self.write(self.right_score, align="center", font=FONT)

    def add_one_left(self):
        """Increases the score of the left player by 1 and updates the scoreboard."""
        self.left_score += 1
        self.update()

    def add_one_right(self):
        """Increases the score of the right player by 1 and updates the scoreboard."""
        self.right_score += 1
        self.update()

    def game_over(self):
        self.setpos(0, -self.y_pos)
        self.write("GAME OVER", align="center", font=FONT)
