#!/usr/bin/env python
# @Name: windmill.py
# @Project: CyberConquest/examples
# @Author: Goofables
# @Created: 2/21/23
import random
from time import sleep

import board
import digitalio

pin0 = digitalio.DigitalInOut(board.G0)
pin0.direction = digitalio.Direction.OUTPUT
pin1 = digitalio.DigitalInOut(board.G1)
pin1.direction = digitalio.Direction.OUTPUT
# pin2 = digitalio.DigitalInOut(board.G2)
# pin2.direction = digitalio.Direction.OUTPUT

print("hi")

pin0.value = False
pin1.value = False
# pin2.value = False

# for s in range(4, 1000):
TRANSITION = 0.1
while True:
    # SLEEP = 1 / s
    SLEEP = random.random()*3
    # print(f"{s}/second")
    for _ in range(2):
        # print("High")
        # pin2.value = True
        # sleep(TRANSITION)
        pin0.value = True
        # pin2.value = False
        sleep(SLEEP)

        # pin2.value = True
        # sleep(TRANSITION)
        pin1.value = True
        # pin2.value = False
        sleep(SLEEP)

        # print("Low")
        # pin2.value = True
        # sleep(TRANSITION)
        pin0.value = False
        # pin2.value = False
        sleep(SLEEP)

        # pin2.value = True
        # sleep(TRANSITION)
        pin1.value = False
        # pin2.value = False
        sleep(SLEEP)
