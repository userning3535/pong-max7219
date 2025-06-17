import random


class Ball:
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.dx_init = dx
        self.dy_init = dy

    def update(self, screen_width, screen_height, paddle_0=None, paddle_x=None):
        board_width_0 = 0 if paddle_0 is None else 1
        board_width_x = 0 if paddle_x is None else 1

        self.x = self.x + self.dx
        self.y = self.y + self.dy

        if self.y < 0:
            self.bounce_vertical()
            self.y = 0
            self.x = round(self.x)
        elif self.y >= screen_height - 1:
            self.bounce_vertical()
            self.y = screen_height - 1
            self.x = round(self.x)

        if self.x < board_width_0:
            if paddle_0:
                if paddle_0.y - 1 <= self.y <= paddle_0.y + 1:
                    self.bounce_horizontal()
                else:
                    self.reset(screen_width // 2 - 1, screen_height // 2 - 1, abs(self.dx_init), self.dy_init * random.choice([-1, 1]))
            else:
                self.bounce_horizontal()
                self.x = board_width_0
                self.y = round(self.y)
        elif self.x >= screen_width - 1 - board_width_x:
            if paddle_x:
                if paddle_x.y - 1 <= self.y <= paddle_x.y + 1:
                    self.bounce_horizontal()
                else:
                    self.reset(screen_width // 2 - 1, screen_height // 2 - 1, -abs(self.dx_init), self.dy_init * random.choice([-1, 1]))
            else:
                self.bounce_horizontal()
                self.x = screen_width - 1 - board_width_x
                self.y = round(self.y)


    def draw(self, matrix):
        x = round(self.x)
        y = round(self.y)
        matrix[x][y] = 1
    
    def reset(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy

    def bounce_vertical(self):
        if abs(self.dx) > 8 * abs(self.dx_init):
            self.dy *= -1.0
        else:
            self.dx *= 1.1
            self.dy *= -1.1

    def bounce_horizontal(self):
        if abs(self.dy) > 8 * abs(self.dy_init):
            self.dx *= -1.0
        else:
            self.dx *= -1.1
            self.dy *= 1.1

class Paddle:
    def __init__(self, x, y, dy, screen_height=8):
        self.screen_height = screen_height

        self.x = x
        self.y = y
        self.dy = dy

    def update(self, input_y = None):
        if input_y is None:
            self.y += random.choice([-1, 1]) * self.dy
        else:
            if input_y > 0:
                self.y += self.dy
            elif input_y < 0:
                self.y -= self.dy
        self.y = max(1, min(self.y, self.screen_height - 2))
    
    def draw(self, matrix):
        y = round(self.y)
        matrix[self.x][y - 1] = 1
        matrix[self.x][y] = 1
        matrix[self.x][y + 1] = 1

class AIPaddle(Paddle):
    def update(self, ball):
        ball_x = ball.x
        ball_y = ball.y
        if abs(ball_x - self.x) < 7:
            if ball_y < self.y:
                self.y -= self.dy
            elif ball_y > self.y:
                self.y += self.dy
            self.y = max(1, min(self.y, self.screen_height - 2))
