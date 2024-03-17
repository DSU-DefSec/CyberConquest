#!/usr/bin/env python
# @Name: test1.py
# @Project: CyberConquest/examples
# @Author: Goofables
# @Created: 2/21/23

import board
import digitalio
import time

#https://learn.adafruit.com/circuitpython-on-any-computer-with-ft232h/pinouts

green = digitalio.DigitalInOut(board.D5)
green.direction = digitalio.Direction.OUTPUT

yellow = digitalio.DigitalInOut(board.D6)
yellow.direction = digitalio.Direction.OUTPUT

red = digitalio.DigitalInOut(board.D7)
red.direction = digitalio.Direction.OUTPUT



print("Hi")


while True:
    green.value = True
    yellow.value = False
    red.value = False
    time.sleep(1)
    green.value = False
    yellow.value = True
    red.value = False
    time.sleep(0.5)
    green.value = False
    yellow.value = False
    red.value = True
    time.sleep(1)


