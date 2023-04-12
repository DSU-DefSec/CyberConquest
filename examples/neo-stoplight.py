#!/usr/bin/env python
# @Name: neo-stoplight.py
# @Project: CyberConquest/examples
# @Author: Goofables
# @Created: 2/22/23
from time import sleep

import board
import neopixel_spi as neopixel

pixels = neopixel.NeoPixel_SPI(
    spi=board.SPI(),
    n=8,
    bpp=4,
    pixel_order=neopixel.GRBW,
    auto_write=True,
    brightness=1
)


class Colors:
    MAX_VAL = 100
    FULL_WHITE = (MAX_VAL, MAX_VAL, MAX_VAL, MAX_VAL)
    WHITE = (MAX_VAL, MAX_VAL, MAX_VAL, 0)
    SOFT_WHITE = (0, 0, 0, MAX_VAL)
    RED = (MAX_VAL, 0, 0)
    RED_WHITE = (MAX_VAL, 0, 0, MAX_VAL)
    YELLOW = (MAX_VAL, MAX_VAL, 0)
    YELLOW_WHITE = (MAX_VAL, MAX_VAL, 0, MAX_VAL)
    GREEN = (0, MAX_VAL, 0)
    GREEN_WHITE = (0, MAX_VAL, 0, MAX_VAL)
    BLUE_GREEN = (0, MAX_VAL, MAX_VAL)
    BLUE_GREEN_WHITE = (0, MAX_VAL, MAX_VAL, MAX_VAL)
    BLUE = (0, 0, MAX_VAL)
    BLUE_WHITE = (0, 0, MAX_VAL, MAX_VAL)
    PURPLE = (MAX_VAL, 0, MAX_VAL)
    PURPLE_WHITE = (MAX_VAL, 0, MAX_VAL, MAX_VAL)
    BLACK = (0, 0, 0)
    BLACK_WHITE = (0, 0, 0, MAX_VAL)


class TrafficLight:

    def __init__(self, pixel_ids: tuple, colors: tuple, off_colors: tuple = None):
        if len(pixel_ids) != len(colors):
            raise ValueError("pixel_ids and colors are different lengths")
        self.lights = pixel_ids
        self.colors = colors
        self.off_colors = off_colors
        self.current = -1

    def tick(self):
        self.current = (self.current + 1) % len(self.lights)
        for i in range(len(self.lights)):
            if i == self.current:
                pixels[self.lights[i]] = self.colors[i]
            else:
                if self.off_colors is None:
                    pixels[self.lights[i]] = Colors.BLACK
                else:
                    pixels[self.lights[i]] = self.off_colors[i]

#
# light1 = TrafficLight((0, 1, 2), (Colors.GREEN, Colors.YELLOW, Colors.RED))
# light2 = TrafficLight((5, 6, 7), (Colors.GREEN, Colors.YELLOW, Colors.RED))
# middle = TrafficLight((3, 4), (Colors.BLUE_GREEN, Colors.BLUE_GREEN), (Colors.PURPLE, Colors.PURPLE))
# light2.tick()

while True:
    # pixels[0] = Colors.YELLOW
    # pixels[1] = Colors.YELLOW_WHITE
    # pixels[2] = Colors.PURPLE
    # pixels[3] = Colors.PURPLE_WHITE
    # pixels[4] = Colors.BLUE_GREEN
    # pixels[5] = Colors.BLUE_GREEN_WHITE
    # pixels[6] = Colors.BLUE
    # pixels[7] =Colors.BLUE_WHITE
    for i in range(8):
        pixels[i] = Colors.FULL_WHITE
        sleep(0.01)
    pixels.fill(0)
    sleep(0.5)
    # for p in range(8):
    #     pixels[p] = Colors.FULL_WHITE
    #     sleep(1)

    # light1.tick()
    # sleep(1)
    # light2.tick()
    # sleep(1)
