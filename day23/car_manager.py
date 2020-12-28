import turtle
import random


COLORS = ["red", "orange", "yellow", "green", "blue", "purple"]
STARTING_MOVE_DISTANCE = 5
MOVE_INCREMENT = 10
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


class CarManager:
    def __init__(self):
        # store the cars in a list
        self.cars = []
        # spawn cars just off the right edge of the screen
        self.x_start = int(SCREEN_WIDTH / 2 + 40)
        # width of the "road"
        self.y_min = int(SCREEN_HEIGHT / -2 + 60)
        self.y_max = int(SCREEN_HEIGHT / 2 - 60)
        self.move_distance = STARTING_MOVE_DISTANCE

    def move_cars(self):
        """Moves all cars and randomly spawns an additional one."""
        # 1 in 6 chance to spawn a new car, anything other than 0 will be "truthy"
        if not random.randint(0, 5):
            self.spawn_car()
        for car in self.cars:
            car.forward(self.move_distance)

    def increase_speed(self):
        """Increases the movement distance if the cars."""
        self.move_distance += MOVE_INCREMENT

    def spawn_car(self):
        """Creates a new car just off the right edge of the screen."""
        new_car = turtle.Turtle("square")
        new_car.shapesize(stretch_len=2)
        new_car.color(random.choice(COLORS))
        new_car.penup()
        new_car.speed(0)
        new_car.setheading(180)
        new_car.setx(self.x_start)
        new_car.sety(random.randint(self.y_min, self.y_max))
        self.cars.append(new_car)
