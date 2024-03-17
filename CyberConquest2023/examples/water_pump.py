#!/usr/bin/env python
# @Name: water_pump.py
# @Project: CyberConquest/examples
# @Author: Goofables
# @Created: 2/23/23

import board
import digitalio
import time

water_sensor = digitalio.DigitalInOut(board.D4)
water_sensor.direction = digitalio.Direction.INPUT


pump = digitalio.DigitalInOut(board.C7)
pump.direction = digitalio.Direction.OUTPUT

while True:
    if water_sensor.value:
        print("Pump off")
        pump.value = False
        time.sleep(5)
    else:
        print("Pump on")
        pump.value = True
    time.sleep(2)
