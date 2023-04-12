#!/usr/bin/env python
# @Name: test-neo.py
# @Project: CyberConquest/examples
# @Author: Goofables
# @Created: 2/21/23

import random
import time

import board
import neopixel_spi as neopixel

NUM_PIXELS = 50
COLORS = (0xFF0000, 0x00FF00, 0x0000FF)
DELAY = 0.5


pixels = neopixel.NeoPixel_SPI(
    board.SPI(),
    NUM_PIXELS,
    bpp=4,
    pixel_order=neopixel.GRBW,
    auto_write=True,
    brightness=0.01
)

# pixels[0] = (255, 0, 0)
# pixels[1] = (255, 255, 0)
# pixels[2] = (255, 0, 255)
# pixels[3] = (0, 255, 0)
# pixels[4] = (0, 255, 255)
# pixels[5] = (0, 0, 255)
# pixels[6] = (255, 255, 255)
# pixels[7] = (0, 0, 0)
# time.sleep(10)

colors = [(255, 0, 0), (255, 255, 0), (255, 0, 255), (0, 255, 0), (0, 255, 255), (0, 0, 255), (255, 255, 255)]

# time.sleep(1)

print("Running")

while True:
    pixels[random.randint(0, NUM_PIXELS - 1)] = colors[random.randint(0, len(colors) - 1)]
    time.sleep(.1)
