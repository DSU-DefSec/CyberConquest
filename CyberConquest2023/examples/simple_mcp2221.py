#!/usr/bin/env python
# @Name: simple_mcp2221.py
# @Project: CyberConquest/examples
# @Author: Goofables
# @Created: 2023-11-29

import os

# Set board model
os.environ["BLINKA_MCP2221"] = "1"

import time

import board
import digitalio

pin = digitalio.DigitalInOut(board.G0)
pin.direction = digitalio.Direction.OUTPUT

while True:
    print("Off")
    pin.value = False
    time.sleep(0.1)

    print("On")
    pin.value = True
    time.sleep(0.1)
