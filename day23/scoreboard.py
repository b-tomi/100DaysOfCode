import turtle


FONT = ("Courier", 22, "normal")
POSITION = (-380, 250)


class Scoreboard(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.level = 1
        self.color("dimgray")
        self.hideturtle()
        self.speed(0)
        self.penup()
        self.setpos(POSITION)
        self.update()

    def update(self):
        """Updates the scoreboard."""
        self.clear()
        self.write(f"Level: {self.level}", align="left", font=FONT)

    def increase_level(self):
        """Increases the level by 1 and updates the scoreboard."""
        self.level += 1
        self.update()

    def game_over(self):
        """Displays the "GAME OVER" message."""
        self.setpos(0, 0)
        self.write("GAME OVER", align="center", font=FONT)
