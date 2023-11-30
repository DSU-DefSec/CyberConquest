#!/usr/bin/env python
# @Name: simple_test.py
# @Project: CyberConquest/examples
# @Author: Goofables
# @Created: 2023-11-29

import os

# Set board model
os.environ["BLINKA_FT232H"] = "1"

import time

import board
import digitalio

pin = digitalio.DigitalInOut(board.C7)
pin.direction = digitalio.Direction.OUTPUT

while True:
    print("Off")
    pin.value = False
    time.sleep(3)

    print("On")
    pin.value = True
    time.sleep(3)
