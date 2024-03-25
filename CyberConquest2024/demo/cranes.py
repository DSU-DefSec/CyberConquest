#!/usr/bin/env python3
# @Name: cranes.py
# @Project: CyberConquest/CyberConquest2024/demo
# @Author: Goofables
# @Created: 2024-03-25
import time
import os

# Set board model
os.environ["BLINKA_MCP2221"] = "1"
import board
import digitalio

# top relay
pin = digitalio.DigitalInOut(board.G0)
pin.direction = digitalio.Direction.INPUT

# bottom relay
pin1 = digitalio.DigitalInOut(board.G1)
pin1.direction = digitalio.Direction.OUTPUT

# switch detector
pin2 = digitalio.DigitalInOut(board.G2)
pin2.direction = digitalio.Direction.OUTPUT

state = False
button_state = False

# When switch triggered, flip crane reel direction
def crane_d1():
    print("D1")
    pin1.value = True
    pin2.value = False

def crane_d2():
    print("D2")
    pin1.value = False
    pin2.value = True

def crane_stop():
    print("STOP")
    pin1.value = False
    pin2.value = False
    time.sleep(0.5)

def tick():
    global state, button_state
    if state:
        crane_d1()
    else:
        crane_d2()

    if pin.value != button_state:
        button_state = pin.value
        if not button_state:
            state = not state
            crane_stop()

def print_pin_state():
    print(f"Pin: {pin.value}")

def main():
    try:
        while True:
            tick()
            time.sleep(0.1)
            # x = input("tick or pin\n>")
            # if x == "tick":
            #     tick()
            # elif x == "pin":
            #     print_pin_state()
            # else:
            #     print("invalid input")
    except KeyboardInterrupt:
        crane_stop()

if __name__ == "__main__":
    main()