from time import sleep

from luma.core.interface.serial import noop, spi
from luma.led_matrix.device import max7219


def main():
    init()
    FPS = 60
    while True:
        # Draw everything
    
        # Update
    
        sleep(1 / FPS)

def init():
    # Setup
    serial = spi(port=0, device=0, gpio=noop())
    device = max7219(serial, cascaded=2, block_orientation=90, rotate=0)
    device.contrast(5)

if __name__ == "__main__":
    main()