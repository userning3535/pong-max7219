from time import sleep

import numpy as np
from luma.core.interface.serial import noop, spi
from luma.led_matrix.device import max7219
from PIL import Image

from src.element import AIPaddle, Ball, Paddle


def main():
    FPS = 60
    WIDTH = 16
    HEIGHT = 8

    device = init()
    ball = Ball(WIDTH // 2 - 1, HEIGHT // 2 - 1, 2 / FPS, 2 / FPS)
    paddle_0 = AIPaddle(0, HEIGHT // 2, 10 / FPS, screen_height=HEIGHT)
    paddle_x = AIPaddle(WIDTH - 1, HEIGHT // 2, 10 / FPS, screen_height=HEIGHT)
    while True:
        # Draw everything
        matrix = np.array(
            [[0 for _ in range(HEIGHT)] for _ in range(WIDTH)], dtype=np.uint8
        )
        ball.draw(matrix)
        paddle_0.draw(matrix)
        paddle_x.draw(matrix)
        matrix_display(device, matrix.T)

        # Update
        ball.update(WIDTH, HEIGHT, paddle_0=paddle_0, paddle_x=paddle_x)
        paddle_0.update(ball)
        paddle_x.update(ball)
        sleep(1 / FPS)


def init():
    # Setup
    serial = spi(port=0, device=0, gpio=noop())
    device = max7219(serial, cascaded=2, block_orientation=180)
    device.contrast(5)
    return device


def matrix_display(device, matrix):
    """Display a 2D numpy array on the LED matrix.
    This is a wrapper function that converts a 2D numpy
    matrix into a 1-bit B/W image and then displays it
    on the LED matrix.

    Parameters
    ----------
    device : luma.led_matrix.device.max7219
        A Luma LED matrix device object.
    matrix: uint8 numpy.ndarray
        A 2D binary numpy array.

    """
    matrix_g = np.where(matrix == 1, 255, matrix)
    image_g = Image.fromarray(matrix_g, mode="L")
    image_bw = image_g.convert("1")
    device.display(image_bw)


if __name__ == "__main__":
    main()
