import random

from settings import COLS, ROWS


class Food:
    def __init__(self, snake_body):
        self.position = self.spawn(snake_body)

    def spawn(self, snake_body):
        while True:
            position = (random.randint(0, COLS - 1), random.randint(0, ROWS - 1))
            if position not in snake_body:
                return position
