import turtle

FONT = ("Arial", 20, "normal")


class Scoreboard(turtle.Turtle):
    def __init__(self):
        """Creates a scoreboard and places it on the screen."""
        super().__init__()
        self.color("silver")
        self.hideturtle()
        self.speed(0)
        self.penup()
        # the x coordinate can be a static 0 so it's centered
        self.setpos(0, int(self.getscreen().window_height() / 2 - 30))
        # set the initial score
        self.score = 0
        self.update()

    def update(self):
        """Updates the scoreboard."""
        # clear this "turtle" object before updating it
        self.clear()
        self.write(f"Score: {self.score}", align="center", font=FONT)

    def add_one(self):
        """Increases score by 1 and updates the scoreboard."""
        self.score += 1
        self.update()

    def game_over(self):
        """Displays "GAME OVER" message."""
        # place it to the middle of the screen
        self.setpos(0, 0)
        self.write("GAME OVER", align="center", font=FONT)
