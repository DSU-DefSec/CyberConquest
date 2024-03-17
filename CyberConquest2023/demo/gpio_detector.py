#!/usr/bin/env python
# @Name: gpio_detector.py
# @Project: CyberConquest/demo
# @Author: Gaelin Shupe
# @Created: 4/1/23


import board
import neopixel

# 10, 12, 18, 21
for a in set(board.__dict__.keys()).difference(board.__builtins__.keys()):
    if "_" in a: continue
    try:
        neopixel.NeoPixel(
            board.__dict__[a],
            n=1,
            bpp=4,
            pixel_order=neopixel.GRBW,
            brightness=0.1
        )[0] = (255, 0, 0)
        print(f"+ {a}")
    except AttributeError:
        pass
    except TypeError:
        print(f"- {a}")
