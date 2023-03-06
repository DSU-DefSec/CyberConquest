#!/usr/bin/env python
# @Name: water-pump-MCP2221.py
# @Project: CyberConquest/water-tower
# @Author: Goofables
# @Created: 3/6/23


from time import sleep

import board
import digitalio

pump = digitalio.DigitalInOut(board.C7)
pump.direction = digitalio.Direction.OUTPUT

sensor = digitalio.DigitalInOut(board.D4)
sensor.direction = digitalio.Direction.INPUT

print("Running...")

while True:
    try:
        if sensor.value:
            # print("Pump off")
            pump.value = False
            sleep(5)
        else:
            # print("Pump on")
            pump.value = True
        sleep(2)
    except OSError:
        print("OSError")
