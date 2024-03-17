#!/usr/bin/env python
# @Name: water_sensor.py
# @Project: CyberConquest/examples
# @Author: Goofables
# @Created: 2/23/23


import board
import digitalio
import time

pin = digitalio.DigitalInOut(board.G0)
pin.direction = digitalio.Direction.INPUT 
pin_led = digitalio.DigitalInOut(board.G1)
pin_led.direction = digitalio.Direction.OUTPUT

pin_led.value = False
time.sleep(1)
pin_led.value = True
time.sleep(1)

while True:
    # try:
    v = pin.value
    print(v)
    pin_led.value = v
    time.sleep(0.2)
    # except:
    #     pass


