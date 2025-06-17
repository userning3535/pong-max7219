from time import sleep

import numpy as np
from luma.core.interface.serial import noop, spi
from luma.led_matrix.device import max7219

from src.element import AIPaddle, Ball, Paddle


def main():
    # init()
    FPS = 60
    WIDTH = 16
    HEIGHT = 8

    ball = Ball(WIDTH // 2 - 1, HEIGHT // 2 - 1, 2 / FPS, 2 / FPS)
    paddle_0 = AIPaddle(0, HEIGHT // 2, 15 / FPS, screen_height=HEIGHT)
    paddle_x = AIPaddle(WIDTH - 1, HEIGHT // 2, 15 / FPS, screen_height=HEIGHT)
    while True:
        # Draw everything
        matrix = np.zeros((WIDTH, HEIGHT))
        ball.draw(matrix)
        paddle_0.draw(matrix)
        paddle_x.draw(matrix)
        print(matrix.T)

        # Update
        ball.update(WIDTH, HEIGHT, paddle_0=paddle_0, paddle_x=paddle_x)
        paddle_0.update(ball)
        paddle_x.update(ball)
        sleep(1 / FPS)

def init():
    # Setup
    serial = spi(port=0, device=0, gpio=noop())
    device = max7219(serial, cascaded=2, block_orientation=90, rotate=0)
    device.contrast(5)

if __name__ == "__main__":
    main()