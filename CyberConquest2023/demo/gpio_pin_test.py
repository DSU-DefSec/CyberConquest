#!/usr/bin/env python
# @Name: gpio_pin_test.py
# @Project: CyberConquest/demo
# @Author: Gaelin Shupe
# @Created: 4/1/23


import board
import neopixel

def board_test(pin,pixels=1):
    neopixel.NeoPixel(
        pin,
        n=pixels,
        bpp=4,
        pixel_order=neopixel.GRBW,
        brightness=0.1
    )[pixels-1] = (255, 128, 0)


if __name__ == "__main__":
    import sys
    try:
        board_test(board.__dict__[sys.argv[1]], int(sys.argv[2]))
    except RuntimeError:
        pass