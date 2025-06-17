import random


class Ball:
    def __init__(self, x, y, dx=1, dy=1):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy

    def move(self):
        self.x += self.dx
        self.y += self.dy

    def bounce_vertical(self):
        self.dy *= -1

    def bounce_horizontal(self):
        self.dx *= -1

    def reset(self, start_x=7, start_y=3):
        self.x = start_x
        self.y = start_y
        self.dx = random.choice([-1, 1])
        self.dy = random.choice([-1, 1])

class Paddle:
    def __init__(self, y):
        self.y = y

    def move(self, direction):
        if direction == 'up' and self.y > 0:
            self.y -= 1
        elif direction == 'down' and self.y < 5:
            self.y += 1

    def get_positions(self):
        return [self.y + i for i in range(3)]  # Paddle is 3 pixels tall