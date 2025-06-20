from time import sleep

import adafruit_ads1x15.ads1115 as ADS
import board
import busio
import numpy as np
from adafruit_ads1x15.analog_in import AnalogIn
from luma.core.interface.serial import noop, spi
from luma.led_matrix.device import max7219
from PIL import Image

from src.element import AIPaddle, Ball, Paddle


def main():
    FPS = 60
    WIDTH = 16
    HEIGHT = 8

    device, player_0_x, _, _, _ = init()
    ball = Ball(WIDTH // 2 - 1, HEIGHT // 2 - 1, 2 / FPS, 2 / FPS)
    paddle_0 = Paddle(0, HEIGHT // 2, 10 / FPS, screen_height=HEIGHT)
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
        paddle_0.update(player_0_x.voltage)
        paddle_x.update(ball)
        sleep(1 / FPS)


def init():
    # Setup
    serial = spi(port=0, device=0, gpio=noop())
    device = max7219(serial, cascaded=2, block_orientation=180)
    device.contrast(5)

    # Create the I2C bus
    i2c = busio.I2C(board.SCL, board.SDA)
    # Create the ADC object using the I2C bus
    ads = ADS.ADS1115(i2c)
    # Create single-ended input on channels
    player_0_x = AnalogIn(ads, ADS.P0)
    player_0_y = AnalogIn(ads, ADS.P1)
    player_1_x = AnalogIn(ads, ADS.P2)
    player_1_y = AnalogIn(ads, ADS.P3)

    return device, player_0_x, player_0_y, player_1_x, player_1_y


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
