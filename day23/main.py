# Turtle Crossing

import turtle
import time

from player import Player
from car_manager import CarManager
from scoreboard import Scoreboard


# screen setup
screen = turtle.Screen()
screen.setup(width=800, height=600)
screen.tracer(0)

# player, etc. setup
player = Player()
car_manager = CarManager()
scoreboard = Scoreboard()

# controls setup
screen.listen()
screen.onkey(player.move_up, "Up")

game_is_over = False
while not game_is_over:
    time.sleep(0.1)
    screen.update()
    car_manager.move_cars()

    # check for level up condition
    if player.reached_finish():
        scoreboard.increase_level()
        car_manager.increase_speed()
        player.reset_position()

    # detect collision
    for car in car_manager.cars:
        if abs(player.xcor() - car.xcor()) < 20 and abs(player.ycor() - car.ycor()) < 15:
            game_is_over = True

# display the game over message
scoreboard.game_over()

# wait for click before closing the window
screen.exitonclick()
