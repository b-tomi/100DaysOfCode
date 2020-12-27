# Pong

import turtle
import time

from paddle import Paddle
from ball import Ball
from scoreboard import Scoreboard


# dimensions for the game window
WIDTH = 800
HEIGHT = 600
# calculate the borders, minus a little for tolerance
x_range = int(WIDTH / 2) - 55
y_range = int(HEIGHT / 2) - 20

# screen setup
screen = turtle.Screen()
screen.setup(width=WIDTH, height=HEIGHT)
screen.title("Pong")
screen.bgcolor("black")
# disable automatic screen updates
screen.tracer(0)

# setup
scoreboard = Scoreboard()
right_paddle = Paddle()
left_paddle = Paddle(side="left")
ball = Ball()

# controls setup
screen.listen()
screen.onkey(right_paddle.move_up, "Up")
screen.onkey(right_paddle.move_down, "Down")
screen.onkey(left_paddle.move_up, "w")
screen.onkey(left_paddle.move_down, "s")

game_is_over = False
while not game_is_over:
    screen.update()
    time.sleep(ball.move_speed)
    ball.move()

    # detect collision with top and bottom walls
    if ball.ycor() < -y_range or ball.ycor() > y_range:
        ball.wall_bounce()

    # detect collision with each paddle
    # ball.distance() is unreliable since it measures from the center point of the paddle
    # better to check the coordinates separately
    if x_range - ball.xcor() < 10 and ball.xcor() < x_range + 20 and abs(right_paddle.ycor() - ball.ycor()) < 50:
        ball.paddle_bounce()
    elif abs(x_range + ball.xcor()) < 10 and ball.xcor() > -x_range - 20 and abs(left_paddle.ycor() - ball.ycor()) < 50:
        ball.paddle_bounce()

    # detect if ball completely passes the right or left side
    if ball.xcor() > WIDTH / 2 + 30:
        # update score
        scoreboard.add_one_left()
        # reset ball position and heading
        ball.reset_position()
    elif ball.xcor() < WIDTH / -2 - 30:
        scoreboard.add_one_right()
        # reset ball position and set the heading to the left
        ball.reset_position(side="left")

    # game over condition
    if scoreboard.left_score == 5 or scoreboard.right_score == 5:
        game_is_over = True

# display the game over message
scoreboard.game_over()

# wait for click before closing the window
screen.exitonclick()
