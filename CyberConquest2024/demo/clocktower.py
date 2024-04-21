#!/usr/bin/env python3
# @Name: clocktower.py
# @Project: CyberConquest/CyberConquest2024/demo
# @Author: Goofables
# @Created: 2024-04-17
import datetime
import logging
import math
import random

import adafruit_is31fl3741
import board
from adafruit_is31fl3741.adafruit_rgbmatrixqt import Adafruit_RGBMatrixQT

logger = logging.getLogger(__name__)


def color_val(r: int, g: int, b: int) -> int:
    # return (r << 16) | (g << 8) | b
    if r == 0 and g == 0 and b == 0:
        return 0
    return random.randint(0, 256 * 256 * 256 - 1)


class ClockTower:
    def __init__(self):
        logger.info("Initializing board")
        # Initialize the rgb matrix
        self.is31 = Adafruit_RGBMatrixQT(board.I2C(), allocate=adafruit_is31fl3741.PREFER_BUFFER)
        # Multiplier for each pixel value
        self.is31.set_led_scaling(0xFF)
        # Total current allowance
        self.is31.global_current = 0x01
        # Enable the matrix
        self.is31.enable = True

        self.CENTER_X = 6.5
        self.CENTER_Y = 4.5

    def xy_from_ar(self, a: float | int, r: float | int = 100, a_max: int = 100, r_max: int = 100) -> tuple[int, int]:
        """
        Calculate the x and y coordinates of an angle and radius projected from the center of the board.

        @param a: Angle from 0 to `a_max`
        @param r: Radius from 0 to `r_max`
        @param a_max: Max for angle
        @param r_max: Max for radius
        @return: A tuple of x and y coordinates
        """
        a = float(a) * math.pi * 2 / float(a_max)
        r = float(r) * 4.3 / float(r_max)
        return int(self.CENTER_X + math.sin(a) * r), int(self.CENTER_Y + -math.cos(a) * r)

    def tick(self) -> None:
        """Update the display"""
        self.is31.fill(color_val(0, 0, 0))
        for i in range(100):
            self.is31.pixel(
                *self.xy_from_ar(i),
                color_val(255, 100, 0),
            )
        now = datetime.datetime.now()
        for i in range(0, 100, 5):
            self.is31.pixel(
                *self.xy_from_ar(now.hour % 12, i, a_max=12),
                color_val(255, 0, 0),
            )
            self.is31.pixel(
                *self.xy_from_ar(now.minute, i, a_max=60),
                color_val(0, 255, 0),
            )
            self.is31.pixel(
                *self.xy_from_ar(now.second, i, a_max=60),
                color_val(0, 0, 255),
            )

        self.is31.show()

    def clear(self) -> None:
        """Clear the display"""
        self.is31.fill(color_val(0, 0, 0))
        self.is31.show()


if __name__ == "__main__":
    tower = ClockTower()
    while True:
        tower.tick()
