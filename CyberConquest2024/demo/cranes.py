#!/usr/bin/env python3
# @Name: cranes.py
# @Project: CyberConquest/CyberConquest2024/demo
# @Author: Goofables
# @Created: 2024-03-25
import dataclasses
import time
import os

import board
import digitalio

#
# # top relay
# pin = digitalio.DigitalInOut(board.G0)
# pin.direction = digitalio.Direction.INPUT
#
# # bottom relay
# pin1 = digitalio.DigitalInOut(board.G1)
# pin1.direction = digitalio.Direction.OUTPUT
#
# # switch detector
# pin2 = digitalio.DigitalInOut(board.G2)
# pin2.direction = digitalio.Direction.OUTPUT

# state = False
# button_state = False


# Please don't laugh at my code.
@dataclasses.dataclass
class Crane:
    direction: bool
    button_state: bool
    relay_1_pin: digitalio.DigitalInOut
    relay_2_pin: digitalio.DigitalInOut
    switch_pin: digitalio.DigitalInOut

    def __init__(self, relay_1_pin, relay_2_pin, switch_pin):
        self.relay_1_pin = digitalio.DigitalInOut(relay_1_pin)
        self.relay_1_pin.direction = digitalio.Direction.OUTPUT

        self.relay_2_pin = digitalio.DigitalInOut(relay_2_pin)
        self.relay_2_pin.direction = digitalio.Direction.OUTPUT

        self.switch_pin = digitalio.DigitalInOut(switch_pin)
        self.switch_pin.direction = digitalio.Direction.INPUT

        # Beware! I have no idea what the default values for this should be.
        self.direction = False
        self.button_state = False

    def crane_dir_1(self):
        self.relay_1_pin.value = True
        self.relay_2_pin.value = False

    def crane_dir_2(self):
        self.relay_1_pin.value = False
        self.relay_2_pin.value = True

    def crane_stop(self):
        self.relay_1_pin.value = False
        self.relay_2_pin.value = False
        time.sleep(0.5)

    def tick(self):
        if self.direction:
            self.crane_dir_1()
        else:
            self.crane_dir_2()

        # If on the tick the switch if pressed,
        if self.switch_pin.value != self.button_state:
            # remember the current button state,
            self.button_state = self.switch_pin.value

            # and if the button is not pressed at all,s
            if not self.button_state:
                # switch the direction and stop the crane.
                self.direction = not self.direction
                self.crane_stop()


crane_1 = Crane(board.G1, board.G2, board.G0)


def main():
    try:
        while True:
            crane_1.tick()
            time.sleep(0.1)
            # x = input("tick or pin\n>")
            # if x == "tick":
            #     tick()
            # elif x == "pin":
            #     print_pin_state()
            # else:
            #     print("invalid input")
    except KeyboardInterrupt:
        crane_1.crane_stop()


if __name__ == "__main__":
    main()
