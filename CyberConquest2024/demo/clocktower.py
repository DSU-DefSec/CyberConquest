#!/usr/bin/env python3
# @Name: clocktower.py
# @Project: CyberConquest/CyberConquest2024/demo
# @Author: Goofables
# @Created: 2024-04-17
import math
import time

import adafruit_is31fl3741
import board
from adafruit_is31fl3741.adafruit_rgbmatrixqt import Adafruit_RGBMatrixQT


def color_val(r: int, g: int, b: int) -> int:
    return (r << 16) | (g << 8) | b


print("Initializing board")
i2c = board.I2C()  # uses board.SCL and board.SDA
is31 = Adafruit_RGBMatrixQT(i2c, allocate=adafruit_is31fl3741.PREFER_BUFFER)
is31.set_led_scaling(0xFF)
is31.global_current = 0xFF
is31.set_led_scaling(20)
print("Global current is: ", is31.global_current)
is31.enable = True


CENTER_Y = 4
CENTER_X = 6

# for y in range(9):
#     for x in range(13):
#         is31.pixel(x, y, color_val(20, 0, 0))
#         is31.show()

print("Playing animation:")

for i in range(360):
    r = i * math.pi / 180.0
    is31.pixel(int(CENTER_X + math.cos(r) * 4), int(CENTER_Y + math.sin(i) * 4), color_val(i, 255, 0))
    is31.show()


time.sleep(10)

# def
#
# while True:
#
