#!/usr/bin/env python
# @Name: simple-check.py
# @Project: CyberConquest/water-tower-scoring
# @Author: Gaelin Shupe
# @Created: 3/22/23


import board
import busio
import digitalio
from adafruit_mcp230xx.mcp23008 import MCP23008

MCP_COUNT = 6
MCP_BASE_ID = 0x20

client_list = []

i2c = busio.I2C(board.SCL, board.SDA)
raw_pins: list[digitalio.DigitalInOut] = []
mcp_list: list[MCP23008] = [MCP23008(i2c, address=MCP_BASE_ID + i) for i in range(MCP_COUNT)]
for m in mcp_list:
    for i in range(8):
        raw_pins.append(m.get_pin(i))


def pin(mcp_id: int, pin_id: int) -> digitalio.DigitalInOut:
    p = mcp_list[mcp_id].get_pin(pin_id)
    p.direction = digitalio.Direction.INPUT
    return p


teams = [
    (pin(0, 0), pin(0, 1)),
    (pin(0, 2), pin(0, 3)),
    (pin(0, 4), pin(0, 5)),
    (pin(0, 6), pin(0, 7)),

    (pin(1, 0), pin(1, 1)),
    (pin(1, 2), pin(1, 3)),
    (pin(1, 4), pin(1, 5)),
    (pin(1, 6), pin(1, 7)),

    (pin(2, 0), pin(2, 1)),
    (pin(2, 2), pin(2, 3)),
    (pin(2, 4), pin(2, 5)),
    (pin(2, 6), pin(2, 7)),

    (pin(3, 0), pin(3, 1)),
    (pin(3, 2), pin(3, 3)),
    (pin(3, 4), pin(3, 5)),
    (pin(3, 6), pin(3, 7)),

    (pin(4, 0), pin(4, 1)),
    (pin(4, 2), pin(4, 3)),
    (pin(4, 4), pin(4, 5)),
    (pin(4, 6), pin(4, 7)),

    (pin(5, 0), pin(5, 1)),
    (pin(5, 2), pin(5, 3)),
    (pin(5, 4), pin(5, 5)),
    (pin(5, 6), pin(5, 7)),

]


while True:
    print(''.join(["1" if p.value else "0" for p in raw_pins]))
