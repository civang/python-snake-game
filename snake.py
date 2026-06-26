from settings import COLS, ROWS


class Snake:
    def __init__(self):
        self.body = [(10, 10)]
        self.direction = (1, 0)

    def head(self):
        return self.body[0]

    def change_direction(self, new_direction):
        current_opposite = (-self.direction[0], -self.direction[1])
        if new_direction != current_opposite:
            self.direction = new_direction

    def move(self, grow=False):
        head_x, head_y = self.head()
        dir_x, dir_y = self.direction
        new_head = (head_x + dir_x, head_y + dir_y)
        self.body.insert(0, new_head)
        if not grow:
            self.body.pop()

    def collides_with_self(self):
        return self.head() in self.body[1:]

    def is_out_of_bounds(self):
        x, y = self.head()
        return x < 0 or x >= COLS or y < 0 or y >= ROWS
